import pygame, random

# parámetros generales reservamos 2 bloques para bordes
ancho_pantalla = 34
alto_pantalla = 34
tamanio_bloque = 16
c = 0
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((ancho_pantalla*tamanio_bloque, alto_pantalla*tamanio_bloque))
pygame.display.set_caption('Snake')
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 15)

class serpiente:
    largo = 1
    x = 16
    y = 16
    direc = 1
    veloc = 25
    colax = []
    colay = []

class manzana:
    x = random.randint(1, 32)
    y = random.randint(1, 32)
    isDorada = False

class juego:
    puntuacion = 0
    salirJuego = False

    @staticmethod
    def grid():
        #Cuadrícula
        for x in range(int(ancho_pantalla)):
            for y in range(int(alto_pantalla)):
                of = 0
                if (y%2==0):
                    of = 1
                if (((x + of) % 2) == 0):
                    pygame.draw.rect(screen, (32,32,32),pygame.Rect(x*tamanio_bloque,y*tamanio_bloque,tamanio_bloque,tamanio_bloque))
                else:
                    pygame.draw.rect(screen, (64,64,64),pygame.Rect(x*tamanio_bloque,y*tamanio_bloque,tamanio_bloque,tamanio_bloque))
    @staticmethod
    def draw():
        #Bordes
        pygame.draw.rect(screen, (128,128,128),
                         pygame.Rect(0, 0, tamanio_bloque, alto_pantalla * tamanio_bloque))
        pygame.draw.rect(screen, (128,128,128),
                         pygame.Rect((ancho_pantalla - 1) * tamanio_bloque, 0, tamanio_bloque, alto_pantalla * tamanio_bloque))
        pygame.draw.rect(screen, (128,128,128),
                         pygame.Rect(0, 0, ancho_pantalla * tamanio_bloque, tamanio_bloque))
        pygame.draw.rect(screen, (128,128,128),
                         pygame.Rect(0, (alto_pantalla - 1) * tamanio_bloque, ancho_pantalla * tamanio_bloque, tamanio_bloque))

        #manzana
        if(manzana.isDorada):
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(screen, color,
                         pygame.Rect(tamanio_bloque*manzana.x+2,tamanio_bloque*manzana.y+2, tamanio_bloque-4, tamanio_bloque-4))

        for i in range(len(serpiente.colax)):
            pygame.draw.rect(screen, (128, 128, 255),
                             pygame.Rect(tamanio_bloque*serpiente.colax[i],tamanio_bloque*serpiente.colay[i], tamanio_bloque, tamanio_bloque))
        pygame.draw.rect(screen, (0, 0, 255),
                         pygame.Rect(tamanio_bloque*serpiente.x,tamanio_bloque*serpiente.y, tamanio_bloque, tamanio_bloque))

        #puntuacion
        textsurface = myfont.render('Puntuacion: ' + str(juego.puntuacion), False, (0, 0, 0))
        screen.blit(textsurface,(0,525))
    @staticmethod
    def keyd():
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.K_UP] and serpiente.direc != 2):
            serpiente.direc=0
        if (pressed[pygame.K_RIGHT] and serpiente.direc != 3):
            serpiente.direc=1
        if (pressed[pygame.K_DOWN] and serpiente.direc != 0):
            serpiente.direc=2
        if (pressed[pygame.K_LEFT] and serpiente.direc != 1):
            serpiente.direc=3

    @staticmethod
    def ref():
        juego.colas()
        if (serpiente.direc == 0):
            juego.move(0,-1)
            #serpiente.y -=1
        elif (serpiente.direc == 1):
            juego.move(1,0)
            #serpiente.x+=1
        elif (serpiente.direc == 2):
            #serpiente.y+=1
            juego.move(0,1)
        elif (serpiente.direc == 3):
            juego.move(-1,0)
            #serpiente.x-=1

    @staticmethod
    def move(x,y):
        #x check
        if (serpiente.x+x)>= ancho_pantalla-1:
            #print ("Fuera de la pantalla")
            serpiente.x = 1;
        elif(serpiente.x+x)<= 0:
            #print ("Fuera de la pantalla")
            serpiente.x = ancho_pantalla-2;
        else:
            serpiente.x+=x
        #y check
        if (serpiente.y+y)>= alto_pantalla-1:
            #print ("Fuera de la pantalla")
            serpiente.y = 1;
        elif(serpiente.y+y)<= 0:
            #print ("Fuera de la pantalla")
            serpiente.y = alto_pantalla-2;
        else:
            serpiente.y+=y

        #manzana
        if (serpiente.x == manzana.x) and (serpiente.y == manzana.y):
            serpiente.largo+=1
            serpiente.veloc = min(serpiente.veloc + 2, 85)
            if manzana.isDorada:
                juego.puntuacion += 3
            else:
                juego.puntuacion += 1
            manzana.x = random.randint(1,ancho_pantalla-2)
            manzana.y = random.randint(1,alto_pantalla-2)
            manzana.isDorada = random.randint(1, 10) == 10
            #print("Posicion manzana:\nX - "+str(manzana.x)+"\nY - "+str(manzana.y))

        #colisión
        for i in range(len(serpiente.colax)):
            if (serpiente.x == serpiente.colax[i]) and (serpiente.y == serpiente.colay[i]):
                print("Pierdes!\nPuntuacion: ", juego.puntuacion)
                juego.reset()
                break

    @staticmethod
    def colas():
        serpiente.colax.append(serpiente.x)
        serpiente.colay.append(serpiente.y)
        if (len(serpiente.colax) > serpiente.largo):
            serpiente.colax.pop(0)
            serpiente.colay.pop(0)

    @staticmethod
    def reset():
        juego.puntuacion = 0
        serpiente.x = 16
        serpiente.y = 16
        serpiente.largo = 1
        serpiente.veloc = 25
        serpiente.direc = 1
        serpiente.colax = []
        serpiente.colay = []
        manzana.x = random.randint(1, 32)
        manzana.y = random.randint(1, 32)
        manzana.isDorada = False

while not juego.salirJuego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego.salirJuego = True

    juego.grid()
    juego.keyd()
    c+=1
    juego.draw()
    if (c >= (200/serpiente.veloc)):
        juego.ref()
        c=0
        #snake.speed+=1
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
