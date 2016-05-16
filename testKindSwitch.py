#This file authorized by qiujieqiong
#!/usr/bin/env python3
#encoding:utf-8

from worker import *
system = System()
w1 = system.workers[0]

w1.closeAllWindows()

def step1To6(windowName,qty):
	#步骤1:打开qty个windowName
	w1.openWindow(windowName,qty)
	#步骤2:键入alt+tab
	w1.fastNextWindow()
	#步骤3:再次键入alt+tab
	w1.fastNextWindow()
	#步骤6:循环4-5步骤1000次
	for x in range(10):
		#步骤4:按下alt键，键入tab/shift+tab键n次（tab/shift+tab：随机选择；n：随机产生）
		for x in range(randint(5,50)):
			randExecOne(w1.normalNextWindow,w1.normalPreWindow)
		#步骤5:再次键入Alt+tab键
		w1.normalNextWindow()

#打开100个google浏览器,循环执行以上1-6步骤
step1To6("chrome",100)
#关掉前面的浏览器
w1.closeAllWindows()
#步骤7:打开100个深度终端,循环执行以上1-6步骤
step1To6("shenduzhongduan",100)
#关掉前面的深度终端
w1.closeAllWindows()
#步骤8:打开100个文件管理器,循环执行以上1-6步骤
step1To6("window",100)
