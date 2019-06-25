from tkinter import *
import os

class Demo1:
    def __init__(self, master):
        self.master = master
        self.master.option_add('*font', ('Ariel', 12, 'bold'))
        self.master.title("Chatbox - Menu")
        self.master.geometry("320x320")
        fm = Frame(self.master)
        w = Label(self.master, text="Welcome to Chatbox App\n Choose to continue")
        w.pack()
        self.T = Text(self.master, height=1, width=20)
        self.T.pack()
        self.T.insert(END, "Enter your name here")
        Button(fm, text='Broadcast', command = self.menu_broadcast).pack(side=TOP, expand=YES)
        Button(fm, text='Listen', command = self.menu_listen).pack(side=TOP, expand=YES)
        Button(fm, text='Help', command = self.new_windows).pack(side=TOP, expand=YES)
        w2 = Label(self.master, text="Made with LOVE\n By @uramirbin")
        w2.pack(side=BOTTOM)
        fm.pack(fill=BOTH, expand=YES)
        self.action = ""
        self.name = ""

    def new_windows(self):
        self.newWindow = Toplevel(self.master)
        self.app = help_menu(self.newWindow)
    

    def menu_broadcast(self):
        self.name = self.T.get("1.0",END)
        self.action = "1"
        self.master.destroy()

    def menu_listen(self):
        self.name = self.T.get("1.0",END)
        self.action = "2"
        self.master.destroy()

    def get(self):
        return self.action, self.name

class help_menu:
    def __init__(self, master):
        self.master = master
        self.master.option_add('*font', ('Ariel', 12))
        self.master.title("Chatbox - Help")
        self.master.geometry("480x240")
        self.fm = Frame(self.master)
        w = Label(self.fm, text="First Run the broadcast then listener")
        w.pack()
        w = Label(self.master, text="WARNING: Broadcaster, broadcasts for about 4 seconds")
        w.pack()
        w = Label(self.master, text="Type in [!q] in chat to disconnect")
        w.pack()
        Button(self.fm, text='Back', command = self.close_windows).pack(side=TOP, expand=YES)
        w2 = Label(self.master, text="Made with LOVE\n By @uramirbin")
        w2.pack(side=BOTTOM)
        self.fm.pack(fill=BOTH, expand=YES)

    def close_windows(self):
        self.master.destroy()
        




def main(): 
    root = Tk()
    app = Demo1(root)
    root.mainloop()
    myaction, myname = app.get()
    address = "python server.py "
    command = address + myaction + " " + myname
    os.system(command)

if __name__ == '__main__':
    main()