#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, StringVar, Label, Text, Entry, LEFT, YES, \
    BOTH, END, Button


class Diary(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack(side=LEFT, expand=YES, fill=BOTH)
        self.grid(row=0, column=0)
        self.create_widgets()

    def create_widgets(self):
        Button(self.frame, text='say "Hello"', command=self.say_hello).grid(row=0, column=0)
        Button(self.frame, text='say "你好"', command=self.say_hello_chs).grid(row=0, column=1)
        Button(self.frame, text='Print', command=self.prt).grid(row=0, column=2)
        self.dc1 = DiaryCell(self.frame, TITLE_1x1, 'blue')
        self.dc1.grid(row=1, column=0)
        DiaryCell(self.frame, TITLE_1x2, 'green').grid(row=1, column=1)
        DiaryCell(self.frame, TITLE_1x3, 'red').grid(row=1, column=2)
        DiaryCell(self.frame, TITLE_2x1, 'yellow').grid(row=2, column=0)
        DiaryMeta(self.frame).grid(row=2, column=1)
        DiaryCell(self.frame, TITLE_2x3, 'blue').grid(row=2, column=2)
        DiaryCell(self.frame, TITLE_3x1, 'green').grid(row=3, column=0)
        DiaryCell(self.frame, TITLE_3x2, 'red').grid(row=3, column=1)
        DiaryCell(self.frame, TITLE_3x3, 'yellow').grid(row=3, column=2)

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

        self.title_var = StringVar()
        self.title_var.set(self.title)
        self.lbl_title = Label(self.frame, textvariable=self.title_var,
            bd=3, bg=self.bg_color)
        self.lbl_title.grid(row=0, column=0, sticky='EW')
        self.txt_cell = Text(self.frame, height=12, width=35, bd=3,
            bg=self.bg_color)
        self.txt_cell.grid(row=1, column=0, sticky='EW')

    def get_title(self):
        return self.title_var.get()

    def set_title(self, str_title):
        self.title_var.set(str_title)

    def get_text(self):
        return self.txt_cell.get(0.0, END)

    def set_text(self, str_text):
        self.txt_cell.delete(0.0, END)
        self.txt_cell.insert(END, str_text)


class DiaryMeta(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack(side=LEFT, expand=YES, fill=BOTH)

        Label(self.frame, text=WEATHER).grid(row=0, column=0, sticky='E')
        self.weather_var = StringVar()
        self.weather_var.set('')
        Entry(self.frame, textvariable=self.weather_var).grid(row=0, column=1)

        Label(self.frame, text=TEMPERATURE).grid(row=1, column=0, sticky='E')
        self.temp_var = StringVar()
        self.temp_var.set('')
        Entry(self.frame, textvariable=self.temp_var).grid(row=1, column=1)

        Label(self.frame, text=HUMIDITY).grid(row=2, column=0, sticky='E')
        self.humidity_var = StringVar()
        self.humidity_var.set('')
        Entry(self.frame, textvariable=self.humidity_var).grid(row=2, column=1)

        Label(self.frame, text=FESTIVAL).grid(row=3, column=0, sticky='E')
        self.festival_var = StringVar()
        self.festival_var.set('')
        Entry(self.frame, textvariable=self.festival_var).grid(row=3, column=1)

        Label(self.frame, text=COMMOMERATION).grid(row=4, column=0, sticky='E')
        self.commomeration_var = StringVar()
        self.commomeration_var.set('')
        Entry(self.frame, textvariable=self.commomeration_var).grid(
            row=4, column=1)

        Label(self.frame, text=MEET).grid(row=5, column=0, sticky='E')
        self.meet_var = StringVar()
        self.meet_var.set('')
        Entry(self.frame, textvariable=self.meet_var).grid(row=5, column=1)

        Label(self.frame, text=BIRTHDAY).grid(row=6, column=0, sticky='E')
        self.birthday_var = StringVar()
        self.birthday_var.set('')
        Entry(self.frame, textvariable=self.birthday_var).grid(row=6, column=1)

        Label(self.frame, text=SLEEP).grid(row=7, column=0, sticky='E')
        self.sleep_var = StringVar()
        self.sleep_var.set('')
        Entry(self.frame, textvariable=self.sleep_var).grid(row=7, column=1)

        Label(self.frame, text=GETUP).grid(row=8, column=0, sticky='E')
        self.getup_var = StringVar()
        self.getup_var.set('')
        Entry(self.frame, textvariable=self.getup_var).grid(row=8, column=1)


class Calendar(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack(side=LEFT, expand=YES, fill=BOTH)



TITLE_1x1 = '人生梦想'
TITLE_1x2 = '工作、同事'
TITLE_1x3 = '家庭、亲戚'
TITLE_2x1 = '金钱、理财'
TITLE_2x3 = '健康、运动'
TITLE_3x1 = '兴趣、爱好'
TITLE_3x2 = '朋友、同学'
TITLE_3x3 = '娱乐、其他'

WEATHER = '天气'
TEMPERATURE = '温度'
HUMIDITY = '湿度'
FESTIVAL = '节日'
COMMOMERATION = '纪念日'
MEET = '邂逅日'
BIRTHDAY = '诞生日'
SLEEP = '睡觉时间'
GETUP = '起床时间'


if __name__ == '__main__':
    app = Tk()
    app.title('晨间日记 - pyMorningDiary')
    diary = Diary(app)
    app.mainloop()
