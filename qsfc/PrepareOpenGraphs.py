"""source .venv/Scripts/activate"""

import tkinter as tk

#from tkinter import tkcalendar
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox, ttk
import re
import os
import glob
from subprocess import check_output
import socket
from pathlib import Path
from PIL import Image, ImageTk
import sys
import functools
from functools import partial
from datetime import date, timedelta, datetime

from Graphs import DrawPlot

##sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from utils import lib_gen
from utils import lib_DialogBox as dbox


class App(tk.Tk):
    '''Create the application on base of tk.Tk, put the frames'''

    def __init__(self):
        super().__init__()
        self.gaSet = {}
        self.title(f'QSFC Graphs Preparing')
        self['relief'] = tk.GROOVE
        self['bd'] = 2

        self.os = os.name
        self.gen = lib_gen.Gen(self)
        ip = self.get_pc_ip()
        self.gaSet['pc_ip'] = ip

        host = ip.replace('.', '_')
        woDir = os.getcwd()
        if '1p_download' in woDir:
            host_fld = os.path.join(woDir, host)
            temp_fld = f'{os.path.dirname(woDir)}/temp'
        else:
            host_fld = os.path.join(woDir, 'hosts', host)
            temp_fld = os.path.join(woDir, 'temp')
        print(f'woDir:<{woDir}> host_fld:<{host_fld}> temp_fld:<{temp_fld}>')
        self.gaSet['host_fld'] = host_fld
        self.gaSet['temp_fld'] = temp_fld
        Path(temp_fld).mkdir(parents=True, exist_ok=True)

        ini_dict = self.gen.read_init(self, host_fld)
        self.gaSet = {**ini_dict}
        self.gaSet['pc_ip'] = ip
        self.gaSet['root'] = self
        self.gaSet['host_fld'] = host_fld
        self.gaSet['temp_fld'] = temp_fld
        #print('aaa', self.gaSet)
        #self.if_rad_net()

        self.put_frames()
        self.put_menu()
        self.gui_num = 1
        self.geometry(self.gaSet['geom'])


        self.status_bar_frame.status("Scan UUT barcode to start")
        # self.bind('<Alt-r>', partial(self.main_frame.frame_start_from.button_run))

    def put_frames(self):
        mainapp = self
        self.main_frame = MainFrame(self, mainapp)
        self.status_bar_frame = StatusBarFrame(self, mainapp)

        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=2, pady=2)
        self.status_bar_frame.pack(expand=True, fill='x')

    def put_menu(self):
        self.config(menu=MainMenu(self))

    def quit(self):
        print('quit', self)
        gen = lib_gen.Gen(self)
        gen.save_init(self)
        #gen = lib_gen.Gen(self)
        gen.play_sound('info.wav')
        db_dict = {
            "title": "Confirm exit",
            "message": "Are you sure you want to close the application?",
            "type": ["Yes", "No"],
            "icon": "::tk::icons::question",
            'default': 0
        }
        dibox = dbox.DialogBox()
        dibox.create(self, db_dict)
        string, res_but, ent_dict = dibox.show()
        # string, res_but, ent_dict = neDialogBox(self, db_dict).show()
        print(string, res_but)
        if res_but == "Yes":
            for f in glob.glob("SW*.txt"):
                os.remove(f)
            self.destroy()
            # ?? no sys ??? sys.exit()

    def get_pc_ip(self):
        if self.os == "posix":
            for ip in check_output(['hostname', '--all-ip-addresses']).decode().split(' '):
                if '10.10.10' not in ip and ip != '\n':
                    break
        else:
            ip = socket.gethostbyname_ex(socket.gethostname())[2][0]

        print(f'get_pc_ip ip:{ip}')
        return ip


class MainMenu(tk.Menu):
    def __init__(self, appwin):
        super().__init__(appwin)

        # ramz = lib_gen.Ramzor()

        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Capture Console")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=appwin.quit)
        self.add_cascade(label="File", menu=file_menu)

        tools_menu = tk.Menu(self, tearoff=0)
        tools_menu.add_command(label="Setup Downloaded Package")
        tools_menu.add_separator()
        # self.pwr_menu = tk.Menu(tools_menu, tearoff=0)
        # self.pwr_menu.add_command(label="PS ON", command=lambda: appwin.gen.gui_Power(1, 1))
        # self.pwr_menu.add_command(label="PS OFF", command=lambda: appwin.gen.gui_Power(1, 0))
        # self.pwr_menu.add_command(label="PS OFF and ON", command=lambda: appwin.gen.gui_PowerOffOn(1))
        # tools_menu.add_cascade(label="Power", menu=self.pwr_menu)
        # tools_menu.add_separator()
        # self.rmz_menu = tk.Menu(tools_menu, tearoff=0)
        # self.rmz_menu.add_command(label="All ON", command=lambda: ramz.ramzor("all", "1"))
        # self.rmz_menu.add_command(label="All OFF", command=lambda: ramz.ramzor("all", "0"))
        # self.rmz_menu.add_command(label="Red ON", command=lambda: ramz.ramzor("red", "1"))
        # self.rmz_menu.add_command(label="Red OFF", command=lambda: ramz.ramzor("red", "0"))
        # self.rmz_menu.add_command(label="Green ON", command=lambda: ramz.ramzor("green", "1"))
        # self.rmz_menu.add_command(label="Green OFF", command=lambda: ramz.ramzor("green", "0"))
        # tools_menu.add_cascade(label="Ramzor", menu=self.rmz_menu)
        self.add_cascade(label="Tools", menu=tools_menu)

        terminal_menu = tk.Menu(self, tearoff=0)
        # terminal_menu.add_command(label=f"UUT: {appwin.gaSet['comDut']}",
        #                           command=lambda: appwin.gen.open_terminal(appwin, "comDut"))
        # self.add_cascade(label="Terminal", menu=terminal_menu)

        chk_menu = tk.Menu(self, tearoff=0)
        chk_menu.add_command(label="chk status",
                             command=lambda: appwin.status_bar_frame.status("comDut", 'green'))
        chk_menu.add_command(label="chk startTime",
                             command=lambda: appwin.status_bar_frame.start_time("11:13:14 23/12/2024"))
        chk_menu.add_command(label="chk runTime",
                             command=lambda: appwin.status_bar_frame.run_time("1234"))
        self.add_cascade(label="checks", menu=chk_menu)


class MainFrame(tk.Frame):
    '''Create the Main Frame on base of tk.Frame'''

    def __init__(self, parent, mainapp):
        super().__init__(parent)
        print(f'MainFrame, self:<{self}>, parent:<{parent}>')
        self['relief'] = self.master['relief']
        # self['bd'] = self.master['bd']
        self.info_frames = []
        self.put_main_frames(mainapp)


    def put_main_frames(self, mainapp):
        self.frame_info_rma = InfoFrame(self, mainapp, 'RMA')
        self.frame_info_pro = InfoFrame(self, mainapp, 'Production')
        self.info_frames.append(self.frame_info_rma)
        self.info_frames.append(self.frame_info_pro)


        self.frame_info_rma.grid(row=1, column=0, sticky="news", padx=2, pady=2)
        #self.frame_info_rma.lab_type.configure(text='RMA')
        self.frame_info_rma.lab_cats.configure(text='Categories: ')

        self.frame_info_pro.grid(row=1, column=1, sticky="news", padx=2, pady=2)
        #self.frame_info_pro.lab_type.configure(text='Production')
        self.frame_info_pro.lab_cats.configure(text='Categories: ')

    def put_widgets(self):
        pass


class StartFromFrame(tk.Frame):
    '''Create the StartFrom Frame on base of tk.Frame'''
    def __init__(self, parent, mainapp):
        super().__init__(parent)
        print(f'StartFromFrame, self:<{self}>, parent:<{parent}>, mainapp:<{mainapp}>')
        self.parent = parent
        self['relief'] = self.master['relief']
        self['bd'] = self.master['bd']
        self.put_widgets()
        self.mainapp = mainapp

    def put_widgets(self):
        self.lab_start_from = ttk.Label(self, text="Start from ")

        self.var_start_from = tk.StringVar()
        self.cb_start_from = ttk.Combobox(self, justify='center', width=20, textvariable=self.var_start_from)

        # script_dir = os.path.dirname(__file__)
        # self.img = Image.open(os.path.join('./../gen_lib', "images", "run1.gif"))
        # use_img = ImageTk.PhotoImage(self.img)
        # self.b_start = ttk.Button(self, text="Start", image=use_img, command=partial(self.button_run))
        # self.b_start.image = use_img
        #
        # self.img = Image.open(os.path.join('./../gen_lib', "images", "stop1.gif"))
        # use_img = ImageTk.PhotoImage(self.img)
        # self.b_stop = ttk.Button(self, text="Stop", image=use_img, command=partial(self.button_stop))
        # self.b_start.b_stop = use_img

        self.lab_curr_test = ttk.Label(self, text='Current Test:')
        self.var_curr_test = tk.StringVar()
        self.lab_curr_test_val = ttk.Label(self, width=20, relief=tk.SUNKEN, anchor="center",
                                           textvariable=self.var_curr_test)

        self.lab_start_from.pack(side='left', padx='2')
        self.cb_start_from.pack(side='left', padx='2')
        # self.b_start.pack(side='left', padx='2')
        # self.b_stop.pack(side='left', padx='2')
        self.lab_curr_test.pack(side='left', padx='2')
        self.lab_curr_test_val.pack(side='left', padx='2')


class InfoFrame(tk.Frame):
    '''Create the Info Frame on base of tk.Frame'''

    def __init__(self, parent, mainapp, frame_name):
        super().__init__(parent)
        print(f'InfoFrame1, self:<{self}>, parent:<{parent}>, mainapp:<{mainapp}, frame_name:<{frame_name}>')
        # self['relief'] = self.master['relief']
        self['relief'] = tk.GROOVE
        self['bd'] = 2
        self.mainapp = mainapp
        self.frame_name = frame_name
        self.parent = parent
        print(f'InfoFrame2, self:<{self}>, parent:<{parent}>, mainapp:<{mainapp}>, self.mainapp:<{self.mainapp}>, self.frame_name:<{self.frame_name}>')

        self.put_widgets(mainapp)

    def put_widgets(self, mainapp):
        print('infoframe put_widgets ', 'self: ', self)
        self.lab_type = ttk.Label(self, text=self.frame_name, font=('', 11))

        self.lab_dates = ttk.Label(self, text='')
        self.fr_from_date = ttk.LabelFrame(self, borderwidth=2, relief="groove", text="Open Form Date")

        self.var_from_range = tk.StringVar()
        self.rb_from_range_lastyear = ttk.Radiobutton(self.fr_from_date, text='Last Year', value='ly',
                                                      variable=self.var_from_range,
                                                      command=lambda: self.fill_res_lab(self.lab_type.cget('text')))
        self.rb_from_range_lastmonth = ttk.Radiobutton(self.fr_from_date, text='Last Month', value='lm',
                                                      variable=self.var_from_range,
                                                      command=lambda: self.fill_res_lab(self.lab_type.cget('text')))
        if f'{self}.var_from_range' in mainapp.gaSet:
            self.var_from_range.set(mainapp.gaSet[f'{self}.var_from_range'])

        self.lab_date_from = DateEntry(self.fr_from_date, width=12, background='darkblue',
                        foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd",
                        firstweekday='sunday', weekenddays=[6,7])
        self.lab_date_from.bind("<<DateEntrySelected>>", self.fill_res_lab)
        if f'{self}.lab_date_from' in mainapp.gaSet:
            self.lab_date_from.set_date(mainapp.gaSet[f'{self}.lab_date_from'])

        self.lab_date_upto = DateEntry(self.fr_from_date, width=12, background='darkblue',
                        foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd",
                        firstweekday='sunday',  weekenddays=[6,7] )
        self.lab_date_upto.bind("<<DateEntrySelected>>", self.fill_res_lab)
        if f'{self}.lab_date_upto' in mainapp.gaSet:
            self.lab_date_upto.set_date(mainapp.gaSet[f'{self}.lab_date_upto'])

        #self.fr_dates = ttk.LabelFrame(self, borderwidth=2, relief="groove", text="Open Form Date")
        #self.date_from = ttk.Label(self.fr_dates)

        self.lab_cats  = ttk.Label(self, text='')
        self.var_cats = tk.StringVar()
        self.cb_cats = ttk.Combobox(self, justify='center', width=25, textvariable=self.var_cats)
        self.cb_cats.bind("<<ComboboxSelected>>", self.fill_res_lab)
        self.cb_subcats = ttk.Combobox(self, justify='center', width=35)
        ## subcat shouldn't refresh self.cb_subcats.bind("<<ComboboxSelected>>", self.fill_res_lab)

        self.fr_graph_details = ttk.Frame(self, borderwidth=0, relief="flat")
        self.var_res_lab = tk.StringVar()
        self.res_lab = ttk.Label(self.fr_graph_details, text='')
        self.but_crt_grph = ttk.Button(self.fr_graph_details, text='Create Graph!', command= lambda: self.create_graph())

        self.lab_type.grid(row=0, column=0, sticky='w', padx=2, pady=2)
        self.lab_dates.grid(row=1, column=0, sticky='w', padx=2, pady=2, columnspan=2)
        self.fr_from_date.grid(row=2, column=0, sticky='w', padx=2, pady=2, columnspan=2)
        self.rb_from_range_lastyear.grid(row=0, column=0, sticky='w', padx=2, pady=2)
        self.rb_from_range_lastmonth.grid(row=1, column=0, sticky='w', padx=2, pady=2)
        self.lab_date_from.grid(row=2, column=0, sticky='w', padx=2, pady=2)
        self.lab_date_upto.grid(row=2, column=1, sticky='w', padx=2, pady=2)

        self.lab_cats.grid(row=3, column=0, sticky='w', padx=2, pady=2)
        self.cb_cats.grid(row=3, column=1, sticky='w', padx=2, pady=2)
        self.cb_subcats.grid(row=4, column=1, sticky='w', padx=2, pady=2)

        self.fr_graph_details.grid(columnspan=2)
        self.res_lab.grid()
        self.but_crt_grph.grid()

    def fill_res_lab(self, *event):
        #print (f'fill_res_lab self:<{self}> , event:{event}')  # self.parent.info_frames:{self.parent.info_frames}




        #print(df_rma)
        txt = self.res_lab.cget("text")
        #rb_var_from_range = self.var_from_range.get()
        #lab_date_from = self.lab_date_from.get_date()
        #lab_date_upto = self.lab_date_upto.get_date()
        #print('res_lab: ', txt, self, 'rb_var_from_range ', rb_var_from_range, 'lab_date_from: ', lab_date_from, 'lab_date_upto: ', lab_date_upto)
        last_y_m = self.var_from_range.get()
        if last_y_m == 'ly':
            date_from = date.today() - timedelta(days=365)
            #date_from = str((date.today() - timedelta(days=365)).strftime("%d/%m/%Y"), )
        else:
            date_from = date.today() - timedelta(days=30)
            #date_from = str((date.today() - timedelta(days=30)).strftime("%d/%m/%Y"), )
        date_from_string = date_from.strftime('%d/%m/%Y')

        today_date = date.today()
        today_date_string = today_date.strftime('%d/%m/%Y')

        '''Set DateEntry accordingly to RadioButtons'''
        self.lab_date_from.set_date(date_from)
        self.lab_date_upto.set_date(today_date)

        cat = self.cb_cats.get()
        subcat = self.cb_subcats.get()
        print('res_lab: ', cat, subcat)

        subs = []
        if self.lab_type.cget('text') == 'RMA':
            dframe = df_rma
        else:
            dframe = df_pro
        for row in dframe:
            if len(re.sub('[\.\-\s]+', '', row[cat])) > 0:
                row_open_date = datetime.strptime(row['open_date'], '%Y-%m-%d %H:%M:%S.%f').date()
                if row_open_date >= date_from and row_open_date<=today_date:
                    subs.append(row[cat])
        unique_subs = sorted(list(set(subs)))
        print('unique_subs: ', cat, type(unique_subs), unique_subs)
        self.cb_subcats.configure(values=unique_subs)
        self.cb_subcats.set(unique_subs[0])

        #self.res_lab["text"] = f'{self.frame_name} {date_from_string} {today_date_string} {self.cb_cats.get()}'

        '''Save options'''
        options = {}
        for info_frame in self.parent.info_frames:
            # print(f'info_frame:<{info_frame}>')
            options[f'{info_frame}.var_from_range'] = info_frame.var_from_range.get()
            options[f'{info_frame}.lab_date_from'] = str(info_frame.lab_date_from.get_date())
            options[f'{info_frame}.lab_date_upto'] = str(info_frame.lab_date_upto.get_date())
            # print (options[f'{info_frame}.lab_date_from'])
        # print(options)
        #lib_gen.Gen.save_init(self, self.mainapp, **options)

    def create_graph(self):
        print('Button CreateGraph', 'res_lab: ', self.res_lab.cget("text"))
        date_from = self.lab_date_from.get_date()
        date_upto = self.lab_date_upto.get_date()
        sql = SqliteDB()
        df = sql.read_table(self.frame_name[0:4], date_from, date_upto)
        dp = DrawPlot()
        dp.by_string(df, self.cb_cats.get(), f'{self.frame_name}s by {self.cb_cats.get()}', 'Quantity', self.cb_cats.get().capitalize())

    def lab_type_fill(self,txt):
        self.lab_type.configure(text=txt)
    def lab_dates_fill(self,txt):
        self.lab_dates.configure(text=txt)

class StatusBarFrame(tk.Frame):
    '''Create the Status Bar Frame on base of tk.Frame'''

    def __init__(self, parent, mainapp):
        super().__init__(parent)
        print(f'StatusBarFrame, self:<{self}>, parent:<{parent}>')
        self['relief'] = self.master['relief']
        self['bd'] = self.master['bd']
        self.mainapp = mainapp

        self.put_widgets()

    def put_widgets(self):
        self.label1 = tk.Label(self, anchor='center', width=66, relief="groove")
        self.label1.pack(side='left', padx=1, pady=1, expand=1, fill=tk.X)
        self.label2 = tk.Label(self, anchor=tk.W, width=15, relief="sunken")
        self.label2.pack(side='left', padx=1, pady=1)
        self.label3 = tk.Label(self, width=5, relief="sunken", anchor='center')
        self.label3.pack(side='left', padx=1, ipadx=2, pady=1)

    def status(self, txt, bg="gray85"):
        #  SystemButtonFace = gray85
        if bg == 'red':
            bg = 'salmon'
        elif bg == 'green':
            bg = 'springgreen'
        self.label1.configure(text=txt, bg=bg)
        self.label1.update_idletasks()

    def read_status(self):
        return self.label1.cget('text')

    def start_time(self, txt):
        self.label2.configure(text=txt)
        self.label2.update_idletasks()

    def run_time(self, txt):
        self.label3.configure(text=txt)
        self.label3.update_idletasks()


if __name__ == '__main__':

    app = App()

    from datetime import date
    from sql_db_rw import SqliteDB
    from utils import lib_gen
    gen = lib_gen.FormatDates()
    date_from = gen.format_date_to_uso('01/01/2020')
    #date_upto = date.today().strftime('%d/%m/%Y')
    date_upto = gen.format_date_to_uso(date.today().strftime('%d/%m/%Y'))
    sql = SqliteDB()
    sql.list_tables()


    for tbl_name, lab_name in zip(["RMA", "Prod"], ['rma', 'pro']):
        print(f'df_{lab_name} tbl_{tbl_name}')

    df_rma = sql.read_table('RMA', date_from, date_upto)
    df_pro = sql.read_table('Prod', date_from, date_upto)
    all_dates = sorted({row['open_date'] for row in df_rma})
    #print(all_dates)
    date_from = min(all_dates).split(' ')[0]
    date_upto = max(all_dates).split(' ')[0]
    print('rma', len(df_rma), len(all_dates), date_from, date_upto, all_dates[-1])
    #print(sorted(df_rma[0].keys()))
    app.main_frame.frame_info_rma.lab_dates_fill(f"Data is available from {date_from} upto {date_upto}")
    #app.main_frame.frame_info_rma.lab_date_from.set_date(date_from)
    #app.main_frame.frame_info_rma.lab_date_upto.set_date(date_upto)
    cats = sorted(df_rma[0].keys())
    app.main_frame.frame_info_rma.cb_cats.configure(values=cats)
    app.main_frame.frame_info_rma.var_cats.set(cats[0])


    all_dates = sorted({row['open_date'] for row in df_pro})
    #print(all_dates)
    date_from = min(all_dates).split(' ')[0]
    date_upto = max(all_dates).split(' ')[0]
    #print(all_dates)
    print('production', len(df_pro), len(all_dates), date_from, date_upto, all_dates[-1])
    app.status_bar_frame.status("")
    app.main_frame.frame_info_pro.lab_dates_fill(f"Data is available from {date_from} upto {date_upto}")
    #app.main_frame.frame_info_pro.lab_date_from.set_date(date_from)
    #app.main_frame.frame_info_pro.lab_date_upto.set_date(date_upto)
    cats = sorted(df_pro[0].keys())
    app.main_frame.frame_info_pro.cb_cats.configure(values=cats)
    app.main_frame.frame_info_pro.var_cats.set(cats[0])
    app.status_bar_frame.status("")
    app.mainloop()