from api.nasdaq_client import NasdaqClient
from engines.bigmacDbEngine import BigmacDatabaseEngine
from datetime import datetime
import warnings
import json

from helpers.dateConverter import dateToStringFormat

NASDAQ_API_KEY = 'someKey'
DATABASE_LINK = "sqlite:///bigmac.db"     # database connection can be swapped here!

nasdaqClient = NasdaqClient(NASDAQ_API_KEY)
bigmacDb = BigmacDatabaseEngine(DATABASE_LINK)


def getAndStoreBigmacIndex(country:str, date:datetime):
    if bigmacDb.isRecordExist(country):     # country already exist in db -> abort request
        warnings.warn(f'{country} country already exist in the database, aborting request')
        return False

    index = nasdaqClient.get_bigmac_index_as_of(date, country)

    if index == None:
        warnings.warn(f'no record found for country: {country} at date {dateToStringFormat(date)}')
        return

    bigmacDb.store(country, date, date, [index])
    return True

def getAndStoreBigmacIndexRange(country:str, from_date:datetime, to_date:datetime):
    if bigmacDb.isRecordExist(country):     # country already exist in db -> abort request
        warnings.warn(f'{country} country already exist in the database, aborting request')
        return False

    indexList = nasdaqClient.get_bigmac_index_from_range(from_date, to_date, country)

    if indexList == None:
        warnings.warn(f'no records found for country: {country} between date range of ({dateToStringFormat(from_date)} - {dateToStringFormat(to_date)})')
        return

    bigmacDb.store(country, from_date, to_date, indexList)
    return True


### TEST EXAMPLES
# getAndStoreBigmacIndex('Hungary', datetime(2022, 7, 31))
# getAndStoreBigmacIndex('Switzerland', datetime(2022, 7, 31)) 

# getAndStoreBigmacIndexRange('United States', datetime(1, 1, 1), datetime(2022, 11, 12))
# getAndStoreBigmacIndexRange('Russia', datetime(1, 1, 1), datetime(2022, 11, 12))
# getAndStoreBigmacIndexRange('Hungary', datetime(2021, 1, 1), datetime(2022, 11, 12))    # ignored (duplicate country request) - warning

print( bigmacDb.queryAll() )
bigmacDb.close()
