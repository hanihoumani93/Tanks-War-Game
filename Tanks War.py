import pygame
import time
import random

pygame.init()

display_width = 800  # game frame display width
display_height = 600  # game frame display height

gameDisplay = pygame.display.set_mode((display_width,display_height))  # All the stuff we will create will be at this surface(gameDisplay) its like the canvas
# pygame.display.update() #Its like the flip book each page have an image when you flip the book you will get a movie (its imp in games)

white = (255, 255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (34, 177, 76)
yellow = (200, 200, 0)
light_green = (0, 255, 0)
light_yellow = (255, 255, 0)
light_red = (255, 0, 0)


pygame.display.set_caption('Tanks')  # set_caption() func it put a tittle to our pygame windows(surface)
#icon =  pygame.image.load('snakeHead.png') # change the icon of the game in the top left of the windows
#pygame.display.set_icon(icon)

clock = pygame.time.Clock()

tankWidth = 40
tankHeight = 20

turretWidth = 5
wheelWidth = 5

ground_height = 35

#img = pygame.image.load('snakeHead.png')
#apple = pygame.image.load('newApple1.png')

fire_sound = pygame.mixer.Sound("fire_sound.wav") #fire sound wav file
exp_sound = pygame.mixer.Sound("exp_sound.wav") #explosion sound wav file


smallfont = pygame.font.Font(None, 25)  # creating a font object
medfont = pygame.font.Font(None, 50)
largefont = pygame.font.Font(None, 80)

def tank(x, y, turPos):
    x = int(x) #we make it int since we are multiply by 0.9 so to avoid float numbers since we are working in pixels
    y= int(y)

    possibleTurrets = [(x-27,y-2), # these are all the postions of the turret from the left to the middle
                       (x-26,y-5),
                       (x-25,y-8),
                       (x-23,y-12),
                       (x-20,y-14),
                       (x-18,y-15),
                       (x-15,y-17),
                       (x-13,y-19),
                       (x-11,y-21)
                       ]
    
    pygame.draw.circle(gameDisplay, black, (x, y), 10)
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight)) #drawing the tank body
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)

    
    startX = 15
    for xWheel in range(7):
        pygame.draw.circle(gameDisplay, black, (x-startX, y+20), wheelWidth)
        startX -=5
    return possibleTurrets[turPos] # we return this value to know the starting location of the fire from the turret 

def enemy_tank(x, y, turPos):
    x = int(x) #we make it int since we are multiply by 0.9 so to avoid float numbers since we are working in pixels
    y= int(y)

    possibleTurrets = [(x+27,y-2), # these are all the postions of the turret from the left to the middle
                       (x+26,y-5),
                       (x+25,y-8),
                       (x+23,y-12),
                       (x+20,y-14),
                       (x+18,y-15),
                       (x+15,y-17),
                       (x+13,y-19),
                       (x+11,y-21)
                       ]
    
    pygame.draw.circle(gameDisplay, black, (x, y), 10)
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight)) #drawing the tank body
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)

    
    startX = 15
    for xWheel in range(7):
        pygame.draw.circle(gameDisplay, black, (x-startX, y+20), wheelWidth)
        startX -=5
    return possibleTurrets[turPos] # we return this value to know the starting location of the fire from the turret 

def paused():

    paused = True
    message_to_screen("Paused", black, -100, size='large')
    message_to_screen("Press C to continue or Q to quit", black, 25, size= 'small')
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)
        
        clock.tick(5)
        

def score (score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def game_controls():
    
    gcont = True
    
    while gcont:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            

            
        gameDisplay.fill(white)
        message_to_screen("Controls", green, -100, size='large')
        message_to_screen("Fire: Spacebar ", black, -30)
        message_to_screen("Move Turret : Up and Down arrows", black, 10)
        message_to_screen("Move Tank : Left and Right arrows", black, 50)
        message_to_screen("Pause : P", black, 90)

        
        button("play", 150, 500, 100, 50, green, light_green, action="play")
        button("Main", 350, 500, 100, 50, yellow, light_yellow, action="Main")
        button("quit",550, 500, 100, 50, red, light_red, action="quit")

        

        pygame.display.update()
        clock.tick(15)

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):
    if size == 'small':
        text_surf = smallfont.render(msg, True, color)
    elif size == 'medium':
        text_surf = medfont.render(msg, True, color)
    elif size == 'large':
        text_surf = largefont.render(msg, True, color)
    
    text_rect = text_surf.get_rect()
    text_rect.center = ((buttonx+(buttonwidth/2)),buttony+(buttonheight/2))
    gameDisplay.blit(text_surf, text_rect)

def button (msg, x, y, width, height, activecolor, inactivecolor, action=None):
    
    mouse_postion = pygame.mouse.get_pos() #get the mouse (x,y) postion
    click = pygame.mouse.get_pressed() #get mouse click so if the left key pressed then we get (1,0,0)
    
    if x+width > mouse_postion[0] > x and y+height> mouse_postion[1] > y: #if mouse is in the box then change the color
        pygame.draw.rect(gameDisplay, inactivecolor, (x,y,width,height))
        if click[0] == 1 and action != None: #if we left click on the button then an action will happen
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameLoop()
            if action == "Main":
                game_intro()
        
    else:
        
        pygame.draw.rect(gameDisplay, activecolor, (x,y,width,height))

    text_to_button(msg, black, x, y, width, height)

def game_intro():
    intro = True
    
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()



            
        gameDisplay.fill(white)
        message_to_screen("Welcome to Tanks War!", green, -100, size='large')
        message_to_screen("The objective is to shoot and destroy ", black, -30)
        message_to_screen("the enemy tank befor they distroy you.", black, 10)
        message_to_screen("The more enemies you destroy, the harder they get.", black, 50)
        #message_to_screen("Press C to play, P to pause or Q to quit", black, 180)

        
        button("play", 150, 500, 100, 50, green, light_green, action="play")
        button("controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
        button("quit",550, 500, 100, 50, red, light_red, action="quit")

        

        pygame.display.update()
        clock.tick(15)


def barrier(xlocation, randomHeight, barrierWidth):
    
    pygame.draw.rect(gameDisplay, black, [xlocation, display_height - randomHeight, barrierWidth, randomHeight]) # 50 is the pixel or thikness og the barrier

def explosion(x, y):

    pygame.mixer.Sound.play(exp_sound)

    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        startPoint = x,y
        colorChoice = [red, light_red, yellow, light_yellow] # a list of colors

        magnitude = 1 #make random circles while magnitude < 50
        while magnitude < 50: # 50 is the size of explosion
            exploding_bit_x = x + random.randint(-1*magnitude, magnitude) #exploding_bit_x are the small circles X postion when explode
            exploding_bit_y = y + random.randint(-1*magnitude, magnitude) #exploding_bit_y are the small circles X postion when explode

            pygame.draw.circle(gameDisplay, colorChoice[random.randrange(0,4)], (exploding_bit_x, exploding_bit_y), random.randrange(1,5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)
        explode = False
    
def fireShell(xy, tankx, tanky, turPos, gun_power, xlocation, randomHeight, barrierWidth, enemy_tankX, enemy_tankY): # xy values are returned from tank func, they are the location of x and y of the turret
    
    pygame.mixer.Sound.play(fire_sound) # it play fire sound wav file

    fire = True

    damage = 0

    gunPower = 0.015 / (gun_power/50) #this algo alow us to change our power as the power incr the gun shell incr and vis versa
    statrtingShell = list(xy) # we should convert it to list since xy are in list
    

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pygame.draw.circle(gameDisplay, red, (statrtingShell[0], statrtingShell[1]), 5)

        statrtingShell[0] -= (12 - turPos)*2 # to change the value of the X to the left so we - and (10 - ....) is to make space between the fire shell

        #quadratic equation : y = x^2
        statrtingShell[1] += int((((statrtingShell[0] - xy[0])*gunPower)**2) - (turPos + turPos / (12 - turPos)))

        if statrtingShell[1] > display_height - ground_height: #stop firing when fireshell hits the buttom of the display, 20 is the ground_height
            hit_x = int((statrtingShell[0] * display_height - ground_height)/statrtingShell[1]) #Place where X should explode
            hit_y = int(display_height - ground_height) #place where Y explode
            

            if enemy_tankX + 10 > hit_x > enemy_tankX - 10: #if the postion of X between these values then increase the damage by 25 
                print("Wonderful HIT!")
                damage = 25
            elif enemy_tankX + 15 > hit_x > enemy_tankX - 15: #if the postion of X between these values then increase the damage by 18 
                print("Hard HIT!")
                damage = 18
            elif enemy_tankX + 25 > hit_x > enemy_tankX - 25: #if the postion of X between these values then increase the damage by 10 
                print("Meduim HIT!")
                damage = 10
            elif enemy_tankX + 35 > hit_x > enemy_tankX - 35: #if the postion of X between these values then increase the damage by 5 
                print("Light HIT!")
                damage = 5

            explosion(hit_x, hit_y) #explosion of the Shell

            print("Impact: ", hit_x, hit_y)

            fire = False

        check_x_1 = statrtingShell[0] <= xlocation + barrierWidth #if X on the up right corner of the barrier
        check_x_2 = statrtingShell[0] >= xlocation # if X on the up surface of the barrier 

        check_y_1 = statrtingShell[1] <= display_height
        check_y_2 = statrtingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2: # call explosion function once the fireShell hits the barrier
            #print("Last Shell ", statrtingShell[0], statrtingShell[1])
            hit_x = int((statrtingShell[0])) #Place where X should explode
            hit_y = int(statrtingShell[1]) #place where Y explode

            explosion(hit_x, hit_y) #explosion of the Shell
            


            #print("Impact: ", hit_x, hit_y)

            fire = False


        pygame.display.update()
        clock.tick(60)
    return damage

def e_fireShell(xy, tankx, tanky, turPos, gun_power, xlocation, randomHeight, barrierWidth, pTankX, pTankY): # xy values are returned from tank func, they are the location of x and y of the turret
    
    pygame.mixer.Sound.play(fire_sound) # it play fire sound wav file
    currentPower = 1
    power_found = False

    damage = 0

    while not power_found:  # --------------the enemy will run first half until  (fire = False) looking for the proper power level is from 1 to 100 ------------
        currentPower += 1
        if currentPower > 100:
            power_found = True
        #print(currentPower)

        fire = True
        statrtingShell = list(xy) # we should convert it to list since xy are in list

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #pygame.draw.circle(gameDisplay, red, (statrtingShell[0], statrtingShell[1]), 5)

            statrtingShell[0] += (12 - turPos)*2 # X variaition of the shell for the enemy tank so we + since its on the left side X will increase 

            #quadratic equation : y = x^2
            statrtingShell[1] += int((((statrtingShell[0] - xy[0])*0.015/(currentPower/50))**2) - (turPos + turPos / (12 - turPos)))

            if statrtingShell[1] > display_height - ground_height: #stop firing when fireshell hits the buttom of the display, 20 is the ground_height
                hit_x = int((statrtingShell[0] * display_height - ground_height)/statrtingShell[1]) #Place where X should explode
                hit_y = int(display_height - ground_height) #place where Y explode
                #explosion(hit_x, hit_y) #explosion of the Shell
                

                if pTankX+15 > hit_x > pTankX-15:
                    #print("Target acquired!")
                    power_found = True
                fire = False 


                

            check_x_1 = statrtingShell[0] <= xlocation + barrierWidth #if X on the up right corner of the barrier
            check_x_2 = statrtingShell[0] >= xlocation # if X on the up surface of the barrier 

            check_y_1 = statrtingShell[1] <= display_height
            check_y_2 = statrtingShell[1] >= display_height - randomHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2: # call explosion function once the fireShell hits the barrier
                hit_x = int((statrtingShell[0])) #Place where X should explode
                hit_y = int(statrtingShell[1]) #place where Y explode
                #explosion(hit_x, hit_y) #explosion of the Shell
                fire = False


    fire = True #----------------when the enemy find the proper power level then he fire and use the currentPower he find up and from their he shot plyer tank
    statrtingShell = list(xy) # we should convert it to list since xy are in list
    

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.draw.circle(gameDisplay, red, (statrtingShell[0], statrtingShell[1]), 5)

        statrtingShell[0] += (12 - turPos)*2 # to change the value of the X to the left so we - and (10 - ....) is to make space between the fire shell

        #quadratic equation : y = x^2
        
        gun_power=random.randrange(int(currentPower *0.90), int(currentPower *1.10)) # random shot cause if we use only cuurentPower he will win the shot always

        statrtingShell[1] += int((((statrtingShell[0] - xy[0])*0.015/(gun_power/50))**2) - (turPos + turPos / (12 - turPos)))

        if statrtingShell[1] > display_height - ground_height: #stop firing when fireshell hits the buttom of the display, 20 is the ground_height
            hit_x = int((statrtingShell[0] * display_height - ground_height)/statrtingShell[1]) #Place where X should explode
            hit_y = int(display_height - ground_height) #place where Y explode

            if pTankX + 10 > hit_x > pTankX - 10: #if the postion of X between these values then increase the damage by 25 
                print(" Enemy Wonderful HIT!")
                damage = 25
            elif pTankX + 15 > hit_x > pTankX - 15: #if the postion of X between these values then increase the damage by 18 
                print("Enemy Hard HIT!")
                damage = 18
            elif pTankX + 25 > hit_x > pTankX - 25: #if the postion of X between these values then increase the damage by 10 
                print("Enemy Meduim HIT!")
                damage = 10
            elif pTankX + 35 > hit_x > pTankX - 35: #if the postion of X between these values then increase the damage by 5 
                print("Enemy Light HIT!")
                damage = 5

            
            explosion(hit_x, hit_y) #explosion of the Shell
            


            fire = False

        check_x_1 = statrtingShell[0] <= xlocation + barrierWidth #if X on the up right corner of the barrier
        check_x_2 = statrtingShell[0] >= xlocation # if X on the up surface of the barrier 

        check_y_1 = statrtingShell[1] <= display_height
        check_y_2 = statrtingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2: # call explosion function once the fireShell hits the barrier
            #print("Last Shell ", statrtingShell[0], statrtingShell[1])
            hit_x = int((statrtingShell[0])) #Place where X should explode
            hit_y = int(statrtingShell[1]) #place where Y explode

            explosion(hit_x, hit_y) #explosion of the Shell
            


            fire = False

        pygame.display.update()
        clock.tick(60)
    return damage #once this function called the it will return this value wich is damage



def fire(level):
    text = smallfont.render("Power: " +str(level) + " % ", True, black)
    gameDisplay.blit(text, [display_width /2, 0])

    
def message_to_screen(msg, color, y_displace=0, size='small'):
    if size == 'small':
        text_surf = smallfont.render(msg, True, color)
    elif size == 'medium':
        text_surf = medfont.render(msg, True, color)
    elif size == 'large':
        text_surf = largefont.render(msg, True, color)
    
    text_rect = text_surf.get_rect()
    text_rect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(text_surf, text_rect)

def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red


    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(gameDisplay, player_health_color, [680, 25, player_health, 25])
    pygame.draw.rect(gameDisplay, enemy_health_color, [20, 25, enemy_health, 25])

def game_over():
    game_over = True
    
    while game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            



            
        gameDisplay.fill(white)
        message_to_screen("Game Over!", red, -100, size='large')
        message_to_screen("You Died!", black, -30)
        
        #message_to_screen("Press C to play, P to pause or Q to quit", black, 180)

        
        button("play again", 150, 500, 100, 50, green, light_green, action="play")
        button("controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
        button("quit",550, 500, 100, 50, red, light_red, action="quit")

        

        pygame.display.update()
        clock.tick(15)

def you_win():
    win = True
    
    while win:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            



            
        gameDisplay.fill(white)
        message_to_screen("You Won!", green, -100, size='large')
        message_to_screen("Congratulations!", black, -30)
        
        #message_to_screen("Press C to play, P to pause or Q to quit", black, 180)

        
        button("play again", 150, 500, 100, 50, green, light_green, action="play")
        button("controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
        button("quit",550, 500, 100, 50, red, light_red, action="quit")

        

        pygame.display.update()
        clock.tick(15)


def gameLoop():
    gameExit = False
    gameOver = False
    FPS = 15

    mainTankX = display_width * 0.9 #its x postion on 90% of the Displaygame Width
    mainTankY = display_height * 0.9 #its x postion on 90% of the Displaygame Height
    tankMove = 0

    currentTurPos = 0
    changeTur = 0

    enemyTankX = display_width *0.1
    enemyTankY = display_height *0.9

    xlocation = (display_width/2) + random.randint(-0.1 * display_width, 0.1 * display_width) #0.2 is 20% of the display_width to draw the barrier
    randomHeight = random.randint(0.1 * display_height, 0.6 * display_height) # generate a random height for the barrier between 10% and 60% of the display height
    barrierWidth = 50

    fire_power = 50
    power_change = 0

    player_health = 100
    enemy_health = 100

    while not gameExit:  # If you want 'while false' functionality, you need 'not'

        
        
        if gameOver == True:
            message_to_screen('Game Over', red, -50, size = 'large')
            message_to_screen(' Press C to play again or Q to quit', black, 50, size = 'medium')
            message_to_screen(' Your Score: ' +str(snakeLength-1), black, 100, size = 'medium')
            pygame.display.update()  # every time you make a message you should then update the display
            
        while gameOver == True:
            #gameDisplay.fill(white)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():  # pygame.event.get() this func gets every event don by the user (Mouse, key press...)
            if event.type == pygame.QUIT:  # when the user close the window the type of event will be QUIT so if its QUIT then close the windows
                gameExit = True
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT:
                    tankMove = -5

                elif event.key == pygame.K_RIGHT:
                    tankMove = 5
                elif event.key == pygame.K_UP:
                    changeTur = 1
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                elif event.key == pygame.K_p: # if we press P key while game is running then the game will be 
                    paused()
                elif event.key == pygame.K_SPACE:
                    damage= fireShell(gun, mainTankX, mainTankY, currentTurPos, fire_power, xlocation, randomHeight, barrierWidth, enemyTankX, enemyTankY) #gun variable is returned from tank function
                    enemy_health -= damage

                    # Keep in mind that damage = func.... means that this func... returns a value and this value (damage) will be stored in damage variable
                    # Then we use this damage variable returned from a func... to use it in the mainLoop() : enemy_health -= damage
                    # We can name same variable twise if each variable (damage) is equals to differnt functions like damage = we use it twise
                    # damage = fireShell(....) means call this function and then return value of this func and store it in damage variable
                    
                    possibleMovment = ["f","r"]
                    movmentIndex = random.randrange(0,2) #generate random number 0,1 only, not 2

                    for x in range(random.randrange(0,10)):
                        if display_width *0.3 > enemyTankX > display_width *0.03: # if enemyTankX in range of 24 and 240 means less than 400 wich is width/2
                            if possibleMovment[movmentIndex] == "f": # means possibleMovment[0] 0 is randomly generated
                                enemyTankX += 5
                            elif possibleMovment[movmentIndex] == "r":
                                enemyTankX -= 5

                            gameDisplay.fill(white)  # change the color of our windows display from black to white
                            health_bars(player_health, enemy_health)
                            gun = tank(mainTankX, mainTankY, currentTurPos) #gun variable will help us to get the position of the turret (x and y) since tank func return xy of turret
                            enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8) # 8 is the 8th position of the turret list it is fixed 
                            fire_power += power_change
                            fire(fire_power)
                            barrier(xlocation, randomHeight, barrierWidth)
                            gameDisplay.fill(green, rect=[0, display_height - ground_height, display_width, ground_height]) # drawing the ground
                            pygame.display.update()
                            clock.tick(FPS)


                    damage = e_fireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, xlocation, randomHeight, barrierWidth, mainTankX, mainTankY) # this function to allow the enemy tank to fire so we can conclude once you fire then enemy tank will fire (in order)
                    player_health -= damage # dcrease the player healthonce it get shot
                    
                elif event.key == pygame.K_a: # decrease the power of the gun since it * by value in fireShell func in the quadratic equation
                    power_change = -1
                elif event.key == pygame.K_d: # increase the power of the gun since it * by value in fireShell func in the quadratic equation
                    power_change = 1
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0
            
        
        mainTankX += tankMove
        currentTurPos += changeTur

        if currentTurPos > 8: # this if to handle the range error once the tur exceed the list more than 8 since +1 or under 0 since -1
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 0

        if mainTankX - (tankWidth / 2) < xlocation + barrierWidth: # avoid the tank to move into the barrier
            mainTankX += 5 # 5 because we are moving the tank 5 (tankMove)
        if mainTankX + tankWidth >= display_width +20: # avoid the tank to move away from the gameDisplay
            mainTankX -= 5

        gameDisplay.fill(white)  # change the color of our windows display from black to white

        health_bars(player_health, enemy_health)

        gun = tank(mainTankX, mainTankY, currentTurPos) #gun variable will help us to get the position of the turret (x and y) since tank func return xy of turret

        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8) # 8 is the 8th position of the turret list it is fixed 

        fire_power += power_change

        if fire_power > 100 : #handle fire_power not more than 100% and less than 1%
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1

        fire(fire_power)
        
       
        barrier(xlocation, randomHeight, barrierWidth)

        gameDisplay.fill(green, rect=[0, display_height - ground_height, display_width, ground_height]) # drawing the ground
        
        pygame.display.update()

        if player_health < 1:
            game_over()
        elif enemy_health < 1:
            you_win()

        clock.tick(FPS)  # its the amount of frames per second (10 frames per second) # it forces the while loop to run each 15 second (FSP frame per second)

    pygame.quit()  # this will quit the pygame windows display
    quit()  # it quits the python code

game_intro()
gameLoop()

