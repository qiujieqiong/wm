#!/usr/bin/env python3
#encoding:utf-8

from worker import *

system = System()
system.closeAllWorker()

system.createNewWorker()
w1 = system.workers[0]
w2 = system.workers[1]
system.switchModle(System.ModleType.normal)
w1.closeAllWindows()
w1.openWindow("doc")
w1.openWindow("window")
w1.openWindow("google")
system.switchModle(System.ModleType.preview)
#把工作区1中的窗口移动到工作区2中区
for i in range(5):
	p1 = (602, 408)
	p2 = (793, 238)
	p3 = (955, 108)
	#m.press(m.position()[0], m.position()[1])
	m.press(p1[0],p1[1])
	time.sleep(0.5)
	m.drag(p2[0],p2[1])
	time.sleep(0.5)
	m.drag(p3[0],p3[1])
	time.sleep(0.5)
	m.release(p3[0],p3[1])
	time.sleep(0.5)

	m.press(p3[0],p3[1])
	time.sleep(0.5)
	m.drag(p2[0],p2[1])
	time.sleep(0.5)
	m.drag(p1[0],p1[1])
	time.sleep(0.5)
	m.release(p1[0],p1[1])
	time.sleep(0.5)	
system.switchModle(System.ModleType.normal)

