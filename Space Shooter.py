
import os
import random
import turtle
import math
import time

turtle.speed(0)
turtle.bgcolor('black')
#turtle.bgpic('starf.gif')
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)




#Function for the tutorial message at beginning of game
def pop_up():
    gd.write(' Space bar to shoot\n Use Left and Right arrow keys to turn the ship\n Use Up and Down arrow keys to increase or decrease speed\n Red enemy: send out a fast scout to hunt player\n Blue enemy: teleport player to random location\n Yellow enemy: explode into fragments that damages player\n PRESS ANY ARROW KEYS TO HIDE THIS MESSAGE   ', align = 'center', font = ('Courier', 10, 'normal'))


#Create a sub-class of Turtle objects called Sprites
class Sprite(turtle.Turtle):
    #initialize Sprite object
    def __init__(self, spriteshape,color,startx,starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1
    #Any sub-class of Sprite later will inherit these functions
    #function for auto moving forward
    def move(self):
        self.fd(self.speed)

    #Check collision with border
        if self.xcor() > 290 :
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290 :
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290 :
            self.sety(290)
            self.rt(60)
        if self.ycor() <- 290 :
            self.sety(-290)
            self.rt(60)

    #function to check collision between 2 objects, using pythagorean
    def isCollision(self,other):
        d = math.sqrt(((self.xcor() - other.xcor())**2) + ((self.ycor() - other.ycor())**2) )
        if d < 20 :
            return True
        else:
            return False


#Create a sub-class of Sprite objects called players
class Player(Sprite):
    #initialize Player object
    def __init__(self, spriteshape,color,startx,starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 1
        self.lives = 3
    #function for controlling movement of player
    def turn_left(self):
        self.lt(30)
        gd.clear() #clear the tutorial message when a key is pressed
    def turn_right(self):
        self.rt(30)
        gd.clear()
    def accelerate(self):
        self.speed += 1
        gd.clear()
    def decelerate(self):
        self.speed -= 1
        gd.clear()
    
#Create sub-class of Sprite called Enemy
class Enemy(Sprite):
    #initialize Enemy object
    def __init__(self, spriteshape,color,startx,starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 2
        self.setheading(random.randint(0,360))

#Create sub-class of Sprite called Particle for explosion effect
class Particle(Sprite):
    #initialize Particle object
    def __init__(self, spriteshape,color,startx,starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.1, stretch_len = 0.1, outline = None)
        self.goto(-1000,-1000)
        self.frame = 0

    #Function for exploding enemy, sending particles over enemy's location and randomize each particle's moving direction
    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1
        
    #function to make particles move straight then dissapear until certain frame is reached
    def move(self):
        if self.frame > 0 : #move straight forward
            self.fd(10)
            self.frame += 1
        if self.frame > 10: #disable once reached maximum frame
            self.frame = 0
            self.goto(-1000,-1000)

#Similar to Particles but for unique type of enemy, when exploded, those fragments can damage players
class fragments(Sprite):
    #initialize Particle object
    def __init__(self, spriteshape,color,startx,starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.5, stretch_len = 0.5, outline = None)
        self.goto(-1000,-1000)
        self.frame = 0

    def breaking(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1
        
    
    def move(self):
        if self.frame > 0 :
            self.fd(10)
            self.frame += 1
            if self.isCollision(player): #check if fragment overlap with player, if yes lower player's lives
                #time.sleep(1)
                game.lives -= 1
                game.show_status()
                player.goto(0,0)
                self.frame = 15 #once damaged player, this fragment need to dissapear to prevent multiple damaging events in short time
            
        if self.frame > 15:
            self.frame = 0
            self.goto(-1000,-1000)


#Create sub-class of Sprite called scouts
class scouts(Sprite):
    #initialize scout object
    def __init__(self, spriteshape,color,startx,starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.8, stretch_len = 0.8, outline = None)
        self.goto(-1000,-1000)
        self.frame = 0

    #sending out scout once defeated
    def scouting(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1
        
        
    
    def move(self):
        if self.frame > 0 :
            self.fd(10)
            self.frame += 1
        if self.frame > 150: # maximum frame that scout can hunt player until it dissapears
            self.frame = 0
            self.goto(-1000,-1000)
    
    #Check collision with border(different rotation from normal enemy)
        if self.xcor() > 290 :
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290 :
            self.setx(-290)
            self.lt(60)
        if self.ycor() > 290 :
            self.sety(290)
            self.lt(60)
        if self.ycor() <- 290 :
            self.sety(-290)
            self.lt(60)
    
    
        
    

#Create sub-class of Sprite called Missile, this is player's weapon
class Missile(Sprite):
    #initialize Enemy object
    def __init__(self, spriteshape,color,startx,starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.3, stretch_len = 0.3, outline = None)
        self.speed = 10
        self.status = 'ready'
        self.goto(-1000,1000)

    #function to fire the missile by sending it to player's location then pointing in player's heading direction
    def fire(self):
        if self.status == 'ready':
            self.setheading(player.heading())
            self.goto(player.xcor(), player.ycor())
            self.status = 'firing'



    def move(self):
        if self.status == 'ready':
            self.goto(-1000,1000)

        if self.status == 'firing':
            self.fd(self.speed)
        
        #check collision with border, reset the missile if reached border
        if self.xcor() < -290 or self.xcor() > 290 or\
            self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000,1000)
            self.status = 'ready'



        



#Create class to handle game-events
class Game():
    #initializing game object
    def __init__(self):
        self.level = 1 #not needed now, but in case when create multiple levels
        self.score = 0 #starting score
        self.h_score = 0
        self.state = 'playing'
        self.pen = turtle.Turtle()
        self.lives = 3 #amount of lives player has
    
    #Create the border that limit all events and objects in the game
    def draw_border(self): 
        self.pen.speed(0)
        self.pen.color('white')
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300) #starting location of the pen
        self.pen.pendown()
        for side in range(4):
            self.pen.forward(600) #using the pen to draw a rectangular zone
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    #function to display the score and lives on top of the border
    def show_status(self):
        self.pen.undo()
        sc ='Score: %s' %(self.score)
        h_sc ='High Score: %s' %(self.h_score)
        lvs = 'Lives: %s' %(self.lives)
        self.pen.penup()
        self.pen.goto(-300,310)
        self.pen.write(sc + h_sc + lvs, font = ('Arial', 16, 'normal'))


#Calling functions to create objects

#Create game object
game = Game()

#Draw game border
game.draw_border()

#Show the game status
game.show_status()

#Create all objects inside the border
player = Player('turtle', 'green', 0 ,0 )
scout = scouts('turtle', 'purple', 0 ,0 )
missile = Missile('circle', 'yellow', 0, 0)
#for visual effect when killing enemy
particles = []
for i in range(20):
    particles.append(Particle('circle', 'orange', 0, 0))
#for bigger fragments when certain enemy die
bullets = []
for i in range (10):
    bullets.append(fragments('circle', 'khaki', 0, 0))

#creating multiple enemies
enemy1 = Enemy('circle', 'red', -100, 0)
enemy2 =Enemy('circle', 'blue', -100, 0)
enemy3 =Enemy('circle', 'khaki', -100, 0)
enemies = [enemy1,enemy2,enemy3]
#for i in range(3):
    #enemies.append(Enemy('circle', 'grey', -100, 0))


#Keyboard bindings
turtle.listen()
turtle.onkey(player.turn_left, 'Left' )
turtle.onkey(player.turn_right, 'Right' )
turtle.onkey(player.accelerate, 'Up' )
turtle.onkey(player.decelerate, 'Down' )
turtle.onkey(missile.fire, 'space' )



#Writing the tutorial/guide
gd = turtle.Turtle()
gd.speed(0)
gd.shape('square')
gd.color('white')
gd.penup()
gd.hideturtle()
gd.goto(0,-290)
pop_up() #create the instruction message once at the beginning of the game








while True: 
    turtle.update() #update each frame without using tracer
    time.sleep(0.01) #set speed of the game/animation


    #check event if player run out of lives
    if game.lives <=0:
        time.sleep(1)
        pop_up()
        #game.gameover()
        #resetting player,enemies,scores and lives
        player.goto(0,0)
        game.lives = 3
        game.score = 0
        game.show_status()
        scout.goto(-1000,-1000)
        for enemy in enemies:
            enemy.goto(-100,0)

    # Making objects move
    missile.move()
    scout.move()
    player.move()
    for particle in particles:
        particle.move()
    for fragment in bullets:
        fragment.move()

    #Loop for interaction with enemies
    for enemy in enemies:
        enemy.move()
        #Check for missile collision with enemy
        if missile.isCollision(enemy):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y) #re-spawn enemy at random location
            missile.status ='ready'
            #Increase score
            game.score += 100
            if game.score >= game.h_score:
                game.h_score = game.score
            game.show_status()

            #explosion and special trait from each enemy type
            
            if enemy.color()[0] == 'red':
                scout.scouting(missile.xcor(), missile.ycor())
                for particle in particles:
                    particle.explode(missile.xcor(), missile.ycor())
            if enemy.color()[0] == 'blue':
                x = random.randint(-250,250)
                y = random.randint(-250,250)
                player.goto(x,y)
                for particle in particles:
                    particle.explode(missile.xcor(), missile.ycor())
            if enemy.color()[0] == 'khaki':
                for fragment in bullets:
                    fragment.breaking(missile.xcor(), missile.ycor())
            if enemy.color()[0] == 'grey':
                #scout.scouting(missile.xcor(), missile.ycor())
                for particle in particles:
                    particle.explode(missile.xcor(), missile.ycor())
                     


        #check if player hit enemy 
        if player.isCollision(enemy):
           
            game.lives -= 1
            game.show_status()
            player.goto(0,0)
            
    
    #check if player hit scout
    if player.isCollision(scout):
        game.lives -=1
        game.show_status()
        x = random.randint(-250,250)
        y = random.randint(-250,250)
        scout.goto(x,y)
        player.goto(0,0)
       


wd.mainloop()
