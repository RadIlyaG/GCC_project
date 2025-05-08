import socket
import urllib3
import urllib.parse
import certifi
import re
import json
from datetime import date, timedelta, datetime
from sql_db_rw import SqliteDB


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


    def get_data_from_qsfc(self, qry_type, dateFrom, dateTo):
        partial_url = qry_type + 'ReportQSFC' + '?dateFrom=' + dateFrom + '&dateTo=' + dateTo
        res, url = self.connect()
        if res:
            self.url = url + partial_url
            res = self.get_data_cert(qry_type)
            print(f'self.url:{self.url} res:{res}')
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
        qsfc = Qsfc()
        qsfc.print_rtext = True
        df = []
        days_ago = config['days_ago']
        date_from_string = str((date.today() - timedelta(days=days_ago)).strftime("%d/%m/%Y"), )
        today_date_string = date.today().strftime('%d/%m/%Y')

        for tbl_name in ['Prod', 'RMA']:
            df = qsfc.get_data_from_qsfc(tbl_name, date_from_string, today_date_string)

            tbl = SqliteDB()
            tbl.fill_table(tbl_name, df)
