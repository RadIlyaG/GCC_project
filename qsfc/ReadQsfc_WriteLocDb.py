import os, sys
import socket
import urllib3
import urllib.parse
import certifi
import re
import json
from datetime import date, timedelta, datetime
import time
import logging
import utils.lib_gen as gen
import utils.mdl_logger
from utils.mdl_logger import setup_logger

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from utils.sql_db_rw import SqliteDB


# def timer(func):
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         result = func(*args, **kwargs)
#         end = time.perf_counter()
#         print(f"Function {func.__name__} done during {end - start:.4f} sec")
#         return result
#     return wrapper


class Qsfc:
    def __init__(self):
        self.headers = {'Authorization': 'Basic d2Vic2VydmljZXM6cmFkZXh0ZXJuYWw='}
        self.hostname = 'ws-proxy01.rad.com'
        self.port = '8445'
        self.path = '/ATE_WS/ws/rest/'
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

    # @timer
    def get_data_cert(self, qry_type):
        print(f'get_data_cert {self.url}')
        data = {}
        err_msg = {f"Fail to get data from QSFC"}
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
        #data = resp.json()
        data = json.loads(resp.data)
        #return data

        inside_data = data[f'{qry_type}ReportQSFC']
        #print(f'type(inside_data):{type(inside_data)} inside_data:{inside_data}')
        # # print(f'inside_data:{inside_data} type(inside_data):{type(inside_data)} len(inside_data):{len(inside_data)}')
        # if len(inside_data) == 0:
        #     return False, err_msg
        # else:
        #     if 'null' in inside_data[0].values():
        #         return False, err_msg
        #     return True, inside_data[0]
        return inside_data


    @gen.timer
    def get_data_from_qsfc(self, qry_type, dateFrom, dateTo):
        partial_url = qry_type + 'ReportQSFC' + '?dateFrom=' + dateFrom + '&dateTo=' + dateTo
        res, url = self.connect()
        if res:
            self.url = url + partial_url
            res = self.get_data_cert(qry_type)
            print(f' len of res:{len(res)}')
            if 'False' in res:
                return False
            else:
                return res
        else:
            return False, url




if __name__ == '__main__':

    try:
        with open("read_qsfc_config.json", 'r') as f:
            config = json.load(f)
    except Exception as exp:
        print(f'Exception when read_qsfc_config.json: {exp}')
    else:
        setup_logger('read_qsfc.db_log.html')
        logger = logging.getLogger(__name__)

        sql_obj = SqliteDB()
        sql_obj.db_name(os.path.dirname(os.path.abspath(__file__)), 'db_qsfc.db')
        #rr = sql_obj.get_last_date('Prod', 'open_date')
        #print(rr)
        #exit(0)

        qsfc = Qsfc()
        qsfc.print_rtext = True
        df = []
        #days_ago = 2000 # 2000 = ~5.5 years  #config['days_ago']
        #date_from_string = str((date.today() - timedelta(days=days_ago)).strftime("%d/%m/%Y"), )
        today_date_string = date.today().strftime('%d/%m/%Y')

        #date_from_string = f"01/01/{(date.today() - timedelta(days=365)).strftime('%Y')}"
        #today_date_string = '31/12/2024'

        for tbl_name in ['Prod', 'RMA']:
            try:
                last_date = sql_obj.get_last_date(tbl_name, 'open_date')
                gen_obj = gen.FormatDates()
                date_from_string = gen_obj.get_next_day(last_date)
            except Exception:
                # if no db file
                date_from_string = '01/01/2021'
                today_date_string = '31/05/2025'
            df = qsfc.get_data_from_qsfc(tbl_name, date_from_string, today_date_string)
            if len(df)==0:
                #logger =utils.mdl_logger.get_logger(__name__, 'read_qsfc_db_log.html')
                #logger = logging.getLogger(__name__)
                logger.warning(f'No new data for {tbl_name} between {date_from_string} and {today_date_string}')
            elif df[0] is False:
                print(f'Error during get QSFC {tbl_name} Data', df[1])
                logger.error(f'Error during get QSFC {tbl_name} Data', df[1])
                exit(df[1])
            else:
                #sql_obj = SqliteDB()
                #sql_obj.db_name(os.path.dirname(os.path.abspath(__file__)), 'db_qsfc.db')
                sql_obj.fill_table(tbl_name, df)
                logger.info(f'QSFC Data from {tbl_name} between {date_from_string} and {today_date_string} '
                           f'has been inserted successfully')
