import os
import socket
import urllib3
import certifi
import json
import logging
import time
from datetime import date, timedelta
from utils.sql_db_rw import SqliteDB
import utils.lib_gen as gen
from utils.mdl_logger import setup_logger
#from utils.mdl_logger import get_logger

# def timer(func):
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         result = func(*args, **kwargs)
#         end = time.perf_counter()
#         time_res = f"Function {func.__name__} {args[1:]} done during {end - start:.4f} sec"
#         print(time_res)
#         logger = get_logger(__name__, 'temp_log.log')
#         logger.info(time_res)
#         return result
#
#     return wrapper


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

    @gen.timer
    def get_data_from_aoi(self, dateFrom, dateTo):
        partial_url = 'GCC_AOI' + '?start_date=' + dateFrom + '&end_date=' + dateTo
        res, url = self.connect()
        if res:
            self.url = url + partial_url
            res = self.get_data_cert()
            # print(f'self.url:{self.url} res1_type:{type(res)} {len(res)}')
            print(f' len of res:{len(res)}')
            if 'False' in res:
                return False
            else:
                return res
        else:
            return False, url

if __name__ == '__main__':
    # https://ws-proxy01.rad.com:8445/ATE_WS/ws/misc/GCC_AOI?start_date=05/06/2025&end_date=10/06/2025
    setup_logger('read_aoi.db_log.html')
    logger = logging.getLogger(__name__)

    aoi = Aoi()
    aoi.print_rtext = True
    #df = []
    days_ago = 180; # config['days_ago']

    for st, en in ('01/01/2025', '28/02/2025'), ('01/03/2025', '31/05/2025'):
        pass
    for st, en in ('29/05/2025', '29/05/2025'),:
        pass
    for st, en in (('01/01/2025', '31/01/2025'), ('01/02/2025', '28/02/2025'),
                   ('01/03/2025', '31/03/2025'), ('01/04/2025', '30/04/2025'),
                   ('01/05/2025', '31/05/2025')):
        pass
    for st, en in ('29/05/2025', '29/05/2025'),:
        date_from_string = st #'09/04/2025' # str((date.today() - timedelta(days=days_ago)).strftime("%d/%m/%Y"), ) #'08/04/2024'  #
        today_date_string = en #'01/06/2025' # date.today().strftime('%d/%m/%Y') #'09/04/2024' #

        df = aoi.get_data_from_aoi(date_from_string, today_date_string)
        if len(df) == 0:
            print(f"No AOI data from {date_from_string} up to {today_date_string}")
            logger.info(f'No new AOI data between {date_from_string} and {today_date_string}')
            exit(-1)
        elif df[0] is False:
            print('ee', df[1])
            logger.error(f'Error during get AOI Data', df[1])
            exit(df[1])
        else:
            db_path = os.path.dirname(os.path.abspath(__file__))
            db_file_name = f'db_aoi.db'
            sql_obj = SqliteDB()
            sql_obj.db_name(db_path, db_file_name)
            sql_obj.fill_table("AOI_data", df, chk_exist='yes')
            logger.info(f'AOI Data between {date_from_string} and {today_date_string} has been inserted successfully')
