import random
#ventana
ancho=1600
alto=800

#fps
maxfps=60

#personaje
escla=0.25
vidas=3
velocidad_expansion=20

#balas
escalabala=0.2
velocidadbala=10
frecbalas=110
damage=30+random.randint(0,5)

#meteoros
escalameteoro=0.3
demorameteoro=300
demorareaparicion=800
salud=100
cordder=[[ancho],[i for i in range(alto)]]
cordizq=[[0],[i for i in range(alto)]]
cordtop=[[i for i in range(ancho)],[0]]
cordbot=[[i for i in range(ancho)],[alto]]
cord=[cordder,cordizq,cordtop,cordbot]
