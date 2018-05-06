import sys, pygame, math
pygame.init()

size = width, height = 1000, 1000
table = tablewidth, tableheight = 800, 450
friction = 0.992

#creates ball class
class Ball:
    mass = 1.00
    xspeed = 0.00
    yspeed = 0.00
    colour = "white"
    radius = 25
    name = ""
    type = ""
    xpos = 20
    ypos = 400
    
    
    def properties(self):
        properties = "Ball " + str(self.name) + " has a mass of " + str(self.mass) + " and a xspeed of " + str(
            self.xspeed) + ". It is a " + str(self.type) + " ball of colour " + str(self.colour)
        return properties

#creates an empty list to store balls, and then creates and adds objects of the Ball class to the list
balls = list()

for i in range(16):
    balls.append(Ball())
    
#coefficient of restitution
e = 0.9

#iteration variable
x = 0

#initialises 16 objects of the ball class
while x <= 15:
    if x == 0:
        balls[x].name = "cue"
        balls[x].type = "cue ball"
    if x == 1:
        balls[x].name = "8"
        balls[x].type = "8 ball"
    if (x % 2) == 0 & x != 1 & x != 0:
        balls[x].name = str(x - 1)
        balls[x].type = "solid"
    if (x % 2 == 1) & x != 1 & x != 0:
        balls[x].name = str(x - 2)
        balls[x].type = "striped"
    balls[x].xpos = 61 * x
    balls[x].ypos = 400 + 10 * (x % 3)
    x += 1

#calculates collision between 2 objects, returning final xspeeds
def collision(u1, u2, m1, m2):

    v2 = (m1 * u1 + m2 * u2 - m1 * e * u1 + m1 * e * u2)/(m1 + m2)
    v1 = e * (u1 - u2) + v2
    return [v1, v2]




#placeholder values for bug testing

balls[3].xspeed = 1000
balls[3].yspeed = 1000

#pygame rendering
win = pygame.display.set_mode((width, height))
pygame.font.init()
pygame.display.set_caption("Pool")
myfont = pygame.font.SysFont('Comic Sans MS', 20)
textsurface = myfont.render('8', False, (0, 0, 0))

run = True
while run:
    win.fill((32,32,32))
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Draws Snooker Table
    
    pygame.draw.rect(win, (39,134,39), (100, 100, tablewidth, tableheight), 0)
    pygame.draw.rect(win, (255, 0, 0), (100, 100, tablewidth, tableheight), 2)
    pygame.draw.rect(win, (0, 0, 0), (99, 99, tablewidth +2, tableheight +2), 1)
    

    #checks for collision, and updates speeds
    i = 0
    while i <= 15:
        j = i + 1
        while j <= 15:
            if math.sqrt((balls[j].xpos - balls[i].xpos)**2 +(balls[j].ypos - balls[i].ypos)**2) <= (balls[j].radius + balls[i].radius):  
                vspeed1 = math.sqrt((balls[j].xspeed **2) + (balls[j].yspeed **2))
                vspeed0 = math.sqrt((balls[i].xspeed **2) + (balls[i].yspeed **2))

                #vspeed1 = math.degrees(math.atan(balls[j].yspeed / balls[j],xspeed))
                #vspeed0 = math.degrees(math.atan(balls[i].yspeed / balls[i],xspeed)) 
                
                angle = math.degrees(math.atan((balls[j].ypos - balls[i].ypos)/(balls[j].xpos - balls[i].xpos)))
        
                finalspeeds = collision(float(vspeed0), float(vspeed1), float(balls[j].mass),float(balls[i].mass))
                if balls[j].xspeed < 0:
                    balls[j].xspeed = finalspeeds[0] * (math.cos(angle)) * -1
                else:
                    balls[j].xspeed = finalspeeds[0] * (math.cos(angle))

                if balls[i].xspeed < 0:
                    balls[i].xspeed = finalspeeds[1] * (math.sin(angle)) * -1
                else:
                    balls[i].xspeed = finalspeeds[1] * (math.sin(angle))

                if balls[j].yspeed > 0:
                    balls[j].yspeed = finalspeeds[0] * (math.sin(angle)) 
                elif balls[j].yspeed >= 0:
                    balls[j].yspeed = finalspeeds[0] * (math.sin(angle)) * -1
                if balls[i].yspeed > 0:
                    balls[i].yspeed = finalspeeds[1] * (math.cos(angle)) 
                elif balls[i].yspeed >= 0:
                    balls[i].yspeed = finalspeeds[1] * (math.cos(angle)) * -1
                
            j+=1
        i+=1
    
    


 
    i = 0
    while i <= 15:
        #checks if balls are going out of bounds and updates speeds with v=-eu
        if balls[i].xpos > (100 + tablewidth) - balls[i].radius:
            balls[i].xspeed = balls[i].xspeed * -1 * e
        if balls[i].xpos < 100 + balls[i].radius:
            balls[i].xspeed = balls[i].xspeed * -1 * e
        if balls[i].ypos > (100 + tableheight) - balls[i].radius:
            balls[i].yspeed = balls[i].yspeed * -1 * e
        if balls[i].ypos < 100 + balls[i].radius:
            balls[i].yspeed = balls[i].yspeed * -1 * e
            
        #updates positions of balls
        balls[i].xpos = balls[i].xpos + balls[i].xspeed
        balls[i].ypos = balls[i].ypos + balls[i].yspeed
    
        #applies friction to balls speed
        balls[i].xspeed *= friction
        balls[i].yspeed *= friction

        #renders balls
        pygame.draw.circle(win, (255, 255, 255), (int(balls[i].xpos), int(balls[i].ypos)), balls[i].radius)
        i+=1
    pygame.display.update()


pygame.quit




##menu to allow manual changing and viewing of properties of balls
def menu():
    print("1: View the properties of a ball")
    print("2: Change the properties of a ball")
    print("3: Change the coefficient of restitution")
    print("4: Simulate collision between two balls")
    selection = input("Please select an option:")

    if selection == "1":
        ball = int(input("Which ball would you like to view?")) - 1
        print(balls[ball].properties())
        menu()

    if selection == "2":
        ball = int(input("Which ball would you like to change the properties of?")) - 1
        balls[ball].xspeed = input("Enter the new xspeed of the ball:")
        balls[ball].mass = input("Enter the new mass of the ball:")
        menu()

    if selection == "3":
        e = input("Enter the coefficient of restitution:")
        menu()

    if selection == "4":
        ball1 = int(input("Please enter the first ball in the collision")) - 1
        ball2 = int(input("Please enter the second ball in the collision")) - 1
        print("These are the properties of the balls after the collision:")
        finalxspeeds = collision(float(balls[ball1].xspeed), float(balls[ball2].xspeed), float(balls[ball1].mass),
                                    float(balls[ball2].mass))
        balls[ball1].xspeed = finalxspeeds[0]
        balls[ball2].xspeed = finalxspeeds[1]
        print(balls[ball1].properties())
        print(balls[ball2].properties())
        menu()

#menu() menu function is not called as it is mainly for debugging purposes







