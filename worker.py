#!/usr/bin/env python3
#encoding:utf-8

import time
import os
import subprocess
from pykeyboard import PyKeyboard
from enum import Enum
import random
from datetime import datetime
from pymouse import PyMouse

m = PyMouse()
k = PyKeyboard()

class Log:
	def info(self,message):
		f = open("log.txt",'a')
		f.write("[%s]: %s \n" % (datetime.now(),message))
		print(message)
		f.close()
log = Log()
class System:
	ModleType = Enum('ModleType', 'normal preview')
	workers=[]
	currentWorker=None
	modle=None
	systemCount=0
	def __init__(self):
		log.info(" new System")
		if System.systemCount>0:
			raise Exception("System count > 1 ")

		self.modle=System.ModleType.normal
		qtys = subprocess.check_output(["wmctrl -d  |awk '{print $1}'"],shell=True).decode().split("\n")
		time.sleep(1)
		qtys=[ n for n in qtys if len(n.strip()) > 0]
		qty=0
		for wid in qtys:
			if int(wid) > qty:
				qty=int(wid)
		log.info("total workers: %d" % (qty+1))		
		for i in range(qty+1):
			Worker(self)
		self.currentWorker=self.workers[0]
		self.currentWorker.show()
		System.systemCount+=1

	def createNewWorker(self,qty=1):
		if qty < 1:
			qty =1
		if(len(self.workers) + qty > 7):
			raise Exception("worker count > 7 ")
		for i in range(qty):
			w = Worker(self)
			self.currentWorker=w
			modle=self.modle
			self.switchModle(System.ModleType.preview)
			k.press_key("+")
			k.release_key("+")
			k.press_key(k.enter_key)
			k.release_key(k.enter_key)
			time.sleep(1)
			
			self.switchModle(modle)			
		return w
	
	#切换预览模式和普通模式
	def switchModle(self,modle=None):
		if (modle!=None and modle==self.modle):
			return
		k.press_key(k.windows_l_key)
		time.sleep(1)
		k.press_key("s")
		k.release_key(k.windows_l_key)
		k.release_key("s")
		time.sleep(1)
		if self.modle == System.ModleType.normal:
			self.modle=System.ModleType.preview
		else:
			self.modle=System.ModleType.normal

	#删除所有工作区
	def closeAllWorker(self):
		log.info("close all %s workers" % str(len(self.workers)))
		if(len(self.workers)==1):
			return
		modle=self.modle
		self.switchModle(System.ModleType.preview)
		workers = self.workers[:]#数组复制
		for w in workers:
			w.close()
		self.switchModle(modle)
		
	#右箭头切换到下一个工作区
	def showNextWorker(self,qty=1):
		index = self.currentWorker.getIndex()+1
		log.info(" show Next" + str(index))
		if index >= len(self.workers):
			return
		self.currentWorker=self.workers[index]
		k.press_key(k.windows_l_key)
		time.sleep(1)
		k.press_key(k.right_key)
		k.release_key(k.right_key)
		k.release_key(k.windows_l_key)
		if qty > 1:
			self.showNextWorker(qty-1)
	#左箭头切换到上一个工作区
	def showPreWorker(self,qty=1):	
		index = self.currentWorker.getIndex()-1
		log.info(" show Pre" + str(index))
		if index < 0:
			return
		self.currentWorker=self.workers[index]
		k.press_key(k.windows_l_key)
		time.sleep(1)
		k.press_key(k.left_key)
		k.release_key(k.left_key)
		k.release_key(k.windows_l_key)
		if qty > 1:
			self.showPreWorker(qty-1)
	#所有工作区的窗口总数
	def getWindowQty(self):
		qty =0
		for w in self.workers:
			qty = qty + len(w.windows)
		return qty
		
class Worker:
	
	
	isExist=True
	system=None
	windows=None

	def __init__(self,system):
		self.system=system	
		system.workers.append(self)
		windowNames = subprocess.check_output(["wmctrl -l -x |awk '{print $1\" \"$2\" \" $NF}'"],shell=True).decode().split("\n")
		windowNames = [ n for n in windowNames if len(n.strip()) > 0]	
		self.windows=[]
		print(windowNames)
		for win in windowNames:
			w = win.split(" ");
			if w[1]==str(self.getIndex()):
				log.info("init Window %s"% w[2])
				winName = w[2]
				if winName == "深度终端":
					winName = "脚本"
				Window(winName,w[0],self)
	#获得工作区ID			
	def getIndex(self):
		for i in range(len(self.system.workers)):
			if self.system.workers[i] == self:
				return i
	#删除工作区
	def close(self):
	
		if len(self.system.workers)==1:
			return
		if self.isExist == False:
			return
		self.show()
		modle=self.system.modle
		self.system.switchModle(System.ModleType.preview)
		k.press_key("-")
		k.release_key("-")
		time.sleep(1)
		self.isExist=False

		tarWorker = None
		if self.getIndex() ==0:
			tarWorker=self.system.workers[1]
		else:
			tarWorker=self.system.workers[self.getIndex()-1]
			
		tarWorker.windows.extend(self.windows)
		
		for win in self.windows:
				win.worker=tarWorker

		self.system.currentWorker=tarWorker

		self.system.workers.remove(self)
		self.system.switchModle(modle)	

	#显示指定工作区
	def show(self):
		if self.isExist == False:
			raise Exception("worker is not exist")
		if(self ==self.system.currentWorker):
			return
		id = str(self.getIndex()+1)
		#windowID = subprocess.check_output(["wmctrl -l -x |awk '{print $2}'"],shell=True).decode().split("\n")
		#windowID = [ n for n in windowID if len(n.strip()) > 0]#去掉最后一个空的list
	
		#subprocess.check_call(["wmctrl -s " + id],shell=True)
		k.press_key(k.control_l_key)
		k.press_key(k.alt_l_key)
		k.press_key(id)
		k.release_key(k.control_l_key)
		k.release_key(k.alt_l_key)
		k.release_key(id)
		log.info("switch to worker %s model -- %s" % (id,str(self.system.modle)))
		self.system.currentWorker=self
		time.sleep(1)
		
		#print("There is no worker %s" % id)
		#return False

	#判断窗口是否在工作区
	def have(self,window):
		return window in self.windows

	#打开窗口
	def openWindow(self,name,qty=1):
		
		self.show()
		modle=self.system.modle
		self.system.switchModle(System.ModleType.normal)
		newWindow = None

		oldWindowNames = subprocess.check_output(["wmctrl -l -x |awk '{print $1\" \"$2\" \" $NF}'"],shell=True).decode().split("\n")
		oldWindowNames = [ n for n in oldWindowNames if len(n.strip()) > 0]
		k.press_key(k.windows_l_key)# 打开菜单栏
		k.release_key(k.windows_l_key)   
		time.sleep(0.7)
		k.type_string(name)#比如输入deepin-movie 就会打开深度影院
		time.sleep(0.8)
		k.press_key(k.enter_key)
		k.release_key(k.enter_key)
		time.sleep(0.1)
		
		if name == "shenduqidong":
			time.sleep(1)
			k.type_string("a")
			time.sleep(0.1)
			k.press_key(k.enter_key)
			k.release_key(k.enter_key)
			time.sleep(0.1)

		start = datetime.now()
		end = None
		for i in range(30):
			windowNames = subprocess.check_output(["wmctrl -l -x |awk '{print $1\" \"$2\" \" $NF}'"],shell=True).decode().split("\n")
			time.sleep(0.3)
			windowNames = [ n for n in windowNames if len(n.strip()) > 0]

			log.info("len(oldWindowNames) %s len(windowNames) %s" % (len(oldWindowNames),len(windowNames)))
			if len(oldWindowNames)<len(windowNames):
				end = datetime.now()
				break
		if end !=None:
			openTime = (end-start).seconds+(end-start).microseconds/1000000.0
			log.info("openWindow %s in %f seconds"% (name,openTime))
			w = [n for n in windowNames if n not in oldWindowNames][0].split(" ")
			newWindow = Window(name,w[0],self)
			newWindow.show()
		else:
			log.info("the window %s already existed"% name)
			
		if end!=None and name == "gparted":
			time.sleep(0.5)
			k.type_string("a")
			time.sleep(0.1)
			k.press_key(k.enter_key)
			k.release_key(k.enter_key)
			time.sleep(1)
			windowNames = subprocess.check_output(["wmctrl -l -x |awk '{print $1\" \"$2\" \" $NF}'"],shell=True).decode().split("\n")	
			windowNames = [ n for n in windowNames if len(n.strip()) > 0]
			w = [n for n in windowNames if n not in oldWindowNames][0].split(" ")
			self.windows.remove(newWindow)#输入密码后,授权窗口就自动关掉了,gparted窗口会显示出来,所以需要把授权窗口给移除掉
			newWindow =Window(name,w[0],self)#然后把gparted窗口给加进来
			newWindow.show()
		if qty>1:
			newWindow = self.openWindow(name,qty-1)
		#如果打开的多个窗口不能再继续打开，比如(gedit只能打开两个窗口)，就把原来打开的窗口给显示出来
		if newWindow == None:
			for win in self.windows:
				if win.name == name:
					win.show()
					return win
		return newWindow

	#关闭所有窗口除了桌面,dock,深度终端
	def closeAllWindows(self):
		for win in self.windows[:]:
			
			win.close()
	#快速正向切换窗口口
	def fastNextWindow(self):
		self.show()
		k.press_key(k.alt_l_key)
		k.press_key(k.tab_key)
		k.release_key(k.alt_l_key)
		k.release_key(k.tab_key)
		time.sleep(0.5)
	#快速反向切换窗口
	def fastPreWindow(self):
		self.show()
		k.press_key(k.alt_l_key)
		k.press_key(k.shift_l_key)
		k.press_key(k.tab_key)
		k.release_key(k.alt_l_key)
		k.release_key(k.shift_l_key)
		k.release_key(k.tab_key)
		time.sleep(0.5)
	#普通正向切换窗口
	def normalNextWindow(self):
		self.show()
		k.press_key(k.alt_l_key)
		time.sleep(0.9)
		k.press_key(k.tab_key)
		k.release_key(k.tab_key)
		k.release_key(k.alt_l_key)
	#普通反向切换窗口
	def normalPreWindow(self):
		self.show()
		k.press_key(k.alt_l_key)
		k.press_key(k.shift_l_key)
		time.sleep(0.9)
		k.press_key(k.tab_key)
		k.release_key(k.tab_key)
		k.release_key(k.alt_l_key)
		k.release_key(k.shift_l_key)


class Window:
	id=None
	name=None
	worker = None

	def __init__(self,name,id,worker):
		self.name = name
		self.id=id
		self.worker=worker
		worker.windows.append(self)

	#关闭窗口
	def close(self):
		if self.name  in ("dde-desktop","dde-dock","脚本"):
			return
		self.show()
		windowNames = subprocess.check_output(["wmctrl -l -x |awk '{print $NF}'"],shell=True).decode().split("\n")
		subprocess.check_call(["wmctrl -i "+self.id+" -c " + self.id],shell=True)
		time.sleep(1)
		log.info("close window %s" % self.name)
		self.worker.windows.remove(self)
	#在普通模式下把窗口移动到相应工作区，预览模式下的切换只需要在调用时在前面加上system.switchModle(System.ModleType.preview)
	def moveToWorker(self,worker):
		id = worker.getIndex()
		worker.show()
		
		subprocess.call(["wmctrl -i -r " + self.id + " -t " + str(id)],shell=True)
		time.sleep(1)

		self.worker.windows.remove(self)
		worker.windows.append(self)
		self.worker=worker
		self.show()
	#新建当前窗口标签页，不同窗口快捷键不一样
	def newTab(self,qty=1):
		self.show()
		for i in range(qty):
			if self.name == "deepin-terminal":
				k.press_key(k.control_l_key)
				k.press_key(k.lookup_character_keycode('/'))
				k.release_key(k.control_l_key)
				k.release_key(k.lookup_character_keycode('/'))
			elif  self.name in ("wpswenzi","wpsbiaoge","wpsyanshi") :
				k.press_key(k.control_l_key)
				k.press_key("n")
				k.release_key(k.control_l_key)
				k.release_key("n")
			else:
				k.press_key(k.control_l_key)
				k.press_key("t")
				k.release_key(k.control_l_key)
				k.release_key("t")
			time.sleep(1)
	#显示当前窗口
	def show(self):
		self.worker.show()
		subprocess.check_call(["wmctrl -i "+self.id+" -a " + self.id],shell=True)
		time.sleep(1)
		return


#从start和end之间获得一个随机数
def randint(start,end):
	return random.randint(start,end)
#随机选择一个
def randSelectOne(obj):
	return obj[randint(0,len(obj)-1)]

def randExecOne(a,b):
	if randint(1,10) > 5 :
		a()
	else:
		b()
