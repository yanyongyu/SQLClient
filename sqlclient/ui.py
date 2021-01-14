import tkinter as tk
from typing import Optional

# root = tk.Tk()

# root.title('tiDB')
# root.geometry('480x240')

# def connect():
#     welcome.pack_forget()
#     connectdb = tk.Label(root, text="连接到数据库", pady=10)
#     connectdb.pack(side="top")

#     frame3 = tk.Frame(root)
#     frame3.pack(side="top", fill="y")

#     frame1 = tk.Frame(frame3, padx=50)
#     frame1.pack(side="left", fill="y")

#     login1 = tk.Label(frame1, text="连接名")
#     login1.pack(side="top")
#     login2 = tk.Label(frame1, text="主机")
#     login2.pack(side="top")
#     login3 = tk.Label(frame1, text="端口")
#     login3.pack(side="top")
#     login4 = tk.Label(frame1, text="用户名")
#     login4.pack(side="top")
#     login5 = tk.Label(frame1, text="密码")
#     login5.pack(side="top")

#     frame2 = tk.Frame(frame3)
#     frame2.pack(side="left", fill="y")

#     connectname = tk.Entry(frame2)
#     connectname.pack(side="top")
#     localhost = tk.Entry(frame2)
#     localhost.pack(side="top")
#     port = tk.Entry(frame2)
#     port.pack(side="top")
#     username = tk.Entry(frame2)
#     username.pack(side="top")
#     password = tk.Entry(frame2)
#     password.pack(side="top")

#     connectbt = tk.Button(root, text="连接", command=sql)
#     connectbt.pack(side="top")

# def disconnect():
#     print('断开数据库')

# def sql():
#     print('sql')

# menuebar = tk.Menu(root)

# filemenu = tk.Menu(menuebar, tearoff=False)
# filemenu.add_command(label="连接数据库", command=connect)
# filemenu.add_separator()
# filemenu.add_command(label="断开数据库", command=disconnect)
# menuebar.add_cascade(label="数据库连接", menu=filemenu)

# menuebar.add_command(label="SQL", command=sql)

# root.config(menu=menuebar)

# welcome = tk.Label(root, text="WELCOME TO TIDB", pady=120)
# welcome.pack()

# root.mainloop()


class UI:

    def __init__(self):
        self._root: Optional[tk.Tk] = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value: tk.Tk):
        if self._root:
            self._root.destroy()
        self._root = value

    def welcome_window(self):
        self.root = tk.Tk()
        self.root.title("TinyDB")
        self.root.geometry("480x360")
        self._welcome_main()

    def _welcome_main(self):
        welcome = tk.Label(self.root, text="WELCOME TO TIDB", font=("等线", 20))
        welcome.pack(side="top", fill="x", pady=25)

        frame = tk.Frame(self.root)
        frame.pack(fill="both")
        host = tk.StringVar()
        port = tk.StringVar()
        username = tk.StringVar()
        password = tk.StringVar()
        self.entry_with_label(frame, "主机", host)
        self.entry_with_label(frame, "端口", port)
        self.entry_with_label(frame, "用户名", username)
        self.entry_with_label(frame, "密码", password)
        connect = tk.Button(frame, text="连接", font=("等线", 15), width=10)
        connect.pack(pady=10)

    def entry_with_label(self, master, label, entry_var):
        frame = tk.Frame(master)
        frame.pack(fill="x", padx=50, pady=15)
        label = tk.Label(frame, text=label, font=("等线", 15))
        label.pack(side="left")
        entry = tk.Entry(frame, textvariable=entry_var, font=("等线", 15))
        entry.pack(side="right")

    def start(self):
        self.welcome_window()
        self.root.mainloop()
