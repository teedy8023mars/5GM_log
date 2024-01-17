import tkinter as tk
from tkinter import *
from tkinter import filedialog, scrolledtext, messagebox
import time
import threading
import socket
import sys
import os

class App:
    def __init__(self, win):
        # (Your initialization code here)

    def change_ip_port(self):
        return [self.pc_ip_entry.get(), self.pc_port_entry.get()]

    def UDP_socket(self):
        self.cus = self.change_ip_port()
        if self.cus[0] != "" and self.cus[1] != "" and self.cus[1].isdigit():
            self.UDP_IP, self.UDP_PORT = str(self.cus[0]), int(self.cus[1])
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                self.sock.bind((self.UDP_IP, self.UDP_PORT))
            except OSError:
                messagebox.showerror("Alert", "Invalid IP and port !!!")
                self.change_state()
        else:
            messagebox.showerror("Alert", "Enter IP and port !!!")
            self.change_state()

    def change_state(self):
        if self.continueLogging:
            self.continueLogging = False
            try:
                self.sock.close()
            except:
                pass
        else:
            self.continueLogging = True
            threading.Thread(target=self.logger).start()

    def logger(self):
        self.UDP_socket()
        while self.continueLogging:
            try:
                self.data = self.sock.recvfrom(1024)
                self.insert_to_dashboard()
                self.textbox.insert(END, self.data[::-1])
                self.textbox.insert(END, "\n")
                self.textbox.see("end")
            except:
                pass

    def insert_to_dashboard(self):
        target = str(self.data[0]).split(",")
        source_ip_value = self.data[1][0]
        internet_time_value = str(self.data[0]).split(" ")
        month, day, time = internet_time_value[0][6:], internet_time_value[1], internet_time_value[2]

        # (Remaining code for inserting data to dashboard)

    def clear_screen(self):
        self.textbox.delete(1.0, END)

    def SaveFileAs(self, whatever=None):
        self.filename = filedialog.asksaveasfilename(
            defaultextension='.out', filetypes=(("All Files", "*.*"),), initialdir="./")
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(self.textbox.get('1.0', 'end'))

    def Openfile(self):
        self.openfile = filedialog.askopenfilename(
            initialdir="./", filetypes=(("All Files", "*.*"),))
        if self.openfile:
            with open(self.openfile, 'r') as f:
                try:
                    self.stuff = f.read()
                    self.clear_screen()
                    self.textbox.insert(END, self.stuff)
                    self.textbox.insert(END, "\n")
                    self.textbox.update()
                except UnicodeDecodeError:
                    messagebox.showerror("Alert", "Failed to decode file type.")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit ?"):
            self.continueLogging = False
            try:
                self.sock.shutdown(1)
                self.sock.close()
            except:
                pass
            root.destroy()
            root.quit()
            sys.exit()

def main():
    a = App(root)
    root.title('Log View')
    root.iconbitmap('log.ico')
    root.protocol("WM_DELETE_WINDOW", a.on_closing)
    root.mainloop()

root = tk.Tk()
if __name__ == "__main__":
    main()
