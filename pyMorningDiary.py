#!/usr/bin/env python3

from datetime import date
import sqlite3
import tkinter as tk
import tkinter.colorchooser as tkcolorchooser
import dlgCalendar

# date.today()
# d.isoformat()
# d.toordinal()
# d.fromordinal()

class UIDiary(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.grid(row=0, column=0)

        self.TITLES = ['人际关系 家庭 朋友', '未来日记 明日摘要', '愿望 人生梦想',
            '健康 饮食 锻炼', '情报 信息 阅读',
            '理财 金钱', '工作 创意 兴趣', '快乐 惊喜 其他']
        self.COLORS = ['#e4fd82', '#affeff', '#fefebb',
            '#d9fefe', '#52c8ff',
            '#fd97b4', '#6bf6a6', '#d287f9']
        self.PANE_ROW = 2      # Diary Pane row offset
        self.POSITIONS = [(self.PANE_ROW, 0), (self.PANE_ROW, 1),
            (self.PANE_ROW, 2), (self.PANE_ROW + 1, 0),
            (self.PANE_ROW + 1, 2), (self.PANE_ROW + 2, 0),
            (self.PANE_ROW + 2, 1), (self.PANE_ROW + 2, 2)]
        self.DIARYPANES = []

        self.create_widgets()

    def create_widgets(self):

        UIDiaryMenu(self.frame).grid(row=0, column=0, columnspan=3, sticky='WE')
        UIDateNavigator(self.frame).grid(row=1, column=0, columnspan=3)
        UIDiaryInfo(self.frame).grid(row=self.PANE_ROW + 1, column=1)

        for i in range(8):
            self.DIARYPANES.append(UIDiaryPane(self.frame,
                self.TITLES[i], self.COLORS[i]))
            self.DIARYPANES[i].grid(row=self.POSITIONS[i][0],
                column=self.POSITIONS[i][1])


class UIDiaryMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.menubar = tk.Frame(self, relief=tk.RAISED, bd=1)
        self.menubar.pack(fill=tk.X)

        self.FILE = '文件(F)'
        self.SAVE = '保存(S)'
        self.DELETE = '删除(D)'
        self.BACKUPDB = '备份数据文件(B)'
        self.EXIT = '退出(X)  Alt+F4'

        self.GOTO = '转到(G)'
        self.NEXT_10YEARS = '下十年这天'
        self.PREV_10YEARS = '上十年这天'
        self.NEXT_YEAR = '下一年这天  Ctrl+PgDown'
        self.PREV_YEAR = '上一年这天  Ctrl+PgUp'
        self.NEXT_MONTH = '下个月这天'
        self.PREV_MONTH = '上个月这天'
        self.NEXT_WEEK = '下星期这天'
        self.PREV_WEEK = '上星期这天'
        self.NEXT_DAY = '后一天  PgDown'
        self.PREV_DAY = '前一天  PgUp'

        self.TOOL = '工具(T)'
        self.OPTION = '选项(O)'

        self.HELP = '帮助(H)'
        self.HELP_F1 = '帮助  F1'
        self.ABOUT = '关于(A)'

        self.btn_file = tk.Menubutton(self.menubar, text=self.FILE,
            underline=3)
        self.btn_file.pack(side=tk.LEFT)
        self.btn_file.menu = tk.Menu(self.btn_file)
        self.btn_file.configure(menu=self.btn_file.menu)
        self.btn_file.menu.add_command(label=self.SAVE,
            command=self.todo_method, underline=3)
        self.btn_file.menu.add_command(label=self.DELETE,
            command=self.todo_method, underline=3)
        self.btn_file.menu.add_command(label=self.BACKUPDB,
            command=self.backupdb, underline=7)
        self.btn_file.menu.add_command(label=self.EXIT, command=self.exit_app,
            underline=3)

        self.btn_goto = tk.Menubutton(self.menubar, text=self.GOTO,
            underline=3)
        self.btn_goto.pack(side=tk.LEFT)
        self.btn_goto.menu = tk.Menu(self.btn_goto)
        self.btn_goto.configure(menu=self.btn_goto.menu)
        self.btn_goto.menu.add_command(label=self.NEXT_DAY,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.PREV_DAY,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.NEXT_WEEK,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.PREV_WEEK,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.NEXT_MONTH,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.PREV_MONTH,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.NEXT_YEAR,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.PREV_YEAR,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.NEXT_10YEARS,
            command=self.todo_method)
        self.btn_goto.menu.add_command(label=self.PREV_10YEARS,
            command=self.todo_method)

        self.btn_tool = tk.Menubutton(self.menubar, text=self.TOOL,
            underline=3)
        self.btn_tool.pack(side=tk.LEFT)
        self.btn_tool.menu = tk.Menu(self.btn_tool)
        self.btn_tool.configure(menu=self.btn_tool.menu)
        self.btn_tool.menu.add_command(label=self.OPTION,
            command=self.todo_method, underline=3)

        self.btn_help = tk.Menubutton(self.menubar, text=self.HELP,
            underline=3)
        self.btn_help.pack(side=tk.LEFT)
        self.btn_help.menu = tk.Menu(self.btn_help)
        self.btn_help.configure(menu=self.btn_help.menu)
        self.btn_help.menu.add_command(label=self.HELP_F1,
            command=self.todo_method)
        self.btn_help.menu.add_command(label=self.ABOUT,
            command=self.todo_method, underline=3)

    def backupdb(self):
        pass

    def exit_app(self):
        pass

    def todo_method(self):
        # TODO
        pass


class UIDiaryPane(tk.Frame):

    def __init__(self, parent, title, bg_color):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.title = title
        self.bg_color = bg_color

        self.TITLE_var = tk.StringVar()
        self.TITLE_var.set(self.title)
        self.lbl_title = tk.Label(self.frame, textvariable=self.TITLE_var,
            bg=self.bg_color)
        self.lbl_title.grid(row=0, column=0, sticky='EW')

        #~ self.btn_color = tk.Button(self.frame, text='Change Color',
            #~ command=self.change_color)
        #~ self.btn_color.grid(row=0, column=1)

        self.txt_cell = tk.Text(self.frame, height=12, width=35,
            bg=self.bg_color)
        self.txt_cell.grid(row=1, column=0, sticky='EWSN')
        self.txt_cell.bind("<FocusIn>", self.focus_in)
        self.txt_cell.bind("<FocusOut>", self.focus_out)

    def get_title(self):
        return self.TITLE_var.get()

    def set_title(self, str_title):
        self.TITLE_var.set(str_title)

    def get_text(self):
        return self.txt_cell.get(tk.START, tk.END)

    def set_text(self, str_text):
        self.txt_cell.delete(tk.START, tk.END)
        self.txt_cell.insert(tk.END, str_text)

    def change_color(self):
        self.bg_color = tkcolorchooser.askcolor(self.bg_color)[-1]
        self.lbl_title.configure(bg=self.bg_color)
        self.txt_cell.configure(bg=self.bg_color)

    def focus_in(self, event):
        # TODO: 自动查出往年的历史日记，并缓存当前日记
        pass

    def focus_out(self, event):
        # TODO: 对比当前日记内容和缓存值，若有更新则自动保存
        pass


class UIDiaryInfo(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.WEATHER = '天气'
        self.TEMPERATURE = '温度'
        self.HUMIDITY = '湿度'
        self.FESTIVAL = '节日'
        self.COMMOMERATION = '纪念日'
        self.MEET = '邂逅日'
        self.BIRTHDAY = '诞生日'
        self.SLEEP = '睡觉时间'
        self.GETUP = '起床时间'

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text=self.WEATHER).grid(
            row=0, column=0, sticky='E')
        self.weather_var = tk.StringVar()
        self.weather_var.set('')
        tk.Entry(self.frame, textvariable=self.weather_var).grid(
            row=0, column=1)

        tk.Label(self.frame, text=self.TEMPERATURE).grid(
            row=1, column=0, sticky='E')
        self.temp_var = tk.StringVar()
        self.temp_var.set('')
        tk.Entry(self.frame, textvariable=self.temp_var).grid(row=1, column=1)

        tk.Label(self.frame, text=self.HUMIDITY).grid(
            row=2, column=0, sticky='E')
        self.humidity_var = tk.StringVar()
        self.humidity_var.set('')
        tk.Entry(self.frame, textvariable=self.humidity_var).grid(
            row=2, column=1)

        tk.Label(self.frame, text=self.FESTIVAL).grid(
            row=3, column=0, sticky='E')
        self.festival_var = tk.StringVar()
        self.festival_var.set('')
        tk.Entry(self.frame, textvariable=self.festival_var).grid(
            row=3, column=1)

        tk.Label(self.frame, text=self.COMMOMERATION).grid(
            row=4, column=0, sticky='E')
        self.commomeration_var = tk.StringVar()
        self.commomeration_var.set('')
        tk.Entry(self.frame, textvariable=self.commomeration_var).grid(
            row=4, column=1)

        tk.Label(self.frame, text=self.MEET).grid(row=5, column=0, sticky='E')
        self.meet_var = tk.StringVar()
        self.meet_var.set('')
        tk.Entry(self.frame, textvariable=self.meet_var).grid(row=5, column=1)

        tk.Label(self.frame, text=self.BIRTHDAY).grid(
            row=6, column=0, sticky='E')
        self.birthday_var = tk.StringVar()
        self.birthday_var.set('')
        tk.Entry(self.frame, textvariable=self.birthday_var).grid(
            row=6, column=1)

        tk.Label(self.frame, text=self.SLEEP).grid(row=7, column=0, sticky='E')
        self.sleep_var = tk.StringVar()
        self.sleep_var.set('')
        tk.Entry(self.frame, textvariable=self.sleep_var).grid(row=7, column=1)

        tk.Label(self.frame, text=self.GETUP).grid(row=8, column=0, sticky='E')
        self.getup_var = tk.StringVar()
        self.getup_var.set('')
        tk.Entry(self.frame, textvariable=self.getup_var).grid(row=8, column=1)


class UIDateNavigator(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.DATE = '日期'
        self.TODAY = '今天'
        self.SEARCH_DEFAULT = '搜索整篇日记内容'
        self.SEARCH = '搜索'
        self.NEXT = '下一篇'

        self.create_widgets()

    def create_widgets(self):

        tk.Label(self.frame, text=self.DATE).grid(row=0, column=0, sticky='E')
        self.date_var = tk.StringVar()
        self.entry_date = tk.Entry(self.frame, textvariable=self.date_var,
            width=10)
        self.entry_date.grid(row=0, column=1)
        self.entry_date.bind("<Button-1>", self.goto_date)

        tk.Button(self.frame, text=self.TODAY, command=self.goto_today).grid(
            row=0, column=2)
        tk.Label(self.frame, text='', width=10).grid(row=0, column=3)

        self.search_var = tk.StringVar()
        self.search_var.set(self.SEARCH_DEFAULT)
        tk.Entry(self.frame, textvariable=self.search_var).grid(row=0, column=4)

        tk.Button(self.frame, text=self.SEARCH, command=self.search).grid(
            row=0, column=5)
        tk.Button(self.frame, text=self.NEXT, command=self.search_next).grid(
            row=0, column=6)

    def goto_today(self):
        pass

    def goto_date(self, event):
        dlgCalendar.tkCalendar(self.frame, 2011, 10, 6, self.date_var)
        # TODO: 在上一个界面中选定日期后刷新显示日记，及该日期的周年纪念信息

    def search(self):
        pass

    def search_next(self):
        pass


class DBSQLite:

    def __init__(self, db_name='.pyMorningDiary.db'):
        self.db_name = db_name
        self.db_path = os.path.join(os.path.expanduser('~'), db_name)

        self.needs_init = False
        if not os.path.isfile(self.db_path):
            self.needs_init = True

        self.con = sqlite3.connect(self.db_path)
        self.con.isolation_level = None
        self.cur = self.con.cursor()

        if self.needs_init:
            try:
                self.init_db()
            except Exception as e:
                print(e)

    def init_db(self):
        self.cur.execute("""
            CREATE TABLE PANESETTING (
                ID              INTEGER PRIMARY KEY AUTOINCREMENT,
                P_INDEX         INTEGER,
                COLOR           TEXT,
                TITLE           TEXT
            );
            CREATE TABLE DIARY (
                ID              INTEGER PRIMARY KEY AUTOINCREMENT,
                DATE            TEXT,
                D_INDEX         INTEGER,
                TITLE           TEXT,
                CONTENT         TEXT
            );
            CREATE TABLE DIARYINFO (
                ID              INTEGER PRIMARY KEY AUTOINCREMENT,
                DATE            TEXT,
                WEATHER         TEXT,
                TEMPERATURE     REAL,
                HUMIDITY        REAL,
                SLEEP_TIME      TEXT,
                GET_UP_TIME     TEXT,
                FESTIVAL        TEXT,
                COMMEMORATION   TEXT,
                MEET_WITH       TEXT,
                BIRTHDAY_OF     TEXT
            );
        """)
        self.con.commit()

    def insert_diary(self, date, diary_index, title, content):
        pass

    def update_diary(self, date, diary_index, title, content):
        pass

    def delete_diary(self, date):
        pass

    def insert_diary_info(self, date, **infos):
        for key, info in infos:
            if key in ('weather', 'temperature', 'humidity', 'sleep_time',
                'get_up_time', 'festival', 'commemoration', 'meet_with',
                'birthday_of'):
                    self.cur.execute("""
                        INSERT INTO DIARYINFO (DATE, ?)
                        VALUES
                        (?, ?)
                    """, (key, date, info))
        self.con.commit()

    def update_diary_info(self, date, **infos):
        for key, info in infos:
            if key in ('weather', 'temperature', 'humidity', 'sleep_time',
                'get_up_time', 'festival', 'commemoration', 'meet_with',
                'birthday_of'):
                    self.cur.execute("""
                        UPDATE DIARYINFO SET
                        ?=?
                        WHERE
                        DATE=?
                    """, (key, info, date))
        self.con.commit()

    def delete_diary_info(self, date):
        pass


if __name__ == '__main__':
    app = tk.Tk()
    app.title('晨间日记 - pyMorningDiary')
    diary = UIDiary(app)
    app.mainloop()
