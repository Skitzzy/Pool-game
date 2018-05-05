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
    ypos = 490
    
    
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
while x < 15:
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
    x += 1

#calculates collision between 2 objects, returning final xspeeds
def collision(u1, u2, m1, m2):

    v2 = (m1 * u1 + m2 * u2 - m1 * e * u1 + m1 * e * u2)/(m1 + m2)
    v1 = e * (u1 - u2) + v2
    return [v1, v2]




#placeholder values for bug testing
balls[1].xpos = 500
balls[1].ypos = 400
balls[0].xspeed = 10
balls[1].radius = 25
balls[0].xpos = 200
balls[0].yspeed = -2

#pygame rendering
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pool")

run = True
while run:
    win.fill((39,134,39))
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Draws Snooker Table
    pygame.draw.rect(win, (255, 0, 0), (100, 100, tablewidth, tableheight), 2)
    pygame.draw.rect(win, (0, 0, 0), (99, 99, tablewidth +2, tableheight +2), 1)
    
    #draws first ball
    pygame.draw.circle(win, (255, 255, 255), (int(balls[0].xpos), int(balls[0].ypos)), balls[0].radius)
    #draws second ball
    pygame.draw.circle(win, (255, 0, 0), (int(balls[1].xpos), int(balls[1].ypos)), balls[1].radius)

    #x = 0
    #while x < 15:
        


    #checks for collision, and updates speeds
    if math.sqrt((balls[1].xpos - balls[0].xpos)**2 +(balls[1].ypos - balls[0].ypos)**2) <= (balls[1].radius + balls[0].radius):  
        finalxspeeds = collision(float(balls[0].xspeed), float(balls[1].xspeed), float(balls[0].mass),float(balls[1].mass))
        balls[1].xspeed = finalxspeeds[0]
        balls[0].xspeed = finalxspeeds[1]
        finalyspeeds = collision(float(balls[0].yspeed), float(balls[1].yspeed), float(balls[0].mass),float(balls[1].mass))
        balls[1].yspeed = finalyspeeds[0]
        balls[0].yspeed = finalyspeeds[1]
        

    #checks if balls are going out of bounds and updates speeds with v=-eu
    if balls[1].xpos > (100 + tablewidth) - balls[1].radius:
        balls[1].xspeed = balls[1].xspeed * -1 * e
    if balls[1].xpos < 100 + balls[1].radius:
        balls[1].xspeed = balls[1].xspeed * -1 * e
    if balls[1].ypos > (100 + height) - balls[1].radius:
        balls[1].yspeed = balls[1].yspeed * -1 * e
    if balls[1].ypos < 100 + balls[1].radius:
        balls[1].yspeed = balls[1].yspeed * -1 * e

    if balls[0].xpos < 100 + balls[0].radius:
        balls[0].xspeed = balls[0].xspeed * -1 * e
    if balls[0].xpos > (100 + tablewidth) - balls[0].radius:
        balls[0].xspeed = balls[0].xspeed * -1 * e
    if balls[0].ypos < 100 + balls[0].radius:
        balls[0].yspeed = balls[0].yspeed * -1 * e
    if balls[0].ypos > (100 + tableheight) - balls[0].radius:
        balls[0].yspeed = balls[0].yspeed * -1 * e

    #updates positions of balls
    balls[1].xpos = balls[1].xpos + balls[1].xspeed
    balls[0].xpos = balls[0].xpos + balls[0].xspeed
    
    balls[1].ypos = balls[1].ypos + balls[1].yspeed
    balls[0].ypos = balls[0].ypos + balls[0].yspeed
    

    #friction"

    balls[1].xspeed *= friction
    balls[1].yspeed *= friction

    balls[0].xspeed *= friction
    balls[0].yspeed *= friction
    
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



