"""source .venv/Scripts/activate"""

import tkinter as tk

#from tkinter import tkcalendar
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
import re
import os
import glob
import subprocess
from subprocess import check_output
import socket
from pathlib import Path
from PIL import Image, ImageTk
import sys
import functools
from functools import partial
from datetime import date, timedelta, datetime
import textwrap

import utils.lib_DialogBox
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
        # print('aaa', self.gaSet)
        # self.if_rad_net()

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
            'default': 0,
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
        self.frame_info_rma.lab_cats.configure(text='Categories: ')

        self.frame_info_pro.grid(row=1, column=1, sticky="news", padx=2, pady=2)
        self.frame_info_pro.lab_cats.configure(text='Categories: ')

        self.frame_info_choose_graph = OpenGraph(self, mainapp)
        self.frame_info_choose_graph.grid(row=2, column=0, sticky="news", padx=2, pady=2, columnspan=2)

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
        self.rb_from_range_exact = ttk.Radiobutton(self.fr_from_date, text='Exact Range', value='er',
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

        self.fr_graph_details = ttk.LabelFrame(self, borderwidth=2, relief="groove", text="")
        co = 0
        ro = 0
        self.lab_show_me = ttk.Label(self.fr_graph_details, text='Show me')
        self.lab_show_me.grid(row=ro, column=co, sticky='w')
        co += 1
        self.cb_show_me_what = TtkMultiSelectCombobox(self.fr_graph_details)
        self.cb_show_me_what.listbox.config(selectmode="single", height=3)
        self.cb_show_me_what.entry.config(width=5)
        self.cb_show_me_what.listbox.bind("<<ListboxSelect>>",
                                          lambda e: (self.fill_titles()), add="+")
        self.cb_show_me_what.set_values(['all', 'when'])
        self.cb_show_me_what.grid(row=ro, column=co, sticky='e', padx=2, pady=2)
        co += 1
        self.cb_ret_cat = TtkMultiSelectCombobox(self.fr_graph_details)
        self.cb_ret_cat.entry.config(width=25)
        self.cb_ret_cat.listbox.bind("<<ListboxSelect>>", lambda e: (self.fill_res_lab(), self.fill_titles()), add="+")
        self.cb_ret_cat.grid(row=ro, column=co, sticky='e', padx=2, pady=2)

        co = 0
        ro += 1
        self.lab_where = ttk.Label(self.fr_graph_details, text='Excluded:')
        self.lab_where.grid(row=ro, column=co, sticky='w')

        co += 1
        self.cb_ret_cat_exclud = TtkMultiSelectCombobox(self.fr_graph_details)
        self.cb_ret_cat_exclud.entry.config(width=25)
        self.cb_ret_cat_exclud.grid(row=ro, column=co, columnspan=2, sticky='ew', padx=2, pady=2)

        co = 0 ; ro += 1
        self.lab_where = ttk.Label(self.fr_graph_details, text='where')
        self.lab_where.grid(row=ro, column=co, sticky='w')

        """
        cb_cats
        """
        co = 0 ; ro += 1
        self.lab_cats  = ttk.Label(self.fr_graph_details, text='')
        self.var_cats = tk.StringVar()
        self.cb_cats = TtkMultiSelectCombobox(self.fr_graph_details)
        # self.cb_cats.listbox.config(selectmode="single")
        self.cb_cats.listbox.bind("<<ListboxSelect>>",
                                  lambda e: (self.fill_res_lab(), self.fill_titles()), add="+")
        #self.cb_cats.entry.config(width=25)
        self.cb_cats.grid(row=ro, column=co, columnspan=1, sticky='ew', padx=2, pady=2)

        co += 1
        self.lab_ret_val_valus = ttk.Label(self.fr_graph_details, text='equal to')
        self.lab_ret_val_valus.grid(row=ro, column=co, sticky='w')
        co += 1
        self.cb_subcats = TtkMultiSelectCombobox(self.fr_graph_details)  # ttk.Combobox(self, width=35)
        self.cb_subcats.listbox.bind("<<ListboxSelect>>", self.fill_titles, add="+")
        #self.cb_subcats.entry.config(width=25)
        self.cb_subcats.grid(row=ro, column=co, columnspan=1, sticky='ew', padx=2, pady=2)


        """
        cb_cats2
        """
        co = 0
        ro += 1
        self.lab_and = ttk.Label(self.fr_graph_details, text='and')
        self.lab_and.grid(row=ro, column=co, sticky='w')

        co = 0
        ro += 1
        self.cb_cats2 = TtkMultiSelectCombobox(self.fr_graph_details)
        self.cb_cats2.listbox.bind("<<ListboxSelect>>",
                                  lambda e: (self.fill_res_lab(), self.fill_titles()), add="+")
        # self.cb_cats2.listbox.config(selectmode="single")
        # self.cb_cats.entry.config(width=25)
        self.cb_cats2.grid(row=ro, column=co, columnspan=1, sticky='ew', padx=2, pady=2)

        co += 1
        self.lab_subcats2 = ttk.Label(self.fr_graph_details, text='equal to')
        self.lab_subcats2.grid(row=ro, column=co, sticky='w')
        co += 1
        self.cb_subcats2 = TtkMultiSelectCombobox(self.fr_graph_details)  # ttk.Combobox(self, width=35)
        self.cb_subcats2.listbox.bind("<<ListboxSelect>>", self.fill_titles, add="+")
        # self.cb_subcats2.entry.config(width=25)
        self.cb_subcats2.grid(row=ro, column=co, columnspan=1, sticky='ew', padx=2, pady=2)

        co = 0
        ro += 1
        self.lab_gr_tit = ttk.Label(self.fr_graph_details, text='Graph Title')
        self.lab_gr_tit.grid(row=ro, column=co, sticky='w')
        co += 1
        self.ent_gr_tit = ttk.Entry(self.fr_graph_details)
        self.ent_gr_tit.grid(row=ro, column=co, columnspan=2, sticky='ew', padx=2, pady=2)

        co = 0
        ro += 1
        self.lab_gr_xaxis_tit = ttk.Label(self.fr_graph_details, text='X axis Title')
        self.lab_gr_xaxis_tit.grid(row=ro, column=co, sticky='w')
        co += 1
        self.ent_gr_xaxis_tit = ttk.Entry(self.fr_graph_details)
        self.ent_gr_xaxis_tit.grid(row=ro, column=co, columnspan=2, sticky='ew', padx=2, pady=2)

        co = 0
        ro += 1
        self.lab_gr_yaxis_tit = ttk.Label(self.fr_graph_details, text='Y axis Title')
        self.lab_gr_yaxis_tit.grid(row=ro, column=co, sticky='w')
        co += 1
        self.ent_gr_yaxis_tit = ttk.Entry(self.fr_graph_details)
        self.ent_gr_yaxis_tit.insert(tk.END, 'Quantity')
        self.ent_gr_yaxis_tit.grid(row=ro, column=co, columnspan=2, sticky='ew', padx=2, pady=2)

        """
        chart_type
        """
        co = 0
        ro += 1
        self.lab_chart_type = ttk.Label(self.fr_graph_details, text='Chart Type')
        self.lab_chart_type.grid(row=ro, column=co, sticky='w')

        co += 1
        self.cb_chart_type = TtkMultiSelectCombobox(self.fr_graph_details)
        self.cb_chart_type.set_values(['bar', 'pie'])
        self.cb_chart_type.listbox.config(height=3)
        #self.cb_chart_type.listbox.bind("<<ListboxSelect>>", self.fill_res_lab, add="+")
        # self.cb_cats2.listbox.config(selectmode="single")
        # self.cb_cats.entry.config(width=25)
        self.cb_chart_type.grid(row=ro, column=co, columnspan=1, sticky='ew', padx=2, pady=2)

        self.fr_buttons = ttk.Frame(self, borderwidth=0, relief="flat")
        self.var_res_lab = tk.StringVar()
        self.res_lab = ttk.Label(self.fr_buttons, text='')
        self.but_crt_grph = ttk.Button(self.fr_buttons, text='Create Graph', command= lambda: self.create_graph())
        self.but_save_grph = ttk.Button(self.fr_buttons, text='Save the Graph', command=lambda: self.save_graph())

        self.lab_type.grid(row=0, column=0, sticky='w', padx=2, pady=2)
        self.lab_dates.grid(row=1, column=0, sticky='w', padx=2, pady=2, columnspan=2)
        self.fr_from_date.grid(row=2, column=0, sticky='w', padx=2, pady=2, columnspan=2)
        self.rb_from_range_lastyear.grid(row=0, column=0, sticky='w', padx=2, pady=2)
        self.rb_from_range_lastmonth.grid(row=1, column=0, sticky='w', padx=2, pady=2)
        self.rb_from_range_exact.grid(row=2, column=0, sticky='w', padx=2, pady=2)
        self.lab_date_from.grid(row=2, column=1, sticky='w', padx=2, pady=2)
        self.lab_date_upto.grid(row=2, column=2, sticky='w', padx=2, pady=2)

        #self.lab_cats.grid(row=3, column=0, sticky='w', padx=2, pady=2)



        self.fr_graph_details.grid(columnspan=2, sticky='snwe', padx=2, pady=2)
        self.fr_buttons.grid(columnspan=2, sticky='snwe', padx=2, pady=2)
        self.res_lab.grid()
        self.but_crt_grph.grid()
        self.but_save_grph.grid()

    def fill_res_lab(self, *event):
        print (f'fill_res_lab self:<{self}> , event:{event}')  # self.parent.info_frames:{self.parent.info_frames}
        #print(df_rma)
        txt = self.res_lab.cget("text")
        #rb_var_from_range = self.var_from_range.get()
        #lab_date_from = self.lab_date_from.get_date()
        #lab_date_upto = self.lab_date_upto.get_date()
        #print('res_lab: ', txt, self, 'rb_var_from_range ', rb_var_from_range, 'lab_date_from: ', lab_date_from, 'lab_date_upto: ', lab_date_upto)
        last_y_m = self.var_from_range.get()
        if last_y_m == 'ly':
            self.date_from = date.today() - timedelta(days=365)
            self.date_upto = date.today()
            #date_from = str((date.today() - timedelta(days=365)).strftime("%d/%m/%Y"), )
        elif last_y_m == 'lm':
            self.date_from = date.today() - timedelta(days=30)
            self.date_upto = date.today()
            #date_from = str((date.today() - timedelta(days=30)).strftime("%d/%m/%Y"), )
        else:
            self.date_from = self.lab_date_from.get_date()
            self.date_upto = self.lab_date_upto.get_date()

        #date_from_string = date_from.strftime('%d/%m/%Y')


        #today_date = date.today()
        #today_date_string = today_date.strftime('%d/%m/%Y')

        # '''Set DateEntry accordingly to RadioButtons'''
        # self.lab_date_from.set_date(date_from)
        # self.lab_date_upto.set_date(today_date)

        #cat = self.cb_cats.get()


        def fill_cat_su_cat(par_w, sub_par_w):
            subs = []
            unique_subs = []
            selected = par_w.get_selected()
            print(f'selected:<{selected}> lenselected:<{len(selected)}>')
            if selected !=[]:
                for cat in selected:
                    print(f'cat:<{cat}>, {type(cat)}')
                    # subcat = self.cb_subcats.get()
                    # print('res_lab: ', cat, subcat)
                    if self.lab_type.cget('text') == 'RMA':
                        dframe = df_rma
                    else:
                        dframe = df_pro
                    for row in dframe:
                        #print(f'row:<row>, row[cat]:<{row[cat]}> {type(row[cat])}')
                        if len(re.sub('[\.\-\s]+', '', row[cat])) > 0:
                            row_open_date = datetime.strptime(row['open_date'], '%Y-%m-%d %H:%M:%S.%f').date()
                            #print(f'row_open_date:<{row_open_date}> self.date_from:<{self.date_from}>  self.date_upto:<{self.date_upto}>')
                            if row_open_date >= self.date_from and row_open_date<=self.date_upto:
                                subs.append(row[cat])
                unique_subs = sorted(list(set(subs)))
                print('unique_subs: ', type(unique_subs), unique_subs)
                if len( unique_subs)>0:
                    # self.cb_subcats.configure(values=unique_subs)
                    # self.cb_subcats.set(unique_subs[0])
                    sub_par_w.set_values(unique_subs)

                    sub_val = sub_par_w.entry_var.get()
                    ##  change only if it empty or the same value
                    if sub_val == '' or sub_val == unique_subs[0]:
                        sub_par_w.entry_var.set(unique_subs[0])
                else:
                    dibox = dbox.DialogBox()
                    db_dict = {
                        "title": "No data",
                        "message": f"No data for {selected}",
                        "type": ["OK"],
                        "icon": "::tk::icons::information",
                        'default': 0

                    }
                    dibox.create(self.mainapp , db_dict)
                    string, res_but, ent_dict = dibox.show()

            else:
                sub_par_w.set_values([])
                sub_par_w.entry_var.set('')

            print('unique_subs: ', type(unique_subs), unique_subs)

        par_w = self.cb_ret_cat
        sub_par_w = self.cb_ret_cat_exclud
        fill_cat_su_cat(par_w, sub_par_w)
        sub_par_w.entry_var.set("")

        par_w = self.cb_cats
        sub_par_w = self.cb_subcats
        fill_cat_su_cat(par_w, sub_par_w)

        par_w = self.cb_cats2
        sub_par_w = self.cb_subcats2
        fill_cat_su_cat(par_w, sub_par_w)



        #self.res_lab["text"] = f'{self.frame_name} {date_from_string} {today_date_string} {self.cb_cats.get()}'

        '''Save options'''
        options = {}
        for info_frame in self.parent.info_frames:
            # print(f'info_frame:<{info_frame}>')
            options[f'{info_frame}.var_from_range'] = info_frame.var_from_range.get()
            options[f'{info_frame}.lab_date_from'] = str(self.date_from)  ## str(info_frame.lab_date_from.get_date())
            options[f'{info_frame}.lab_date_upto'] = str(self.date_upto)  ## str(info_frame.lab_date_upto.get_date())
            # print (options[f'{info_frame}.lab_date_from'])
        # print(options)
        #lgen = lib_gen.Gen()
        lib_gen.Gen.save_init(self, self.mainapp, **options)

    def fill_titles(self, *args):
        #print(f'\nfill_titles')
        ret_cat = self.cb_ret_cat.entry.get()
        cat = self.cb_cats.entry.get()
        cat_val = self.cb_subcats.entry.get()
        cat2 = self.cb_cats2.entry.get()
        cat2_val = self.cb_subcats2.entry.get()
        all_when = self.cb_show_me_what.entry.get()
        print(f'<{all_when}>, {type(all_when)}')

        tit =  (f"{ret_cat.replace('_', ' ')}").upper()
        if cat!='':
            tit += f" where {cat.upper()} is {cat_val.upper()}"
        if cat2!='':
            tit +=f" and {cat2.upper()} is {cat2_val.upper()}"
        tit = tit.replace('/', '_')
        self.ent_gr_tit.delete(0, tk.END)
        self.ent_gr_tit.insert(0, tit)

        xtit = ret_cat.replace('_', " ").upper()
        xtit = xtit.replace('/', '_')
        self.ent_gr_xaxis_tit.delete(0, tk.END)
        self.ent_gr_xaxis_tit.insert(0, xtit)

        if all_when == 'when':
            self.cb_chart_type.entry_var.set('bar')
        elif all_when == 'all':
            self.cb_chart_type.entry_var.set('bar, pie')




    def get_db_gr_opts(self):
        self.db_opts = {}
        self.gr_opts = {}
        mast_be_filled = []
        empty_entrs = ''
        self.db_opts['tbl_name'] = self.frame_name[0:4]

        self.db_opts['last_y_m'] = self.var_from_range.get()
        self.db_opts['date_from'] = self.lab_date_from.get_date()
        self.db_opts['date_upto'] = self.lab_date_upto.get_date()

        self.db_opts['show_me_what'] = self.cb_show_me_what.entry.get()
        mast_be_filled.append((self.cb_show_me_what.entry, 'Show me'))
        self.db_opts['ret_cat']      = self.cb_ret_cat.entry.get().split(', ')
        mast_be_filled.append((self.cb_ret_cat.entry, 'Show me'))
        self.db_opts['cat']          = self.cb_cats.entry.get()
        self.db_opts['cat_val']      = self.cb_subcats.entry.get().split(', ')
        self.db_opts['cat2']         = self.cb_cats2.entry.get()
        self.db_opts['cat2_val']     = self.cb_subcats2.entry.get()
        self.db_opts['excludes']     = self.cb_ret_cat_exclud.entry.get().split(', ')

        self.gr_opts['tit']       = self.ent_gr_tit.get()
        mast_be_filled.append((self.ent_gr_tit, 'Title'))
        self.gr_opts['xaxis_tit'] = self.ent_gr_xaxis_tit.get()
        mast_be_filled.append((self.ent_gr_xaxis_tit, 'X axis Title'))
        self.gr_opts['yaxis_tit'] = self.ent_gr_yaxis_tit.get()
        mast_be_filled.append((self.ent_gr_yaxis_tit, 'Y axis Title'))
        self.gr_opts['excludes']  = self.cb_ret_cat_exclud.entry.get().split(',')
        self.gr_opts['chart_type'] = self.cb_chart_type.entry.get().split(',')
        mast_be_filled.append((self.cb_chart_type.entry, 'Chart Type'))

        print(f'self.db_opts:{self.db_opts}')
        print(f'self.gr_opts:{self.gr_opts}')
        print(f'type of self.db_opts["ret_cat"]: {type(self.db_opts["ret_cat"])}')
        print(f'self.db_opts["excludes"]: <{self.db_opts["excludes"]}>, {len(self.db_opts["excludes"])}')

        for w, labtxt in mast_be_filled:
            if w.get() == '':
                empty_entrs += f"{labtxt}, "

        if empty_entrs != []:
            return empty_entrs
        else:
            return None

    def create_graph(self):
        print('Button CreateGraph', 'res_lab: ', self.res_lab.cget("text"))
        ret = self.get_db_gr_opts()
        if ret:
            ret= ret[:-2]  # strip last ", "
            messagebox.showerror("Empty fields", f'The following entries:\n\n{ret}\n\n must be full')
            return

        read_tbl_args = []
        read_tbl_args.append(self.db_opts['tbl_name'])
        last_y_m = self.db_opts['last_y_m']
        if last_y_m == 'ly':
            date_from = date.today() - timedelta(days=365)
            date_upto = date.today()
            #date_from = str((date.today() - timedelta(days=365)).strftime("%d/%m/%Y"), )
        elif last_y_m == 'lm':
            date_from = date.today() - timedelta(days=30)
            date_upto = date.today()
            #date_from = str((date.today() - timedelta(days=30)).strftime("%d/%m/%Y"), )
        else:
            date_from = self.db_opts['date_from']
            date_upto = self.db_opts['date_upto']
        read_tbl_args.extend([date_from])
        read_tbl_args.extend([date_upto])

        read_tbl_kwargs = {}
        read_tbl_kwargs['ret_cat'] = self.db_opts['ret_cat']
        read_tbl_kwargs['cat'] = self.db_opts['cat'] if self.db_opts['cat']!="" else None
        read_tbl_kwargs['cat_val'] = self.db_opts['cat_val'] if self.db_opts['cat_val']!=[''] else None
        read_tbl_kwargs['cat2'] = self.db_opts['cat2'] if self.db_opts['cat2']!="" else None
        read_tbl_kwargs['cat2_val'] = self.db_opts['cat2_val'] if self.db_opts['cat2_val']!="" else None
        read_tbl_kwargs['excludes'] = self.db_opts['excludes'] if self.db_opts['excludes']!=[''] else None

        print(f'read_tbl_args:<{read_tbl_args}>')
        print(f'read_tbl_kwargs:<{read_tbl_kwargs}>')

        sql = SqliteDB()
        df = sql.read_table(*read_tbl_args, **read_tbl_kwargs)
        #print(df)

        gr_kwargs = {}
        gr_kwargs['cat'] = self.db_opts['ret_cat'][0]
        gr_kwargs['tit'] = self.gr_opts['tit']
        gr_kwargs['xaxis_tit'] = self.gr_opts['xaxis_tit']
        gr_kwargs['yaxis_tit'] = self.gr_opts['yaxis_tit']
        gr_kwargs['chart_type'] = self.gr_opts['chart_type']
        gr_kwargs['excludes'] = read_tbl_kwargs['excludes']
        print(f'gr_kwargs:<{gr_kwargs}>')

        dp = DrawPlot()

        if self.db_opts['show_me_what'] == 'when':
            dp.by_cat_day(df, **gr_kwargs)
        elif self.db_opts['show_me_what'] == 'all':
            dp.by_category(df, **gr_kwargs)

        return

    def save_graph(self):
        # check all fields are full
        ret = self.get_db_gr_opts()
        if ret:
            ret = ret[:-2]  # strip last ", "
            messagebox.showerror("Empty fields", f'The following entries:\n\n{ret}\n\n must be full')
            return

        init_dir = self.mainapp.gaSet['host_fld']
        fname = ""
        ini_file = self.ent_gr_tit.get().replace(',', '_').replace(' ', '_')+'.py'

        fname = asksaveasfilename(initialdir=init_dir,
                                title="Open file okay?",
                                initialfile=ini_file,
                                filetypes=(("text files", "*.py"),
                                           ("all files", "*.*"))
                                )
        print(f'fname: <{fname}>')
        if fname is None or fname=="" :
            return None



        print('self.db_opts')
        for item in self.db_opts.items():
            print(item)
        print('self.gr_opts')
        for item in self.gr_opts.items():
            print(item)

        if self.gr_opts["excludes"] == ['']:
            excludes = None

        options = {
            'cat': f'{self.db_opts["ret_cat"][0]}',
            'tit': f'{self.gr_opts["tit"]}',
            'xaxis_tit': f'{self.gr_opts["xaxis_tit"]}',
            'yaxis_tit': f'{self.gr_opts["yaxis_tit"]}',
            'chart_type': f'{self.gr_opts["chart_type"]}',
        }
        if self.gr_opts["excludes"] != ['']:
            options['excludes'] =  self.gr_opts["excludes"]

        include_extra = False

        lines = []
        lines += [
            "from qsfc.sql_db_rw import SqliteDB",
            "from qsfc.Graphs import DrawPlot",
            "from utils import lib_gen",
            "",
        ]
        
        lines += [
            "gen = lib_gen.FormatDates()",
            # f"date_from = gen.format_date_to_uso('{date_from}')",
            # f"date_upto = gen.format_date_to_uso('{date_upto}', last_sec=True)",
            #self.date_from = date.today() - timedelta(days=365)
            #self.date_upto = date.today()
        ]
        if self.db_opts['last_y_m'] == 'ly':
            lines += ["date_from = date.today() - timedelta(days=365)",]
            lines += ["date_upto = date.today()", ]
        elif self.db_opts['last_y_m'] == 'lm':
            lines += ["date_from = date.today() - timedelta(days=30)",]
            lines += ["date_upto = date.today()", ]
        else:
            lines += [f"date_from = '{self.db_opts['date_from']}'",]
            lines += [f"date_upto = '{self.db_opts['date_upto']}'", ]

        lines += [
            "sql = SqliteDB()",
            "dp = DrawPlot()",
            "",
            "options = {"
        ]
        for key, val in options.items():
            lines.append(f'    "{key}": "{val}",')
        lines.append("}")
        lines.append("")

        db_call = (f"df = sql.read_table("
                   f"'{self.db_opts['tbl_name']}', "
                   "date_from, date_upto, " 
                   f"ret_cat={self.db_opts['ret_cat']}"
                   )
        if self.db_opts['cat'] != '':
             print('cat')
             db_call += f", cat='{self.db_opts['cat']}', cat_val={self.db_opts['cat_val']}"
        if self.db_opts['cat2'] != '':
             db_call += f", cat2='{self.db_opts['cat2']}', cat2_val={self.db_opts['cat2_val']}"

        if self.gr_opts["excludes"] != ['']:
            db_call += f", excludes={ self.gr_opts['excludes']}"
        db_call += ")"
        lines.append(db_call)

        if self.db_opts['show_me_what'] == 'all':
            lines.append("dp.by_category(df, **options)")
        elif self.db_opts['show_me_what'] == 'when':
            lines.append("dp.by_cat_day(df, **options)")

        if include_extra:
            lines += [
                "",
                'dp.fig.write_image("output_plot.png")',
            ]

        with open(fname, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))



    def lab_type_fill(self,txt):
        self.lab_type.configure(text=txt)
    def lab_dates_fill(self,txt):
        self.lab_dates.configure(text=txt)


class OpenGraph(tk.Frame):
    '''Create the Info Frame on base of tk.Frame'''

    def __init__(self, parent, mainapp):
        super().__init__(parent)
        print(f'OpenGraph, self:<{self}>, parent:<{parent}>, mainapp:<{mainapp}>')
        # self['relief'] = self.master['relief']
        self['relief'] = tk.GROOVE
        self['bd'] = 2
        self.mainapp = mainapp
        self.parent = parent
        print(f'OpenGraph2, self:<{self}>, parent:<{parent}>, mainapp:<{mainapp}>, self.mainapp:<{self.mainapp}>')

        self.put_widgets(mainapp)

    def put_widgets(self, mainapp):
        print('open_graph put_widgets ', 'self: ', self)
        self.lab_koteret = ttk.Label(self, text="Choose saved graph", font=('', 11))
        #self.lab_koteret.grid(row=0, column=0, sticky='w', padx=2, pady=2)

        self.open_file = ttk.Button(self, text="Choose saved graph", command=self.load_file)
        self.open_file.grid(row=0, column=0, sticky='w', padx=2, pady=2)

    def load_file(self):
        init_dir = self.mainapp.gaSet['host_fld']
        fname = askopenfilename(initialdir=init_dir,
                                title="Open file okay?",
                                filetypes=(("text files", "*.py"),
                                           ("all files", "*.*"))
                                )
        if fname:
            try:
                subprocess.run([sys.executable, fname], check=True)
            except Exception as e:  # <- naked except is a bad idea
                showerror("Open Source File",
                          f"Failed to read file {fname}, \nError: {e}")
            return



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


class TtkMultiSelectCombobox(ttk.Frame):
    def __init__(self, master=None, values=None, **kwargs):
        super().__init__(master, **kwargs)
        self.values = values or []
        self.selected = []
        style = ttk.Style()
        combo_bg = style.lookup('TCombobox', 'fieldbackground', default='white')

        self.entry_var = tk.StringVar()

        self.input_frame = ttk.Frame(self, relief='groove', borderwidth=2)
        self.input_frame.pack(fill="x", ipady=0)

        small_font = ("Segoe UI", 8)
        #self.entry = ttk.Entry(self.input_frame, textvariable=self.entry_var, state="readonly")
        self.entry = tk.Entry(
            self.input_frame,
            textvariable=self.entry_var,
            state="readonly",
            relief="flat",
            background=combo_bg,
            disabledbackground=combo_bg,
            font=small_font,
        )
        self.entry.grid(row=0, column=0, sticky="ew", ipady=0, padx=0, pady=0)
        self.entry.bind("<Button-1>", self.toggle_dropdown)

        # Arrow button
        #self.arrow_btn = ttk.Button(self.input_frame, text="\u2228", width=2, command=self.toggle_dropdown, padding=(0, 0))  # text="▼"
        self.arrow_btn = tk.Button(
            self.input_frame,
            text="\u2228",
            command=self.toggle_dropdown,
            relief="flat",
            background=combo_bg,
            activebackground=combo_bg,
            borderwidth=0,
            font=small_font,
        )
        self.arrow_btn.grid(row=0, column=1, sticky="ns", ipady=0, padx=0, pady=0)

        self.input_frame.columnconfigure(0, weight=1)  # растягиваем Entry

        self.dropdown_visible = False

        # # Dropdown frame
        self.dropdown_frame = ttk.Frame(self, borderwidth=1, relief="solid", style="TCombobox",)

        #style.theme_use('default')

        self.listbox = tk.Listbox(
            self.dropdown_frame,
            selectmode="multiple",
            exportselection=False,
            activestyle="none",
            height=6, # min(6, len(values))
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            background=style.lookup('TCombobox', 'fieldbackground', default='white'),
            foreground=style.lookup('TCombobox', 'foreground', default='black'),
            #selectbackground=style.lookup('TCombobox', 'selectbackground', default='#0A64A4'),
            #selectforeground=style.lookup('TCombobox', 'selectforeground', default='white'),
            font=style.lookup('TCombobox', 'font', default="TkDefaultFont")
        )
        # for val in values:
        #     self.listbox.insert(tk.END, val)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.dropdown_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox.bind("<<ListboxSelect>>", self.update_selection)

        # Закрытие по клику вне
        #self.bind_all("<Button-1>", self.check_click_outside)
        self.bind_all("<Button-1>", self.check_click_outside, add="+")

    def toggle_dropdown(self, event=None):
        if self.dropdown_visible:
            self.hide_dropdown()
        else:
            self.show_dropdown()

    def insert(self, index, value):
        """Добавляет элемент в список."""
        if index == "end" or index == tk.END:
            self.values.append(value)
        else:
            self.values.insert(index, value)
        self.listbox.insert(index, value)

    def show_dropdown(self):
        self.dropdown_frame.pack(fill="x")
        self.dropdown_visible = True

    def hide_dropdown(self):
        self.dropdown_frame.pack_forget()
        self.dropdown_visible = False

    def check_click_outside(self, event):
        widget = event.widget
        widgets = [self.entry, self.listbox, self.scrollbar, self.dropdown_frame]
        if any(widget is w or str(widget).startswith(str(w)) for w in widgets):
            return

        self.hide_dropdown()
        # if widget not in (self.entry, self.listbox) and not str(widget).startswith(str(self.dropdown_frame)):
        #     self.hide_dropdown()

    def update_selection(self, event=None):
        selected_indices = self.listbox.curselection()
        # print(f'update_selection selected_indices:<{selected_indices}>')
        self.selected = [self.values[i] for i in selected_indices]
        # print(f'update_selection selected:<{self.selected}>')
        self.entry_var.set(", ".join(self.selected))

        if self.listbox.cget("selectmode") == "single":
            self.hide_dropdown()

    def get_selected(self):
        return self.selected

    def set_values(self, values):
        self.values = values
        self.listbox.delete(0, tk.END)
        for val in values:
            self.listbox.insert(tk.END, val)

    def add_value(self, value):
        self.listbox.insert(tk.END, value)
        self.values.append(value)

    def clear_selection(self):
        if self.listbox.cget("selectmode") == "single":
            self.listbox.selection_clear(0, tk.END)
            self.selected = []
            self.entry_var.set("")  # Очистить поле ввода, если нужно

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
    print(f'maint cats:<{cats}>')
    # #app.main_frame.frame_info_rma.cb_cats.configure(values=cats)
    for cat in cats:
        app.main_frame.frame_info_rma.cb_ret_cat.insert(tk.END, cat)
        app.main_frame.frame_info_rma.cb_cats.insert(tk.END, cat)
        app.main_frame.frame_info_rma.cb_cats2.insert(tk.END, cat)
        #app.main_frame.frame_info_rma.cb_cats.values.append(cat)

    print(f'maint cb_cats values:<{app.main_frame.frame_info_rma.cb_ret_cat.values}>')
    #app.main_frame.frame_info_rma.var_cats.set(cats[0])


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
    for cat in cats:
        app.main_frame.frame_info_pro.cb_ret_cat.insert(tk.END, cat)
        #app.main_frame.frame_info_pro.cb_cats.values.append(cat)
    app.main_frame.frame_info_pro.cb_ret_cat.configure(height = 6)
    #app.main_frame.frame_info_pro.var_cats.set(cats[0])

    app.status_bar_frame.status("")
    app.mainloop()