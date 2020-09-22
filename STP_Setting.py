# -*- coding: UTF-8 -*-
import paramiko
from tkinter import *
import tkinter.messagebox
import time
import base64, os
from icon import img


top = Tk()
top.title('STP设置 - 拓达电子有限公司')
top.geometry('350x140')
top.resizable(0,0)

tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
top.iconbitmap("tmp.ico")
os.remove("tmp.ico")

L1 = Label(top, text="IP地址")
L1.place(x=10,y=10)
E1 = Entry(top, bd =5, width =20)
E1.place(x=130,y=10)
L2 = Label(top, text="密码")
L2.place(x=10,y=50)
E2 = Entry(top, show = '*',bd =5, width =20)
E2.place(x=130,y=50)
L3 = Label(top, text="版本: 2020/09/07/V1.01")
L3.place(x=10,y=90)


def check():
    if len(E1.get())  == 0 or len(E2.get()) == 0:
        tkinter.messagebox.showerror("错误", message="IP地址或密码不能为空")
        return


def submit():
    if len(E1.get()) == 0 or len(E2.get()) == 0:
        tkinter.messagebox.showerror("错误", message="IP地址或密码不能为空")
        return
    IP = E1.get()
    pwd = E2.get()
    # 设置命令
    cmd = "brctl show | grep yes | awk '{print $3}'"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=IP, port=22, username="root", password=pwd)
    stdin, stdout, stderr = client.exec_command(cmd)
    # 输出结果
    #print(stdout.read().decode('utf-8'))
    result = str(stdout.read() , encoding = "utf-8")
    # 如果STP enable = no， 则执行所需代码
    if "yes" in result:
        pass
    else:
        stdin, stdout, stderr = client.exec_command(
            "uci set network.lan.stp=1 && uci commit && /etc/init.d/network restart")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command(cmd)
    result = str(stdout.read() , encoding = "utf-8")
    if "yes" in result:
        tkinter.messagebox.showinfo("提示",message="STP设置成功")
    else:
        tkinter.messagebox.showerror("错误",message="设置失败")
    client.close()


def cancel():
    if len(E1.get()) == 0 or len(E2.get()) == 0:
        tkinter.messagebox.showerror("错误", message="IP地址或密码不能为空")
        return
    hostname = E1.get()
    pwd = E2.get()
    # 设置命令
    cmd = "brctl show | grep yes | awk '{print $3}'"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username="root", password=pwd)
    stdin, stdout, stderr = client.exec_command(cmd)
    # 输出结果
    print(stdout.read().decode('utf-8') + "te")
    result = str(stdout.read() , encoding = "utf-8")
    # 如果STP enable = yes， 则执行所需代码
    if "yes" in result:
        stdin, stdout, stderr = client.exec_command("uci set network.lan.stp=0 && uci commit && /etc/init.d/network restart")
    cmd = "brctl show | grep no | awk '{print $3}'"
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command(cmd)
    result = str(stdout.read() , encoding = "utf-8")
    if "no" in result:
        tkinter.messagebox.showinfo("提示", message="STP取消成功")
    else:
        tkinter.messagebox.showerror("错误", message="设置失败")
    client.close()


def query():
    if len(E1.get()) == 0 or len(E2.get()) == 0:
        tkinter.messagebox.showerror("错误", message="IP地址或密码不能为空")
        return
    IP = E1.get()
    pwd = E2.get()
    # 设置命令
    cmd = "brctl show | grep yes | awk '{print $3}'"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=IP, port=22, username="root", password=pwd)
    stdin, stdout, stderr = client.exec_command(cmd)
    result = str(stdout.read() , encoding = "utf-8")
    if "yes" in result:
        tkinter.messagebox.showinfo("提示", message="STP已设置")
    else:
        tkinter.messagebox.showinfo("提示", message="STP未设置")

def reboot():
    if len(E1.get()) == 0 or len(E2.get()) == 0:
        tkinter.messagebox.showerror("错误", message="IP地址或密码不能为空")
        return
    hostname = E1.get()
    pwd = E2.get()
    # 设置命令
    cmd = "firstboot -y && reboot"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username="root", password=pwd)
    stdin, stdout, stderr = client.exec_command(cmd)
    # 输出结果
    tkinter.messagebox.showinfo("提示", message="复位完成")
    client.close()


framet = Frame(top)
framet.pack(side='bottom')
frame1 = Frame(framet)
frame1.pack(side='left')
frame2 = Frame(framet)
frame2.pack(side='right',padx = 50)
b1 = Button(frame1,text="查询", command = query)
b1.pack(side='left')
b = Button(frame1,text="设置STP", command = submit).pack(side='left')
b2 = Button(frame1,text="取消STP", command = cancel)
b2.pack(side='left')
b3= Button(frame2,text="复位", command = reboot)
b3.pack(side ='right')
top.mainloop()
