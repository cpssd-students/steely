import csv
import codecs

import requests

from plugin import create_plugin
from message import SteelyMessage

HELP_STR = """Get live Coronavirus numbers in various regions.
Run /corona to get some info.
"""

plugin = create_plugin(name='corona', author='iandioch', help=HELP_STR)

def get_canton_data(canton='ZH'):
    # This CSV is messy. There are very many missing fields, because each canton
    # reports different data, and each new row is populated in increments (eg.
    # they might know how many are in quarantine that day in the morning, but
    # might not take hospital counts until the evening, etc.).
    csv_url = f'https://github.com/openZH/covid_19/raw/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_{canton}_total.csv'
    csv_lines = requests.get(csv_url).iter_lines()
    print(csv_lines)
    reader = csv.reader(codecs.iterdecode(csv_lines, 'utf-8'), delimiter=',')
    # Columns of CSV:
    # [0: date, 1: time, 2: abbreviation_canton_and_fl, 3: ncumul_tested, 
    # 4: ncumul_conf, 5: new_hosp, 6: current_hosp, 7: current_icu,
    # 8: current_vent, 9: ncumul_released, 10: ncumul_deceased, 11: source,
    # 12: current_isolated, 13: current_quarantined,
    # 14: current_quarantined_riskareatravel, 15: current_quarantined_total]

    # Rows N-2, N-1
    last_rows = (None, None)
    for i, row in enumerate(reader):
        last_rows = (last_rows[-1], row)
        # Skip the first few rows to avoid going None in last_rows,
        # and to skip the header row.
        if i < 3:
            continue
        # Make sure all the rows we need are present, as they are not all
        # updated at the same time.
        if any(row[i] == '' for i in [0, 4, 11]):
            continue
        try: 
            num_new_cases = int(last_rows[-1][4]) - int(last_rows[-2][4])
            num_isolated = last_rows[-1][12]
            num_isolated = num_isolated if num_isolated != '' else '(idk)'
            num_quarantined = last_rows[-1][13]
            num_quarantined = num_quarantined if num_quarantined != '' else '(idk)'
            date = last_rows[-1][0]
            source = last_rows[-1][11]
        except Exception as e:
            # We don't really care if it failed because a row was missing or w/e.
            pass

    return (f'On {date}, there were {num_new_cases} new cases reported in ' +
            f'Canton {canton}, with {num_isolated} in isolation and ' +
            f'{num_quarantined} in quarantine. Source: {source}')


def get_country_data(country):
    # This is a simple API that has a scraper of worldometers.info behind it.
    # Sometimes some fields are empty...
    url = f'https://covid-19.dataflowkit.com/v1/{country}'
    data = requests.get(url).json()

    date = data['Last Update']
    new_cases = data['New Cases_text']
    total_active = data['Active Cases_text']
    source_url = f'https://www.worldometers.info/coronavirus/country/{country}/'

    return (f'{date}: There were {new_cases} new cases, for a total of ' +
            f'{total_active} active cases in {country}. Source: {source_url}')



# Each mapped func should return a string ready to send to the bot. All dict
# keys should be lowercased.
LOCATION_FUNCTION_MAP = {
    # Countries, and aliases (country codes, native forms, etc).
    'ireland': lambda: get_country_data('ireland'),
    'éire': lambda: get_country_data('ireland'),
    'eire': lambda: get_country_data('ireland'),
    'roi': lambda: get_country_data('ireland'),
    'ire': lambda: get_country_data('ireland'),
    'ie': lambda: get_country_data('ireland'),
    'switzerland': lambda: get_country_data('switzerland'),
    'switz': lambda: get_country_data('switzerland'),
    'schweiz': lambda: get_country_data('switzerland'),
    'suisse': lambda: get_country_data('switzerland'),
    'svizzera': lambda: get_country_data('switzerland'),
    'svizra': lambda: get_country_data('switzerland'),
    'ch': lambda: get_country_data('switzerland'),
    'greece': lambda: get_country_data('greece'),
    'ελλάδα': lambda: get_country_data('greece'),
    'gr': lambda: get_country_data('greece'),
    'romania': lambda: get_country_data('romania'),
    'românia': lambda: get_country_data('romania'),
    'ro': lambda: get_country_data('romania'),
    'italy': lambda: get_country_data('italy'),
    'italia': lambda: get_country_data('italy'),
    'it': lambda: get_country_data('italy'),
    'germany': lambda: get_country_data('germany'),
    'deutschland': lambda: get_country_data('germany'),
    'de': lambda: get_country_data('germany'),
    'france': lambda: get_country_data('france'),
    'fr': lambda: get_country_data('france'),
    'austria': lambda: get_country_data('austria'),
    'österreich': lambda: get_country_data('austria'),
    'at': lambda: get_country_data('austria'),
    'uk': lambda: get_country_data('uk'),
    'gb': lambda: get_country_data('uk'),

    # Swiss cantons, and some common shortened forms and aliases.
    'zurich': lambda: get_canton_data(canton='ZH'),
    'zuerich': lambda: get_canton_data(canton='ZH'),
    'zürich': lambda: get_canton_data(canton='ZH'),
    'zrh': lambda: get_canton_data(canton='ZH'),
    'zh': lambda: get_canton_data(canton='ZH'),
    'geneva': lambda: get_canton_data(canton='GE'),
    'geneve': lambda: get_canton_data(canton='GE'),
    'genève': lambda: get_canton_data(canton='GE'),
    'ge': lambda: get_canton_data(canton='GE'),
    'bern': lambda: get_canton_data(canton='BE'),
    'be': lambda: get_canton_data(canton='BE'),
    'zug': lambda: get_canton_data(canton='ZG'),
    'zg': lambda: get_canton_data(canton='ZG'),
    'vaud': lambda: get_canton_data(canton='VD'),
    'vd': lambda: get_canton_data(canton='VD'),
    'valais': lambda: get_canton_data(canton='VS'),
    'wallis': lambda: get_canton_data(canton='VS'),
    'vs': lambda: get_canton_data(canton='VS'),
}

@plugin.listen(command='corona [location]')
def corona(bot, message: SteelyMessage, **kwargs):
    locs = ', '.join(sorted(LOCATION_FUNCTION_MAP.keys()))
    text = f'Please provide a location to look up. Recognised locations: {locs}'
    if 'location' in kwargs:
        loc = kwargs['location'].lower()
        if loc in LOCATION_FUNCTION_MAP:
            try:
                text = LOCATION_FUNCTION_MAP[loc]()
            except Exception as e:
                text = 'Error looking up location "{}": `{}`'.format(loc,
                                                                     str(e))
        else:
            text = f'Location "{loc}" not recognised. Recognised locations: {locs}'

    bot.sendMessage(text,
                    thread_id=message.thread_id,
                    thread_type=message.thread_type)

