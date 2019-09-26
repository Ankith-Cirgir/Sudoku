import pygame,sys
from collections import defaultdict
from pygame.locals import *
pygame.init()

#FPS
FPS = 60


#GRID

WINDOWMULTIPLIER = 3
WINDOWSIZE = 162

#dimension
WINDOWHEIGHT = int(WINDOWSIZE*WINDOWMULTIPLIER)
WINDOWWIDTH = int(WINDOWSIZE*WINDOWMULTIPLIER)


#Square
SQUARESIZE = int((WINDOWSIZE*WINDOWMULTIPLIER)/3)
CELLSIZE = int(WINDOWSIZE/3)
NUMBERSIZE = int(CELLSIZE/3)


#colors
LIGHTGRAY = (190,190,190)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,102,255)
GREEN = (0,255,0)



#FONT
global BASICFONT,FONTSIZE,LARGEFONT,LARGEFONTSIZE
FONTSIZE = 15
LARGEFONTSIZE = 55
BASICFONT = pygame.font.Font('C:\\Users\\sys\\Desktop\\game\\freesansbold.ttf',FONTSIZE)
BASICFONT = pygame.font.SysFont('arial', FONTSIZE)
LARGEFONT = pygame.font.SysFont('arial', LARGEFONTSIZE)

def main():
	global FPSCLOCK,DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	mouseClicked = False
	mousex = 0
	mousey = 0
	pygame.display.set_caption("Sudoku !!")
	DISPLAYSURF.fill(WHITE)
	currentGrid = intitiateCells()
	FPSCLOCK = pygame.time.Clock()
	while True:
		
		drawGrid()
		currentGrid = intitiateCells()
		displayCells(currentGrid)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				sys.exit()
			if event.type == MOUSEMOTION:
				mousex,mousey = event.pos
			if event.type == pygame.MOUSEBUTTONUP:
				mousex,mousey = event.pos
				mouseClicked = True
		if mouseClicked == True:
			print(mousex,mousey)
			currentGrid = displaySelectedNumber(mousex,mousey,currentGrid)

		pygame.display.update()
		FPSCLOCK.tick(FPS)
		DISPLAYSURF.fill(WHITE)
		displayCells(currentGrid)
		drawGrid()
		drawBox(mousex,mousey)

		#pygame.display.update()
		#FPSCLOCK.tick(FPS)




def drawGrid():
	#THIN LINES
	for x in range(0,WINDOWWIDTH,CELLSIZE):
		pygame.draw.line(DISPLAYSURF,LIGHTGRAY,(x,0),(x,WINDOWHEIGHT))
	for y in range(0,WINDOWHEIGHT,CELLSIZE):
		pygame.draw.line(DISPLAYSURF,LIGHTGRAY,(0,y),(WINDOWWIDTH,y))
	#THICK LINES
	for x in range(0,WINDOWWIDTH,SQUARESIZE):
		pygame.draw.line(DISPLAYSURF,BLACK,(x,0),(x,WINDOWHEIGHT))
	for y in range(0,WINDOWHEIGHT,SQUARESIZE):
		pygame.draw.line(DISPLAYSURF,BLACK,(0,y),(WINDOWWIDTH,y))
	return None

def intitiateCells():
	currentGrid = {}
	fullCell = [1,2,3,4,5,6,7,8,9]
	for xCoord in range(9):
		for yCoord in range(9):
			currentGrid[xCoord,yCoord] = list(fullCell)
	return currentGrid

def displayCells(currentGrid):
	
	xFactor = 0
	yFactor = 0
	for item in currentGrid:
		cellData = currentGrid[item]
		for number in cellData: #iterates through each number
			if number != ' ': # ignores those already dismissed
				xFactor = ((number-1)%3) # 1/4/7 = 0 2/5/8 = 1 3/6/9 =2
				if number <= 3:
					yFactor = 0
				elif number <=6:
					yFactor = 1
				else:
					yFactor = 2
                #(item[0] * CELLSIZE) Positions in the right Cell
                #(xFactor*NUMBERSIZE) Offsets to position number    
			
			if cellData.count(' ') < 8:    
				populateCells(number,(item[0]*CELLSIZE)+(xFactor*NUMBERSIZE),(item[1]*CELLSIZE)+(yFactor*NUMBERSIZE),'small')
			else:
				populateCells(number,(item[0]*CELLSIZE),(item[1]*CELLSIZE),'large')
	return None

def populateCells(cellData, x, y,size):
	if size =='small':
		cellSurf = BASICFONT.render('%s'%(cellData),True,LIGHTGRAY)
	elif size == 'large':
		cellSurf = LARGEFONT.render('%s'%(cellData),True,GREEN)


	cellRect = cellSurf.get_rect()
	cellRect.topleft = (x, y)
	DISPLAYSURF.blit(cellSurf, cellRect)


def drawBox(mousex, mousey):
	boxx =((mousex*27) / WINDOWWIDTH) * (NUMBERSIZE )
	boxy =((mousey*27) / WINDOWHEIGHT) * (NUMBERSIZE )
	pygame.draw.rect(DISPLAYSURF, BLUE, (boxx,boxy,NUMBERSIZE,NUMBERSIZE), 1)


def displaySelectedNumber(mousex, mousey, currentGrid):
	xNumber = (mousex*27) / WINDOWWIDTH # range 0 - 26
	yNumber = (mousey*27) / WINDOWWIDTH # range 0 - 26
	#Determine a 0,1 or 2 for x and y
	modXNumber = int(xNumber % 3)
	modYNumber = int(yNumber % 3)
	if modXNumber == 0:
		xChoices = [1,4,7]
		number = xChoices[modYNumber]        
	elif modXNumber == 1:
		xChoices = [2,5,8]
		number = xChoices[modYNumber]
	else:
		xChoices = [3,6,9]
		number = xChoices[modYNumber]

	xCellNumber = int(xNumber / 3)
	yCellNumber = int(yNumber / 3)
   
	currentState = currentGrid[xCellNumber,yCellNumber]
	inNum = 0
    
	while inNum < 9:
		if inNum+1 != number:
			currentState[inNum] = ' '
		else:
			currentState[inNum] = number

		currentGrid[xCellNumber,yCellNumber] = currentState
		inNum += 1
	return currentGrid








if __name__=='__main__':
    main()
