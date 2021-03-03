# Resolution : 1280x720

# ****************** References ******************
# assets/fish.png - https://www.pngwing.com/en/free-png-pdncr
# (License - Non-commercial use, DMCA - pngwing.com@gmail.com)

# assets.boss.png - Owned by Aditya Agarwal (Developer)
# assets/menu.png - Owned by Aditya Agarwal (Developer)
# assets/load.png - Owned by Aditya Agarwal (Developer)
# assets/leader.png - Owned by Aditya Agarwal (Developer)
# assets/ins.png - Owned by Aditya Agarwal (Developer)
# assets/player.png - Owned by Aditya Agarwal (Developer)

# Snake Chan Font on backgrounds - Owned by Darrell Flood
# (License - Non-commercial use, dadiomouse@gmail.com, License file included)

# ****************** Cheat Codes ******************
# Number <1> - Snake's health grows by 10 circles
# Number <2> - Snake's health grows by 20 circles
# Number <3> - Snake's health grows by 30 circles
# <p> - Pause game
# <u> - Unpause game
# <b> - Boss Key (Toggle on and off)

# ****************** Customize controls ******************
# To customize controls, go to Instructions menu
# Click on the respective CUSTOMIZE button
# Press any key on the keyboard to set it as the keybind.

from tkinter import Tk, Canvas, PhotoImage, Label
from tkinter import Frame, Button, Entry, messagebox
from random import randint as rand
from time import sleep
import json
import platform


def setWindowDimensions(w, h):
    '''The function places the window in the
    centre of the screen'''
    window = Tk()
    window.title("Snakeock")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window


def move(event):
    '''The function is responsible for moving the
    snake based on the position of the mouse'''
    global gameOver
    if not gameOver:
        x = event.x
        y = event.y
        positions = []
        pos = canvas.coords(snake[0])
        canvas.coords(snake[0], x, pos[1], x + snakeSize, pos[3])
        canvas.coords(snakeLengthText, x + 35, pos[1] + 10)
        for j in range(0, len(snake)):
            positions.append(canvas.coords(snake[j]))

        # The subsequent snake circles assume positions
        # of the circle just before them to give a wavy move
        for i in range(len(snake) - 1):
            canvas.coords(snake[i + 1], positions[i][0], positions[i + 1]
                          [1], positions[i][2], positions[i + 1][3])


def start(event):
    '''The function is responsible to begin the
    game after the user does a left click'''
    global scoringStart, x, rectLine, score, h, loadScore, loadSc
    global toStartTxt, canvas, pauseControl, unpauseControl
    # Doesn't lets multiple invoke of the functions
    # if the user does a left click multiple times
    if x == 1:
        canvas.bind("<Motion>", move)
        canvas.bind(pauseControl, pause)
        canvas.bind(unpauseControl, unpause)
        window.after(1, overlapping)
        tmpCoord = canvas.coords(rectLine[0][1])
        if (tmpCoord[1] > h / 2):
            score = -10
        else:
            score = 0
        if loadSc:
            score = score + loadScore
            loadSc = False
        canvas.delete(toStartTxt)
    scoringStart = True
    x += 1


def growSnake(size):
    ''' The function is responsible for increasing
    the length of the snake, ie, snake's health'''
    global snakeSize, snake, canvas

    for j in range(size):
        positions = []
        positions.append(canvas.coords(snake[len(snake) - 1]))
        snake.append(canvas.create_oval(
            positions[0][0], positions[0][1] + snakeSize, positions[0][2],
            positions[0][3] + snakeSize, fill="green"))


def rectGenerate():
    '''The function is responsible for generating and
    placing the rectangular blocks and food fishes when
    earlier sets reach the bottom of the screen'''
    global snake, rectLine, rectNumber, xCoord, collided, food, foodNumber
    global fishImages, canvas, snakeLengthText, fishImage
    var = 0
    calcX = []
    numberBlocks = rand(5, 6)
    for i in range(numberBlocks):
        num = rand(1, 30)

        # Place blocks to cover the screen if 6 blocks
        # else randomly place them
        if(numberBlocks == 6):
            xCoord.append(i * 213)
            rectLine.append([num, canvas.create_rectangle(
                xCoord[i], 0, xCoord[i] + 213, 100, fill="red")])
            rectNumber.append(canvas.create_text(
                xCoord[i] + 106, 50, text=str(num),
                font=("Arial", 60), fill="white"))

        else:
            # The following while loop prevents overlapping
            # of the blocks to some extent
            while True:
                calcX.append(rand(1, 1067))
                if i == 0:
                    break
                for j in xCoord:
                    if ((calcX[i] < j + 200 and calcX[i] > j) or
                            (calcX[i] + 200 > j and calcX[i] < j)):
                        calcX.pop()
                        var = 1
                        break
                    else:
                        var = 0
                if var == 1:
                    continue
                break

            # Assign the found coordinate and create block
            xCoord = calcX
            rectLine.append([num, canvas.create_rectangle(
                xCoord[i], 0, xCoord[i] + 213, 100, fill="red")])
            rectNumber.append(canvas.create_text(
                xCoord[i] + 106, 50, text=str(num),
                font=("Arial", 60), fill="white"))
    collided = [False] * len(rectLine)
    xCoord.clear()
    quantityFood = rand(2, 3)

    # The for loop creates fish food
    for k in range(quantityFood):
        foodCoord = rand(30, 690)
        foodNum = rand(2, 5)
        food.append([foodNum, canvas.create_oval(
            foodCoord, 140, foodCoord + 70, 210)])
        fishImages.append(canvas.create_image(foodCoord, 140, image=fishImage))
        foodNumber.append(canvas.create_text(
            foodCoord, 165, text=foodNum, fill="white", font=("Arial", 15)))

    for j in range(len(snake)):
        canvas.lift(snake[j])
    canvas.lift(snakeLengthText)


def block():
    '''This function is responsible for moving the blocks
    and the fish food from the top to the bottom of the screen.
    It also destroys them once they reach the bottom'''
    global collided, gameOver, rectNumber, score, scoringStart
    global food, snake, moveSpeed
    try:
        if not gameOver:
            for i in range(len(rectLine)):
                if True in collided:
                    pass
                else:
                    canvas.move(rectLine[i][1], 0, moveSpeed)
                    canvas.move(rectNumber[i], 0, moveSpeed)
            for j in range(len(food)):
                if True in collided:
                    pass
                else:
                    canvas.move(food[j][1], 0, moveSpeed)
                    canvas.move(foodNumber[j], 0, moveSpeed)
                    canvas.move(fishImages[j], 0, moveSpeed)

                rectCoords = canvas.coords(rectLine[i][1])

                # If the blocks reach the bottom of screen
                # they are destroyed and new blocks are created
                if rectCoords[1] > 720:
                    for i in range(len(rectLine)):
                        canvas.delete(rectLine[i][1])
                        canvas.delete(rectNumber[i])
                    for i in range(len(food)):
                        canvas.delete(food[i][1])
                        canvas.delete(fishImages[i])
                        canvas.delete(foodNumber[i])
                    rectLine.clear()
                    rectNumber.clear()
                    collided.clear()
                    rectGenerate()
                    if scoringStart:
                        score = score + 10
                        newScore = "SCORE : " + str(score)
                        canvas.itemconfig(scoreText, text=newScore)

                    # Increase speed of game
                    if score == 100:
                        moveSpeed += 1
                    if score == 200:
                        moveSpeed += 1
                    break
            if len(snake) != 0:
                window.after(2, block)

    except Exception:
        pass


def overlapping():
    '''This function checks if the snake collides with
    any of the rectangular blocks or the food fishes
    and then takes appropriate actions'''
    global collided, gameOver, score
    try:
        if not gameOver:
            for i in range(len(rectLine)):
                a = canvas.coords(snake[0])
                b = canvas.coords(rectLine[i][1])
                if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:

                    # If snake collides, reduce its health
                    canvas.delete(snake[len(snake) - 1])
                    snake.pop()
                    collided[i] = True
                    rectLine[i][0] = rectLine[i][0] - 1
                    canvas.itemconfig(rectNumber[i], text=rectLine[i][0])
                    if len(snake) == 0:
                        break
                    if (rectLine[i][0] == 0):
                        canvas.delete(rectLine[i][1])
                        canvas.delete(rectNumber[i])
                        rectLine.pop(i)
                        rectNumber.pop(i)
                        collided.pop(i)
                        break

                else:
                    collided[i] = False
            for j in range(len(food)):
                try:
                    a = canvas.coords(snake[0])
                    b = canvas.coords(food[j][1])
                    c = canvas.coords(snake[1])

                    # Checks overlapping of the first 2 circles of
                    # snake with the food
                    if ((a[0] < b[2] and a[2] > b[0] and
                         a[1] < b[3] and a[3] > b[1]) or
                        (c[0] < b[2] and c[2] > b[0] and
                         c[1] < b[3] and c[3] > b[1])):
                        growSnake(food[j][0])
                        canvas.delete(food[j][1])
                        canvas.delete(foodNumber[j])
                        canvas.delete(fishImages[j])
                        fishImages.pop(j)
                        food.pop(j)
                        foodNumber.pop(j)
                        break
                except Exception:
                    pass

            # If the snake's length becomes 0, it stops game
            # and throws a dialogue box asking for a restart
            length = len(snake)
            canvas.itemconfig(snakeLengthText, text=length)
            if(length == 0):
                gameOver = True
                leaderCalc()
                msgBody = "Your score was : " + \
                    str(score) + '''\nA good score huh? or maybe not
                    \nDo you want to play again?'''
                msg = messagebox.askquestion(
                    'What next?', msgBody, icon='question')
                if msg == "yes":
                    canvas.delete("all")
                    gameFrame.destroy()
                    window.after(500, canvasPack)
                else:
                    canvas.delete("all")
                    gameFrame.destroy()
                    gameUnpack()
            else:
                window.after(100, overlapping)
    except Exception:
        pass


def boss(event):
    '''This function is responsible for invoking the
    boss screen once the correct key is pressed'''
    global bossCount, gameOver, check
    if bossCount % 2 == 0:
        bossCount += 1

        # To check which frame is visible
        # and then pack_forget it
        if insFrame.winfo_ismapped():
            insFrame.pack_forget()
            check = 1
        elif ins2Frame.winfo_ismapped():
            ins2Frame.pack_forget()
            check = 2
        elif mainMenuFrame.winfo_ismapped():
            mainMenuFrame.pack_forget()
            check = 4
        elif loadFrame.winfo_ismapped():
            loadFrame.pack_forget()
            check = 5
        elif leaderFrame.winfo_ismapped():
            leaderFrame.pack_forget()
            check = 6
        elif usernameFrame.winfo_ismapped():
            usernameFrame.pack_forget()
            check = 7
        try:
            if gameFrame.winfo_ismapped():
                gameFrame.pack_forget()
                check = 3
        except Exception:
            pass
        try:
            if scoringStart:
                pause()
                pauseFrame.pack_forget()
        except Exception:
            pass
        bossFrame.pack()
    elif bossCount % 2 == 1:
        bossCount += 1
        bossFrame.pack_forget()

        # To redisplay the frame which was open
        try:
            if scoringStart:
                unpause()
        except Exception:
            pass
        if check == 1:
            insFrame.pack()
        elif check == 2:
            ins2Frame.pack()
        elif check == 3:
            gameFrame.pack()
        elif check == 4:
            mainMenuFrame.pack()
        elif check == 5:
            loadFrame.pack()
        elif check == 6:
            leaderFrame.pack()
        elif check == 7:
            usernameFrame.pack()


def leaderCalc():
    '''This function is used to calculate and write
    new scores to the external score file'''
    global score, fileDict, file, userName
    file = open('assets/leader.txt', 'w')
    for i in range(len(fileDict)):
        if score > fileDict[i][1]:
            fileDict.insert(i, [userName, score])
            fileDict.pop()
            break
    strr = str(fileDict)

    # To replace single quotes with double quotes as
    # Json and its parser doesn't recognise single quotes
    strr = strr.replace("'", '"')
    file.write(strr)
    file.close()


def pause(event=None):
    '''This function is used to invoke the pause screen
    upon pressing the correct key for the functionality'''
    global gameOver, paused, onlyWhen
    pauseFrame.pack()
    gameFrame.pack_forget()
    gameOver = True
    onlyWhen = True


def unpause(event=None):
    '''This function is used to invoke the unpause screen
    upon pressing the correct key for the functionality'''
    global paused, gameOver, onlyWhen

    # Only unpause if the game has been paused
    if onlyWhen:
        gameOver = False
        paused = False
        gameFrame.pack()
        pauseFrame.pack_forget()
        window.after(1, overlapping)
        window.after(1, block)
        onlyWhen = False


def cheat(event):
    '''This function increases the health of the snake
    based on the cheatcode being used'''
    global cheat1Control, cheat2Control, cheat3Control

    # To check if the key pressed is a Number or not
    try:
        tmp = int(event.keysym)
        if str(event.keysym) == str(cheat1Control):
            growSnake(10)
        if str(event.keysym) == str(cheat2Control):
            growSnake(20)
        if str(event.keysym) == str(cheat3Control):
            growSnake(30)
    except Exception:

        # Try blocks because different keybinds can
        # be a combination of number and strings
        try:
            if str(event.keysym) == str(cheat1Control[1:len(cheat1Control)-1]):
                growSnake(10)
        except Exception:
            pass
        try:
            if str(event.keysym) == str(cheat2Control[1:len(cheat2Control)-1]):
                growSnake(20)
        except Exception:
            pass
        try:
            if str(event.keysym) == str(cheat3Control[1:len(cheat3Control)-1]):
                growSnake(30)
        except Exception:
            pass


def canvasPack():
    '''This function creates and packs our game screen'''
    global snakeSize, snake, rectLine, rectNumber, xCoord, scoringStart
    global file, fileDict, x, loadSc, loadScore, bossCount, score
    global collided, food, foodNumber, fishImages, gameOver, toStartTxt
    global bossControl, unpauseControl, startControl, pauseControl
    global canvas, bossImage, fishImage, snakeLengthText, scoreText, gameFrame
    global cheat1Control, cheat2Control, cheat3Control, moveSpeed
    gameFrame = Frame(window)
    snakeSize = 20
    x = 1
    snake = []
    rectLine = []
    rectNumber = []
    xCoord = []
    collided = []
    food = []
    foodNumber = []
    fishImages = []
    gameOver = False
    paused = False
    scoringStart = False
    score = -10
    fishImage = PhotoImage(file="assets/fish.png")
    canvas = Canvas(gameFrame, width=w, height=h, bg="black")
    canvas.pack()
    canvas.focus_set()

    # Sets the speed of the game according
    # to the platform being used
    osType = platform.system()
    if osType == "Darwin":
        moveSpeed = 4
    elif osType == "Windows":
        moveSpeed = 2
    else:
        moveSpeed = 2
    snake.append(canvas.create_oval(w / 2, h / 2, w / 2 + snakeSize,
                                    (h / 2) + snakeSize, fill="white"))
    growSnake(30)
    toStartTxt = canvas.create_text(w / 2, 100, text="LEFT CLICK TO START",
                                    font=("Verdana", 50), fill="green")
    scoreText = canvas.create_text(
        w / 2, 30, text="SCORE : 0", font=("Verdana", 35), fill="white")

    # Give a custom score if a savegame is being loaded
    if loadSc:
        txt = "SCORE : " + str(loadScore)
        canvas.itemconfig(scoreText, text=txt)
    snakeLengthText = canvas.create_text(
        w / 2 + 35, (h / 2) + 10,
        text=len(snake), font=("Arial", 15), fill="white")
    rectGenerate()
    canvas.bind(cheat1Control, cheat)
    canvas.bind(cheat2Control, cheat)
    canvas.bind(cheat3Control, cheat)
    canvas.bind(startControl, start)
    window.after(1, block)

    # Store the existing leaderboards incase the game
    # closes unexpectedly
    file = open('assets/leader.txt', 'r')
    fileDict = file.read()
    fileDict = json.loads(fileDict)
    file.close()
    mainMenuFrame.pack_forget()
    gameFrame.pack()


def loadPack():
    '''This function creates and packs our load menu'''
    global loadCanvas, loadListName, firstLoad
    global buttonList, loadBg, loadListScore
    if not firstLoad:
        loadBg = PhotoImage(file="assets/load.png")
        loadCanvas = Canvas(loadFrame, width=w, height=h, bg="black")
        loadCanvas.pack()
        loadCanvas.create_image(0, 0, image=loadBg, anchor="nw")
        back = Button(loadFrame, text="Back", font=(
            "Arial", 25), bg="white", command=loadUnpack)
        loadCanvas.create_window(80, 50, window=back)
        back = Button(loadFrame, text="Reset saved games", font=(
            "Arial", 25), bg="white", command=resetLoad,)
        loadCanvas.create_window(w / 2, 670, window=back)
        data = fileReadLoad()
        tmpCoord = 200

        # Creates the different save game texts and their
        # respective load buttons
        for i in range(len(data)):
            buttonList.append(Button(loadFrame, text="Load this", font=(
                "Arial", 15), bg="white", height=1,
                command=lambda i=i: load(i)))
            loadCanvas.create_window(920, tmpCoord, window=buttonList[i])
            loadCanvas.create_text(280, tmpCoord, text=str(
                i + 1) + ".", fill="white", font=("Arial", 45), anchor="w")
            loadListName.append(loadCanvas.create_text(
                (w / 2) - 300, tmpCoord, text=data[i][0],
                fill="white", font=("Arial", 45), anchor="w"))
            loadCanvas.create_text(
                650, tmpCoord, text=":", fill="white", font=("Arial", 45))
            loadListScore.append(loadCanvas.create_text(
                (w / 2) + 70, tmpCoord, text=data[i][1],
                fill="white", font=("Arial", 45), anchor="w"))

            tmpCoord += 55
        firstLoad = True
    else:
        results = fileReadLoad()

        # Except for the first load, the values keep getting updated
        for i in range(len(results)):
            loadCanvas.itemconfig(loadListName[i], text=results[i][0])
            loadCanvas.itemconfig(loadListScore[i], text=results[i][1])

    mainMenuFrame.pack_forget()
    loadFrame.pack()


def leaderPack():
    '''This function creates and packs our leader menu screen.'''
    global leaderCanvas, leaderListName, firstLead, leaderBg, leaderListScore

    # If if is the first load, it creates the elements
    # else it moves to the else block to update the scores
    if not firstLead:
        leaderBg = PhotoImage(file="assets/leader.png")
        leaderCanvas = Canvas(leaderFrame, width=w, height=h, bg="black")
        leaderCanvas.pack()
        leaderCanvas.create_image(0, 0, image=leaderBg, anchor="nw")
        back = Button(leaderFrame, text="Back", font=(
            "Arial", 25), bg="white", command=leaderUnpack)
        leaderCanvas.create_window(80, 50, window=back)
        back = Button(leaderFrame, text="Reset Leaderboards",
                      font=("Arial", 25), bg="white", command=resetLB)
        leaderCanvas.create_window(w / 2, 670, window=back)
        results = fileRead()
        tmpCoord = 200
        leaderListName.clear()

        # Creates the different score texts and displays them
        for i in range(len(results)):
            leaderCanvas.create_text(270, tmpCoord, text=str(
                i + 1) + ".", fill="white", font=("Arial", 45))
            leaderListName.append(leaderCanvas.create_text(
                (w / 2) - 250, tmpCoord, text=results[i][0],
                fill="white", font=("Arial", 45), anchor="w"))
            leaderCanvas.create_text(
                650, tmpCoord, text=":", fill="white", font=("Arial", 45))
            leaderListScore.append(leaderCanvas.create_text(
                (w / 2) + 200, tmpCoord, text=results[i][1],
                fill="white", font=("Arial", 45), anchor="w"))

            tmpCoord += 50
        firstLead = True
    else:
        results = fileRead()
        for i in range(len(results)):
            leaderCanvas.itemconfig(leaderListName[i], text=results[i][0])
            leaderCanvas.itemconfig(leaderListScore[i], text=results[i][1])

    mainMenuFrame.pack_forget()
    leaderFrame.pack()

# The following functions are used to pack and unpack
# the screens upon pressing the respective buttons


def insPack():
    mainMenuFrame.pack_forget()
    insFrame.pack()


def usernamePack():
    mainMenuFrame.pack_forget()
    usernameFrame.pack()


def loadUnpack():
    loadFrame.pack_forget()
    mainMenuFrame.pack()


def leaderUnpack():
    leaderFrame.pack_forget()
    mainMenuFrame.pack()


def insUnpack():
    insFrame.pack_forget()
    mainMenuFrame.pack()


def ins2Unpack():
    ins2Frame.pack_forget()
    mainMenuFrame.pack()


def gameUnpack():
    gameFrame.pack_forget()
    pauseFrame.pack_forget()
    mainMenuFrame.pack()


def usernameUnpack():
    usernameFrame.pack_forget()
    mainMenuFrame.pack()


def ins2():
    insFrame.pack_forget()
    ins2Frame.pack()


def ins1():
    insFrame.pack()
    ins2Frame.pack_forget()


def getUsername():
    '''This function gets the user input for the
    username from the set player menu'''
    global userName
    userName = entry.get()
    userName = userName[0:9]
    if len(userName) < 1:
        userName = 'Guest'
    dialogueString = "Playername set to : " + userName
    messagebox.showinfo('Playername Set!', message=dialogueString)
    usernameUnpack()


def fileRead():
    '''This function reads the leader scores file
    and returns the parsed data'''
    file = open('assets/leader.txt', 'r')
    fileDict = file.read()
    fileDict = json.loads(fileDict)
    file.close()
    return fileDict


def fileReadLoad():
    '''This function reads the load game file
    and returns the parsed data'''
    file = open('assets/savegame.txt', 'r')
    fileDict = file.read()
    fileDict = json.loads(fileDict)
    file.close()
    return fileDict


def resetLB():
    '''This function resets the scores in the
    external file'''
    file = open('assets/leader.txt', 'w')
    resetVal = '''[["User1", 0], ["User2", 0], ["User3", 0], ["User4", 0],
    ["User5", 0], ["User6", 0], ["User7", 0], ["User8", 0]]'''
    file.write(resetVal)
    file.close()
    messagebox.showinfo(
        'Erased!',
        message="Erased the leaderboards! Play again to become the champion!")
    leaderUnpack()
    leaderPack()


def resetLoad():
    '''This function resets the save games in the
    external file'''
    file = open('assets/savegame.txt', 'w')
    resetVal = '''[["User1", 0], ["User2", 0], ["User3", 0], ["User4", 0],
    ["User5", 0], ["User6", 0], ["User7", 0], ["User8", 0]]'''
    file.write(resetVal)
    file.close()
    messagebox.showinfo('Erased!', message="Erased the saved games!")
    loadUnpack()
    loadPack()


def save():
    '''This function saves the current game in the
    external file'''
    global userName, score
    saveData = fileReadLoad()

    # The scoring might start with -10 to eradicate
    # the case where blocks are immmediately below
    # the snake's head. So, it will be zeroed if -10
    # before saving.
    if score == -10:
        score == 0
    saveData.insert(0, [userName, score])
    saveData.pop()
    strr = str(saveData)
    strr = strr.replace("'", '"')
    f = open('assets/savegame.txt', 'w')
    f.write(str(strr))
    msg = "Game Saved.\n\nName : " + str(userName) + "\nScore : " + str(score)
    messagebox.showinfo('Saved!', message=msg)
    exit()


def load(gameNumber):
    '''This function loads the save game from the
    external file'''
    global score, userName, loadScore, loadSc
    loadData = fileReadLoad()
    userName = loadData[gameNumber][0]
    loadScore = loadData[gameNumber][1]
    loadSc = True
    loadFrame.pack_forget()
    canvasPack()


def exit():
    '''This function exits the game and
    returns back to the main menu'''
    global gameOver
    gameOver = True
    canvas.delete("all")
    unpause()
    gameFrame.destroy()
    gameUnpack()


def customize(control):
    '''This function is used to customize the controls
    of the game'''
    global insCanvas, controlK
    controlK = control
    insCanvas.focus_set()
    insCanvas.bind("<Key>", catchKey)


def catchKey(event):
    '''This function is used to catch the key that user
    presses in order to customize the controls'''
    global insCanvas, controlK, pauseControl, bossControl, unpauseControl, c1
    global c2, c3, pauseText, bossText, unpauseText, startText, startControl
    global cheat1Control, cheat2Control, cheat3Control

    # To see if pressed key was a number or not
    try:
        a = int(event.keysym)
        b = "Number <" + event.keysym + ">"
    except Exception:
        a = "<" + event.keysym + ">"
        b = "<" + event.keysym + ">"

    # Based on which control user wants the customise
    # the variable and the text are updated
    if controlK == 1:
        pauseControl = a
        insCanvas.itemconfig(pauseText, text=str(b) + " - Pause game")
    elif controlK == 2:
        unpauseControl = a
        insCanvas.itemconfig(unpauseText, text=str(b) + " - Unpause game")
    elif controlK == 3:
        window.unbind(bossControl)
        bossControl = a
        insCanvas.itemconfig(bossText,
                             text=str(b) + " - Boss Key (toggle on/off)")
        window.bind(bossControl, boss)
    elif controlK == 4:
        startControl = a
        insCanvas.itemconfig(startText, text=str(b) + " - Start the game")
    elif controlK == 5:
        cheat1Control = a
        insCanvas.itemconfig(c1,
                             text=str(b) + " - Snake's health "
                             "grows by 10 circles")
    elif controlK == 6:
        cheat2Control = a
        insCanvas.itemconfig(c2,
                             text=str(b) + " - Snake's health "
                             "grows by 20 circles")
    elif controlK == 7:
        cheat3Control = a
        insCanvas.itemconfig(c3,
                             text=str(b) + " - Snake's health "
                             "grows by 30 circles")
    else:
        print("Error in catchKey Function")
    insCanvas.unbind("<Key>")


w = 1280
h = 720
firstLead = False
firstLoad = False
loadSc = False
loadListName = []
loadListScore = []
leaderListName = []
leaderListScore = []
buttonList = []
userName = 'Guest'
bossCount = 0

# The default controls if the user doesn't
# customizes any of the controls
pauseControl = "<p>"
unpauseControl = "<u>"
bossControl = "<b>"
startControl = "<Button-1>"
cheat1Control = 1
cheat2Control = 2
cheat3Control = 3

window = setWindowDimensions(w, h)
mainMenuFrame = Frame(window)
loadFrame = Frame(window)
leaderFrame = Frame(window)
insFrame = Frame(window)
ins2Frame = Frame(window)
usernameFrame = Frame(window)
pauseFrame = Frame(window)
bossFrame = Frame(window)


mainMenuFrame.pack()
window.bind(bossControl, boss)


# *****************
# Main Menu Frame
# *****************

menuBg = PhotoImage(file="assets/menu.png")
menuCanvas = Canvas(mainMenuFrame, width=w, height=h, bg="white")
menuCanvas.pack()
menuCanvas.create_image(0, 0, image=menuBg, anchor="nw")

back = Button(text="Play Game", font=("Courier", 20),
              command=canvasPack, width=15, activeforeground="green")
menuCanvas.create_window(w / 2, 310, window=back)
back = Button(text="Load Game", font=("Courier", 20),
              command=loadPack, width=15, activeforeground="green")
menuCanvas.create_window(w / 2, 370, window=back)
back = Button(text="Leaderboard", font=("Courier", 20),
              command=leaderPack, width=15, activeforeground="green")
menuCanvas.create_window(w / 2, 430, window=back)
back = Button(text="Instructions", font=("Courier", 20),
              command=insPack, width=15, activeforeground="green")
menuCanvas.create_window(w / 2, 490, window=back)
back = Button(text="Set Player Name", font=("Courier", 20),
              command=usernamePack, width=15, activeforeground="green")
menuCanvas.create_window(w / 2, 550, window=back)
back = Button(text="Exit the game", font=("Courier", 20),
              command=window.destroy, width=15, activeforeground="green")
menuCanvas.create_window(w / 2, 610, window=back)

# *****************
# Load Frame
# *****************

# Inside the loadPack() function.

# *****************
# Instructions Page 1 Frame
# *****************

insBg = PhotoImage(file="assets/ins.png")
insCanvas = Canvas(insFrame, width=w, height=h, bg="black")
insCanvas.pack()
insCanvas.create_image(0, 0, image=insBg, anchor="nw")

insCanvas.create_text(60, 130, text="How to Play : ",
                      fill="white", font=("Arial", 35), anchor='w')
insCanvas.create_text(120, 180, text="To start the game, do a left click. "
                      "Move your mouse to guide the snake of balls and"
                      " try to get past as many walls of bricks \nas you can."
                      " Every pass past the wall will earn you 10 points. Eat"
                      " the fish food on the way to grow your snake's"
                      " health.\nEvery time the score increases by 100, "
                      "the speed increases (upto the score of 200).",
                      fill="white", font=("Arial", 15), anchor='w')


insCanvas.create_text(60, 240, text="Cheatcodes : ",
                      fill="white", font=("Arial", 35), anchor='w')
c1 = insCanvas.create_text(120, 290,
                           text="Number <1> - Snake's health "
                           "grows by 10 circles",
                           fill="white", font=("Arial", 20), anchor='w')
c2 = insCanvas.create_text(120, 315,
                           text="Number <2> - Snake's health "
                           "grows by 20 circles",
                           fill="white", font=("Arial", 20), anchor='w')
c3 = insCanvas.create_text(120, 340,
                           text="Number <3> - Snake's health "
                           "grows by 30 circles",
                           fill="white", font=("Arial", 20), anchor='w')

insCanvas.create_text(60, 400, text="Controls : ",
                      fill="white", font=("Arial", 35), anchor='w')
pauseText = insCanvas.create_text(120, 450, text="<p> - Pause game",
                                  fill="white", font=("Arial", 20), anchor='w')
unpauseText = insCanvas.create_text(120, 475, text="<u> - Unpause game",
                                    fill="white",
                                    font=("Arial", 20), anchor='w')
bossText = insCanvas.create_text(120, 500, text="<b> - Boss Key "
                                 "(toggle on/off)",
                                 fill="white", font=("Arial", 20), anchor='w')

insCanvas.create_text(120, 430, text="Motion of Mouse - Guide the snake",
                      fill="white", font=("Arial", 20), anchor='w')
startText = insCanvas.create_text(120, 525,
                                  text="<Left Mouse Click> - Start the game",
                                  fill="white", font=("Arial", 20), anchor='w')

insCanvas.create_text(60, 560, text="Customize : ",
                      fill="white", font=("Arial", 35), anchor='w')
insCanvas.create_text(120, 595,
                      text="To customize a control, click the respective "
                      "CUSTOMIZE button and press ANY key on your keyboard"
                      " to set it as the keybind.",
                      fill="white", font=("Arial", 15), anchor='w')
insCanvas.create_text(120, 620,
                      text="MAKE SURE TO NOT SET TWO CONTROLS TO THE SAME KEY"
                      " AS THIS MIGHT THROW ERRORS",
                      fill="yellow", font=("Arial", 17), anchor='w')


back = Button(insFrame, text="Back", font=(
    "Arial", 25), bg="white", command=insUnpack)
insCanvas.create_window(80, 50, window=back)

back = Button(insFrame, text="Next Page", font=(
    "Arial", 25), bg="white", command=ins2)
insCanvas.create_window(w / 2, 670, window=back)

back = Button(insFrame, text="Customize", font=(
    "Arial", 8), bg="white", command=lambda: customize(1), bd=0)
insCanvas.create_window(590, 450, window=back)

back = Button(insFrame, text="Customize", font=(
    "Arial", 8), bg="white", command=lambda: customize(2), bd=0)
insCanvas.create_window(590, 475, window=back)

back = Button(insFrame, text="Customize", font=(
    "Arial", 8), bg="white", command=lambda: customize(3), bd=0)
insCanvas.create_window(590, 500, window=back)

back = Button(insFrame, text="Customize", font=(
    "Arial", 8), bg="white", command=lambda: customize(4), bd=0)
insCanvas.create_window(590, 525, window=back)

back = Button(insFrame, text="Customize", font=(
    "Arial", 8), bg="white", command=lambda: customize(5), bd=0)
insCanvas.create_window(750, 290, window=back)

back = Button(insFrame, text="Customize", font=(
    "Arial", 8), bg="white", command=lambda: customize(6), bd=0)
insCanvas.create_window(750, 315, window=back)

back = Button(insFrame, text="Customize", font=(
    "Arial", 8), bg="white", command=lambda: customize(7), bd=0)
insCanvas.create_window(750, 340, window=back)

# *****************
# Instructions Page 2 Frame
# *****************

ins2Canvas = Canvas(ins2Frame, width=w, height=h, bg="black")
ins2Canvas.pack()
ins2Canvas.create_image(0, 0, image=insBg, anchor="nw")

ins2Canvas.create_text(60, 130, text="Save Game : ",
                       fill="white", font=("Arial", 35), anchor='w')
ins2Canvas.create_text(120, 180, text="To save a game, press 'p' to pause "
                       "while playing and click on 'Save and Exit'. "
                       "This will save the score with the username.\nSaving a"
                       " new game will remove the oldest savegame record.",
                       fill="white", font=("Arial", 15), anchor='w')
ins2Canvas.create_text(60, 240, text="Load Game : ",
                       fill="white", font=("Arial", 35), anchor='w')
ins2Canvas.create_text(120, 290, text="To load a game, go to LOAD MENU from"
                       " the MAIN MENU and click on the respective load "
                       "button for the game you wish to load.",
                       fill="white", font=("Arial", 15), anchor='w')

ins2Canvas.create_text(60, 350, text="Compatibility with macOS, "
                       "Linux and Windows : ",
                       fill="white", font=("Arial", 35), anchor='w')
ins2Canvas.create_text(120, 410, text="The game has been built for macOS "
                       "specifically and works the best on macOS. The game "
                       "might show varying"
                       " performance on a\nmacOS, Linux and Windows platforms"
                       " owing to Tkinter being a GUI library. This has "
                       "been fixed to a great extent but still might throw\n"
                       "some styling errors. The game has been tested on "
                       "Windows 10, macOS and Linux platforms. ",
                       fill="white", font=("Arial", 15), anchor='w')

ins2Canvas.create_text(60, 460, text="Player Name : ",
                       fill="white", font=("Arial", 35), anchor='w')
ins2Canvas.create_text(120, 510, text="To set a player name, go to "
                       "MainMenu/SetPlayerName and enter in your player name."
                       " The default player name is Guest.",
                       fill="white", font=("Arial", 15), anchor='w')

ins2Canvas.create_text(60, 570, text="Contact the Developer : ",
                       fill="white", font=("Arial", 35), anchor='w')
ins2Canvas.create_text(120, 620, text="To report a bug or to submit feedback,"
                       " send an email to <aditya@student.manchester.ac.uk>",
                       fill="white", font=("Arial", 15), anchor='w')

back = Button(ins2Frame, text="Back", font=(
    "Arial", 25), bg="white", command=ins2Unpack)
ins2Canvas.create_window(80, 50, window=back)

back = Button(ins2Frame, text="Previous Page", font=(
    "Arial", 25), bg="white", command=ins1)
ins2Canvas.create_window(w / 2, 670, window=back)


# *****************
# Username Frame
# *****************

userBg = PhotoImage(file="assets/player.png")
userCanvas = Canvas(usernameFrame, width=w, height=h, bg="black")
userCanvas.pack()
userCanvas.create_image(0, 0, image=userBg, anchor="nw")
entry = Entry(usernameFrame, width=40)
userCanvas.create_window(w / 2, 300, window=entry)
userCanvas.create_text(
    w / 2, 240, text="Enter the name of the player",
    fill="white", font=("Arial", 30))
userCanvas.create_text(
    w / 2, 440, text="(Upto 10 characters and Default : Guest)",
    fill="white", font=("Arial", 20))

back = Button(usernameFrame, text="Set", font=(
    "Arial", 25), bg="white", command=getUsername)
userCanvas.create_window(w / 2, 370, window=back)
back = Button(usernameFrame, text="Back", font=(
    "Arial", 25), bg="white", command=usernameUnpack)
userCanvas.create_window(80, 50, window=back)

# *****************
# Leader Frame
# *****************

# Inside the leaderPack() function.

# *****************
# Game Frame
# *****************

# Inside the canvasPack() function.

# *****************
# Pause Frame
# *****************

pauseCanvas = Canvas(pauseFrame, width=w, height=h, bg="black")
pauseCanvas.pack()
back = Button(pauseFrame, text="Resume", font=("Arial", 25),
              bg="white", command=unpause, width=30)
pauseCanvas.create_window(w / 2, 340, window=back)
back = Button(pauseFrame, text="Exit", font=(
    "Arial", 25), bg="white", command=exit, width=30)
pauseCanvas.create_window(w / 2, 410, window=back)
back = Button(pauseFrame, text="Save and Exit", font=(
    "Arial", 25), bg="white", command=save, width=30)
pauseCanvas.create_window(w / 2, 480, window=back)

# *****************
# Boss Frame
# *****************

bossImage = PhotoImage(file="assets/boss.png")
bossCanvas = Canvas(bossFrame, width=w, height=h, bg="black")
bossCanvas.pack()
bossCanvas.create_image(0, 0, image=bossImage, anchor="nw")

window.mainloop()
