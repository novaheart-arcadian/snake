#Este es el juego de la serpiente
import pygame
import time 
import random 
import tienda
import economia

data = economia.load_data()

# Cuando quieras abrir la tienda:
tienda.pantalla_tienda(screen, data)

from shop_dlc import load_save, buy_skin, equip_skin, redeem_dlc_dialog, add_coins

s = load_save()
# mostrar monedas: s['coins']
# mostrar skins desbloqueadas: s['unlocked_skins']

# para canjear con diálogo:
redeem_dlc_dialog()

# para comprar una skin (por ejemplo cuando presionan comprar):
ok, msg = buy_skin("skin_neon")

# Ejemplo: añadir monedas al hacer puntos
economia.add_coins(data, 5)

# Para colorear el snake según skin equipada:
snake_color = economia.get_equipped_color(data)

#Creamos la pantalla
pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255, 0, 0)
green =(0, 255, 0)
blue = (0, 0, 255)
gold = (255, 215, 0)

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Serpiente by NovaHeart Arcadian')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

#Niveles
level = 1
speed = 10  # FPS inicial

font_style = pygame.font.SysFont('bahnschrift', 25)
score_font = pygame.font.SysFont('comicsansms', 35)

#Comida Especial: Puntos Extra
special_food = None
special_food_timer = 0
SPECIAL_FOOD_DURATION = 7      # segundos que dura la comida especial
SPECIAL_FOOD_POINTS = 5        # puntos extra por comerla


#Tienda
def mostrar_tienda(data):
    print("\n--- TIENDA DE SKINS ---")
    print(f"Monedas: {data['coins']}\n")

    for name, info in economia.SKINS.items():
        owned = "✓" if name in data["owned_skins"] else f"{info['price']} monedas"
        print(f"{name} -> {owned}")

    op = input("\nComprar skin (nombre) / equipar / salir: ")

    if op in economia.SKINS:
        print(economia.buy_skin(data, op))
    elif op.startswith("equip "):
        skin = op.split(" ")[1]
        print(economia.equip_skin(data, skin))
    else:
        print("Volviendo al menú...")



#Contador de Puntos
def Your_score(score):
    value = score_font.render('Tus Puntos:' + str(score), True, yellow)
    dis.blit(value, [0, 0])

#Definimos la comida especial
def spawn_food(grid_width, grid_height):
    return [random.randint(0, grid_width-1), random.randint(0, grid_height-1)]

def spawn_special_food(grid_width, grid_height):
    return [random.randint(0, grid_width-1), random.randint(0, grid_height-1)]

#La serpiente se alarga cuando va a comer
def our_nake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
    
    # Dibujar comida especial (color dorado)
    if special_food is not None:
       pygame.draw.rect(screen, (255, 215, 0), (special_food[0]*cell, special_food[1]*cell, cell, cell))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [des_width/6, dis_height/3])

def gameLoop():#creando una funcion
    game_over = False
    game_close = False

#Canjear Desde Menú
def canjear_dlc(data):
ruta = input("Ruta del archivo DLC: ")
print(economia.redeem_dlc_file(ruta, data))


    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0

    snake_List = []
    Lenght_of_snake = 1

  #Comida de la serpiente 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0)
    foody = round(random.randrange(0, dis_width - snake_block) / 10.0)
    
    # Spawn comida especial aleatoriamente (5% de probabilidad cada frame)
    if special_food is None and random.randint(1, 200) == 1:
       special_food = spawn_special_food(grid_width, grid_height)
       special_food_timer = time.time()

    # La comida especial desaparece si pasa el tiempo
    if special_food is not None:
       if time.time() - special_food_timer > SPECIAL_FOOD_DURATION:
        special_food = None   

#Que pasa cuando el juego se termina
while not game_over:
    while game_close == True:
        dis.fill(blue)
        message('¡Pierdes! Presiona Q- Salir o C-Jugar Otra Vez', red)
        Your_score(Lenght_of_snake - 1)
    # Aumentar nivel cada 10 puntos
       if score >= level * 10:
          level += 1
          speed += 2   # velocidad más rápida

        pygame.display,update()


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_q:
                game_over = True
                game_close = False
             if event.type == pygame.K_c:
                gameLoop()   

        #Bloque De Juego   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

    if x1 >= dis_width or x1 <0 or y1 >= dis_height or y1 < 0:
        game_close = True             

    x1 += x1_change
    y1 += y1_change
    dis.fill(blue)

    #Dibujamos comida y serpiente. 
    #Serpiente se alarga cuando encuentra comida
    pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

    snake_Head = []
    snake_Head.append(x1)
    snake_Head.append(y1)
    snake_List.append(snake_Head)
    if len(snake_List) > Lenght_of_snake:
        del snake_List[0]

    # Si come comida especial
    if special_food is not None and snake_head == special_food:  
       score += SPECIAL_FOOD_POINTS
       snake_length += 1  # si quieres que crezca
    special_food = None    

    for x in snake_List[:1]:
        if x == snake_Head:
            game_close = True 

    our_snake(snake_block, snake_List)        

    pygame.display.update()  

    #Serpiente encuentra comida
    if x1 == foodx and y1 == foody:
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        Lenght_of_snake +=1
       
    clock.tick(snake_speed, speed)            

    #Salir del juego
    pygame.quit()
    quit()

gameLoop()    
