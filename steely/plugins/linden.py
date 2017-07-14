#!/usr/bin/env python3


from tinydb import TinyDB, Query, where
from tinydb.operations import increment
from datetime import datetime, timedelta
import tabulate
import random
import requests
import json


COMMAND = ".linden"
USERDB = TinyDB("linden.json")
USER = Query()


def user_from_name(name, list):
    for user in list:
        if user.first_name == name:
            return user


def list_users(bot, thread_id):
    group = bot.fetchGroupInfo(thread_id)[thread_id]
    user_ids = group.participants
    yield from bot.fetchUserInfo(*user_ids).values()


def create_user(id, first_name):
    data = {"id": id,
            "first_name": first_name,
            "investments": {},
            "lindens": 2000}
    USERDB.insert(data)
    return data


def get_balance(user_id):
    matching_users = USERDB.get(USER.id == user_id)
    if len(matching_users) == 0:
        return
    return matching_users['lindens']


def give_cmd(bot, message_parts, author_id, thread_id, thread_type):
    users = list_users(bot, thread_id)
    if not message_parts[-1].isdigit() or message_parts[-1] == "0":
        bot.sendMessage('please enter a valid amount',
                        thread_id=thread_id, thread_type=thread_type)
        return
    reciever_name, amount = message_parts[0].lstrip("@").capitalize(), int(message_parts[-1])
    reciever_model = user_from_name(reciever_name, users)
    reciever = USERDB.get(USER.id == reciever_model.uid)
    sender_model = bot.fetchUserInfo(author_id)[author_id]
    sender = USERDB.get(USER.id == author_id)
    if sender_model.uid == reciever_model.uid:
        bot.sendMessage('no', thread_id=thread_id, thread_type=thread_type)
        return
    if not reciever:
        reciever = create_user(reciever_model.uid, reciever_model.first_name)
    if not sender:
        sender = create_user(author_id, sender_model.first_name)
    new_sender_balance = sender['lindens'] - amount
    if new_sender_balance < 0:
        bot.sendMessage('you\'d be broke boyo', thread_id=thread_id, thread_type=thread_type)
        return
    USERDB.update({'lindens': new_sender_balance}, USER.id == author_id)
    USERDB.update({'lindens': reciever['lindens'] + amount}, USER.id == reciever_model.uid)
    bot.sendMessage('you gave {} {} Linden Dollars™'.format(reciever_name, amount),
                    thread_id=thread_id, thread_type=thread_type)


def table_cmd(bot, message_parts, author_id, thread_id, thread_type):
    max_lindens = len(str(max(user['lindens'] for user in USERDB.all())))
    max_name = len(max((user['first_name'] for user in USERDB.all()), key=len))
    string = '```'
    for user in sorted(USERDB.all(), key=lambda user: user['lindens'], reverse=True):
        string += '\n{name:<{max_name}} {lindens:>{max_lindens}.3f}L$'.format(name=user['first_name'],
                                                                         lindens=user['lindens'],
                                                                         max_name=max_name,
                                                                         max_lindens=max_lindens + 4)
    string += '\n```'
    bot.sendMessage(string, thread_id=thread_id, thread_type=thread_type)


QUOTE_CACHE = {}
QUOTE_TTL = timedelta(minutes=10)

def invest_get_quotes(tickers):
    if not tickers:
        return []
    base_url = 'https://query.yahooapis.com/v1/public/yql'
    param_string = '?q={}&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    query = 'select Symbol,Ask,Bid from yahoo.finance.quotes where symbol in ("{}")'

    filled_q = query.format('","'.join(tickers))
    filled_params = param_string.format(filled_q)

    r = requests.get(base_url + filled_params)
    if len(tickers) == 1:
        # Yahoo for some reson changes the API slightly if you reqest only one ticker.
        # Wrap the return in a list so we have a consistent API
        return [json.loads(r.text)['query']['results']['quote']]
    return json.loads(r.text)['query']['results']['quote']

def invest_get_quote_slow_backup(ticker):
    base_url = "https://www.alphavantage.co/query"
    params = "?function=TIME_SERIES_INTRADAY&symbol={}&interval=1min&apikey={}"
    KEY = "6A98QBQPTOVNV1AD"
    url = base_url + params.format(ticker, KEY)

    r = requests.get(url)
    resp = json.loads(r.text)
    if "Error Message" in resp:
        return {"Symbol": ticker, "Bid": None, "Ask": None}

    most_recent_time = max(resp["Time Series (1min)"])
    latest = resp["Time Series (1min)"][most_recent_time]
    return {
        "Symbol": ticker,
        "Bid": latest["4. close"],
        "Ask": latest["4. close"],
    }

def invest_check_valid_quote(quote):
    return "Bid" in quote and quote["Bid"] and "Ask" in quote and quote["Ask"]

def invest_get_quotes_w_cache(tickers):
    cached_quotes = []
    tics_to_get = []
    for tic in tickers:
        if tic not in QUOTE_CACHE:
            tics_to_get.append(tic)
        elif datetime.now() - QUOTE_CACHE[tic]['time'] > QUOTE_TTL:
            tics_to_get.append(tic)
        elif not invest_check_valid_quote(QUOTE_CACHE[tic]):
            tics_to_get.append(tic)
        else:
            cached_quotes.append(QUOTE_CACHE[tic])
    new_quotes = invest_get_quotes(tics_to_get)
    for quote in new_quotes:
        if not invest_check_valid_quote(quote):
            quote = invest_get_quote_slow_backup(quote["Symbol"])
        QUOTE_CACHE[quote['Symbol']] = quote
        QUOTE_CACHE[quote['Symbol']]['time'] = datetime.now()
    return cached_quotes + new_quotes


def invest_buy_cmd(user_id, args):
    # Sanitise that input
    if not 1 <= len(args) <= 2:
        return 'Usage: .linden invest buy STOCK_TICKER [QUANTITY]'
    tic, qt = args[0].upper().lstrip('$'), 1
    if len(args) == 2:
        if not args[1].isdigit() or args[1] == '0':
            return "Quantity must be a positive int, idiot"
        qt = int(args[1])
    # Get the stock deets
    quote = invest_get_quotes_w_cache([tic])[0]
    if quote['Ask'] is None:
        return "Stock ${} not found (you sure it's on the NASDAQ?)".format(tic)
    ask = float(quote['Ask'])
    total_cost = ask * qt
    # Check the user's not a snek
    user_balance = get_balance(user_id)
    if user_balance is None:
        return "User doesn't exist, get urself some Lindens"
    elif user_balance < total_cost:
        return "you don't have enough Lindens\n" \
               "you have {user_balance:.2f}L$,\n" \
               "but you need {total_cost:.2f}L$ ({qt} * {ask:.2f})".format_map(locals())
    # Edit that database
    total_holdings = USERDB.get(USER.id == user_id)['investments']
    new_holding = {'symbol': tic, 'quantity': qt, 'orig_value': total_cost}
    if tic in total_holdings:
        new_holding['quantity'] += total_holdings[tic]['quantity']
        new_holding['orig_value'] += total_holdings[tic]['orig_value']
    total_holdings[tic] = new_holding
    USERDB.update({'investments': total_holdings}, USER.id == user_id)
    USERDB.update({'lindens': user_balance - (total_cost)}, USER.id == user_id)
    return "Successfully bought {} shares of ${} for {:.4f}L$".format(qt, tic, total_cost)


def invest_sell_cmd(user_id, args):
    # Clean input
    if not 0 < len(args) < 3:
        return 'Usage: .linden invest sell STOCK_TICKER [QUANTITY]'
    tic, qt = args[0].upper().lstrip('$'), 1
    if len(args) == 2:
        if not args[1].isdigit() or args[1] == 0:
            return "Quantity must be a positive int, fool"
        qt = int(args[1])
    # Get stock deets
    quote = invest_get_quotes_w_cache([tic])[0]
    if quote['Bid'] is None:
        return "Can't find that stock, friend"
    bid = float(quote['Bid'])
    # Check the user's not a snek
    user_balance = get_balance(user_id)
    if user_balance is None:
        return "User does not exist, ask a friend for Lindens"
    total_holdings = USERDB.get(USER.id == user_id)['investments']
    if tic not in total_holdings or total_holdings[tic]['quantity'] < qt:
        return "You don't own enough ${} to sell {}".format(tic, qt)
    # Edit that database
    orig_bid = total_holdings[tic]['orig_value'] / total_holdings[tic]['quantity']
    total_holdings[tic]['orig_value'] -= orig_bid * qt
    total_holdings[tic]['quantity'] -= qt
    if total_holdings[tic]['quantity'] == 0:
        del total_holdings[tic]
    USERDB.update({'investments': total_holdings}, USER.id == user_id)
    USERDB.update({'lindens': user_balance + (qt * bid)}, USER.id == user_id)
    return "Successfully sold {} shares of ${} for {} Lindens ({:.2f}L profit)".format(
            qt, tic, qt * bid, qt * (bid - orig_bid))


def invest_list_cmd(user_id, args):
    user_balance = get_balance(user_id)
    if user_balance is None:
        return "User does not exist, poke Senan"
    user = USERDB.get(USER.id == user_id)
    out = "```\n{}: {:.2f}L$ Cash\n\n".format(user['first_name'], user['lindens'])
    tics = list(user['investments'])
    quotes = invest_get_quotes_w_cache(tics)
    total_profit = 0
    table = []
    for quote in quotes:
        holding = user['investments'][quote['Symbol']]
        quant, orig_value = holding['quantity'], holding['orig_value']

        if quote['Bid'] is None:
            print("Broken stock", holding['symbol'], 'for', user_id, '\nfull quote:\n', quote)

            return "The following stock broke: " + holding['symbol']

        bid = float(quote['Bid'])

        table.append([quote['Symbol'], quant, quant * bid,
            100 * ((quant * bid) - orig_value) / orig_value])
        total_profit += (quant * bid) - orig_value
    out += tabulate.tabulate(table, headers=("ticker", "quant", "value", "% profit"), tablefmt="plain", floatfmt=".4f")
    out += "\nCurrent Profit: {:.2f}L$```".format(total_profit)
    return out


def invest_quote_cmd(user_id, args):
    if len(args) != 1:
        return "Usage: .linden invest quote TICKER"
    quote = invest_get_quotes_w_cache(args)[0]
    return "${Symbol}\nbid: {Bid}, ask: {Ask}".format(**quote)


def invest_cmd(bot, message_parts, author_id, thread_id, thread_type):
    if len(message_parts) == 0:
        message_parts = ['list']

    invest_cmds = {
        'buy': invest_buy_cmd,
        'sell': invest_sell_cmd,
        'list': invest_list_cmd,
        'quote': invest_quote_cmd,
    }
    out_message = ''
    if message_parts[0] not in invest_cmds:
        out_message = 'Invalid investment decision, available commands: ' + ', '.join(
                invest_cmds)
    else:
        out_message = invest_cmds[message_parts[0]](author_id, message_parts[1:])
    bot.sendMessage(out_message, thread_id=thread_id, thread_type=thread_type)


def invalid_cmd(bot, message_parts, author_id, thread_id, thread_type):
    bot.sendMessage("invalid subcommand", thread_id=thread_id, thread_type=thread_type)


def gamble_cmd(bot, message_parts, author_id, thread_id, thread_type):
    if not message_parts or not message_parts[0].isdigit() or len(message_parts) != 1:
        bot.sendMessage("usage: .linden gamble <number 1-3>\nit's 2L$ to enter\n5$L if you win",
            thread_id=thread_id, thread_type=thread_type)
        return
    guess, number = int(message_parts[0]), random.randint(1, 3)
    if 1 > guess or guess > 3:
        bot.sendMessage("number between 1 and 3 please",
            thread_id=thread_id, thread_type=thread_type)
        return
    user = USERDB.get(USER.id == author_id)
    user_lindens = user["lindens"]
    if user_lindens < 3:
        bot.sendMessage(u"you'd be broke boyo",
                thread_id=thread_id, thread_type=thread_type)
        return

    if guess == number:
        bot.sendMessage(u"you won, thats ✔ some good👌👌\n5L$ added to your balance",
                thread_id=thread_id, thread_type=thread_type)
        USERDB.update({"lindens": user_lindens + 5}, USER.id == author_id)

    else:
        bot.sendMessage(u"you lost, the number was {}\n3L$ removed from your balance".format(number),
            thread_id=thread_id, thread_type=thread_type)
        USERDB.update({"lindens": user["lindens"] - 3}, USER.id == author_id)
    bot.sendMessage(u"your new balance is {:.4f}L$".format(get_balance(author_id)),
            thread_id=thread_id, thread_type=thread_type)


SUBCOMMANDS = {
    'give': give_cmd,
    'gamble': gamble_cmd,
    'send': give_cmd,
    'table': table_cmd,
    'list': table_cmd,
    'invest': invest_cmd,
}


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage('you have {:.4f} Linden Dollars™'.format(get_balance(author_id)),
                        thread_id=thread_id, thread_type=thread_type)
        return

    subcommand, *args = message.split()
    SUBCOMMANDS.setdefault(subcommand, invalid_cmd)(bot, args, author_id, thread_id, thread_type)


if __name__ == "__main__":
    # tests
    class Bot:

        @staticmethod
        def sendMessage(message, *args, **kwargs):
            print(message)

        @staticmethod
        def fetchAllUsers(*args, **kwargs):
            return [{"id": "2343", "name": "steely"},
                    {"id": "5435", "name": "dan"},
                    {"id": "54344445", "name": "egg gggggggbobu"}]

    b = Bot()
    main(Bot, '2343', 'send dan 6', 1, 1)
    main(Bot, '2343', 'send egg gggggggbobu 6', 1, 1)
    main(Bot, '2343', 'table', 1, 1)
