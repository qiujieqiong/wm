#This file authorized by qiujieqiong
#!/usr/bin/env python3
#encoding:utf-8

from worker import *

system = System()
system.closeAllWorker()

system.switchModle(System.ModleType.preview)
system.createNewWorker(6)
system.showPreWorker(6)																													
system.switchModle(System.ModleType.normal)

#工作区1打开9种窗口
w1 = system.workers[0]	
#打开5个文件管理器和文档阅读器
for wn in ["window","doc"]:
	w1.openWindow(wn,5)
#打开wps文字、wps表格、wps演示，每个都新建5个标签页
for wn in ["wpswenzi","wpsbiaoge","wpsyanshi"]:
	w1.openWindow(wn).newTab(5)
#打开firefox浏览器、深度终端、google浏览器各5个,每个窗口都新建5个标签页
for wn in ["Firefox","deepin-terminal","chrome"]:
	for i in range(5):
		w1.openWindow(wn).newTab(5)
#打开gedit编辑器（打开n次gedit也只能打开两个gedit）
for i in range(2):
	w1.openWindow("gedit").newTab(5)

#工作区2打开6种窗口
w2 = system.workers[1]
#打开深度音乐
w2.openWindow("deepin-music")
#打开firefox浏览器、深度终端各5个，每个窗口都新建5个标签页
for wn in ["Firefox","deepin-terminal"]:
	for i in range(5):
		w2.openWindow(wn).newTab(5)
#打开wps文字，新建5个标签页
w2.openWindow("wpswenzi").newTab(5)
#打开文件管理器、图像查看器，每个窗口都新建5个标签页
for wn in ["window","picture"]:
	w2.openWindow(wn,5)

#工作区3打开5种窗口
w3 = system.workers[2]
#打开firefox浏览器、深度终端各5个，每个窗口都新建5个标签页
for wn in ["Firefox","deepin-terminal"]:
	for i in range(5):
		w3.openWindow(wn).newTab(5)
#打开wps表格，新建5个标签页
w2.openWindow("wpsbiaoge").newTab(5)
#打开深度影院
w3.openWindow("deepin-movie")
#打开5个文件管理器
w3.openWindow("window",5)

#接下来有7个动作要执行
#随机普通正向反向切换窗口
def mormalSwitchWindow():
	system.switchModle(System.ModleType.normal)
	randomWorker=randSelectOne(system.workers)
	for i in range(randint(5,20)):
		randExecOne(randomWorker.normalNextWindow,randomWorker.normalPreWindow)
#随机快速正向反向切换窗口
def fastSwitchWindow():
	system.switchModle(System.ModleType.normal)
	randomWorker=randSelectOne(system.workers)
	for i in range(randint(5,20)):
		randExecOne(randomWorker.fastPreWindow,randomWorker.fastNextWindow)
#随机打开窗口
def openWin():
	#控制打开窗口个数在30以内
	if system.getWindowQty() > 30 :
		return
	system.switchModle(System.ModleType.normal)
	winNames=["chrome","fire","doc","deepin-terminal"]
	randomWorker=randSelectOne(system.workers)
	for i in range(3):
		randomWorker.openWindow(randSelectOne(winNames),5)	
	randomWorker.openWindow("deepin-movie")
	randomWorker.openWindow("deepin-music")
#随机关闭窗口
def closeWin():
	#控制窗口在5个以上
	if system.getWindowQty() < 5 :
		return
	system.switchModle(System.ModleType.normal)
	#关闭窗口
	randomWorker=randSelectOne(system.workers)
	if len(randomWorker.windows)> 3:
		for i in range(len(randomWorker.windows)-1):
			randSelectOne(randomWorker.windows).close()
#普通模式下随机切换工作区
def normaSwitchlWorker():
	system.switchModle(System.ModleType.normal)
	#用箭头随机切换工作区
	for i in range(30):
		randExecOne(system.showNextWorker,system.showPreWorker)
#随机把窗口在工作区之间切换
def moveWinToWorker():
	system.switchModle(System.ModleType.preview)
	#把窗口移动到工作区
	for i in range(randint(5,10)):
		src = randSelectOne(system.workers)
		target = randSelectOne(system.workers)
		if src != target and len(src.windows)>0:
			randSelectOne(src.windows).moveToWorker(target)
#预览模式下随机切换工作区
def previewSwitchWorker():
	system.switchModle(System.ModleType.preview)
	#用箭头随机切换工作区
	for i in range(30):
		randExecOne(system.showNextWorker,system.showPreWorker)
		
steps = (mormalSwitchWindow,fastSwitchWindow,openWin,closeWin,normaSwitchlWorker,moveWinToWorker,previewSwitchWorker)
#这7个动作顺序执行
for s in steps:
	s()
#这7个动作随机执行
start=datetime.now()
while (datetime.now()-start).days < 7:
	randSelectOne(steps)()

