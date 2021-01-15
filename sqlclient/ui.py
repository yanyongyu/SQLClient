import tkinter as tk
from tkinter.messagebox import showerror
from typing import List, Optional, Callable

from prettytable import PrettyTable

from .sql import SQL


class UI:

    def __init__(self):
        self._root: Optional[tk.Tk] = None
        self._db: SQL = SQL()
        self.WIDTH = 960
        self.HEIGHT = 640
        self.DB_WIDTH = 200
        self.SQL_HEIGHT = 500

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value: tk.Tk):
        if self._root:
            self._root.destroy()
        self._root = value

    @property
    def db(self):
        return self._db

    @property
    def SQL_WIDTH(self):
        return self.WIDTH - self.DB_WIDTH

    @property
    def DB_HEIGHT(self):
        return self.HEIGHT

    @property
    def RESULT_WIDTH(self):
        return self.SQL_WIDTH

    @property
    def RESULT_HEIGHT(self):
        return self.HEIGHT - self.SQL_HEIGHT

    def close(self):
        self.db.close()
        self.root.destroy()

    def welcome_window(self):
        self.root = tk.Tk()
        self.root.title("TinyDB")
        self.root.geometry("480x360")
        self._welcome_main()

    def _welcome_main(self):
        welcome = tk.Label(self.root, text="WELCOME TO TINYDB", font=("等线", 20))
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

        def _connect_database():
            try:
                self.db.connect(host.get(), int(port.get()), username.get(),
                                password.get())
            except Exception as e:
                print(repr(e))
                showerror("连接错误", repr(e))
                return

            self.db_window()

        connect = tk.Button(frame,
                            text="连接",
                            command=_connect_database,
                            font=("等线", 15),
                            width=10)
        connect.pack(pady=10)
        self.root.bind_all("<Return>", lambda x: _connect_database())

    def entry_with_label(self, master, label, entry_var):
        frame = tk.Frame(master)
        frame.pack(fill="x", padx=50, pady=15)
        label = tk.Label(frame, text=label, font=("等线", 15))
        label.pack(side="left")
        entry = tk.Entry(frame, textvariable=entry_var, font=("等线", 15))
        entry.pack(side="right")

    def db_window(self):
        self.root = tk.Tk()
        self.root.title("TinyDB")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        result_string = tk.StringVar(self.root)
        sql_string = tk.StringVar(self.root)

        frame1 = tk.Frame(self.root, width=self.DB_WIDTH, height=self.DB_HEIGHT)
        frame1.pack(side="left", fill="y")

        def _change_database(database_name):
            self.db.execute(f"USE {database_name}")
            result_string.set(f"成功切换到数据库: {database_name}")

        self._db_databases(frame1, _change_database)

        frame = tk.Frame(self.root)
        frame.pack(side="right", fill="both", expand=True)
        frame2 = tk.Frame(frame, height=self.SQL_HEIGHT)
        frame2.pack(side="top", fill="x", expand=True)
        self._db_sql(frame2, sql_string, result_string)

        frame3 = tk.Frame(frame)
        frame3.pack(side="bottom", fill="x", expand=True)
        self._db_result(frame3, result_string)
        self.root.mainloop()

    def _db_databases(self, master, on_change_database: Callable[[str], None]):
        frame = self.frame_with_scrollbar(master, self.DB_WIDTH, self.DB_HEIGHT)
        label = tk.Label(frame, text="数据库列表", font=("等线", 15))
        label.pack(side="top", fill="x", pady="10")
        buttons: List[tk.Button] = []

        def _refresh():
            for button in buttons:
                button.destroy()
            buttons.clear()
            _, databases = self.db.execute("SHOW DATABASES")
            for database in databases:
                database_name = database["Database"]
                button = tk.Button(frame, text=database_name)
                button.pack(side="top", fill="x")
                button.bind(
                    "<Button-1>",
                    lambda event: on_change_database(event.widget["text"]))
                buttons.append(button)

        menu = tk.Menu(frame, tearoff=0)
        menu.add_command(label="刷新", command=_refresh)

        def _popup(event):
            menu.tk_popup(event.x_root, event.y_root)

        frame.bind_all("<Button-3>", _popup)

        _refresh()

    def _db_sql(self, master, input, output):
        # toolbar
        def _run_sql():
            sql = input.get().strip()
            try:
                row, data = self.db.execute(sql)
            except Exception as e:
                print(repr(e))
                output.set(repr(e))
                return

            message = f"执行成功！共有{row}行数据受到影响。\n"
            if data:
                x = PrettyTable()
                x.field_names = [*data[0].keys()]
                x.add_rows([[*x.values()] for x in data])
                message += str(x)
            output.set(message.strip())

        frame1 = tk.Frame(master)
        frame1.pack(side="top", fill="x", expand=False)
        button1 = tk.Button(frame1, text="运行", command=_run_sql)
        button1.pack(side="left", fill="y")
        button2 = tk.Button(frame1, text="清空", command=lambda: input.set(""))
        button2.pack(side="left", fill="y")

        frame2 = tk.Frame(master)
        frame2.pack(side="top", fill="both", expand=True)
        text = tk.Text(frame2, font=("等线", 15), undo=True, maxundo=10)
        text.pack(side="left", fill="both", expand=True)
        text.bind("<Control-Z>", lambda x: text.edit_undo())
        text.bind("<Control-Shift-Z>", lambda x: text.edit_redo())
        text.bind("<F5>", lambda x: _run_sql())
        bar = AutoShowScrollbar(frame2)
        bar.pack(side="right", fill="y", expand=False)
        bar.configure(command=text.yview)
        text.configure(yscrollcommand=bar.set)

        def _set(value: str):
            text.delete(1.0, "end")
            text.insert(1.0, value)

        def _get() -> str:
            return text.get(1.0, "end")

        input.get = _get
        input.set = _set

    def _db_result(self, master, output):
        text = tk.Text(master, font=("等线", 15))
        text.pack(side="left", fill="x", expand=True)
        bar = AutoShowScrollbar(master)
        bar.pack(side="right", fill="y", expand=False)
        bar.configure(command=text.yview)
        text.configure(yscrollcommand=bar.set)

        def _set(value: str):
            text.delete(1.0, "end")
            text.insert(1.0, value)

        def _get() -> str:
            return text.get(1.0, "end")

        output.get = _get
        output.set = _set

    def frame_with_scrollbar(self, master, width: int, height: int):
        frame = tk.Frame(master, width=width, height=height)
        frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(frame, width=width, height=height)
        canvas.pack(side="left", fill="both", expand=True)

        frame_inner = tk.Frame(canvas, width=width, height=height)
        frame_id = canvas.create_window(0, 0, window=frame_inner, anchor="nw")
        bar = AutoShowScrollbar(frame, orient="vertical")
        bar.pack(side="right", fill="y", expand=False)
        bar.configure(command=canvas.yview)
        canvas.configure(yscrollcommand=bar.set)

        def _scroll_canvas(event):
            canvas.yview_scroll(int(-event.delta / 60), "units")

        def _unscroll_canvas(event):
            return "break"

        def _configure_frame(event):
            canvas.configure(scrollregion=(0, 0, frame_inner.winfo_reqwidth(),
                                           frame_inner.winfo_reqheight()))
            if frame_inner.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=frame_inner.winfo_reqwidth())

            if frame_inner.winfo_reqheight() < canvas.winfo_height():
                canvas.bind_all("<MouseWheel>", _unscroll_canvas)
            else:
                canvas.bind_all("<MouseWheel>", _scroll_canvas)

        def _configure_canvas(event):
            if frame_inner.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(frame_id, width=canvas.winfo_width())

        frame_inner.bind("<Configure>", _configure_frame)
        canvas.bind("<Configure>", _configure_canvas)
        canvas.bind_all("<MouseWheel>", _scroll_canvas)
        return frame_inner

    def start(self):
        self.welcome_window()
        self.root.mainloop()


class AutoShowScrollbar(tk.Scrollbar):
    "自动隐藏滚动条"

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("pack", "forget", self)
        else:
            self.pack(fill="y", side="right", expand=False)
        super().set(lo, hi)
