import socket
import urllib3
import urllib.parse
import certifi
import re
import json
from datetime import date, timedelta, datetime
from aoi_sql_db_rw import SqliteDB


class Aoi:
    def __init__(self):
        self.headers = {'Authorization': 'Basic d2Vic2VydmljZXM6cmFkZXh0ZXJuYWw='}
        self.hostname = 'ws-proxy01.rad.com'
        self.port = '8445'
        self.path = '/ATE_WS/ws/misc/'
        self.data_obj = {}

    def connect(self):
        url = 'https://'

        # context = ssl.create_default_context()
        url += self.hostname + ':' + self.port + self.path
        try:
           with socket.create_connection((self.hostname, self.port)):
               # print(f'connect url:{url}')
               return True, url
        except Exception as e:
           return False, {f'Failed to connect to {self.hostname}:{self.port}, {e}'}

    def get_data_cert(self):
        print(f'get_data_cert {self.url}')
        data = {}
        err_msg = {f"Fail to get data from AOI"}
        http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )

        resp = http.request('GET', self.url, headers=self.headers)
        print(f'resp.status:{resp.status}')
        if resp.status != 200:
            return False, err_msg

        if self.print_rtext:
            pass; #print(f'r.data:<{resp.data.decode()}>')

        #if self.print_rtext:
        #    print(f'r.text:<{data}>')
        data = json.loads(resp.data)
        # return data

        inside_data = data[f'GCC_AOI']
        return inside_data


    def get_data_from_aoi(self, dateFrom, dateTo):
        partial_url = 'GCC_AOI' + '?start_date=' + dateFrom + '&end_date=' + dateTo
        res, url = self.connect()
        if res:
            self.url = url + partial_url
            res = self.get_data_cert()
            print(f'self.url:{self.url} res1_type:{type(res)} {len(res)}')
            if 'False' in res:
                return False
            else:
                return res
        else:
            return False, url

if __name__ == '__main__':
    # https://ws-proxy01.rad.com:8445/ATE_WS/ws/misc/GCC_AOI?start_date=08/04/2024&end_date=09/04/2024
    aoi = Aoi()
    aoi.print_rtext = True
    #df = []
    days_ago = 8; # config['days_ago']
    date_from_string = str((date.today() - timedelta(days=days_ago)).strftime("%d/%m/%Y"), ) #'08/04/2024'  #
    today_date_string = date.today().strftime('%d/%m/%Y') #'09/04/2024' #


    df = aoi.get_data_from_aoi(date_from_string, today_date_string)
    if len(df) == 0:
        print(f"No AOI data from {date_from_string} up to {today_date_string}")
        exit(-1)
    elif df[0] is False:
        print('ee', df[1])
        exit(df[1])
    else:
        tbl = SqliteDB()
        tbl.fill_table("AOI_data", df)
