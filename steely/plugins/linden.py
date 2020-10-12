#!/usr/bin/env python3
'''
linden gives the plebians currency.

initialise your account:
.linden init

give lindens to people:
.linden give <user> <amount>
.linden send <user> <amount>

gamble:
.linden gamble <number between 1 and 3>

list the current lindens:
.linden list
.linden table

invest in the stock market:
.linden invest <`buy|sell|quote|list`> <nasdaq stock>
.linden invest list
'''


from datetime import datetime, timedelta
from formatting import *
from plugins import gex
from tinydb import Query, where
from tinydb.operations import increment
from utils import new_database
import json
import random
import requests
import tabulate


__author__ = 'CianLR'
COMMAND = "linden"
USERDB = new_database('linden')
USER = Query()
REED_ID = None


class YahooTickerFetcher:

    def __init__(self):
        self.base_url = 'https://query.yahooapis.com/v1/public/yql'
        self.param_string = ('?q={}&format=json&env='
                             'store://datatables.org/alltableswithkeys')
        self.query = ('select Symbol,Ask,Bid '
                      'from yahoo.finance.quotes where symbol in ("{}")')

    def GetMultiple(self, tickers):
        if not tickers:
            return []

        filled_q = self.query.format('","'.join(tickers))
        filled_params = self.param_string.format(filled_q)

        r = requests.get(self.base_url + filled_params)
        if len(tickers) == 1:
            # Yahoo for some reson changes the API slightly if you reqest only one ticker.
            # Wrap the return in a list so we have a consistent API
            return [json.loads(r.text)['query']['results']['quote']]
        return json.loads(r.text)['query']['results']['quote']

    def GetSingle(self, ticker):
        return self.GetMultiple([ticker])[0]


class AlphaVantageTickerFetcher:

    def __init__(self):
        self.base_url = "https://www.alphavantage.co/query"
        self.params = ("?function=TIME_SERIES_INTRADAY"
                       "&symbol={}&interval=1min&apikey={}")
        self.KEY = "6A98QBQPTOVNV1AD"

    def GetMultiple(self, tickers):
        return [self.GetSingle(t) for t in tickers]

    def GetSingle(self, ticker):
        url = self.base_url + self.params.format(ticker, self.KEY)

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


class IEXTickerFetcher:

    def __init__(self):
        self.base_url = 'https://api.iextrading.com/1.0/tops/last?symbols='

    def GetMultiple(self, tickers):
        url = self.base_url + ','.join(tickers)
        r = requests.get(url)
        res = []
        for i, quote in enumerate(json.loads(r.text)):
            if quote is None:
                res.append({'Symbol': tickers[i], 'Bid': None, 'Ask': None})
                continue
            res.append({'Symbol': tickers[i], 'Bid': quote[
                       'price'], 'Ask': quote['price']})
        return res

    def GetSingle(self, ticker):
        return self.GetMultiple([ticker])[0]


TICKER_FETCHERS = [
    IEXTickerFetcher(),  # Fast, hopefully robust
    YahooTickerFetcher(),  # Fast, super flakey
    AlphaVantageTickerFetcher()  # Slow, little flakey
]


def user_from_name(name, user_list):
    # TODO(CianLR): Assuming a first name is unique is not good, use something
    # else maybe. (user_id?)
    for user in user_list:
        if user['first_name'].lower() == name.lower():
            return user


def list_users(bot, thread_id):
    groups = bot.fetchGroupInfo(thread_id)
    if len(groups) == 0:
        return
    user_ids = groups[0]['users']
    for user_id in user_ids:
        matching_users = bot.fetchUserInfo(user_id)
        if len(matching_users) == 0:
            continue
        yield matching_users[0]


def create_user(uid, first_name):
    data = {"id": uid,
            "first_name": first_name,
            "investments": {},
            "lindens": 2000}
    USERDB.insert(data)
    return data


def handle_gex_sell_cards(user_id, ticker, profit):
    NOAH_ID = '100003244958231'
    MIN_TICKER_CARD_DELTA = 25
    ticker_cards = [
        ('dcth', 'I traded the meme stock'),
        ('aapl', 'I drank a cupertino of the kool aid'),
        ('goog', 'I only know like one stock ticker symbol'),
        ('snap', 'I am the hot dog'),
        ('nvda', 'Green is the warmest colour'),
        ('amd', 'The Red Army and Navy and the whole Soviet people must fight for every inch of Soviet soil, fight to the last drop of blood for our towns and villages...onward, to victory!'),
    ]
    cards = ticker_cards[:]
    vals = [2000, 1500, 1000, 750, 500, 250, 100]
    for v in vals:
        cards.append(
            ('{}-gain'.format(v), 'I earned {} lindens in one sell xo'.format(v)))
        cards.append(
            ('{}-loss'.format(v), 'I dropped a bag of {} lindens :('.format(v)))

    # try to create badges if they don't already exist
    for card_id, desc in cards:
        try:
            gex.gex_create(card_id, [REED_ID, NOAH_ID], desc)
        except RuntimeError as e:
            print('Could not create card:', e)

    # give ticker cards
    for card_id, desc in ticker_cards:
        if card_id.upper() == ticker and abs(profit) >= MIN_TICKER_CARD_DELTA:
            gex.gex_give(REED_ID, card_id, user_id)

    # give profit & loss cards
    for val in vals:
        if profit > val:
            gex.gex_give(REED_ID, '{}-gain'.format(val), user_id)
        if profit < -val:
            gex.gex_give(REED_ID, '{}-loss'.format(val), user_id)


def get_balance(user_id):
    matching_users = USERDB.search(USER.id == user_id)
    if len(matching_users) == 0:
        return
    return matching_users[0]['lindens']


def give_cmd(bot, message_parts, author_id, thread_id, thread_type):
    users = list_users(bot, thread_id)
    if not message_parts[-1].isdigit() or message_parts[-1] == "0":
        bot.sendMessage('please enter a valid amount',
                        thread_id=thread_id, thread_type=thread_type)
        return
    reciever_name, amount = message_parts[0].lstrip(
        "@").capitalize(), int(message_parts[-1])
    reciever_model = user_from_name(reciever_name, users)
    if reciever_model is None:
        bot.sendMessage("Unrecognised reciever",
                        thread_id=thread_id, thread_type=thread_type)
        return
    reciever = USERDB.get(USER.id == reciever_model['id'])
    sender_model = bot.fetchUserInfo(author_id)[0]
    sender = USERDB.get(USER.id == author_id)
    if sender_model['id'] == reciever_model['id']:
        bot.sendMessage('no', thread_id=thread_id, thread_type=thread_type)
        return
    if not reciever:
        reciever = create_user(
            reciever_model['id'],
            reciever_model['first_name'])
    if not sender:
        sender = create_user(author_id, sender_model['first_name'])
    new_sender_balance = sender['lindens'] - amount
    if new_sender_balance < 0:
        bot.sendMessage('you\'d be broke boyo',
                        thread_id=thread_id, thread_type=thread_type)
        return
    USERDB.update({'lindens': new_sender_balance}, USER.id == author_id)
    USERDB.update(
        {'lindens': reciever['lindens'] + amount}, USER.id == reciever_model['id'])
    bot.sendMessage('you gave {} {} Linden Dollars™'.format(reciever_name, amount),
                    thread_id=thread_id, thread_type=thread_type)


def table_cmd(bot, message_parts, author_id, thread_id, thread_type):
    users = list(USERDB.all())
    if not users:
        bot.sendMessage(
            "Database returned no users",
            thread_id=thread_id,
            thread_type=thread_type)
        return
    max_lindens = len(str(max(user['lindens'] for user in USERDB.all())))
    max_name = len(max((user['first_name'] for user in USERDB.all()), key=len))
    string = ''
    for user in sorted(
            USERDB.all(), key=lambda user: user['lindens'], reverse=True):
        string += '\n{name:<{max_name}} {lindens:>{max_lindens}.3f}L$'.format(
            name=user['first_name'], lindens=user['lindens'],
            max_name=max_name, max_lindens=max_lindens + 4)
    bot.sendMessage(code_block(string), thread_id=thread_id,
                    thread_type=thread_type)


QUOTE_CACHE = {}
QUOTE_TTL = timedelta(minutes=10)


def invest_check_valid_quote(quote):
    return "Bid" in quote and quote["Bid"] and "Ask" in quote and quote["Ask"]


def invest_get_quotes_multi_source(tickers):
    # Iterate through each of the fetchers, removing tickers as a quote is
    # found.
    if not tickers:
        return []
    done = []
    for source in TICKER_FETCHERS:
        redo = []
        for res in source.GetMultiple(tickers):
            if invest_check_valid_quote(res):
                done.append(res)
            else:
                redo.append(res['Symbol'])
        if not redo:
            break
        tickers = redo
    return done


def invest_get_quotes_w_cache(tickers):
    cached_quotes = []
    tics_to_get = []
    # Check for a quote from the cache
    for tic in tickers:
        if tic not in QUOTE_CACHE:
            tics_to_get.append(tic)
        elif datetime.now() - QUOTE_CACHE[tic]['time'] > QUOTE_TTL:
            tics_to_get.append(tic)
        elif not invest_check_valid_quote(QUOTE_CACHE[tic]):
            tics_to_get.append(tic)
        else:
            cached_quotes.append(QUOTE_CACHE[tic])
    # Get all the new/expired/invalid quotes
    new_quotes = invest_get_quotes_multi_source(tics_to_get)
    for quote in new_quotes:
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
               "but you need {total_cost:.2f}L$ ({qt} * {ask:.2f})".format_map(
                   locals())
    # Edit that database
    total_holdings = USERDB.get(USER.id == user_id)['investments']
    new_holding = {'symbol': tic, 'quantity': qt, 'orig_value': total_cost}
    if tic in total_holdings:
        new_holding['quantity'] += total_holdings[tic]['quantity']
        new_holding['orig_value'] += total_holdings[tic]['orig_value']
    total_holdings[tic] = new_holding
    USERDB.update({'investments': total_holdings}, USER.id == user_id)
    USERDB.update({'lindens': user_balance - (total_cost)}, USER.id == user_id)
    return "Successfully bought {} shares of ${} for {:.4f}L$".format(
        qt, tic, total_cost)


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
    orig_bid = total_holdings[tic]['orig_value'] / \
        total_holdings[tic]['quantity']
    total_holdings[tic]['orig_value'] -= orig_bid * qt
    total_holdings[tic]['quantity'] -= qt
    if total_holdings[tic]['quantity'] == 0:
        del total_holdings[tic]
    USERDB.update({'investments': total_holdings}, USER.id == user_id)
    USERDB.update({'lindens': user_balance + (qt * bid)}, USER.id == user_id)

    profit = qt * (bid - orig_bid)
    handle_gex_sell_cards(user_id, tic, profit)
    return "Successfully sold {} shares of ${} for {} Lindens ({:.2f}L profit)".format(
        qt, tic, qt * bid, qt * (bid - orig_bid))


def invest_list_cmd(user_id, args):
    user_balance = get_balance(user_id)
    if user_balance is None:
        return "User does not exist, poke Senan"
    user = USERDB.get(USER.id == user_id)
    out = "{}: {:.2f}L$ Cash\n\n".format(user['first_name'], user['lindens'])
    total_assets = float(user['lindens'])
    tics = list(user['investments'])
    quotes = invest_get_quotes_w_cache(tics)
    total_profit = 0
    table = []
    for quote in quotes:
        holding = user['investments'][quote['Symbol']]
        quant, orig_value = holding['quantity'], holding['orig_value']

        if quote['Bid'] is None:
            print("Broken stock", holding['symbol'],
                  'for', user_id, '\nfull quote:\n', quote)

            return "The following stock broke: " + holding['symbol']

        bid = float(quote['Bid'])
        total_assets += quant * bid

        table.append([quote['Symbol'], quant, quant * bid,
                      100 * ((quant * bid) - orig_value) / orig_value])
        total_profit += (quant * bid) - orig_value
    out += tabulate.tabulate(table, headers=("ticker", "quant",
                                             "value", "% profit"), tablefmt="plain", floatfmt=".4f")
    out += "\nCurrent Profit: {:.2f}L$".format(total_profit)
    out += "\nTotal Assets: {:.2f}L$".format(total_assets)
    return code_block(out)


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
        out_message = invest_cmds[message_parts[0]](
            author_id, message_parts[1:])
    bot.sendMessage(out_message, thread_id=thread_id, thread_type=thread_type)


def invalid_cmd(bot, message_parts, author_id, thread_id, thread_type):
    bot.sendMessage("invalid subcommand", thread_id=thread_id,
                    thread_type=thread_type)


def gamble_cmd(bot, message_parts, author_id, thread_id, thread_type):
    if not message_parts or not message_parts[0].isdigit() or len(
            message_parts) != 1:
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


def init_cmd(bot, message_parts, author_id, thread_id, thread_type):
    user = USERDB.get(USER.id == author_id)
    if user:
        bot.sendMessage("You already have an account sir/maam.",
                        thread_id=thread_id, thread_type=thread_type)
        return
    users = list_users(bot, thread_id)
    user_model = bot.fetchUserInfo(author_id)[0]
    user = create_user(author_id, user_model['first_name'])
    bot.sendMessage('Welcome {}, enjoy your Linden Dollars™'.format(user['first_name']),
                    thread_id=thread_id, thread_type=thread_type)


SUBCOMMANDS = {
    'init': init_cmd,
    'give': give_cmd,
    'gamble': gamble_cmd,
    'send': give_cmd,
    'table': table_cmd,
    'list': table_cmd,
    'invest': invest_cmd,
}


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    REED_ID = bot.uid
    if not message:
        balance = get_balance(author_id)
        if balance is None:
            bot.sendMessage('you have no account, loser',
                            thread_id=thread_id, thread_type=thread_type)
            return
        bot.sendMessage('you have {:.4f} Linden Dollars™'.format(balance),
                        thread_id=thread_id, thread_type=thread_type)
        return

    subcommand, *args = message.split()
    SUBCOMMANDS.setdefault(subcommand, invalid_cmd)(
        bot, args, author_id, thread_id, thread_type)


if __name__ == "__main__":
    # tests
    class Bot:
        def __init__(self):
            self.uid = "4444"
            self._users = [
                {"id": "2343", "first_name": "steely"},
                {"id": "5435", "first_name": "dan"},
                {"id": "54344445", "first_name": "egg"},
                {"id": "1234", "first_name": "Cian"}
            ]

        def sendMessage(self, message, *args, **kwargs):
            print(message)

        def fetchUserInfo(self, user_id):
            for u in self._users:
                if u['id'] == user_id:
                    return [u]
            return None

        def fetchGroupInfo(self, thread_id):
            return [{'users': [u['id'] for u in self._users]}]

        def fetchAllUsers(self, *args, **kwargs):
            return self._users

    b = Bot()
    main(b, '1234', 'init', 1, 1)
    main(b, '2343', 'send dan 6', 1, 1)
    main(b, '2343', 'send egg 6', 1, 1)
    main(b, '2343', 'table', 1, 1)
