import sys, pygame, math
pygame.init()
 
size = width, height = 1000, 1000
table = tablewidth, tableheight = 800, 450
friction = 0.992
 
#creates ball class
class Ball:
    vel = [0.00,0.00]
    pos = [20, 400]
    colour = "white"
    radius = 22
    name = ""
    type = ""
       
#coefficient of restitution
e = 0.9
 
#Initialises functions to handle vector math
 
def vadd(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]
 
def vsub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]
 
def vsmult(v1, scalar):
    return [v1[0] * scalar, v1[1] * scalar]
 
def vlength(v1):
    return math.sqrt(v1[0] * v1[0] + v1[1] * v1[1])
 
def vdot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]
 
#creates an empty list to store balls, and then creates and adds objects of the Ball class to the list
balls = list()
 
for i in range(16):
    balls.append(Ball())
 
 
#initialises 16 objects of the ball class
x = 0
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
    x += 1
 
 
 
 
#placeholder values for bug testing
 
balls[15].radius = 0
print(balls[15].radius)
balls[3].radius = -2
print(balls[15].radius)
print(balls[3].radius)
print(balls[1].radius)
 
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
 
    #Draws Snooker Table outline
   
    pygame.draw.rect(win, (39,134,39), (100, 100, tablewidth, tableheight), 0)
    pygame.draw.rect(win, (255, 0, 0), (100, 100, tablewidth, tableheight), 2)
    pygame.draw.rect(win, (0, 0, 0), (99, 99, tablewidth +2, tableheight +2), 1)
   
 
    #checks for collision, and updates speeds
    i = 0
    while i <= len(balls) - 1:
        j = i + 1
        while j <= len(balls) - 1:
        #finds a normal vector
            n = vsub(balls[i].pos, balls[j].pos)
        #finds the length between balls
            length = vlength(n)
            if length <= (balls[j].radius + balls[i].radius) and length >= 0.01:  
 
                #find a unit normal vector
                un = vsmult(n, 1/length)
 
                #find minimum translation distance
                mtd = vsmult(n, (balls[j].radius + balls[i].radius - length)/length)                
             
                #push and pull balls
                balls[i].pos = vadd(balls[i].pos, vsmult(mtd, 0.5))
                balls[j].pos = vsub(balls[j].pos, vsmult(mtd, 0.5))
           
                #find the unit tangent vector
                ut = [un[1] * -1, un[0]]
               
                #project velocities onto unit tangent and unit normal vectors
                v1n = vdot(un, balls[i].vel)
                v1t = vdot(ut, balls[i].vel)
                v2n = vdot(un, balls[j].vel)
                v2t = vdot(ut, balls[j].vel)
           
                #find new normal velocities
                v1nTag = v2n
                v2nTag = v1n
 
                #convert the scalar normal and tangential velocities into vectors
                v1nTag = vsmult(un, v1nTag)
                v1tTag = vsmult(ut, v1t)
                v2nTag = vsmult(un, v2nTag)
                v2tTag = vsmult(ut, v2t)
               
                #update velocities of ball objects
                balls[i].vel = vadd(v1nTag, v1tTag)
                balls[j].vel = vadd(v2nTag, v2tTag)
            j+=1
        i+=1
   
   
 
 
 
    i = 0
    while i <= len(balls) - 1:
        #checks if balls are going out of bounds and updates speeds with v=-eu
        if balls[i].pos[0] > (100 + tablewidth) - balls[i].radius:
            balls[i].vel[0] = balls[i].vel[0] * -1 * e
        if balls[i].pos[0] < 100 + balls[i].radius:
            balls[i].vel[0] = balls[i].vel[0] * -1 * e
        if balls[i].pos[1] > (100 + tableheight) - balls[i].radius:
            balls[i].vel[1] = balls[i].vel[1] * -1 * e
        if balls[i].pos[1] < 100 + balls[i].radius:
            balls[i].vel[1] = balls[i].vel[1] * -1 * e
           
        #updates positions of balls
        balls[i].pos = vadd(balls[i].pos, balls[i].vel)
 
        #applies friction to balls speed
        balls[i].vel = vsmult(balls[i].vel, friction)
       
        #renders balls
        pygame.draw.circle(win, (255, 255, 255), (int(balls[i].pos[0]), int(balls[i].pos[1])), balls[i].radius)
        i+=1
    pygame.display.update()
 
 
pygame.quit




