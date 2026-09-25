import pygame
import random
import math
from pygame import mixer

#Inicializar Pygame
pygame.init()

#Crear la pantalla
pantalla =pygame.display.set_mode((800,600))

#Titulo e icono
pygame.display.set_caption("Invasion Espacial")
icono=pygame.image.load("ovni.png")
pygame.display.set_icon(icono) #Mostar
fondo= pygame.image.load("Fondo.jpg")
'''#Agregar musica
mixer.music.load('MusicaFondoJuego2.mp3')
mixer.music.play(-1)'''


#jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x=368 #800/2 =400-32  32 es la mitad del ancho del jugador
jugador_y=500#600-64 la altura del jugador 64
jugador_x_cambio=0

#Enemigo
img_enemigo = []
enemigo_x= []
enemigo_y= []
enemigo_x_cambio= []
enemigo_y_cambio= []
cantidad_enemigos=10
for e in range(cantidad_enemigos):
    img_enemigo.append( pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(1)
    enemigo_y_cambio.append(50)

#Variables de la bala
img_bala = pygame.image.load("bala.png")
bala_x=0
bala_y=500
bala_x_cambio=0
bala_y_cambio=3
bala_visible=False

#Puntaje
puntaje = 0
fuente = pygame.font.Font('Soviet2.ttf',32)
texto_x=10
texto_y=10


#Final de juego
fuente_final=pygame.font.Font("Soviet2.ttf",50)

def texto_final():
    mi_fuente_final=fuente_final.render("JUEGO TERMINADO",True,(255,255,255))
    pantalla.blit(mi_fuente_final,(60,200))

#funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto=fuente.render(f"puntaje : {puntaje}",True,(255,255,255))
    pantalla.blit(texto,(x,y))



def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))


def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))


#Funcion disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible=True
    pantalla.blit(img_bala,(x+16,y+10))

#Funcion detectar colision
def colision(x_1,y_1,x_2,y_2):
    distancia=math.sqrt(math.pow(x_1 - x_2,2) + math.pow(y_1-y_2,2))
    if distancia < 27:
        return True
    else:
        return False


#Loop juego
se_ejecuta=True

while se_ejecuta:
    # Imagen de fono
    pantalla.blit(fondo,(0,0))

    for evento in pygame.event.get():
        #Evento cerrar el programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False

    #   Evento presionar flechas
        if evento.type==pygame.KEYDOWN:
            if evento.key==pygame.K_LEFT:
                jugador_x_cambio= -1#Cambios negativos
            if evento.key==pygame.K_RIGHT:
                jugador_x_cambio= 1 #Hacia la derecha cambios positivos
            if evento.key==pygame.K_SPACE:
                sonido_bala=mixer.Sound('disparojuego2.mp3')
                sonido_bala.play()
                if bala_visible == False:
                    bala_x=jugador_x
                    disparar_bala(bala_x,bala_y)

            #Evento soltra flechas
        if evento.type == pygame.KEYUP:
            if evento.key== pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio= 0
#Modificar ubicacion
    jugador_x=jugador_x+jugador_x_cambio

    #Mantener bordes
    if jugador_x <= 0: #El valorse va a restablcer cuando jugador x sea menor a 0
        jugador_x=0
    elif jugador_x >=736:
        jugador_x=736
    jugador(jugador_x,jugador_y)


    # Modificar enemigo
    for e in range(cantidad_enemigos):

        #Fin del juego
        if enemigo_y[e]>500:
            for k in range(cantidad_enemigos):
                enemigo_y[k]=1000
            texto_final()
            break
        enemigo_x[e] = enemigo_x[e] + enemigo_x_cambio[e]

        # Mantener bordes al enemigo
        if enemigo_x[e] <= 0:  # El valorse va a restablcer cuando jugador x sea menor a 0
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] +=enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        #Movimiento bala
        if bala_y<= -64:
            bala_y=500
            bala_visible=False

        if bala_visible:
            disparar_bala(bala_x,bala_y)
            bala_y -=bala_y_cambio

            # Colision
        valor_colision = colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if valor_colision:
            sonido_colision=mixer.Sound("Golpejuego2.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e]=random.randint(0, 736)
            enemigo_y[e]=random.randint(50, 200)
        enemigo(enemigo_x[e], enemigo_y[e],e)

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x,texto_y)

    #Actyualizar
    pygame.display.update()

    pass