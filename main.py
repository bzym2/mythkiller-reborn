import os
import tkinter as tk
import keyboard
import psutil
import ctypes
from tkinter import font
import random
import pyautogui
import winreg
import win32api
import win32con
import win32gui
import ctypes
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
flg1 = 0


root=ttk.Window(themename="simplex")
x, y = 0, 0
root.attributes('-alpha', 0.8)
window_size = '250x350'
randtitle = str(random.randint(10000000,999999999))
root.title(randtitle)
root.attributes("-toolwindow", 2)
root.geometry(f"{window_size}+10+10")
root.resizable(0,0)
windowStatus = 1
boardcastWindow = '屏幕广播'
list_var=['']
list_var.append(f'[{datetime.now()}][Debug Center] Successful get font list {font.families}')
list_var.append(font.families())
keyboardstr = tk.StringVar()
keyboardstr = 'ctrl+b'
list_var.append(f'[{datetime.now()}][Debug Center] Successful get random title {randtitle}')
list_var.append(f'[{datetime.now()}][Debug Center] 程序正在初始化')
# 设置获取PID函数
def getPID(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    return None

# 设置ctypes信息框函数
def message_box(message, title):
    list_var.append(f"[{datetime.now()}][Debug Center] Successful opened messagebox window:[{message}]-[{title}]")
    ctypes.windll.user32.MessageBoxW(0, message, title, 1)

# 获取python的PID
ppid = getPID('python.exe')
# 打印python的PID
list_var.append(f"[{datetime.now()}][Debug Center] Successful get python.exe pid {ppid}")

# 获取网管程序的PID
mpid = getPID('MasterHelper.exe')
# 打印网管程序的PID
list_var.append(f"[{datetime.now()}][Debug Center] Successful get MasterHelper.exe pid {mpid}")

# 获取StudentMain的PID
spid = getPID('StudentMain.exe')
# 未识别到StudentMain进程则退出程序
# if spid == None:
#     message_box('未识别到StudentMain进程','程序已退出')
#     exit(114514)
# 打印StudentMain的PID
list_var.append(f"[{datetime.now()}][Debug Center] Successful get StudentMain.exe pid {spid}")



# 设置置顶函数
def openTopLevel():
    root.wm_attributes('-topmost',1)
    root.after(50, openTopLevel)
openTopLevel()

# 设置杀死学生端函数
def killSM():
    global list_var,spid
    try:
        process = psutil.Process(spid)
        process.kill()
        list_var.append(f"进程 {spid} 已成功杀死")
        # 获取python的PID
        ppid = getPID('python.exe')
        # 打印python的PID
        list_var.append(f"[{datetime.now()}][Debug Center] Successful get python.exe pid {ppid}")
    except psutil.NoSuchProcess:
        list_var.append(f"找不到进程 {spid}")
    except psutil.AccessDenied:
        list_var.append(f"没有权限杀死进程 {spid}")
    spid = getPID('StudentMain.exe')

# 设置杀死网管程序函数
def killWG():
    global list_var
    try:
        # 获取网管程序的PID
        mpid = getPID('MasterHelper.exe')
        # 打印网管程序的PID
        list_var.append(f"[{datetime.now()}][Debug Center] Successful get MasterHelper.exe pid {mpid}")
        process = psutil.Process(mpid)
        process.kill()
        list_var.append(f"进程 {mpid} 已成功杀死")
        os.popen('sc stop tdnetfilter')
        list_var.append('success stopped netfilter')
    except psutil.NoSuchProcess:
        list_var.append(f"找不到进程 {mpid}")
    except psutil.AccessDenied:
        list_var.append(f"没有权限杀死进程 {mpid}")

# 切换窗口的显示状态
def toggleWindow():
    global windowStatus
    if windowStatus == 1:
        windowStatus=0
        root.withdraw()
        root.wm_attributes('-topmost', 0)
    else:
        windowStatus=1
        root.deiconify()
        openTopLevel()

def closeWindow():
    exit()

def fuckUDisk():
    os.system("sc stop TDFileFilter")

def setboard():
    global keyboardstr
    keyboard.remove_hotkey(keyboardstr)
    keyboardstr = kbentry.get()
    keyboard.add_hotkey(keyboardstr, toggleWindow)

def minimizeWindow():
    # 查找窗口
    window = pyautogui.getWindowsWithTitle(boardcastWindow)[0]
    # 最小化窗口
    window.minimize()
def maximizeWindow():
    # 查找窗口
    window = pyautogui.getWindowsWithTitle(boardcastWindow)[0]
    # 最大化窗口
    window.maximize()

def get_mythware_password_from_regedit():
    global list_var
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\TopDomain\\e-Learning Class\\Student", 0,
                             winreg.KEY_QUERY_VALUE | winreg.WOW64_32KEY)
        value = winreg.QueryValueEx(key, "knock1")[0]
        password = ""
        for i in range(0, len(value), 4):
            value[i:i + 4] = [(value[i + j] ^ 0x50 ^ 0x45) for j in range(4)]
        for i in range(0, len(value)):
            password += chr(value[i])
            if i % 8 == 0:
                list_var.append("".join(["%x " % value[i]]))
        return password
    except Exception as e:
        list_var.append(f"An error occurred: {e}")
        return None
def patch():
    message_box("此方法仅适用于新版极域","注意")
    if(get_mythware_password_from_regedit()):
        message_box("极域密码为:" + str(get_mythware_password_from_regedit()), "已破解成功！")
    else:
        message_box("极域密码为：mythware_super_password","已破解成功！")

def refreshConsole():
    global text_widget
    text_widget.delete(1.0, tk.END)  # 清除文本widget中的内容
    for item in list_var:
        text_widget.insert(tk.END, str(item) + '\n')
def console():
    global list_var,text_widget
    window2=tk.Tk()
    window2.title('console')
    window2.wm_attributes('-topmost', 1)
    window2.attributes("-toolwindow", 2)
    refreshbtn = ttk.Button(window2,text='刷新',width=10,command=refreshConsole)
    refreshbtn.pack()
    text_widget = tk.Text(window2)
    text_widget.delete(1.0, tk.END)  # 清除文本widget中的内容
    for item in list_var:
        text_widget.insert(tk.END, str(item) + '\n')
    text_widget.pack()

def lol_lmao():
    message_box("暂未完成（没学过咋Hook）", ":)")

keyboard.add_hotkey(keyboardstr,toggleWindow)
killprocess = ttk.Button(text='杀死进程',width=12,command=killSM,bootstyle=(PRIMARY, OUTLINE))
killprocess.place(x=10,y=30)
killprocess = ttk.Button(text='杀死网管',width=12,command=killWG,bootstyle=(PRIMARY, OUTLINE))
killprocess.place(x=130,y=30)
kbentry = ttk.Entry(root,width=13,textvariable=keyboardstr)
kbentry.place(x=10,y=65)
kbset = ttk.Button(text='设置快捷键',width=12,command=setboard,bootstyle=(PRIMARY, OUTLINE))
kbset.place(x=130,y=65)
mythwarelaji = ttk.Label(text='MythKiller-Reborn v1.1',font=('Consolas',13))
mythwarelaji.place(x=20,y=0)
minimize = ttk.Button(text='最小化广播',width=12,command=minimizeWindow,bootstyle=(PRIMARY, OUTLINE))
minimize.place(x=10,y=100)
minimize = ttk.Button(text='最大化广播',width=12,command=maximizeWindow,bootstyle=(PRIMARY, OUTLINE))
minimize.place(x=130,y=100)
patchPassword = ttk.Button(text='破解极域密码',width=12,command=patch,bootstyle=(PRIMARY, OUTLINE))
patchPassword.place(x=10,y=135)
fuckDisk = ttk.Button(text='去除U盘锁',width=12,command=fuckUDisk,bootstyle=(PRIMARY, OUTLINE))
fuckDisk.place(x=130,y=135)
themes = ttk.Style().theme_names()
theme_combobox = ttk.Combobox(root,width=13,values=themes)
theme_combobox.current(0)
theme_combobox.place(x=10, y=170)
def change_theme(event=None):
    selected_theme = theme_combobox.get()
    ttk.Style(selected_theme)
theme_combobox.bind("<<ComboboxSelected>>", change_theme)
menu = tk.Menu(root, tearoff=0)
menu.add_cascade(label="控制台",command=console)
root.config(menu=menu)
kbentry.insert(0,keyboardstr)
root.mainloop()