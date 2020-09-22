# -*- coding: utf-8 -*-
import os
import tkinter as tk  # 装载tkinter模块,用于Python3
from tkinter import ttk  # 装载tkinter.ttk模块,用于Python3
import paramiko
from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
from MultiPing import *
from IPy import IP
import base64, os
from icon import img

root = tk.Tk()  # 创建窗口对象
root.title(string='Project')  # 设置窗口标题
root.geometry('900x250+200+200')
root.resizable(0, 1)
tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()
root.iconbitmap("tmp.ico")
os.remove("tmp.ico")

tabControl = ttk.Notebook(root)  # 创建Notebook
tab1 = tk.Frame(tabControl)  # 增加新选项卡
tabControl.add(tab1, text='单IP模式')  # 把新选项卡增加到Notebook
tab2 = tk.Frame(tabControl)
tabControl.add(tab2, text='批量模式')

# tab1
top = Frame(tab1)
top.pack(expand=1, fill=BOTH)
L1 = Label(top, text="IP")
L1.place(x=10, y=10)
E1 = Entry(top, bd=5, width=20)
E1.place(x=130, y=10)
L2 = Label(top, text="密码")
L2.place(x=10, y=50)
E2 = Entry(top, show='*', bd=5, width=20)
E2.place(x=130, y=50)
L4 = Label(top, text="命令")
L4.place(x=10, y=90)
E4 = Entry(top, bd=5, width=20)
E4.place(x=130, y=90)
t = Text(top, height=11)
t.place(x=300, y=10)
scroll = Scrollbar()
scroll.pack(side=RIGHT, fill=Y)
scroll.config(command=t.yview)
t.config(yscrollcommand=scroll.set)


def submit():
    if len(E1.get()) == 0 or len(E2.get()) == 0:
        tkinter.messagebox.showerror("错误", message="IP地址或密码不能为空")
        return
    hostname = E1.get()
    pwd = E2.get()
    cmd = E4.get()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username="root", password=pwd)
    stdin, stdout, stderr = client.exec_command(cmd)
    # 输出结果
    print(stdout.read().decode('utf-8'))
    result = stdout.read().decode('utf-8')
    t.insert('insert', result)
    client.close()


b = Button(top, text="执行", command=submit)
b.pack(side='bottom')




# tab2
window = Frame(tab2)
window.pack(expand=YES, fill="both")
leftFrame = Frame(window)
leftFrame.pack(side='left')
frame1 = Frame(leftFrame)
frame1.pack()
frame2 = Frame(leftFrame)
frame2.pack()
frame3 = Frame(leftFrame)
frame3.pack()
frame4 = Frame(leftFrame)
frame4.pack(fill=BOTH, expand=YES)
frame5 = Frame(leftFrame)
frame5.pack()
# Frame1：网段 添加按钮
l1 = Label(frame1, text="网段")
l1.pack(side='left')
e1 = Entry(frame1, width=26, bd=5)
e1.pack(side='left')

# a list to record the network segments
nslist = []


def addIP():
    # check format of the input
    try:
        IP(e1.get())
    except Exception as e:
        tkinter.messagebox.showwarning(title='Warning', message="ip地址格式不正确")
        return
    list = []
    list.append(e1.get())
    nslist.append(e1.get())
    str = var.get()
    for i in list:
        str = str + ' ' + i
    var.set(str)


add = Button(frame1, text='添加', width=3, height=1, command=addIP)
add.pack(side='right')

# Frame2: added segment and the search button
ip_list = []


# search for network segments
def query():
    if len(nslist) == 0:
        tkinter.messagebox.showwarning(title="Warning", message="未输入网段")
        return
    global ip_list
    ip_list = search(nslist)
    print(ip_list)
    # 检查
    for i in range(1, 1 + len(ip_list)):
        exec("""
try:
    cb%d.destroy()
except:
    pass
try:
    global v%d
    global cb%d
except:
    pass
v%d = BooleanVar()
cb%d = Checkbutton(frame3,text = ip_list[i-1], variable = v%d)
cb%d.pack()
"""%(i,i,i,i,i,i,i))


def clear():
    nslist = []
    var.set('已添加网段: ')


var = StringVar()
var.set('已添加网段: ')
l2 = Label(frame2, textvariable=var)
l2.pack()
b1 = Button(frame2, text="搜索", width=3, height=1, command=query)
b1.pack(side='left')
b2 = Button(frame2,text='清空',width=3,height=1,command = clear)
b2.pack(side='left')
# Frame3: 搜索到的IP列表可打勾 全选按钮 全不选按钮\

# 全选/不选按钮
frame3_1 = Frame(frame3)
frame3_1.pack(side="bottom")


# 全选
def select_all():
    for i in range(1, 1 + len(ip_list)):
        exec("cb%d.select()" % (i))


# 全不选
def select_none():
    for i in range(1, 1 + len(ip_list)):
        exec("cb%d.deselect()" % (i))


b2 = Button(frame3_1, text="全选", width=3, height=1, command=select_all)
b2.pack(side="left")
b3 = Button(frame3_1, text="全部不选", width=6, height=1, command=select_none)
b3.pack(side="right")
# Frame4: 输入密码
l4 = Label(frame4, text='密码')
l4.pack(side='left')
e4 = Entry(frame4, width=26, show='*', bd=5)
e4.pack(side='left')


# Frame5: 输入命令 执行按钮
def execute():
    if len(e4.get()) == 0 or len(e5.get()) == 0:
        tkinter.messagebox.showerror("错误", message="IP地址或密码不能为空")
        return
    pwd = e4.get()
    cmd = e5.get()
    for i in range(1, 1 + len(ip_list)):
        exec("""
if v%d.get() == 1:
    hostname = ip_list[i - 1]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username="root", password=pwd)
    stdin, stdout, stderr = client.exec_command(cmd)
    # 输出结果
    result = stdout.read().decode('utf-8')
    t.insert('end',"results from %s :")
    t.insert(INSERT,"\\r\\n")
    t.insert('end', result)
    client.close()
"""%(i,ip_list[i-1]))


l5 = Label(frame5, text='命令')
l5.pack(side='left')
e5 = Entry(frame5, width=26, bd=5)
e5.pack(side='left')
b5 = Button(frame5, text='执行', command=execute)
b5.pack(side='left')
# 右屏显示执行结果
rightframe = Frame(window)
rightframe.pack(side='right')
t = ScrolledText(rightframe, height=11)
t.pack()
tabControl.pack(expand=1, fill="both")

tabControl.select(tab1)  # 选择tab1

root.mainloop()  # 进入消息循环
