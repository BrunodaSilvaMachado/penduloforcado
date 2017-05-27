#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt 
import getopt,sys

#variables
dt = 0.001
g = 9.8 
y = 0.5
A = 0
wf = 2./3.
m=1
t=0
_imagName = 'a'
#end

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

def grafico(_tlist,_dlist,_pos,_l,_cor,visivel):
	plt.subplot(_pos)
	axes = plt.gca()
	axes.axes.get_xaxis().set_visible(visivel)
	axes.spines['top'].set_color('none')
	axes.spines['right'].set_color('none')
	axes.yaxis.set_ticks_position('left')
	axes.xaxis.set_ticks_position('bottom')
	axes.spines['bottom'].set_position(('data',0))
	plt.ylabel(_l)
	plt.plot(_tlist,_dlist,_cor)
#end 

#begin

''' ---------command line--------------
	pendulo.py -f <_imagName> -a <value>
'''

opcao,valor = getopt.getopt(sys.argv[1:],'f:a: ')

for opcao,valor in opcao:
	if opcao == '-f':
		_imagName = str(valor)
	if opcao == '-a':
		A = float(valor)

#p1 = Pendulo(1.,10.,math.pi/6,0)
p1 = Pendulo(1.,10.,math.pi/6 - 1e4,0) #caos em acao

remove = 3000
tmax=30*p1.T
t=np.arange(0,tmax,dt)
x=np.zeros(t.size)
v=np.zeros(t.size)
e=np.zeros(t.size)
x[0],v[0],e[0]=p1.x,p1.v,p1.e


for i in range(t.size):
	p1.move(t[i])
	p1.x=(p1.x+math.pi)%(2*math.pi)-math.pi
	x[i],v[i],e[i]=p1.x,p1.v,p1.e

plt.figure(figsize=(9,8),facecolor='white')
plt.subplot(6,1,(1,3))
plt.xlabel('x')
plt.ylabel('v')

axes = plt.gca()
axes.set_xlim([-math.pi,math.pi])

plt.xticks( [-3.14, -3.14/2,0, 3.14/2, 3.14],[r'$-\pi$', r'$-\pi/2$','0', r'$+\pi/2$', r'$+\pi$'])
plt.text(x[0],v[0],'P',color='blue')

nx,nv = x[remove:],v[remove:]
plt.scatter(nx,nv, s=0.0003)

grafico(t,x,614,'x','r-',False)
grafico(t,v,615,'y','b-',False)
grafico(t,e,616,'E','g-',True)
plt.savefig(_imagName,dpi=96)
#plt.show()

print 'concluido'
#end
