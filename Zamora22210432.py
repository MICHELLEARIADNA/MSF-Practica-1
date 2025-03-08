"""
Práctica 1: Diseño de controladores

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Zamora Chon Michelle Ariadna
Número de control: 22210432
Correo institucional: l22210432@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tend, dt, w, h = 0, 0, 10, 1E-3, 6, 3
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u1 = np.ones(N) #Escalon unitario
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1 #Impulso
u3 = (np.linspace(0,tend, N))/tend #Rampa con pendiente 1/10
u4 = np.sin(m.pi/2*t) #Funcion sinusoidal, pi/2 = 250 mHz

u = np.stack((u1, u2, u3, u4), axis = 1)
signal = ['Escalon', 'Impulso', 'Rampa','Sin']


# Componentes del circuito RLC y función de transferencia
R = 1E3
L = 10E-6
C = 1E-6
num = [C*L*R,C*R**2+L,R]
den = [3*C*L*R,5*C*R**2+L,2*R]
sys = ctrl.tf(num,den)
print(sys)

# Componentes del controlador

Cr = 1E-6
ki = 782.68992
Re = 1/(ki*Cr) ;
numPI = [1]
denPI = [Re*Cr, 0]
PI = ctrl.tf(numPI, denPI)
print(PI)

# Sistema de control en lazo cerrado
X = ctrl.series(PI, sys)
sysPI = ctrl.feedback(X, 1, sign = -1)
print(sysPI)   



# Respuesta del sistema en lazo abierto y en lazo cerrado
#rojo [0.5, 0.5, 0.5]
AMARILLO = [252/255, 199/255, 55/255]
NARANJA = [242/255, 107/255, 15/255]
ROSA = [231/255, 56/255, 121/255]
MORADO = [126/255, 24/255, 145/255]

fig1 = plt.figure();
plt.plot(t,u1,'-', color = AMARILLO, label = 'Pao(t)')
_,PA = ctrl.forced_response(sys,t,u1,x0)
plt.plot(t,PA,'-', color = NARANJA, label = 'PA(t)')
_,VPI = ctrl.forced_response(sysPI,t,u1,x0)
plt.plot(t,VPI,':', linewidth = 3, color = AMARILLO, label = 'VPI(t)')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize = 11)
plt.ylabel('Vi[t][V]',fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig1.savefig('ESCALON.pdf',bbox_inches = 'tight')

fig2 = plt.figure();
plt.plot(t,u2,'-', color = NARANJA, label = 'Pao(t)')
_,PA = ctrl.forced_response(sys,t,u2,x0)
plt.plot(t,PA,'-', color = ROSA, label = 'PA(t)')
_,VPI = ctrl.forced_response(sysPI,t,u2,x0)
plt.plot(t,VPI,':', linewidth = 3, color = AMARILLO, label = 'VPI(t)')
plt.xlabel('t[s]',fontsize = 11)
plt.ylabel('Vi[t][V]',fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig2.savefig('IMPULSO.pdf',bbox_inches = 'tight')

fig3 = plt.figure();
plt.plot(t,u3,'-', color = ROSA, label = 'Pao(t)')
_,PA = ctrl.forced_response(sys,t,u3,x0)
plt.plot(t,PA,'-', color = MORADO, label = 'PA(t)')
_,VPI = ctrl.forced_response(sysPI,t,u3,x0)
plt.plot(t,VPI,':', linewidth = 3, color = AMARILLO, label = 'VPI(t)')
plt.xlabel('t[s]',fontsize = 11)
plt.ylabel('Vi[t][V]',fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig3.savefig('RAMPA.pdf',bbox_inches = 'tight')

fig4 = plt.figure();
plt.plot(t,u4,'-', color = MORADO, label = 'Pao(t)')
_,PA = ctrl.forced_response(sys,t,u4,x0)
plt.plot(t,PA,'-', color = AMARILLO, label = 'PA(t)')
_,VPI = ctrl.forced_response(sysPI,t,u4,x0)
plt.plot(t,VPI,':', linewidth = 3, color = AMARILLO, label = 'VPI(t)')
plt.xlabel('t[s]',fontsize = 11)
plt.ylabel('Vi[t][V]',fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig4.savefig('SIN.pdf',bbox_inches = 'tight')