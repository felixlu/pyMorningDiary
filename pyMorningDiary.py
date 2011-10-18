#!/usr/bin/env python3

from datetime import date
from datetime import timedelta
import os
import sqlite3
import tkinter as tk
import tkinter.colorchooser as tkcolorchooser

# date.today()
# d.isoformat()
# d.toordinal()
# d.fromordinal()

class UIDiary(tk.Frame):

    def __init__(self, parent, db):
        tk.Frame.__init__(self, parent)
        self.db = db
        self.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.titles = self.db.get_pane_titles()
        self.colors = self.db.get_pane_colors()

        self.PANE_ROW = 2      # Diary Pane row offset
        self.POSITIONS = [(self.PANE_ROW, 0), (self.PANE_ROW, 1),
            (self.PANE_ROW, 2), (self.PANE_ROW + 1, 0),
            (self.PANE_ROW + 1, 2), (self.PANE_ROW + 2, 0),
            (self.PANE_ROW + 2, 1), (self.PANE_ROW + 2, 2)]
        self.PANES = ['P1SETTING', 'P1CONTENT', 'P2SETTING', 'P2CONTENT',
            'P3SETTING', 'P3CONTENT', 'P4SETTING', 'P4CONTENT',
            'P5SETTING', 'P5CONTENT', 'P6SETTING', 'P6CONTENT',
            'P7SETTING', 'P7CONTENT', 'P8SETTING', 'P8CONTENT']
        self.INFOS = ['WEATHER', 'TEMPERATURE', 'HUMIDITY',
            'SLEEP_TIME', 'GET_UP_TIME',
            'FESTIVAL', 'COMMEMORATION', 'MEET_WITH', 'BIRTHDAY_OF']
        self.DATE = ['YEAR', 'MONTH', 'DAY']
        self.DIARY_FIELDS = self.DATE + self.PANES + self.INFOS

        self.create_widgets()
        self.display_diary_today()

    def create_widgets(self):

        self.bind_all("<Control-KeyPress-s>", self.save_diary)

        self.main_menu = UIDiaryMenu(self)
        self.main_menu.grid(row=0, column=0, columnspan=4, sticky='WE')

        self.date_nav = UIDateNavigator(self, self)
        self.date_nav.grid(row=1, column=0, columnspan=4, sticky='WE')

        self.diary_info = UIDiaryInfo(self, self.INFOS)
        self.diary_info.grid(row=self.PANE_ROW+1, column=1)

        self.related_diary = RelatedDiary(self)
        self.related_diary.grid(row=self.PANE_ROW, column=3, rowspan=3)

        self.diary_panes = []
        for i in range(8):
            self.diary_panes.append(UIDiaryPane(self,
                self.titles[i], self.colors[i], self))
            self.diary_panes[i].grid(row=self.POSITIONS[i][0],
                column=self.POSITIONS[i][1])

    def display_diary_today(self):
        self.display_diary_by_date(date.today())

    def display_diary_by_date(self, ddate):
        diary = self.db.get_diary_by_date(ddate, self.DIARY_FIELDS)
        if diary:
            self.display_diary(diary)
        else:
            for i in range(len(self.diary_panes)):
                self.diary_panes[i].clear_text()
                self.diary_panes[i].set_title(self.titles[i])
                self.diary_info.clear_infos()

    def display_diary(self, diary):
        self.display_panes(diary)
        self.diary_info.display_infos(diary)

    def display_panes(self, diary):
        prefix = 'P'
        surfix_s = 'SETTING'
        surfix_c = 'CONTENT'
        for i in range(8):
            index = i + 1
            key_s = prefix + str(index) + surfix_s
            key_c = prefix + str(index) + surfix_c
            self.diary_panes[i].set_title(diary[key_s])
            self.diary_panes[i].set_text(diary[key_c][:-1]) # Remove the tailing '\n'

    def display_first_diary_by_keyword(self, keyword):
        diaries = self.db.get_diary_by_keyword(keyword, self.DIARY_FIELDS)
        if diaries:
            for diary in diaries:
                if diary:
                    ddate = self.get_date_from_diary(diaries[0])
                    self.date_nav.set_date(ddate)
                    self.display_diary(diaries[0])
                    break
        else:
            pass # TODO: 未找到相关日记，弹出提示
                
    def get_date_from_diary(self, diary):
        year = diary['YEAR']
        month = diary['MONTH']
        day = diary['DAY']
        return date(year, month, day)

    def display_next_diary_by_keyword(self, keyword):
        # TODO
        print('next')

    def get_related_diary(self, title):
        print('Diary:', self.date_nav.get_date_input(), 'Title:', title)

    def get_diary_input(self):
        ddate = self.date_nav.get_date_input()
        diary = {'YEAR': ddate.year, 'MONTH': ddate.month, 'DAY': ddate.day}

        prefix = 'P'
        surfix_s = 'SETTING'
        surfix_c = 'CONTENT'
        for i in range(8):
            index = i + 1
            key_s = prefix + str(index) + surfix_s
            key_c = prefix + str(index) + surfix_c
            diary[key_s] = self.diary_panes[i].get_title()
            diary[key_c] = self.diary_panes[i].get_text()

        diary.update(self.diary_info.get_info_input())

        return diary

    def save_diary(self, event):
        diary = self.get_diary_input()
        self.db.save_diary(diary, self.DIARY_FIELDS)

class UIDiaryMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief=tk.RAISED, bd=1)
        self.pack(fill=tk.X)

        self.FILE = '文件(F)'
        self.SAVE = '保存(S)    Ctrl + S'
        self.DELETE = '删除(D)'
        self.BACKUPDB = '备份数据文件(B)'
        self.EXIT = '退出(X)    Alt + F4'

        self.GOTO = '转到(G)'
        self.NEXT_10YEARS = '下十年'
        self.PREV_10YEARS = '上十年'
        self.NEXT_YEAR = '下一年    Ctrl + PgDown'
        self.PREV_YEAR = '上一年    Ctrl + PgUp'
        self.NEXT_MONTH = '下个月'
        self.PREV_MONTH = '上个月'
        self.NEXT_WEEK = '下星期'
        self.PREV_WEEK = '上星期'
        self.NEXT_DAY = '后一天    PgDown'
        self.PREV_DAY = '前一天    PgUp'

        self.TOOL = '工具(T)'
        self.OPTION = '选项(O)'

        self.HELP = '帮助(H)'
        self.HELP_F1 = '帮助    F1'
        self.ABOUT = '关于(A)'

        self.create_menus()

    def create_menus(self):
        self.btn_file = tk.Menubutton(self, text=self.FILE, underline=3)
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

        self.btn_goto = tk.Menubutton(self, text=self.GOTO, underline=3)
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

        self.btn_tool = tk.Menubutton(self, text=self.TOOL, underline=3)
        self.btn_tool.pack(side=tk.LEFT)
        self.btn_tool.menu = tk.Menu(self.btn_tool)
        self.btn_tool.configure(menu=self.btn_tool.menu)
        self.btn_tool.menu.add_command(label=self.OPTION,
            command=self.todo_method, underline=3)

        self.btn_help = tk.Menubutton(self, text=self.HELP,underline=3)
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


class UIDateNavigator(tk.Frame):

    def __init__(self, parent, ui):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.ui = ui

        self.DATE = '  日期'
        self.YEAR = '年'
        self.MONTH = '月'
        self.DAY = '日'
        self.GOTO = '转到'
        self.TODAY = '今天'
        self.PREV_DAY = '前一天'
        self.NEXT_DAY = '后一天'

        self.KEYWORD = '     关键字'
        self.SEARCH_DEFAULT = '搜索整篇日记内容'
        self.SEARCH = '搜索'
        self.NEXT = '下一篇'

        self.date = date.today()
        self.year_var = tk.IntVar()
        self.year_var.set(self.date.year)
        self.month_var = tk.IntVar()
        self.month_var.set(self.date.month)
        self.day_var = tk.IntVar()
        self.day_var.set(self.date.day)
        self.search_var = tk.StringVar()
        self.search_var.set(self.SEARCH_DEFAULT)

        self.create_widgets()

    def create_widgets(self):

        tk.Label(self, text=self.DATE).grid(row=0, column=0, sticky='E')

        tk.Entry(self, textvariable=self.year_var, width=4).grid(
            row=0, column=1)
        tk.Label(self, text=self.YEAR).grid(row=0, column=2, sticky='E')

        tk.Entry(self, textvariable=self.month_var, width=2).grid(
            row=0, column=3)
        tk.Label(self, text=self.MONTH).grid(row=0, column=4, sticky='E')

        tk.Entry(self, textvariable=self.day_var, width=2).grid(
            row=0, column=5)
        tk.Label(self, text=self.DAY).grid(row=0, column=6, sticky='E')

        tk.Button(self, text=self.GOTO, command=self.goto_date_input).grid(
            row=0, column=7)
        tk.Button(self, text=self.TODAY, command=self.goto_today).grid(
            row=0, column=8)
        tk.Button(self, text=self.PREV_DAY, command=self.goto_date_prev).grid(
            row=0, column=9)
        tk.Button(self, text=self.NEXT_DAY, command=self.goto_date_next).grid(
            row=0, column=10)

        tk.Label(self, text=self.KEYWORD).grid(row=0, column=11, sticky='E')
        tk.Entry(self, textvariable=self.search_var).grid(row=0, column=12)

        tk.Button(self, text=self.SEARCH, command=self.search_input_first).grid(
            row=0, column=13)
        tk.Button(self, text=self.NEXT, command=self.search_input_next).grid(
            row=0, column=14)

    def set_date(self, ddate):
        self.year_var.set(ddate.year)
        self.month_var.set(ddate.month)
        self.day_var.set(ddate.day)

    def goto_today(self):
        self.goto_date(date.today())

    def goto_date(self, ddate):
        self.set_date(ddate)
        self.ui.display_diary_by_date(ddate)

    def get_date_input(self):
        year = self.year_var.get()
        month = self.month_var.get()
        day = self.day_var.get()
        return date(year, month, day)

    def goto_date_input(self):
        self.ui.display_diary_by_date(self.get_date_input())

    def goto_date_prev(self):
        ddate = self.get_date_input() - timedelta(days=1)
        self.goto_date(ddate)

    def goto_date_next(self):
        ddate = self.get_date_input() + timedelta(days=1)
        self.goto_date(ddate)

    def get_search_input(self):
        return self.search_var.get()
        
    def search_input_first(self):
        keyword = self.get_search_input()
        self.ui.display_first_diary_by_keyword(keyword)

    def search_input_next(self):
        pass


class UIDiaryPane(tk.Frame):

    def __init__(self, parent, title, bg_color, ui):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.title = title
        self.bg_color = bg_color
        self.ui = ui

        self.title_var = tk.StringVar()
        self.title_var.set(self.title)
        self.lbl_title = tk.Label(self, textvariable=self.title_var,
            bg=self.bg_color)
        self.lbl_title.grid(row=0, column=0, sticky='EW')

        self.txt_cell = tk.Text(self, height=12, width=35, bg=self.bg_color)
        self.txt_cell.grid(row=1, column=0, sticky='EWSN')
        self.txt_cell.bind("<FocusIn>", self.focus_in)

    def get_title(self):
        return self.title_var.get()

    def set_title(self, str_title):
        self.title_var.set(str_title)

    def get_text(self):
        return self.txt_cell.get(0.0, tk.END)

    def set_text(self, str_text):
        self.clear_text()
        self.insert_text(str_text)

    def clear_text(self):
        self.txt_cell.delete(0.0, tk.END)

    def insert_text(self, str_text):
        self.txt_cell.insert(tk.END, str_text)

    def change_color(self):
        self.bg_color = tkcolorchooser.askcolor(self.bg_color)[-1]
        self.lbl_title.configure(bg=self.bg_color)
        self.txt_cell.configure(bg=self.bg_color)

    def focus_in(self, event):
        # TODO: 自动查出往年的历史日记 related_list
        pass
        #~ self.ui.get_related_diary(self.get_title())


class UIDiaryInfo(tk.Frame):

    def __init__(self, parent, infos):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.INFOS = infos
        self.LABELS = ['天气', '温度', '湿度',
            '睡觉时间', '起床时间',
            '节日', '纪念日', '邂逅日', '诞生日']
        self.INFO_LABELS = {}
        if len(self.INFOS) == len(self.LABELS):
            for i in range(len(self.INFOS)):
                self.INFO_LABELS[self.INFOS[i]] = self.LABELS[i]
        else:
            raise Exception('Diary Infos not equals to Labels')

        self.info_vars = {}
        for key in self.INFO_LABELS.keys():
            self.info_vars[key] = tk.StringVar()
            self.info_vars[key].set('')

        for i in range(len(self.INFOS)):
            if self.LABELS[i] in ('温度', '湿度'):
                width = 5
                columnspan = 1
                justify = 'right'
            elif self.LABELS[i] in ('睡觉时间', '起床时间'):
                width = 5
                columnspan = 3
                justify = 'right'
            else:
                width = 20
                columnspan = 3
                justify = 'left'
            self.create_line(i, self.LABELS[i],
                self.info_vars[self.INFOS[i]], width, columnspan, justify)

        tk.Label(self, text='℃').grid(row=1, column=2, sticky='W')
        tk.Label(self, text='%').grid(row=2, column=2, sticky='W')
        tk.Label(self, text='\t\t').grid(row=1, column=3)

    def create_line(self, row, label, text_var, width, columnspan, justify):
        tk.Label(self, text=label).grid(row=row, column=0, sticky='E')
        tk.Entry(self, textvariable=text_var, width=width,
            justify=justify).grid(
            row=row, column=1, columnspan=columnspan, sticky='W')

    def get_info_input(self):
        infos = {}
        for key in self.info_vars.keys():
            infos[key] = self.info_vars[key].get()
        return infos

    def display_infos(self, dict_infos):
        for key, value in dict_infos.items():
            if key in self.INFOS:
                self.info_vars[key].set(value)

    def clear_infos(self):
        for key in self.INFO_LABELS.keys():
            self.info_vars[key].set('')


class RelatedDiary(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack()

        self.ANNUAL_DAY = '历年今日'

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=self.ANNUAL_DAY).grid(row=0, column=0)



class DBSQLite:

    def __init__(self, db_name='.pyMorningDiary.db'):
        self.db_name = db_name
        self.db_path = os.path.join(os.path.expanduser('~'), self.db_name)

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

    def __del__(self):
        self.con.close()

    def init_db(self):
        self.cur.execute("""
            CREATE TABLE PANESETTING (
                ID              INTEGER PRIMARY KEY AUTOINCREMENT,
                PINDEX          INTEGER,
                COLOR           TEXT,
                TITLE           TEXT,
                ISACTIVE        INTEGER
            );
            """)
        self.cur.execute("""
            CREATE TABLE DIARY (
                ID              INTEGER PRIMARY KEY AUTOINCREMENT,
                YEAR            INTEGER,
                MONTH           INTEGER,
                DAY             INTEGER,
                P1SETTING       INTEGER,
                P1CONTENT       TEXT,
                P2SETTING       INTEGER,
                P2CONTENT       TEXT,
                P3SETTING       INTEGER,
                P3CONTENT       TEXT,
                P4SETTING       INTEGER,
                P4CONTENT       TEXT,
                P5SETTING       INTEGER,
                P5CONTENT       TEXT,
                P6SETTING       INTEGER,
                P6CONTENT       TEXT,
                P7SETTING       INTEGER,
                P7CONTENT       TEXT,
                P8SETTING       INTEGER,
                P8CONTENT       TEXT,
                WEATHER         TEXT,
                TEMPERATURE     REAL,
                HUMIDITY        REAL,
                SLEEP_TIME      TEXT,
                GET_UP_TIME     TEXT,
                FESTIVAL        TEXT,
                COMMEMORATION   TEXT,
                MEET_WITH       TEXT,
                BIRTHDAY_OF     TEXT,
                ISACTIVE        INTEGER
            );
            """)
        self.cur.executemany("""
            INSERT INTO PANESETTING (PINDEX, TITLE, COLOR, ISACTIVE)
            VALUES (?, ?, ?, ?)
            """, [('0', '人际关系 家庭 朋友', '#e4fd82', 1),
            ('1', '未来日记 明日摘要', '#affeff', 1),
            ('2', '愿望 人生梦想', '#fefebb', 1),
            ('3', '健康 饮食 锻炼', '#d9fefe', 1),
            ('4', '情报 信息 阅读', '#52c8ff', 1),
            ('5', '理财 金钱', '#fd97b4', 1),
            ('6', '工作 创意 兴趣', '#6bf6a6', 1),
            ('7', '快乐 惊喜 其他', '#d287f9', 1)])
        self.con.commit()

    def update_pane_setting(self, pane_index, **setting):
        for key, value in setting:
            if key in ('COLOR', 'TITLE', 'ISACTIVE'):
                self.cur.execute("""
                    UPDATE PANESETTING SET ?=?
                    WHERE PINDEX=?;
                    """, (key, value, pane_index))
        self.con.commit()

    def get_pane_colors(self):
        self.cur.execute("""
            SELECT COLOR
            FROM PANESETTING
            WHERE ISACTIVE='1'
            ORDER BY PINDEX;
            """)
        results = self.cur.fetchall()
        colors = []
        for result in results:
            colors.append(result[0])
        return colors

    def get_pane_titles(self):
        self.cur.execute("""
            SELECT TITLE
            FROM PANESETTING
            WHERE ISACTIVE='1'
            ORDER BY PINDEX;
            """)
        results = self.cur.fetchall()
        titles = []
        for result in results:
            titles.append(result[0])
        return titles

    def get_pane_setting(self, id):
        self.cur.execute("""
            SELECT PINDEX, TITLE, COLOR
            FROM PANESETTING
            WHERE ID=?
            ;
            """, id)
        return self.cur.fetchall()

    def reset_pane_settings(self):
        self.cur.execute("""
            UPDATE PANESETTING
            SET ISACTIVE='0'
            WHERE ISACTIVE='1';
            """)
        self.cur.execute("""
            UPDATE PANESETTING
            SET ISACTIVE='1'
            WHERE ID IN (1, 2, 3, 4, 5, 6, 7, 8);
            """)
        self.con.commit()

    def insert_diary(self, diary, fields):
        diary_value = []
        for i in range(len(fields)):
            diary_value.append(diary[fields[i]])
        self.cur.execute("""
            INSERT INTO DIARY
            (YEAR, MONTH, DAY,
                P1SETTING, P1CONTENT, P2SETTING, P2CONTENT,
                P3SETTING, P3CONTENT, P4SETTING, P4CONTENT,
                P5SETTING, P5CONTENT, P6SETTING, P6CONTENT,
                P7SETTING, P7CONTENT, P8SETTING, P8CONTENT,
                WEATHER, TEMPERATURE, HUMIDITY, SLEEP_TIME, GET_UP_TIME,
                FESTIVAL, COMMEMORATION, MEET_WITH, BIRTHDAY_OF, ISACTIVE)
            VALUES
            (?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, '1');
            """, tuple(diary_value))
        self.con.commit()

    def delete_diary_by_id(self, id):
        self.cur.execute("""
            UPDATE DIARY SET
            ISACTIVE='0'
            WHERE
            ID=?;
            """, id)
        self.con.commit()

    def delete_diary_by_date(self, ddate):
        self.cur.execute("""
            UPDATE DIARY SET
            ISACTIVE='0'
            WHERE YEAR=?
            AND MONTH=?
            AND DAY=?
            AND ISACTIVE='1';
            """, (ddate.year, ddate.month, ddate.day))
        self.con.commit()

    def save_diary(self, diary, fields):
        ddate = date(diary['YEAR'], diary['MONTH'], diary['DAY'])
        if self.get_diary_id_by_date(ddate):
            self.delete_diary_by_date(ddate)
        self.insert_diary(diary, fields)

    def update_diary(self, diary, fields):
        ddate = date(diary['YEAR'], diary['MONTH'], diary['DAY'])
        self.delete_diary_by_date(ddate)
        self.insert_diary(diary, fields)

    def get_diary_id_by_date(self, ddate):
        self.cur.execute("""
            SELECT ID
            FROM DIARY
            WHERE YEAR=?
            AND MONTH=?
            AND DAY=?
            AND ISACTIVE='1';
            """, (ddate.year, ddate.month, ddate.day))
        return self.cur.fetchone()  # TODO：美化返回的结果

    def get_diary_by_date(self, ddate, fields):
        self.cur.execute("""
            SELECT YEAR, MONTH, DAY,
                P1SETTING, P1CONTENT, P2SETTING, P2CONTENT,
                P3SETTING, P3CONTENT, P4SETTING, P4CONTENT,
                P5SETTING, P5CONTENT, P6SETTING, P6CONTENT,
                P7SETTING, P7CONTENT, P8SETTING, P8CONTENT,
                WEATHER, TEMPERATURE, HUMIDITY, SLEEP_TIME, GET_UP_TIME,
                FESTIVAL, COMMEMORATION, MEET_WITH, BIRTHDAY_OF
            FROM DIARY
            WHERE YEAR=?
            AND MONTH=?
            AND DAY=?
            AND ISACTIVE='1'
            ORDER BY MONTH, DAY;
            """, (ddate.year, ddate.month, ddate.day))
        result = self.cur.fetchone()
        if result:
            results = {}
            for i in range(len(result)):
                results[fields[i]] = result[i]
            return results
        else:
            return None

    def get_diary_by_keyword(self, keyword, fields):
        self.cur.execute("""
            SELECT YEAR, MONTH, DAY,
                P1SETTING, P1CONTENT, P2SETTING, P2CONTENT,
                P3SETTING, P3CONTENT, P4SETTING, P4CONTENT,
                P5SETTING, P5CONTENT, P6SETTING, P6CONTENT,
                P7SETTING, P7CONTENT, P8SETTING, P8CONTENT,
                WEATHER, TEMPERATURE, HUMIDITY, SLEEP_TIME, GET_UP_TIME,
                FESTIVAL, COMMEMORATION, MEET_WITH, BIRTHDAY_OF
            FROM DIARY
            WHERE P1CONTENT LIKE ?
            OR P2CONTENT LIKE ?
            OR P3CONTENT LIKE ?
            OR P4CONTENT LIKE ?
            OR P5CONTENT LIKE ?
            OR P6CONTENT LIKE ?
            OR P7CONTENT LIKE ?
            OR P8CONTENT LIKE ?
            OR FESTIVAL LIKE ?
            OR COMMEMORATION LIKE ?
            OR MEET_WITH LIKE ?
            OR BIRTHDAY_OF LIKE ?
            ORDER BY YEAR, MONTH, DAY;
            """, ('%' + keyword + '%', '%' + keyword + '%',
            '%' + keyword + '%', '%' + keyword + '%',
            '%' + keyword + '%', '%' + keyword + '%',
            '%' + keyword + '%', '%' + keyword + '%',
            '%' + keyword + '%', '%' + keyword + '%',
            '%' + keyword + '%', '%' + keyword + '%'))
        db_results = self.cur.fetchall()
        if db_results:
            dict_results = []
            for result in db_results:
                dict_result = {}
                for i in range(len(result)):
                    dict_result[fields[i]] = result[i]
                dict_results.append(dict_result)
            return dict_results
        else:
            return None

    def get_related_diary(self, date):
        self.cur.execute("""
            SELECT *
            FROM DIARY
            WHERE MONTH=?
            AND DAY=?;
            """, (date.month, date.day))
        return self.cur.fetchall()  # TODO：美化返回的结果


def main():
    app = tk.Tk()
    app.title('晨间日记 - pyMorningDiary')
    db = DBSQLite()
    diary = UIDiary(app, db)
    app.mainloop()
    del(db)

if __name__ == '__main__':
    main()
