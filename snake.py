from tkinter import *
import random

root = Tk()
root.title('Snake')
winWidth = 500 ## In pixels
winHeight = 500 ## In pixels
stepFrequency = 100 ## In milliseconds
gameOver = 0
root.geometry(str(winWidth) + 'x' + str(winHeight))


canvas = Canvas(width=winWidth, height=winHeight, bg='#222244')
canvas.pack()

parts = []
partPoligons = []
yum = None
yumPoli = None
blockSize = 20

class Yummy:
    x = 0
    y = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        

class SnakePart:
    x = 0
    y = 0
    bx = 0
    by = 0
    isMain = 0
    direction = ''
    _id = 0
    
    def __init__(self, startPos, __id, isMain):
        self.x = startPos[0]
        self.y = startPos[1]
        self._id = __id
        self.isMain = isMain
        print('Id: ' + str(self._id) + '\nX: ' + str(self.x) + '\nY: ' + str(self.y))
    
    def move(self, xx, yy):
        global canvas
        global partPoligons
        self.bx = self.x
        self.by = self.y
        canvas.move(partPoligons[self._id], xx, yy)
        self.x = self.x + xx
        self.y = self.y + yy

def begin(startCount):
    global mainPart
    for i in range(startCount):        
        if i == 0:
            parts.append(SnakePart([i*blockSize + blockSize/2, blockSize/2], i, 1))
            parts[i].direction = 3
        else: parts.append(SnakePart([i*blockSize + blockSize/2, blockSize/2], i, 0))
        
        partPoligons.append(canvas.create_rectangle(i*blockSize, 0, i*blockSize+blockSize, blockSize, fill='#ccbbbb'))
        
def keyPress(event):
    global parts
    key = event.keycode
    if key == 87: ## W pressed
        parts[0].direction = 1
    if key == 65: ## A pressed
        parts[0].direction = 4
    if key == 83: ## S pressed
        parts[0].direction = 3
    if key == 68: ## D pressed        
        parts[0].direction = 2

root.bind('w', keyPress)
root.bind('s', keyPress)
root.bind('a', keyPress)
root.bind('d', keyPress)

def step():
    global parts
    global partPoligons
    global blockSize
    global stepFrequency
    global yum
    global gameOver
    
    d = parts[0].direction
    parts[0].bx = parts[0].x
    parts[0].by = parts[0].y    
    
    if d == 1:
        parts[0].move(0, -blockSize)
        
    if d == 2:        
        parts[0].move(blockSize, 0) 
        
    if d == 3:        
        parts[0].move(0, blockSize)
        
    if d == 4:
        parts[0].move(-blockSize, 0)        
    
    for i in range(1, len(parts)):
        parts[i].move(parts[i-1].bx - parts[i].x, parts[i-1].by - parts[i].y)
          
    if parts[0].x == yum.x and parts[0].y == yum.y:
        newX = parts[-2].x - 2 * parts[-1].x
        newY = parts[-2].y - 2 * parts[-1].y
        createYummy()
        parts.append(SnakePart([newX, newY], len(parts), 0))
        partPoligons.append(canvas.create_rectangle(newX - blockSize/2, newY - blockSize/2, newX + blockSize/2, newY + blockSize/2, fill='#ccbbbb'))
        
    for i in range(1, len(parts)):
        if parts[i].x == parts[0].x and parts[i].y == parts[0].y:
            gameOver = 1
            GameOver()
    
    if gameOver == 0:    
        root.after(stepFrequency, step)

def GameOver():
    l = Label(text='GameOver', fg='#dd2222', bg='#222244', font=('Helvetica', '18')).place(width=120, height=20, x=int(winWidth/2)-60, y=int(winHeight/2)-10)

def createYummy():
    global winWidth
    global winHeight
    global blockSize
    global canvas
    global yum
    global yumPoli
    global parts
    
    lenX = winWidth / blockSize
    lenY = winHeight / blockSize
    x = 0
    y = 0
    ok = 0
    while(ok == 0):
        x = random.randint(0, lenX-1) * blockSize
        y = random.randint(0, lenY-1) * blockSize 
        n = 0
        for i in range(len(parts)):
            if x != parts[i].x and y != parts[i].y:
                n += 1
        if n == len(parts):
            break
    yum = Yummy(x + blockSize / 2,y + blockSize / 2)
    canvas.delete(yumPoli)
    yumPoli = canvas.create_rectangle(x, y, x + blockSize, y + blockSize, fill='#bbbb22')

createYummy()
begin(5)
root.after(0, step)
root.mainloop()