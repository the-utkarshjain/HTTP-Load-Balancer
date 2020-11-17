from tkinter import *
import time
import os.path

class A:
    def __init__(self, master):
        self.master = master
        self.labels = []
        self.read_file()

    def read_file(self):
        file = open("temp.txt", "r").read()
        self.status = file.split("\n")[:-1]

        for i in range(len(self.labels)):
            self.labels[i].pack_forget()

        self.labels = []

        for i in range(len(self.status)):
            self.labels.append(Text(self.master, height=4, width=500, font=("TkDefaultFont", 15), state='disabled'))

        for i in range(len(self.labels)):
            text = self.status[i].split(" ")
            msg = 'Server: ' + text[0] + '\nActive: ' + text[1] + '\nOpen Connections: ' + text[2]
            self.labels[i].config(state='normal')
            self.labels[i].delete('1.0', END)
            self.labels[i].insert(END,msg)
            self.labels[i].config(state='disabled')
            self.labels[i].pack()

        self.labels[0].after(60, self.read_file)

root = Tk()
root.title('Load balancer')
root.geometry("600x700")
A(root)
root.mainloop()