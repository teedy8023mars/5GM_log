try:
    import Tkinter as tk  # for Python 2.x
except ImportError:
    import tkinter as tk  # for Python 3.x

from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as tkscrolled
import tkinter.messagebox as mb
import time
import threading
import socket
import re


class App:
    def __init__(self, win):
        self.bot_frame = Frame(win, bg="lightblue")
        self.bot_frame.pack(side=BOTTOM, expand=1, fill=BOTH)

        self.top_frame = Frame(win)
        self.top_frame.pack(side=BOTTOM, expand=1, fill=BOTH)
        # textbox and scrollbar
        self.scrollbar = Scrollbar(self.top_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.filename = ''
        self.textbox = Text(self.top_frame, bg='powderblue', yscrollcommand=self.scrollbar.set,
                            wrap="word", font="{Times new Roman} 11")
        self.textbox.pack(fill=BOTH, expand=1)
        self.scrollbar.config(command=self.textbox.yview)

        # left frame
        self.left_frame = Frame(self.bot_frame, bg="lightblue")
        self.left_frame.pack(side=LEFT, padx=5, expand=1)
        self.save_button = Button(
            self.left_frame, text="Save", bg="steelblue", command=self.SaveFileAs, width=10)
        self.save_button.pack(side=BOTTOM,  pady=5)
        self.open_button = Button(
            self.left_frame, text="Open", bg="dodgerblue", command=self.Openfile, width=10)
        self.open_button.pack(side=TOP,  pady=5)

        # Dashboard
        self.label_frame = LabelFrame(
            self.bot_frame, text="Real time info", font="{Helvetica} 9 bold", bg="lightblue")
        self.label_frame.pack(side=LEFT, pady=1, padx=5, fill=X, expand=1)
        self.continueLogging = False

        # right frame
        self.right_frame = Frame(self.bot_frame, bg="lightblue")
        self.right_frame.pack(side=LEFT, padx=5, expand=1)
        self.toggle = Button(self.right_frame, text="Start  /  Stop",
                             command=self.gui_handler, bg="dodgerblue")
        self.toggle.pack(side=TOP, pady=5)
        self.clear_button = Button(
            self.right_frame, text="Clear Screen", command=self.clear_screen, bg="steelblue")
        self.clear_button.pack(side=BOTTOM, pady=5)

        # GPS info
        self.frame2 = LabelFrame(
            self.label_frame, text="GPS info", font="{Helvetica} 8 bold", bg="lightblue")
        self.frame2.pack(side=LEFT, pady=5, padx=5)

        self.latitude = Label(self.frame2, text="Latitude:", bg="lightblue")
        self.latitude.grid(row=0, column=0, pady=5)
        self.latitude_entry = Text(self.frame2, height=1, width=12)
        self.latitude_entry.grid(row=0, column=1, pady=5)

        self.longitude = Label(self.frame2, text="Longitude:", bg="lightblue")
        self.longitude.grid(row=0, column=2, pady=5)
        self.longitude_entry = Text(self.frame2, height=1, width=12)
        self.longitude_entry.grid(row=0, column=3, pady=5, padx=5)

        self.altitude = Label(self.frame2, text="Altitude:", bg="lightblue")
        self.altitude.grid(row=1, column=0, pady=5)
        self.altitude_entry = Text(self.frame2, height=1, width=12)
        self.altitude_entry.grid(row=1, column=1, pady=5)

        self.hdop = Label(self.frame2, text="Precision:", bg="lightblue")
        self.hdop.grid(row=2, column=0, pady=5)
        self.hdop_entry = Text(self.frame2, height=1, width=12)
        self.hdop_entry.grid(row=2, column=1, pady=5)

        self.fix = Label(self.frame2, text="Positioning:", bg="lightblue")
        self.fix.grid(row=2, column=2, pady=5)
        self.fix_entry = Text(self.frame2, height=1, width=12)
        self.fix_entry.grid(row=2, column=3, padx=5, pady=5)

        self.utc = Label(self.frame2, text="UTC:", bg="lightblue")
        self.utc.grid(row=1, column=2, pady=5)
        self.utc_entry = Text(self.frame2, height=1, width=12)
        self.utc_entry.grid(row=1, column=3, padx=5, pady=5)

        self.cog = Label(self.frame2, text="cog:", bg="lightblue")
        self.cog.grid(row=3, column=0, pady=5)
        self.cog_entry = Text(self.frame2, height=1, width=12)
        self.cog_entry.grid(row=3, column=1, pady=5)

        self.spkm = Label(self.frame2, text="spkm:", bg="lightblue")
        self.spkm.grid(row=4, column=0, pady=5)
        self.spkm_entry = Text(self.frame2, height=1, width=12)
        self.spkm_entry.grid(row=4, column=1, pady=5)

        self.spkn = Label(self.frame2, text="spkn:", bg="lightblue")
        self.spkn.grid(row=4, column=2, pady=5)
        self.spkn_entry = Text(self.frame2, height=1, width=12)
        self.spkn_entry.grid(row=4, column=3, pady=5)

        self.nsat = Label(self.frame2, text="No. Satellite:", bg="lightblue")
        self.nsat.grid(row=3, column=2, pady=5)
        self.nsat_entry = Text(self.frame2, height=1, width=12)
        self.nsat_entry.grid(row=3, column=3, pady=5)

        # signal strength
        self.frame1 = LabelFrame(
            self.label_frame, text="Signal info", font="{Helvetica} 8 bold", bg="lightblue")
        self.frame1.pack(side=LEFT, pady=5, padx=5)
        self.RSRP = Label(self.frame1, text="RSRP:", bg="lightblue")
        self.RSRP.grid(row=0, column=0,  pady=5)
        self.RSRP_entry = Text(self.frame1, height=1, width=8)
        self.RSRP_entry.grid(row=0, column=1, pady=5)

        self.RSRQ = Label(self.frame1, text="RSRQ:", bg="lightblue")
        self.RSRQ.grid(row=0, column=2, pady=5)
        self.RSRQ_entry = Text(self.frame1, height=1, width=8)
        self.RSRQ_entry.grid(row=0, column=3, pady=5)

        self.SINR = Label(self.frame1, text="SINR:", bg="lightblue")
        self.SINR.grid(row=1, column=0,  pady=5)
        self.SINR_entry = Text(self.frame1, height=1, width=8)
        self.SINR_entry.grid(row=1, column=1, pady=5)

        self.RSSI = Label(self.frame1, text="RSSI:", bg="lightblue")
        self.RSSI.grid(row=1, column=2,  pady=5)
        self.RSSI_entry = Text(self.frame1, height=1, width=8)
        self.RSSI_entry.grid(row=1, column=3,  pady=5)

        self.CQI = Label(self.frame1, text="CQI:", bg="lightblue")
        self.CQI.grid(row=0, column=4,  pady=5)
        self.CQI_entry = Text(self.frame1, height=1, width=8)
        self.CQI_entry.grid(row=0, column=5,  pady=5)

        self.tx_power = Label(self.frame1, text="TX_power:", bg="lightblue")
        self.tx_power.grid(row=1, column=4, pady=5)
        self.tx_power_entry = Text(self.frame1, height=1, width=8)
        self.tx_power_entry.grid(row=1, column=5, padx=5, pady=5)

        self.ULBW = Label(self.frame1, text="UL_BW:", bg="lightblue")
        self.ULBW.grid(row=2, column=4, pady=5)
        self.ULBW_entry = Text(self.frame1, height=1, width=8)
        self.ULBW_entry.grid(row=2, column=5, padx=5, pady=5)

        self.DLBW = Label(self.frame1, text="DL_BW:", bg="lightblue")
        self.DLBW.grid(row=3, column=4,  pady=5)
        self.DLBW_entry = Text(self.frame1, height=1, width=8)
        self.DLBW_entry.grid(row=3, column=5, padx=5, pady=5)

        self.MCC = Label(self.frame1, text="MCC:", bg="lightblue")
        self.MCC.grid(row=2, column=0,  pady=5)
        self.MCC_entry = Text(self.frame1, height=1, width=8)
        self.MCC_entry.grid(row=2, column=1, pady=5)

        self.MNC = Label(self.frame1, text="MNC:", bg="lightblue")
        self.MNC.grid(row=2, column=2,  pady=5)
        self.MNC_entry = Text(self.frame1, height=1, width=8)
        self.MNC_entry.grid(row=2, column=3, pady=5)

        self.CELL_ID = Label(self.frame1, text="Cell_id:", bg="lightblue")
        self.CELL_ID.grid(row=3, column=0, pady=5)
        self.CELL_ID_entry = Text(self.frame1, height=1, width=8)
        self.CELL_ID_entry.grid(row=3, column=1, pady=5)

        self.PCID = Label(self.frame1, text="PCID:", bg="lightblue")
        self.PCID.grid(row=3, column=2,  pady=5)
        self.PCID_entry = Text(self.frame1, height=1, width=8)
        self.PCID_entry.grid(row=3, column=3, pady=5)

        self.TAC = Label(self.frame1, text="TAC:", bg="lightblue")
        self.TAC.grid(row=4, column=0,  pady=5)
        self.TAC_entry = Text(self.frame1, height=1, width=8)
        self.TAC_entry.grid(row=4, column=1,  pady=5)

        self.earfcn = Label(self.frame1, text="earfcn:", bg="lightblue")
        self.earfcn.grid(row=4, column=2,  pady=5)
        self.earfcn_entry = Text(self.frame1, height=1, width=8)
        self.earfcn_entry.grid(row=4, column=3,  pady=5)

        self.is_tdd = Label(self.frame1, text="LTE-mode:", bg="lightblue")
        self.is_tdd.grid(row=4, column=4,  pady=5)
        self.is_tdd_entry = Text(self.frame1, height=1, width=8)
        self.is_tdd_entry.grid(row=4, column=5, padx=5, pady=5)
        # hehe
        self.duplex = Label(self.frame1, text="Duplex_mode:", bg="lightblue")
        self.duplex.grid(row=5, column=0,  pady=5)
        self.duplex_entry = Text(self.frame1, height=1, width=8)
        self.duplex_entry.grid(row=5, column=1,  pady=5)

        self.band = Label(self.frame1, text="SA-ARFCN:", bg="lightblue")
        self.band.grid(row=5, column=2,  pady=5)
        self.band_entry = Text(self.frame1, height=1, width=8)
        self.band_entry.grid(row=5, column=3,  pady=5)

        self.arfcn = Label(self.frame1, text="ARFCN:", bg="lightblue")
        self.arfcn.grid(row=5, column=4,  pady=5)
        self.arfcn_entry = Text(self.frame1, height=1, width=8)
        self.arfcn_entry.grid(row=5, column=5, padx=5, pady=5)

        self.frame4 = Frame(self.label_frame, bg="lightblue")
        self.frame4.pack(side=LEFT, pady=5)

        # general info
        self.frame3 = LabelFrame(
            self.frame4, text="General info", font="{Helvetica} 8 bold", bg="lightblue")
        self.frame3.pack(side=TOP, fill=X, pady=5, padx=5, expand=1)
        # work mode
        self.work_mode = Label(
            self.frame3, text="Cellular Mode:", bg="lightblue")
        self.work_mode.grid(row=0, column=0, pady=5)
        self.work_mode_entry = Text(self.frame3, height=1, width=17)
        self.work_mode_entry.grid(row=0, column=1, pady=5, padx=5)

        # source IP
        self.source_ip = Label(self.frame3, text="Source IP:", bg="lightblue")
        self.source_ip.grid(row=1, column=0, pady=5)
        self.source_ip_entry = Text(self.frame3, height=1, width=17)
        self.source_ip_entry.grid(row=1, column=1, padx=5, pady=5)

        # internet Time
        self.internet_time = Label(
            self.frame3, text="Date&Time:", bg="lightblue")
        self.internet_time.grid(row=2, column=0, pady=5)
        self.internet_time_entry = Text(self.frame3, height=1, width=17)
        self.internet_time_entry.grid(row=2, column=1, padx=5, pady=5)

        self.frame0 = LabelFrame(
            self.frame4, text="Config your PC", font="{Helvetica} 8 bold", bg="lightblue")
        self.frame0.pack(side=TOP, fill=X, padx=5, pady=5, expand=1)

        self.pc_ip = Label(self.frame0, text="IP:", bg="lightblue")
        self.pc_ip.pack(side=LEFT, expand=0, pady=5)
        self.pc_ip_entry = Entry(self.frame0, width=15)
        self.pc_ip_entry.pack(side=LEFT)

        self.pc_port = Label(self.frame0, text="Port:", bg="lightblue")
        self.pc_port.pack(side=LEFT, expand=0, padx=5, pady=5)
        self.pc_port_entry = Entry(self.frame0, width=8)
        self.pc_port_entry.pack(side=LEFT, padx=5, pady=5)

    def change_ip_port(self):
        self.pc_ip_value = self.pc_ip_entry.get()
        self.pc_port_value = self.pc_port_entry.get()
        return [self.pc_ip_value, self.pc_port_value]

    def UDP_socket(self):
        # change it according to your current computer, preferably static ip
        self.cus = self.change_ip_port()
        if self.cus[0] != "" and self.cus[1] != "" and self.cus[1].isdigit():
            self.UDP_IP = str(self.cus[0])
            self.UDP_PORT = int(self.cus[1])
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.UDP_IP, self.UDP_PORT))

    def gui_handler(self):
        self.change_state()
        if self.continueLogging:
            threading.Thread(target=self.logger).start()

    def change_state(self):
        if self.continueLogging == True:
            self.continueLogging = False

        else:
            self.continueLogging = True


    def logger(self):
        self.UDP_socket()
        while self.continueLogging:
            self.data = self.sock.recvfrom(1024)
            self.insert_to_dashboard()
            self.textbox.insert(END, self.data[::-1])
            self.textbox.insert(END, "\n")
            self.textbox.see("end")
    def insert_to_dashboard(self):
        target = str(self.data[0]).split(",")
        source_ip_value = self.data[1][0]
        internet_time_value = str(self.data[0]).split(" ")
        month = internet_time_value[0][6:]
        day = internet_time_value[1]
        time = internet_time_value[2]
        # insert time
        self.internet_time_entry.delete(1.0, END)
        self.internet_time_entry.insert('1.0', month+"-" + day+","+time)
        # insert source ip
        self.source_ip_entry.delete(1.0, END)
        self.source_ip_entry.insert('1.0', source_ip_value)
        if "QGPSLOC" in target[0]:
            # print(target)
            # derive gps location
            self.latitude_value = (
                float(target[1])//100)+(float(target[1]) % 100)/60
            self.latitude_value = round(self.latitude_value, 6)
            self.longitude_value = (
                float(target[3])//100)+(float(target[3]) % 100)/60
            self.longitude_value = round(self.longitude_value, 6)

            # derive utc-time
            self.utc_value = target[0].split(":")[-1]
            h = float(self.utc_value)//10000
            m = (float(self.utc_value) % 10000)//100
            s = float(self.utc_value) % 100
            h = int(h)
            m = int(m)
            s = int(s)

            self.cog_value_d = target[-5].split(".")[0]+"°"
            self.cog_value_m = target[-5].split(".")[-1]+"\'"

            # insert gps data
            self.latitude_entry.delete(1.0, END)
            self.latitude_entry.insert(
                '1.0', str(self.latitude_value)+" "+target[2])
            self.longitude_entry.delete(1.0, END)
            self.longitude_entry.insert('1.0', str(
                self.longitude_value)+" "+target[4])
            self.altitude_entry.delete(1.0, END)
            self.altitude_entry.insert('1.0', target[6]+" m")
            self.utc_entry.delete(1.0, END)
            hour = "0"+str(h) if h < 10 else str(h)
            minute = "0"+str(m) if m < 10 else str(m)
            second = "0"+str(s) if s < 10 else str(s)
            self.utc_entry.insert('1.0', hour + ":" + minute + ":" + second)
            self.hdop_entry.delete(1.0, END)
            self.hdop_entry.insert('1.0', target[5])
            self.fix_entry.delete(1.0, END)
            self.fix_entry.insert('1.0', target[7]+"D")
            self.cog_entry.delete(1.0, END)
            self.cog_entry.insert(
                '1.0', self.cog_value_d+self.cog_value_m)
            self.spkm_entry.delete(1.0, END)
            self.spkm_entry.insert('1.0', target[-4]+" km/h")
            self.spkn_entry.delete(1.0, END)
            self.spkn_entry.insert('1.0', target[-3]+" knots")
            self.nsat_entry.delete(1.0, END)
            self.nsat_entry.insert('1.0', target[-1].replace('\'', ""))

        if len(target) > 8 and "servingcell" in target[0]:
            # print(target)
            # LTE mode or EN-DC_LTE
            if '"LTE"' == target[2]:
                self.RSRP_value = target[-7]
                self.RSRQ_value = target[-6]
                self.SINR_value = target[-4]
                self.RSSI_value = target[-5]
                self.mode_value = target[2]
                self.MCC_value = target[4]
                self.MNC_value = target[5]
                self.CELL_ID_value = target[6]
                self.PCID_value = target[7]
                self.earfcn_value = target[8]
                self.TAC_value = target[12]
                self.CQI_value = target[-3]
                self.tx_power_value = target[-2]
                self.ULBW_value = target[10]
                self.DLBW_value = target[11]
                self.is_tdd_value = target[3].replace("\"", "")
            # EN-DN LTE
            if '"LTE"' in target[0]:
                self.RSRP_value = target[-7]
                self.RSRQ_value = target[-6]
                self.SINR_value = str(int(target[-4])*2-20)
                self.RSSI_value = target[-5]
                self.mode_value = target[0]
                self.MCC_value = target[2]
                self.MNC_value = target[3]
                self.CELL_ID_value = target[4]
                self.PCID_value = target[5]
                self.earfcn_value = target[6]
                self.TAC_value = target[10]
                self.CQI_value = target[-3]
                self.tx_power_value = target[-2]
                self.ULBW_value = target[8]
                self.DLBW_value = target[9]

            # 5G_SA mode
            if "NR5G-SA" == target[2]:
                self.RSRP_value = target[-5]
                self.RSRQ_value = target[-4]
                self.SINR_value = target[-3]
                self.mode_value = target[2]
                self.MCC_value = target[4]
                self.MNC_value = target[5]
                self.CELL_ID_value = target[6]
                self.PCID_value = target[7]
                self.TAC_value = target[8]
                self.tx_power_value = target[-2]
                self.duplex_value = target[3].replace("\"", "")
                self.band_value = target[10]
                self.arfcn_value = target[9]
                self.duplex_entry.delete(1.0, END)
                self.duplex_entry.insert('1.0', self.duplex_value)
                self.band_entry.delete(1.0, END)
                self.band_entry.insert('1.0', self.band_value)
                self.arfcn_entry.delete(1.0, END)
                self.arfcn_entry.insert('1.0', self.arfcn_value)
            # 5G_SA mode
            if "NR5G-NSA" in target[0]:
                self.RSRP_value = target[-5]
                self.RSRQ_value = target[-3]
                self.SINR_value = target[-4]
                self.mode_value = target[0]
                self.MCC_value = target[1]
                self.MNC_value = target[2]
                self.PCID_value = target[3]
                self.band_value = target[-1]
                self.arfcn_value = target[-2]
                self.band_entry.delete(1.0, END)
                self.band_entry.insert('1.0', self.band_value)
                self.arfcn_entry.delete(1.0, END)
                self.arfcn_entry.insert('1.0', self.arfcn_value)
        # print("RSRP:", self.RSRP_value, "RSRQ:", self.RSRQ_value,
            # "SINR:", self.SINR_value, "RSSI:", self.RSSI_value)
            self.RSRP_entry.delete(1.0, END)
            self.RSRP_entry.insert('1.0', self.RSRP_value+" dBm")
            self.RSRQ_entry.delete(1.0, END)
            self.RSRQ_entry.insert('1.0', self.RSRQ_value+" dB")
            self.SINR_entry.delete(1.0, END)
            self.SINR_entry.insert('1.0', self.SINR_value+" dB")
            self.RSSI_entry.delete(1.0, END)
            self.RSSI_entry.insert('1.0', self.RSSI_value+" dB")
            self.work_mode_entry.delete(1.0, END)
            self.work_mode_entry.insert(
                '1.0', self.mode_value.replace('"', ''))
            self.MCC_entry.delete(1.0, END)
            self.MCC_entry.insert('1.0', self.MCC_value)
            self.MNC_entry.delete(1.0, END)
            self.MNC_entry.insert('1.0', self.MNC_value)
            self.CELL_ID_entry.delete(1.0, END)
            self.CELL_ID_entry.insert('1.0', self.CELL_ID_value)
            self.PCID_entry.delete(1.0, END)
            self.PCID_entry.insert('1.0', self.PCID_value)
            self.earfcn_entry.delete(1.0, END)
            self.earfcn_entry.insert('1.0', self.earfcn_value)
            self.TAC_entry.delete(1.0, END)
            self.TAC_entry.insert('1.0', self.TAC_value)
            self.CQI_entry.delete(1.0, END)
            self.CQI_entry.insert('1.0', self.CQI_value)
            self.tx_power_entry.delete(1.0, END)
            self.tx_power_entry.insert('1.0', self.tx_power_value)
            self.ULBW_entry.delete(1.0, END)
            if self.ULBW_value == '5':
                self.UL_ = '20 MHz'
            if self.ULBW_value == '4':
                self.UL_ = '15 MHz'
            if self.ULBW_value == '3':
                self.UL_ = '10 MHz'
            if self.ULBW_value == '2':
                self.UL_ = '5 MHz'
            if self.ULBW_value == '1':
                self.UL_ = '3 MHz'
            if self.ULBW_value == '0':
                self.UL_ = '1.4 MHz'
            if self.DLBW_value == '5':
                self.DL_ = '20 MHz'
            if self.DLBW_value == '4':
                self.DL_ = '15 MHz'
            if self.DLBW_value == '3':
                self.DL_ = '10 MHz'
            if self.DLBW_value == '2':
                self.DL_ = '5 MHz'
            if self.DLBW_value == '1':
                self.DL_ = '3 MHz'
            if self.DLBW_value == '0':
                self.DL_ = '1.4 MHz'
            self.ULBW_entry.insert('1.0', self.UL_)
            self.DLBW_entry.delete(1.0, END)
            self.DLBW_entry.insert('1.0', self.DL_)
            self.is_tdd_entry.delete(1.0, END)
            self.is_tdd_entry.insert('1.0', self.is_tdd_value)

    def clear_screen(self):
        self.textbox.delete(1.0, END)

    def SaveFileAs(self, whatever=None):
        self.filename = tk.filedialog.asksaveasfilename(
            defaultextension='.out', filetypes=(("All Files", "*.*"),), initialdir="./")
        if self.filename:
            f = open(self.filename, 'w')
            f.write(self.textbox.get('1.0', 'end'))
            f.close()

    def Openfile(self):
        self.openfile = tk.filedialog.askopenfilename(
            initialdir="./", filetypes=(("All Files", "*.*"),))
        if self.openfile:
            self.open = open(self.openfile, 'r')
            try:
                self.stuff = self.open.read()
                self.clear_screen()
                self.textbox.insert(END, self.stuff)
                self.textbox.insert(END, "\n")
                self.textbox.update()
                self.open.close()
            except UnicodeDecodeError:
                mb.showerror("Alert","Failed to decode file type.")
           

def main():
    root = tk.Tk()
    App(root)
    root.title('Log View')
    root.iconbitmap('log.ico')
    root.mainloop()


if __name__ == "__main__":
    main()