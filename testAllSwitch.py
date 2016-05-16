#!/usr/bin/env python3
#encoding:utf-8

from worker import *

system = System()
w1 = system.workers[0]
w1.closeAllWindows()

#launcher中的所有应用名称(除了多任务视图和控制中心)
'''
allWindowNames = ("brasero","chmyueduqi","crossover","fcitx","firefox","gdebi",\
			"gparted","chrome","remmina","thunderbird","wpswenzi","wpsyanshi",\
			"wpsbiaoge","gedit","picture","ziti","guidang","dayin",\
			"saomiao","window","youdao","shenduqidong","shendushangdian",\
			"shenduyingyuan","shenduyonghu","shenduzhongduan","shenduyinyue","xitong","jisuanqi")
'''
allWindowNames = ("gparted","wpswenzi","wpsyanshi",\
			"wpsbiaoge","gedit","picture","ziti","guidang","dayin",\
			"saomiao","window","youdao","shenduqidong","shendushangdian",\
			"shenduyingyuan","shenduyonghu","shenduzhongduan","shenduyinyue","xitong","jisuanqi")

#步骤1:依次打开launcher里面的所有应用
for eachName in allWindowNames:
	w1.openWindow(eachName)

#步骤2:键入alt+tab
w1.fastNextWindow()
#步骤3:再次键入alt+tab
w1.fastNextWindow()
#步骤6:循环4-5步骤1000次

for x in range(1000):
	#步骤4:按下alt键，键入tab键n次（n：随机产生）
	for i in range(randint(5,50)):
		w1.normalNextWindow()
	#步骤5:再次键入alt+tab，可以切换到最后一个窗口计算器
	w1.fastNextWindow()
