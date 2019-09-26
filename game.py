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
		
		displayCells(currentGrid)
		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or (event.type == pygame.QUIT):
				sys.exit()

			if event.type == pygame.MOUSEBUTTONUP:
				mouseClicked = True
		if mouseClicked == True:
			mousex,mousey = event.pos
			print(mousex,mousey)
			currentGrid = displaySelectedNumber(mousex,mousey,currentGrid)
			mouseClicked = False
			
			

		

		pygame.display.update()
		
		DISPLAYSURF.fill(WHITE)
		SolveSudoku(currentGrid)
		drawGrid()
		displayCells(currentGrid)
		drawBox(mousex,mousey)
		FPSCLOCK.tick(FPS)
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
		cellSurf = LARGEFONT.render('%s'%(cellData),True,BLACK)


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




def SolveSudoku(currentGrid):
	for item in currentGrid: # item is x,y co-ordinate from 0-8
		cellData = currentGrid[item]
		if cellData.count(' ') == 8: # only look at those with one number remaining
			for number in cellData: # Determine the number there
				if number != ' ':
					updateNumber = number
			currentGrid = removeX(currentGrid, item, updateNumber)
			currentGrid = removeY(currentGrid, item, updateNumber)
			currentGrid = removeGrid(currentGrid, item, updateNumber)
	return currentGrid


def removeX(currentGrid, item, number):
	for x in range(0,9):
		if x != item[0]:
			currentState = currentGrid[(x,item[1])]
			currentState[number-1] = ' '
			currentGrid[(x,item[1])] = currentState
	return currentGrid

def removeY(currentGrid, item, number):
	for y in range(0,9):
		if y != item[1]:
			currentState = currentGrid[(item[0],y)]
			currentState[number-1] = ' '
			currentGrid[(item[0],y)] = currentState
	return currentGrid




def removeGrid(currentGrid, item, number):

	if item[0] < 3:
		xGrid = [0,1,2]
	elif item[0] > 5:
		xGrid = [6,7,8]
	else: xGrid = [3,4,5]

	if item[1] < 3:
		yGrid = [0,1,2]
	elif item[1] > 5:
		yGrid = [6,7,8]
	else: yGrid = [3,4,5]
    
    #iterates through each of the nine numbers in the grid
	for x in xGrid:
		for y in yGrid:
			if (x,y) != item: # for all squares except the one containing the number
				currentState = currentGrid[(x,y)] # isolates the numbers still available for that cell
				currentState[number-1] = ' ' # make them blank.
				currentGrid[(x,y)] = currentState
	return currentGrid





if __name__=='__main__':
    main()
