import pygame, sys, random

#game variables
player = 0
game_active = True
board = [[3,3,3,3,3,3,3],
		 [3,3,3,3,3,3,3],
		 [3,3,3,3,3,3,3],
		 [3,3,3,3,3,3,3],
		 [3,3,3,3,3,3,3],
		 [3,3,3,3,3,3,3]]
stone_list = []
fall_list = []
error = False
turn = 0



#initiate pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1024,840))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('Comic Sans MS',64)
small_font = pygame.font.SysFont('Comic Sans MS',40)

#loading assets
bg_surface = pygame.image.load('assets/Background.png').convert()
board_surface = pygame.image.load('assets/Board.png').convert_alpha()
stone0_surface = pygame.image.load('assets/Stone0.png').convert_alpha()
stone1_surface = pygame.image.load('assets/Stone1.png').convert_alpha()
icon_surface = pygame.image.load('assets/Icon.png').convert_alpha()

#changing icon
pygame.display.set_icon(icon_surface)

#loading sounds
win_sound = pygame.mixer.Sound('sound/Win.wav')
error_sound = pygame.mixer.Sound('sound/Error.wav')

#game logic
def play(key):
	global error, player, board, stone_list, game_active, turn;
	for x in range(6):
		if board[x][key] == 3:			
			board[x][key] = player
			pos = (90*key+207,-80*x+678)
			begin = (90*key+207, 153)
			fall_list.append(fallingStone(player, begin, pos))
			#stone_list.append(Stone(player, pos))
			if winner(board):
				win_sound.play()				
				game_active = False
				break;
			player = (player+1) % 2
			error = False
			turn += 1
			break;
		if x == 5 :
			error = True
			error_sound.play()
	return

#finding Winner
def winner(board):
	#horizontal
	for row in board:
		for i in range(4):
			if row[i] == row[i+1] == row[i+2] == row[i+3] != 3:
				return True
    #vertical
	for i in range(7):
		for j in range(3):
			if board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] != 3:
				return True
	#diagonal pos
	for i in range(3):
		for j in range(4):
			if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] != 3:
				return True
	#diagonal neg
	for i in range(3):
		for j in range(4):
			if board[i][j+3] == board[i+1][j+2] == board[i+2][j+1] == board[i+3][j] != 3:
				return True
	if turn == 41:
		return True
	return False


#adding stone
def Stone(player, pos):
	new_Stone = stone1_surface.get_rect(topleft = pos)
	return new_Stone , player

def fallingStone(player, begin, pos):
	new_Stone = stone1_surface.get_rect(topleft = begin)
	return new_Stone, player, pos

#displaying stones
def draw_stones(stone_list):
	for stone in stone_list:
		if stone[1] == 0:
			screen.blit(stone0_surface, stone[0])
		else:
			screen.blit(stone1_surface, stone[0])

#display falling strones and adding pos
def draw_fall(fall_list):
	global stone_list;
	if game_active == False:
		for stone in fall_list:
			stone_list.append(Stone(stone[1], stone[2]))
			fall_list.remove(stone)
	for stone in fall_list:
		if stone[1] == 0:
			screen.blit(stone0_surface, stone[0])
		else:
			screen.blit(stone1_surface, stone[0])
		stone[0][1] += 10;
		if stone[0][1]>=stone[2][1]:
			stone_list.append(Stone(stone[1], stone[2]))
			fall_list.remove(stone)


#displaying text
def text(message, pos):
	text_surface = game_font.render(message,True,(255,255,255))
	text_rect = text_surface.get_rect(center = pos)
	screen.blit(text_surface,text_rect)

def reset():
	global error, board, stone_list, game_active, player, turn;
	error = False
	turn = 0
	fall_list = []
	stone_list=[]
	game_active=True
	player = (player+1) % 2
	board = [[3,3,3,3,3,3,3],
			 [3,3,3,3,3,3,3],
			 [3,3,3,3,3,3,3],
			 [3,3,3,3,3,3,3],
			 [3,3,3,3,3,3,3],
			 [3,3,3,3,3,3,3]]


while True:
	#event tracker
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#Keyboard input
		if event.type == pygame.KEYDOWN:
			if not game_active:
				reset()

		#Mouse input
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				if game_active:
					if 200 <= pos[0] < 830 and 175 <= pos[1] <= 775:
						play(int((pos[0]-200)/90))
				else :
					reset()
	


	screen.blit(bg_surface,(0,0))
	draw_fall(fall_list)
	screen.blit(board_surface,(192,272))
	draw_stones(stone_list)

	if game_active:
		if player:
			screen.blit(stone1_surface, (254,65))
			screen.blit(stone1_surface, (700,65))
		else:
			screen.blit(stone0_surface, (254,65))
			screen.blit(stone0_surface, (700,65))
		text(f"Player  {player+1 }", (512, 100))
		if error:
			text_surface = small_font.render("This Column is full, please choose another one!",True,(255,255,255))
			text_rect = text_surface.get_rect(center = (512, 200))
			screen.blit(text_surface,text_rect)
			#text("This Column is full, please choose another one!" , (512, 200))
	else:
		if turn < 41:
			text(f"Player  {player+1 } won!", (512, 100))
		else :
			text(f"It's a draw!", (512, 100))
		text("Press any button to start a new game" , (512, 200))


	pygame.display.update()
	clock.tick(30)



