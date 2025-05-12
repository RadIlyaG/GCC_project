import os
import time
import re
from datetime import datetime
from pathlib import Path
import subprocess
import socket
import json
import webbrowser
#import serial

#import lib_radapps_1pDownload as radapps

# import app_logger
# logger = app_logger.get_logger(__name__)


class Gen:
    def __init__(self, mainapp):
        self.os = os.name
        self.hidraw = "0"
        self.mainapp = mainapp
        
    def read_init(self, appwin, host_fld):
        print(f'read_init, self:{self}, appwin:{appwin}, host_fld:{host_fld}')
        # logger.info(f'\nread_hw_init, gui_num:{gui_num}, host_fld:{host_fld}')
        # print(f'read_init script_dir {os.path.dirname(__file__)}')
        # host = ip.replace('.', '_')
        Path(host_fld).mkdir(parents=True, exist_ok=True)
        ini_file = Path(os.path.join(host_fld, "init" + ".json"))
        if os.path.isfile(ini_file) is False:
            dicti = {
                'geom': '+210+210'
            }
            self.save_init(appwin)

        try:
            with open(ini_file, 'r') as fi:
                dicti = json.load(fi)
        except Exception as e:
            # print(e)
            # raise(e)
            raise Exception("e")

        print(f'read_init {ini_file} {dicti}')
        return dicti

    def save_init(self, appwin, **options):
        print(f'save_init, self:{self}, appwin:{appwin}, {appwin.gaSet}, options: {options}')
        ip = appwin.gaSet['pc_ip']
        host = ip.replace('.', '_')
        host_fld = appwin.gaSet['host_fld']
        Path(f'hosts/'+host).mkdir(parents=True, exist_ok=True)
        ini_file = Path(os.path.join(host_fld, "init" + ".json"))
        print(f'save_init host:<{host}>, pwd:<{os.getcwd()}>, ini_file:<{ini_file}>')

        di = {}
        try:
            di =  Gen.read_init(self, appwin, host_fld)
        except:
            di = {}
        #self.gaSet = {**ini_dict}
        try:
            # di['geom'] = "+" + str(dicti['root'].winfo_x()) + "+" + str(dicti['root'].winfo_y())
            geom = self.get_xy(appwin)
        except:
            geom = "+230+233"

        di['geom'] = geom

        #print('rb_var_from_range: ', appwin.gaSet['rb_var_from_range'])
        print('options: ', options)
        if options:
            for key in options.keys():
                di[key] = options[key]
        print(f'save_init, geom:{geom}')
        print(f'save_init, di:{di}')
        try:
            with open(ini_file, 'w+') as fi:
                json.dump(di, fi, indent=2, sort_keys=True)
                # json.dump(gaSet, fi, indent=2, sort_keys=True)
        except Exception as e:
            print(f'Exception: {e}')
            raise (e)

    def get_xy(self, top):
        print('get_xy', top)
        return str("+" + str(top.winfo_x()) + "+" + str(top.winfo_y()))

    def open_history(self):
        new = 2  # open in a new tab, if possible
        url = "history.html"
        webbrowser.open(url, new=new)

    def my_time(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def add_to_log(self, txt):
        with open(self.mainapp.gaSet['log'], 'a') as log:
            if txt == '':
                text = f'\n'
            else:
                text = f'{self.my_time()} {txt}\n'
            log.write(text)


    def play_sound(self, sound='pass.wav'):
        """ 'fail.wav' 'info.wav' 'pass.wav' 'warning.wav' """
        # with subprocess.Popen([f'aplay /home/ilya/Wav/{sound}'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                  stderr=subprocess.PIPE, text=True) as process:
        #     print(f'returncode:<{process.returncode}>')
        subprocess.Popen([f'aplay /home/ilya/Wav/{sound}'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True)

class FormatDates:
    def __init__(self):
        pass

    def format_date_to_uso(self, date):  # rom '15/06/2024' → '2024-06-15 2024-06-15 00:00:00.000000'
        date_from_obj = datetime.strptime(date, '%d/%m/%Y')
        return date_from_obj.strftime('%Y-%m-%d %H:%M:%S.%f')

    def format_date_from_iso(self, date):  # from '2024-06-15' → '15/06/2024'
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
