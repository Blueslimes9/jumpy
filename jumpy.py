import pygame, random

#init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((480, 800))
clock = pygame.time.Clock()
running = True

#window info
pygame.display.set_caption("Jumpy")
icon = pygame.image.load("player.ico")
pygame.display.set_icon(icon)

#constants/other variables
global defFont, cloudI, playerI, coinI, dt, camY, clouds, plats, dif, playerHB
#fonts
defFont = pygame.font.Font(None, 30)
titleFont = pygame.font.Font("Rubik.ttf", 120)
smallerFont = pygame.font.Font("Rubik.ttf", 50)
#images
groundI = pygame.image.load("ground.png")
cloudI = pygame.image.load("cloud.png")
playerI = pygame.image.load("player.png")
coinI = pygame.image.load("coin.png")
platformI = pygame.image.load("platform.png")
#var
dt = 1
FPS = 60
camY = 0
playerX = 215
playerY = 650
playerXVel = 0
playerYVel = 0
playing = False
a = False
d = False
dif = 0
loss = 0
deathPlayed = False
#sounds
jumpSnd = pygame.mixer.Sound("jump.wav")
coinSnd = pygame.mixer.Sound("coin.wav")
deathSnd = pygame.mixer.Sound("death.wav")

#classes
class cloud():
	def __init__(self, y,):
		self.y = y
		if round(random.random()) == 1:
			self.x = -332
			self.vel = random.random()
		else:
			self.x = 480
			self.vel = random.random()*-1

	def upPos(self):
		if self.x < -340:
			self.x = 480
		elif self.x > 490:
			self.x = -332
		
		self.x = self.x + (self.vel*dt)
		screen.blit(cloudI, (self.x, self.y))
		
		self.y = self.y + (dif*0.2)
		
		if self.y > 850:
			del clouds[0]
		
class platform():
	def __init__(self, y, type):
		self.y = y
		self.x = random.random()*480-50
		self.type = type
		
	def upPos(self):
		self.y = self.y + dif
		self.hb = pygame.Rect(self.x, self.y, 100, 20)
		pygame.draw.rect(screen, (255, 0, 0), self.hb)
		screen.blit(platformI, (self.x, self.y))
		if self.y > 820:
			del plats[0]

class coin():
	def __init__(self, y, x):
		self.y = y
		self.x = x+60
		self.collide = False
	
	def upPos(self):
		screen.blit(coinI, (self.x-5, self.y-5))

		
	def draw(self):
		self.y = self.y + dif
		self.hb = pygame.Rect(self.x, self.y, 20, 20)
		pygame.draw.rect(screen, (255, 0, 0), self.hb)
		self.collide = self.hb.colliderect(playerHB)
		if self.y > 820:
			del coins[0]
	
def	ini():
	global nextCloud, nextPlat, nextCoin, clouds, plats, coins, coinscore
	coinscore = 0
	#init clouds
	clouds = [cloud(200)]
	nextCloud = 500

	#init platforms
	plats = [platform(500, 0), platform(250, 0), platform(30, 0)]
	plats[0].x = 190
	nextPlat = 250

	#init coins
	coins = [coin(400, 230)]
	nextCoin = 750

ini()

#main loop
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
				running = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				a = True
			if event.key == pygame.K_d:
				d = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				a = False
			if event.key == pygame.K_d:
				d = False
				
	
	if playing == False:
		if a == True or d == True:
			playing = True
			playerYVel = 7

	#player pos
	if a:
		if playerXVel > -5:
			playerXVel = playerXVel - 0.35
	elif d:
		if playerXVel < 5:
			playerXVel = playerXVel + 0.35
	else:
		if playerXVel > 0:
			playerXVel = playerXVel - 0.15
		elif playerXVel < 0:
			playerXVel = playerXVel + 0.15
	
	if abs(playerXVel) < 0.1:
		playerXVel = 0
	
	if playing == True:
		playerYVel = playerYVel-(0.1*dt)
	
	playerX = playerX+(playerXVel*dt)
	playerY = playerY-(playerYVel*dt)
	if playerY < 400:
		dif = ((playerY-400)*-1)
		camY = camY + dif
		playerY = 400
	else:
		dif = 0	
	
	#hitboxes
	playerHB = pygame.Rect(playerX, playerY, 50, 50)
	pygame.draw.rect(screen, (255, 0, 0), playerHB)
	
	for x in coins:
		x.draw()
	
	screen.fill((50, 137, 168))
	
	#render ground
	if camY < 150:
		screen.blit(groundI, (0, camY))
	
	#clouds
	if camY > nextCloud:
		clouds.append(cloud(-50))
		nextCloud = camY + (4000 + random.random()*1000)
	for x in clouds:
		x.upPos()

	#render title
	if camY < 750:
		text = titleFont.render("Jumpy", True, (77, 178, 232))
		screen.blit(text, (50, 50+camY))
	
	#platforms
	if camY > nextPlat:
		plats.append(platform(-25, 0))
		nextPlat = camY + (150 + random.random()*100)
	for x in plats:
		x.upPos()
		
	#render player
	screen.blit(playerI, (playerX, playerY))
	
	#coins
	if camY > nextCoin:
		coins.append(coin(-10, plats[1].x))
		nextCoin = camY + (500 + random.random()*400)
	for x in coins:
		x.upPos()
		if x.collide == True:
			coins.remove(x)
			coinSnd.play()
			coinscore = coinscore+1
	
	#collisions
	if playerYVel < 0:
		for obj in plats:
			if playerHB.colliderect(obj.hb):
				playerYVel = 7
				jumpSnd.play()
				
	#loss detection
	if playerY > 830:
		loss = loss+1*dt
	
		text = titleFont.render("You Lost!", True, (0, 0, 0))
		screen.blit(text, (0, 50))
		
		if coinscore == 1:
			cointxt = " Coin"
		else:
			cointxt = " Coins"
		
		text = smallerFont.render("You Had " + str(coinscore) + cointxt, True, (0, 0, 0))
		screen.blit(text, (50, 200))
		
		
		if not deathPlayed:
			deathSnd.play()
			deathPlayed = True
		if loss > 240:
			playing = False
			playerX = 215
			playerY = 650
			playerXVel = 0
			playerYVel = 0
			camY = 0
			ini()
			loss = 0
			deathPlayed = False

	#fps/delta
	fps = str(round(clock.get_fps()))
	text = defFont.render(fps, True, (255, 0, 0))
	screen.blit(text, (0, 0))

	pygame.display.flip()

	dt = clock.tick(FPS)/10
	
	
pygame.quit()