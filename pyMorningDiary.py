#!/usr/bin/env python3

import tkinter as tk
import tkinter.colorchooser as tkcolorchooser
import dlgCalendar


class Diary(tk.Frame):

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

        self.create_widgets()

    def create_widgets(self):

        DateNavigator(self.frame).grid(row=0, column=0, columnspan=3)
        self.dc1 = DiaryCell(self.frame, self.TITLES[0], self.COLORS[0])
        self.dc1.grid(row=1, column=0)
        DiaryCell(self.frame, self.TITLES[1], self.COLORS[1]).grid(
            row=1, column=1)
        DiaryCell(self.frame, self.TITLES[2], self.COLORS[2]).grid(
            row=1, column=2)
        DiaryCell(self.frame, self.TITLES[3], self.COLORS[3]).grid(
            row=2, column=0)
        DiaryInfo(self.frame).grid(row=2, column=1)
        DiaryCell(self.frame, self.TITLES[4], self.COLORS[4]).grid(
            row=2, column=2)
        DiaryCell(self.frame, self.TITLES[5], self.COLORS[5]).grid(
            row=3, column=0)
        DiaryCell(self.frame, self.TITLES[6], self.COLORS[6]).grid(
            row=3, column=1)
        DiaryCell(self.frame, self.TITLES[7], self.COLORS[7]).grid(
            row=3, column=2)


class DiaryCell(tk.Frame):

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


class DiaryInfo(tk.Frame):

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


class DateNavigator(tk.Frame):

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
        # TODO: 弹出日期选择框，选定日期后刷新显示日记，及该日期的周年纪念信息
        dlgCalendar.tkCalendar(self.frame, 2011, 10, 6, self.date_var)

    def search(self):
        pass

    def search_next(self):
        pass


if __name__ == '__main__':
    app = tk.Tk()
    app.title('晨间日记 - pyMorningDiary')
    diary = Diary(app)
    app.mainloop()
