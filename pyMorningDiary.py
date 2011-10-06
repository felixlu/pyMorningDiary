#!/usr/bin/env python3

from tkinter import Tk, Frame, StringVar, Label, Text, Entry, LEFT, YES, \
    BOTH, END, Button, colorchooser

from dlgCalendar import tkCalendar


class Diary(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack(side=LEFT, expand=YES, fill=BOTH)
        self.grid(row=0, column=0)

        self.TITLE_1x1 = '人生梦想'
        self.TITLE_1x2 = '工作'
        self.TITLE_1x3 = '家庭'
        self.TITLE_2x1 = '金钱'
        self.TITLE_2x3 = '健康'
        self.TITLE_3x1 = '兴趣'
        self.TITLE_3x2 = '人际关系'
        self.TITLE_3x3 = '娱乐及其他'

        self.create_widgets()

    def create_widgets(self):
        DateNavigator(self.frame).grid(row=0, column=0, columnspan=3)
        self.dc1 = DiaryCell(self.frame, self.TITLE_1x1, 'blue')
        self.dc1.grid(row=1, column=0)
        DiaryCell(self.frame, self.TITLE_1x2, 'green').grid(row=1, column=1)
        DiaryCell(self.frame, self.TITLE_1x3, 'red').grid(row=1, column=2)
        DiaryCell(self.frame, self.TITLE_2x1, 'yellow').grid(row=2, column=0)
        DiaryMeta(self.frame).grid(row=2, column=1)
        DiaryCell(self.frame, self.TITLE_2x3, 'blue').grid(row=2, column=2)
        DiaryCell(self.frame, self.TITLE_3x1, 'green').grid(row=3, column=0)
        DiaryCell(self.frame, self.TITLE_3x2, 'red').grid(row=3, column=1)
        DiaryCell(self.frame, self.TITLE_3x3, 'yellow').grid(row=3, column=2)

    def say_hello(self):
        self.dc1.set_text('Hello')

    def say_hello_chs(self):
        self.dc1.set_text('你好')

    def prt(self):
        print(self.dc1.get_text())


class DiaryCell(Frame):

    def __init__(self, parent, title, bg_color):
        Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack(side=LEFT, expand=YES, fill=BOTH)
        self.title = title
        self.bg_color = bg_color

        self.TITLE_var = StringVar()
        self.TITLE_var.set(self.title)
        self.lbl_title = Label(self.frame, textvariable=self.TITLE_var,
            bg=self.bg_color)
        self.lbl_title.grid(row=0, column=0, sticky='EW')

        #self.btn_color = Button(self.frame, text='Change Color',
        #    command=self.change_color)
        #self.btn_color.grid(row=0, column=1)

        self.txt_cell = Text(self.frame, height=12, width=35,
            bg=self.bg_color)
        self.txt_cell.grid(row=1, column=0, sticky='EWSN')
        self.txt_cell.bind("<FocusIn>", self.focus_in)
        self.txt_cell.bind("<FocusOut>", self.focus_out)

    def get_title(self):
        return self.TITLE_var.get()

    def set_title(self, str_title):
        self.TITLE_var.set(str_title)

    def get_text(self):
        return self.txt_cell.get(0.0, END)

    def set_text(self, str_text):
        self.txt_cell.delete(0.0, END)
        self.txt_cell.insert(END, str_text)

    def change_color(self):
        self.bg_color = colorchooser.askcolor(self.bg_color)[-1]
        self.lbl_title.configure(bg=self.bg_color)
        self.txt_cell.configure(bg=self.bg_color)

    def focus_in(self, event):
        # 自动查出往年的历史日记
        pass

    def focus_out(self, event):
        # 自动保存
        pass


class DiaryMeta(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack(side=LEFT, expand=YES, fill=BOTH)

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
        Label(self.frame, text=self.WEATHER).grid(row=0, column=0, sticky='E')
        self.weather_var = StringVar()
        self.weather_var.set('')
        Entry(self.frame, textvariable=self.weather_var).grid(row=0, column=1)

        Label(self.frame, text=self.TEMPERATURE).grid(
            row=1, column=0, sticky='E')
        self.temp_var = StringVar()
        self.temp_var.set('')
        Entry(self.frame, textvariable=self.temp_var).grid(row=1, column=1)

        Label(self.frame, text=self.HUMIDITY).grid(row=2, column=0, sticky='E')
        self.humidity_var = StringVar()
        self.humidity_var.set('')
        Entry(self.frame, textvariable=self.humidity_var).grid(row=2, column=1)

        Label(self.frame, text=self.FESTIVAL).grid(row=3, column=0, sticky='E')
        self.festival_var = StringVar()
        self.festival_var.set('')
        Entry(self.frame, textvariable=self.festival_var).grid(row=3, column=1)

        Label(self.frame, text=self.COMMOMERATION).grid(
            row=4, column=0, sticky='E')
        self.commomeration_var = StringVar()
        self.commomeration_var.set('')
        Entry(self.frame, textvariable=self.commomeration_var).grid(
            row=4, column=1)

        Label(self.frame, text=self.MEET).grid(row=5, column=0, sticky='E')
        self.meet_var = StringVar()
        self.meet_var.set('')
        Entry(self.frame, textvariable=self.meet_var).grid(row=5, column=1)

        Label(self.frame, text=self.BIRTHDAY).grid(row=6, column=0, sticky='E')
        self.birthday_var = StringVar()
        self.birthday_var.set('')
        Entry(self.frame, textvariable=self.birthday_var).grid(row=6, column=1)

        Label(self.frame, text=self.SLEEP).grid(row=7, column=0, sticky='E')
        self.sleep_var = StringVar()
        self.sleep_var.set('')
        Entry(self.frame, textvariable=self.sleep_var).grid(row=7, column=1)

        Label(self.frame, text=self.GETUP).grid(row=8, column=0, sticky='E')
        self.getup_var = StringVar()
        self.getup_var.set('')
        Entry(self.frame, textvariable=self.getup_var).grid(row=8, column=1)


class DateNavigator(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack(side=LEFT, expand=YES, fill=BOTH)

        self.PREV_YEAR = '去年'
        self.PREV_MONTH = '上个月'
        self.PREV_WEEK = '上星期'
        self.PREV_DAY = '昨天'
        self.NEXT_YEAR = '明年'
        self.NEXT_MONTH = '下个月'
        self.NEXT_WEEK = '下星期'
        self.NEXT_DAY = '明天'
        self.TODAY = '今天'

        self.create_widgets()

    def create_widgets(self):

        Button(self.frame, text=self.TODAY, command=self.goto_today).grid(
            row=0, column=4)

        Button(self.frame, text=self.PREV_YEAR,
            command=self.goto_prev_year).grid(row=1, column=0)
        Button(self.frame, text=self.PREV_MONTH,
            command=self.goto_prev_month).grid(row=1, column=1)
        Button(self.frame, text=self.PREV_WEEK,
            command=self.goto_prev_week).grid(row=1, column=2)
        Button(self.frame, text=self.PREV_DAY,
            command=self.goto_prev_day).grid(row=1, column=3)

        self.date_var = StringVar()
        Entry(self.frame, textvariable=self.date_var, width=10).grid(
            row=1, column=4)

        Button(self.frame, text=self.NEXT_DAY,
            command=self.goto_next_day).grid(row=1, column=5)
        Button(self.frame, text=self.NEXT_WEEK,
            command=self.goto_next_week).grid(row=1, column=6)
        Button(self.frame, text=self.NEXT_MONTH,
            command=self.goto_next_month).grid(row=1, column=7)
        Button(self.frame, text=self.NEXT_YEAR,
            command=self.goto_next_year).grid(row=1, column=8)

    def goto_today(self):
        pass

    def goto_prev_year(self):
        pass

    def goto_prev_month(self):
        pass

    def goto_prev_week(self):
        pass

    def goto_prev_day(self):
        pass

    def goto_next_year(self):
        pass

    def goto_next_month(self):
        pass

    def goto_next_week(self):
        pass

    def goto_next_day(self):
        pass


if __name__ == '__main__':
    app = Tk()
    app.title('晨间日记 - pyMorningDiary')
    diary = Diary(app)
    app.mainloop()
