import tkinter as tk
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
from gen_lib import lib_gen
from gen_lib import lib_DialogBox as dbox


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
        self.put_main_frames(mainapp)

    def put_main_frames(self, mainapp):
        #self.frame_start_from = StartFromFrame(self, mainapp)
        self.frame_info = InfoFrame(self, mainapp)
        #self.frame_barcodes = BarcodesFrame(self, mainapp)

        #self.frame_start_from.grid(row=0, column=0, columnspan=2, sticky="news")
        self.frame_info.grid(row=1, column=0, sticky="news", padx=2, pady=2)
        #self.frame_barcodes.grid(row=1, column=1, sticky="news", padx=2, pady=2)

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

    def __init__(self, parent, mainapp):
        super().__init__(parent)
        print(f'InfoFrame, self:<{self}>, parent:<{parent}>, mainapp:<{mainapp}>')
        # self['relief'] = self.master['relief']
        self['relief'] = tk.GROOVE
        self['bd'] = 2
        self.put_widgets()
        self.mainapp = mainapp

    def put_widgets(self):
        self.lab_act_package_txt = ttk.Label(self, text='Package:')
        self.lab_act_package_val = ttk.Label(self, text='')
        self.lab_sw_txt = ttk.Label(self, text='SW Ver.:')
        self.lab_sw_val = ttk.Label(self, text='')
        self.lab_flash_txt = ttk.Label(self, text='Flash Image:')
        self.lab_flash_val = ttk.Label(self, text='')

        self.lab_act_package_txt.grid(row=0, column=0, sticky='w', padx=2, pady=2)
        self.lab_act_package_val.grid(row=0, column=1, sticky='e', padx=2, pady=2)
        self.lab_sw_txt.grid(row=1, column=0, sticky='w', padx=2, pady=2)
        self.lab_sw_val.grid(row=1, column=1, sticky='e', padx=2, pady=2)
        # self.lab_flash_txt.grid(row=2, column=0, sticky='w', padx=2, pady=2)
        # self.lab_flash_val.grid(row=2, column=1, sticky='e', padx=2, pady=2)


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


app = App()
app.mainloop()