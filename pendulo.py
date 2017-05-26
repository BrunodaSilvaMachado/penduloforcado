#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt 

#variables
dt = 0.001
g = 9.8 
y = 0.5
A = 0.2
wf = 2./3.
m=1
t=0

class Pendulo(object):
	def __init__(self,massa,l,theta,v):
		self.m = massa
		self.l = l 
		self.x = theta
		self.v = v
		self.w2 = g/l 
		self.T = 2*math.pi*math.sqrt(l/g)
		self.k = massa*self.w2
		self.e = 0.5*massa*(l*v)**2+m*g*l*(1-math.cos(theta))
		
	def a(self,x,v,t):
		return -self.w2*math.sin(x) - y*v + A*math.sin(wf*t)
				
	def move(self,t):
		at = self.a(self.x,self.v,t)
		self.x += self.v*dt + at*dt*dt/2
		a_tmp = self.a(self.x,self.v,t)
		v_tmp = self.v+(at+a_tmp)*dt/2 
		a_tmp = self.a(self.x,v_tmp,t)
		self.v += (a_tmp+at)*dt/2
		self.e = 0.5*self.m*(self.l*self.v)**2 + (self.m*g*self.l*(1-math.cos(self.x)))
#end

def grafico(_tlist,_dlist,_pos,_l,_cor,visivel,_legend):
	plt.subplot(_pos)
	axes = plt.gca()
	axes.axes.get_xaxis().set_visible(visivel)
	axes.spines['top'].set_color('none')
	axes.spines['right'].set_color('none')
	axes.yaxis.set_ticks_position('left')
	axes.xaxis.set_ticks_position('bottom')
	axes.spines['bottom'].set_position(('data',0))
	plt.ylabel(_l)
	plt.plot(_tlist,_dlist,_cor,label = _legend)
	plt.legend(loc = 'upper right')
#end 

def seed(_pendulum,_imagName,_legend = ''):

	tmax=30*_pendulum.T
	t=np.arange(0,tmax,dt)
	x=np.zeros(t.size)
	v=np.zeros(t.size)
	e=np.zeros(t.size)
	x[0],v[0],e[0]=_pendulum.x,_pendulum.v,_pendulum.e


	for i in range(t.size):
		_pendulum.move(t[i])
		_pendulum.x=(_pendulum.x+math.pi)%(2*math.pi)-math.pi
		x[i],v[i],e[i]=_pendulum.x,_pendulum.v,_pendulum.e

	plt.figure(figsize=(8,12),facecolor='white')
	plt.subplot(6,1,(1,3))
	plt.xlabel('x')
	plt.ylabel('v')
	axes = plt.gca()
	axes.set_xlim([-math.pi,math.pi])
	plt.xticks( [-3.14, -3.14/2,0, 3.14/2, 3.14],[r'$-\pi$', r'$-\pi/2$','0', r'$+\pi/2$', r'$+\pi$'])
	plt.text(x[0],v[0],'S',color='green')
	plt.scatter(x,v, s=0.003)
	grafico(t,x,614,'x','r-',False,_legend)
	grafico(t,v,615,'y','b-',False,_legend)
	grafico(t,e,616,'E','g-',True,_legend)
	plt.savefig(_imagName,dpi=96)
	#plt.show()

def main():
	
	p1 = Pendulo(1.,10.,0,math.pi/6)
	seed(p1,"image1","A = 0.2")
	A = 0.75
	seed(p1,"image2","A = 0.75")
	A = 1.25
	seed(p1,"image3","A = 1.25")

main()