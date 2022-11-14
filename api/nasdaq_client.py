from typing import List, Optional
from datetime import datetime
import http.client
import json
import pycountry

from helpers.dateConverter import dateToStringFormat
from helpers.countryCode import getCountryCode

class NasdaqClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_bigmac_index_as_of(self, date: datetime, country: str) -> float:
        """
        Returns the value of the BigMac index for `country` as of `date`
        Return type: float
        """

        return self.__get_bigmac_index(country, date)

    def get_bigmac_index_from_range(self, from_date: datetime, to_date: datetime, country:str) -> List[float]:
        """
        Returns the values of the BigMac index for `country` for a range from `from_date`
        to `to_date`
        Return type: list of float
        """

        return self.__get_bigmac_index(country, from_date, to_date)

    def __get_bigmac_index(self, country:str, from_date:datetime, to_date:Optional[datetime]=None):
        """
            same logic principle applies for both 'get_bigmac_index_from_range()' and 'get_bigmac_index_as_of()'
            using single function to avoid code duplication
        """
        try:
            db_code = f'ECONOMIST/BIGMAC_{getCountryCode(country)}'
            fromdate = dateToStringFormat(from_date)

            if to_date == None:
                todate = fromdate
            else:
                todate = dateToStringFormat(to_date)

            queryString = f'api_key={self.api_key}&start_date={fromdate}&end_date={todate}&order=asc'
            url = f'/api/v3/datasets/{db_code}/data.json?{queryString}'

            connection = http.client.HTTPSConnection('data.nasdaq.com')
            connection.request('GET', url)
            response = json.loads(connection.getresponse().read().decode())
            data = response.get('dataset_data', {}).get('data')

            if data == None or len(data) == 0:  # incorrect response format or no data found
                return None

            # one record possible in this case
            if to_date == None:
                return response.get('dataset_data').get('data')[0][5]   # dollar valuation (test requred)

            # collecting possible multiple records
            result = []
            for record in data:
                result.append(record[5])    # dollar valuation (test requred)

            return result
        except http.client.HTTPException as e:
            # do some connection error loggin here maybe...
            raise e
        except Exception as e:
            # do some general error loggin here maybe...
            raise e

    def getApiKey(self):
        return self.api_key
