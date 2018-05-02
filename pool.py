import sys, pygame
pygame.init()

size = width, height = 1000, 1000

#creates ball class
class Ball:
    mass = 1.00
    speed = 0.00
    colour = "white"
    radius = 25
    name = ""
    type = ""
    xpos = 20
    ypos = 490
    
    
    def properties(self):
        properties = "Ball " + str(self.name) + " has a mass of " + str(self.mass) + " and a speed of " + str(
            self.speed) + ". It is a " + str(self.type) + " ball of colour " + str(self.colour)
        return properties

#creates an empty list to store balls, and then creates and adds objects of the Ball class to the list
balls = list()

for i in range(16):
    balls.append(Ball())
    
#coefficient of restitution
e = 0.7

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

#calculates collision between 2 objects, returning final speeds
def collision(u1, u2, m1, m2):
    momentum = float(u1 * m1) + float(u2 * m2)

    v1 = (float(momentum) - float(float(e) * float(m2) * ((float(u1) - float(u2))))) / (float(m1) * float(m2))
    v2 = (float(momentum) - float(v1) * float(m1)) / float(m2)
    return [v1, v2]

#placeholder values for bug testing
balls[1].xpos = 500
balls[0].speed = 5
balls[1].radius = 25

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

    #draws first ball
    pygame.draw.circle(win, (255, 255, 255), (int(balls[0].xpos), int(balls[0].ypos)), balls[0].radius)
    #draws second ball
    pygame.draw.circle(win, (255, 0, 0), (int(balls[1].xpos), int(balls[1].ypos)), balls[1].radius)

    #updates positions of balls
    balls[1].xpos = balls[1].xpos + balls[1].speed
    balls[0].xpos = balls[0].xpos + balls[0].speed

    #checks for collision, and updates speeds
    if balls[1].xpos - balls[0].xpos <= balls[1].radius + balls[2].radius:
        finalspeeds = collision(float(balls[0].speed), float(balls[1].speed), float(balls[0].mass),float(balls[1].mass))
        balls[0].speed = finalspeeds[0]
        balls[1].speed = finalspeeds[1]

    #checks if balls are going out of bounds and updates speeds with v=-eu
    if balls[1].xpos > width - balls[1].radius:
        balls[1].speed = balls[1].speed * -1 * e
    if balls[1].xpos < 0 + balls[1].radius:
        balls[1].speed = balls[1].speed * -1 * e

    if balls[0].xpos < 0 + balls[0].radius:
        balls[0].speed = balls[0].speed * -1 * e
    if balls[0].xpos > width - balls[0].radius:
        balls[0].speed = balls[0].speed * -1 * e

    #"friction"
    if balls[1].speed > 0:
        balls[1].speed -= 0.01
    if balls[0].speed > 0:
        balls[0].speed -= 0.01
    
    pygame.display.update()




            
pygame.quit




#menu to allow manual changing and viewing of properties of balls
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
        balls[ball].speed = input("Enter the new speed of the ball:")
        balls[ball].mass = input("Enter the new mass of the ball:")
        menu()

    if selection == "3":
        e = input("Enter the coefficient of restitution:")
        menu()

    if selection == "4":
        ball1 = int(input("Please enter the first ball in the collision")) - 1
        ball2 = int(input("Please enter the second ball in the collision")) - 1
        print("These are the properties of the balls after the collision:")
        finalspeeds = collision(float(balls[ball1].speed), float(balls[ball2].speed), float(balls[ball1].mass),
                                    float(balls[ball2].mass))
        balls[ball1].speed = finalspeeds[0]
        balls[ball2].speed = finalspeeds[1]
        print(balls[ball1].properties())
        print(balls[ball2].properties())
        menu()

#menu() menu function is not called as it is mainly for debugging purposes


