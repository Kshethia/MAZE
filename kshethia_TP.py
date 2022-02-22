#################################################
# Term Project: MAZE
#
# By: Karina Shethia
# Andrew ID: Kshethia
# Recitation Section: H
#################################################

# This is the file to be run. It contains all the code for the TP

import random, time
from cmu_112_graphics import *

#################################################
# Main / Overall Functions
#################################################

# Colours used in all the redrawAll and View functions found at:
# http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter


# Initializes the parameters when the app is run
def appStarted(app):
    app.timerDelay = 25
    app._root.resizable(False, False)
    app.margin = 75
    app.mode = "chooseMode"

    app.currentMode = None
    app.modes = ["Absolutism", "Eternalism", "Idealism"]
    app.backgroundColours = ["black", "navy", "orange red"]
    app.modeSelectionIndex = 0
    app.playerColour = ""

    app.currentDifficulty = None
    app.difficulty = ["Easy", "Medium", "Hard"]
    app.difficultySelectionIndex = 0

    app.timeLimit = 0
    app.hasEnemies = None

    appReset(app)


# Initializes the parameters when the app is started or game is reset
def appReset(app):
    currentModeParameters(app)
    currentDifficultyParameters(app)

    if app.mode == "game":
        app.gameOver = False
        app.collideTime = 0
        app.collideAnimation = False
        app.explosionRadius = 0
        app.explosionStipple = ""

        app.player.x = 0
        app.player.y = 0

        app.maze = []

        app.goal.x = random.randint(app.cols//2, app.cols - 1)
        app.goal.y = random.randint(app.rows//2, app.rows - 1)

        app.startTime = time.time()
        app.elapsedTime = time.time() - app.startTime
        app.paused = False
        app.pausedTime = 0
        app.startPause = 0
        app.endPause = 0

        app.highScore = highScoreFromFile(app)

        createMaze(app)


    elif app.mode == "gameOver":
        btnColr = app.backgroundColour
        app.rButton, app.mButton, app.dButton = btnColr, btnColr, btnColr
        app.rText, app.mText, app.dText = "white", "white", "white"
        


# Returns the coords that define the bounds of a cell when given its row & col
def getCellBounds(app, row, col):
    x0 = app.margin + col*app.cellSize
    y0 = app.margin + row*app.cellSize
    x1 = app.margin + (col+1)*app.cellSize
    y1 = app.margin + (row+1)*app.cellSize
    return x0, y0, x1, y1



#################################################
# Choosing The Mode Functions
#################################################

# Defines how our model will change according to certain keyboard inputs
def chooseMode_keyPressed(app, event):
    if event.key == "Up": 
        app.modeSelectionIndex -= 1
        if app.modeSelectionIndex < 0: 
            app.modeSelectionIndex = len(app.modes)-1
        
    elif event.key == "Down":
        app.modeSelectionIndex += 1
        if app.modeSelectionIndex > len(app.modes)-1: 
            app.modeSelectionIndex = 0
    
    elif event.key == "Enter":
        app.currentMode = app.modes[app.modeSelectionIndex]
        app.mode = "chooseDifficulty"
        appReset(app)


# Defines model parameters based on mode selected
def currentModeParameters(app):
    app.backgroundColour = app.backgroundColours[app.modeSelectionIndex]
    if app.currentMode == "Absolutism":
        app.hasHappinessLevel = False
        app.isTimed = True
    
    elif app.currentMode == "Eternalism":
        app.hasHappinessLevel = False
        app.isTimed = False

    elif app.currentMode == "Idealism":
        app.hasHappinessLevel = True
        app.numHearts = 0
        app.isTimed = True


# View functions for chooseMode mode
def chooseMode_redrawAll(app, canvas):
    # Background colour
    canvas.create_rectangle(0, 0, app.width, app.height, 
                        fill = app.backgroundColours[app.modeSelectionIndex])
    # Title of the game:
    canvas.create_text(250, 115, text = "MAZE", anchor = 'w',
                            fill = "white", font = "Arial 140 bold")
    textSpacing = 100
    drawTitleAndModeSelectionText(app, canvas, textSpacing)
    drawInstructions(app, canvas, textSpacing)
    drawModeIcons(app, canvas)


# Draws the title of the different modes to choose from
def drawTitleAndModeSelectionText(app, canvas, textSpacing):
    for textIndex in range(len(app.modes)):
        if app.modeSelectionIndex == textIndex:
            fontStyle = "Arial 75 bold"
        else: 
            fontStyle = "Arial 50"
        canvas.create_text(textSpacing, textSpacing*(textIndex+3),
                            text = f"{app.modes[textIndex]}", anchor = 'w',
                            fill = "white", font = f"{fontStyle}")

        drawDefinitions(app, canvas, textSpacing)


# Draws the instructions for choosing a mode
def drawInstructions(app, canvas, textSpacing):
    instructions = ["Press the Up or Down key to change the current mode",
                    "Press Enter key to confirm selection"]

    for messageIndex in range(len(instructions)):
        canvas.create_text(textSpacing, textSpacing*7.6 + 15*messageIndex, 
                    anchor = 'w',text = instructions[messageIndex],
                    fill = "white", font = "Arial 10")


# Draws the icon related to each mode by the Title when it is selected
def drawModeIcons(app, canvas):
    if app.modeSelectionIndex == 0:
        canvas.create_polygon(100, 182, 243, 182, 171, 50,
                             fill = "white", width = 0)
        canvas.create_polygon(130, 83, 213, 83, 171, 166,
                             fill = "black", width = 0)

    elif app.modeSelectionIndex == 1:
        canvas.create_polygon(100, 49, 243, 49, 171, 113, 
                            fill = "sandy brown", width = 0)
        canvas.create_polygon(100, 182, 243, 182, 171, 113, 
                            fill = "white", width = 0)
        canvas.create_polygon(120, 54, 223, 54, 171, 103, 
                            fill = "navy", width = 0)
        canvas.create_polygon(120, 171, 223, 171, 171, 123, 
                            fill = "navy", width = 0)

    else:
        canvas.create_oval(100, 43, 243, 186, fill = "coral", width = 0)
        canvas.create_oval(115, 58, 228, 171, fill = "light salmon", width = 0)
        canvas.create_oval(130, 73, 213, 156, fill = "peach puff", width = 0)
        canvas.create_polygon(134, 113, 209, 113, 171, 159, fill = "orange red",
                                width = 0)
        canvas.create_oval(133, 81, 174, 126, fill = "orange red", width = 0)
        canvas.create_oval(169, 81, 210, 126, fill = "orange red", width = 0)


# Displays the definition of the mode depending on which mode selected
def drawDefinitions(app, canvas, textSpacing):
    # Definitions adapted from Genis Carreras' series: Philographics at:
    # https://studiocarreras.com/#/philographics/
    if app.modeSelectionIndex == 0:
        definition = [
        "Within a particular school of thought, all different",
        "perspectives are either absolutely true or absolutely false."
                    ]

    elif app.modeSelectionIndex == 1:
        definition = [
        "Time is just another dimension, that future events already exist,",
        "and that all points in time are equally real."
                    ]

    else:
        definition = [
        "Reality is fundamentally based on, and shaped by,",
        "ideas and mental experience, rather than material forces."
                    ]

    for index in range(len(definition)):
        canvas.create_text(textSpacing, textSpacing*6.2 + 25*index,
                            text = f"{definition[index]}", anchor = 'w',
                            font = "Arial 15 italic", fill = "white")



#################################################
# Choosing The Level of Difficulty Functions
#################################################

# Defines how our model will change according to certain keyboard inputs
def chooseDifficulty_keyPressed(app, event):
    if event.key == "Up": 
        app.difficultySelectionIndex -= 1
        if app.difficultySelectionIndex < 0: 
            app.difficultySelectionIndex = len(app.modes)-1
        
    elif event.key == "Down":
        app.difficultySelectionIndex += 1
        if app.difficultySelectionIndex > len(app.modes)-1: 
            app.difficultySelectionIndex = 0
    
    elif event.key == "Enter":
        app.currentDifficulty = app.difficulty[app.difficultySelectionIndex]
        currentDifficultyParameters(app)
        app.mode = "game"
        if app.currentMode == "Absolutism":
            app.playerColour = "white"
        elif  app.currentMode == "Eternalism":
            app.playerColour = "sandy brown"
        else:
            app.playerColour = "black"
        app.player = Player(app)
        app.goal = Goal(app)
        appReset(app)


# Defines model parameters based on difficulty level selected
def currentDifficultyParameters(app):
    app.goalMargin = -1
    if app.currentDifficulty == "Easy":
        app.timeLimit = 30
        app.rows, app.cols = 10, 10
        app.cellSize = (app.width-2*app.margin)//app.rows
        app.playerMargin = 10
        if app.currentMode != "Eternalism":
            app.enemies = [Enemy(app)]
            app.hasEnemies = True
        else:
            app.hasEnemies = False
        
        if app.currentMode == "Idealism":
            app.hearts = [Heart(app) for i in range(16)]

    elif app.currentDifficulty == "Medium":
        app.timeLimit = 20
        app.rows, app.cols = 15, 15
        app.cellSize = (app.width-2*app.margin)//app.rows
        app.playerMargin = 6
        app.hasEnemies = True
        if app.currentMode == "Eternalism":
            app.enemies = [Enemy(app)]
        else:
            app.enemies = [Enemy(app), Enemy(app)]
        
        if app.currentMode == "Idealism":
            app.hearts = [Heart(app) for i in range(11)]

    elif app.currentDifficulty == "Hard":
        app.timeLimit = 10
        app.rows, app.cols = 20, 20
        app.cellSize = (app.width-2*app.margin)//app.rows
        app.playerMargin = 3
        app.hasEnemies = True
        app.enemies = [Enemy(app), Enemy(app), Enemy(app)]

        if app.currentMode == "Idealism":
            app.hearts = [Heart(app) for i in range(6)]


# View functions for chooseDifficulty mode
def chooseDifficulty_redrawAll(app, canvas):
    textSpacing = 100
    # Background colour
    canvas.create_rectangle(0, 0, app.width, app.height, 
                        fill = app.backgroundColour)

    # Title of the game
    canvas.create_text(250, 115, text = "MAZE", anchor = 'w',
                            fill = "white", font = "Arial 140 bold")

    drawModeIcons(app, canvas)
    drawInstructions(app, canvas, textSpacing)
    
    for textIndex in range(len(app.difficulty)):
        if app.difficultySelectionIndex == textIndex:
            fontStyle = "Arial 75 bold"
        else: 
            fontStyle = "Arial 50"
        canvas.create_text(textSpacing, textSpacing*(textIndex+3),
                            text = f"{app.difficulty[textIndex]}", anchor = 'w',
                            fill = "white", font = f"{fontStyle}")

        drawDifficultyExplanations(app, canvas, textSpacing)


# Draws the rules for the game depending on game mode and difficulty selected
def drawDifficultyExplanations(app, canvas, textSpacing):
    if app.currentMode == "Absolutism":
        if app.difficultySelectionIndex == 0:
            rules = [
        "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
        "○ Finish the maze before time runs out or you get caught",
        "○ You will have 30 seconds to complete each maze"
            ]
        elif app.difficultySelectionIndex == 1:
            rules = [
        "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
        "○ Finish the maze before time runs out or you get caught",
        "○ You will have 20 seconds to complete each maze"
            ]
        else:
            rules = [
        "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
        "○ Finish the maze before time runs out or you get caught",
        "○ You will have 10 seconds to complete each maze"
            ]

    elif app.currentMode == "Eternalism":
        if app.difficultySelectionIndex == 0:
            rules = [
        "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
        "○ There is no time limit to complete the maze",
        "○ Nobody is trying to catch you" 
            ]
        elif app.difficultySelectionIndex == 1:
            rules = [
        "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
        "○ There is no time limit to complete the maze",
        "○ Finish before you get caught (only 1 person trying to catch you)" 
            ]
        else:
            rules = [
        "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
        "○ There is no time limit to complete the maze",
        "○ Finish the maze before you get caught"
            ]

    else:
        if app.difficultySelectionIndex == 0:
            rules = [
    "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
    "○ Finish the maze in 30 seconds, or before you get caught",
    "○ As time runs out, your happiness depletes & your enemies multiply",
    "○ Pick up hearts to increase happiness & kill your enemies with kindness"
            ]
        elif app.difficultySelectionIndex == 1:
            rules = [
    "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
    "○ Finish the maze in 20 seconds, or before you get caught",
    "○ As time runs out, your happiness depletes & your enemies multiply",
    "○ Pick up hearts to increase happiness & kill your enemies with kindness"
            ]
        else:
            rules = [
    "○ Use arrow keys to move, 'e' to end game, 'r' to reset, 'p' to pause",
    "○ Finish the maze in 10 seconds, or before you get caught",
    "○ As time runs out, your happiness depletes & your enemies multiply",
    "○ Pick up hearts to increase happiness & kill your enemies with kindness"
            ]

    for index in range(len(rules)):
        canvas.create_text(textSpacing, textSpacing*6 + 25*index,
                            text = f"{rules[index]}", anchor = 'w',
                            font = "Arial 15 italic", fill = "white")



#################################################
# Game Functions
#################################################

# When in game mode and not paused / Game over), executes the steps in doStep
def game_timerFired(app):
    if not app.paused:
        game_doStep(app)


# Decrease the time and happiness (if applicable). Checks for win or collision
def game_doStep(app):
    app.elapsedTime = time.time() - app.startTime - app.pausedTime

    if app.gameOver:
        if app.player.score > app.highScore:
            prevHighScore = app.highScore
            app.highScore = app.player.score
            updateHighScores(app, prevHighScore)
        app.mode = 'gameOver'
        appReset(app)

    else:
        
        if not app.collideAnimation:
            checkForWin(app)
            game_animateGoal(app)
            
            if app.isTimed and app.timeLimit - app.elapsedTime < 0:
                app.gameOver = True
            
            if app.hasHappinessLevel:
                checkForHeartPickup(app)
                addEnemy = random.choice([True] + [False]*14)
                if addEnemy: app.enemies.append(Enemy(app))
            
        if app.hasEnemies:
            for enemy in app.enemies:
                if not app.collideAnimation:
                    (x, y) = random.choice([(0, -1), (0, 1), (1, 0), (-1, 0)])
                    enemy.move(x, y)
                    app.collideTime = app.elapsedTime
                
                if enemyCollision(app, enemy):
                    collisionAnimation(app)
                    if app.elapsedTime - app.collideTime > 2:
                        app.gameOver = True


def checkForHeartPickup(app):
    for heart in app.hearts:
        if heart.x == app.player.x and heart.y == app.player.y:
            app.hearts.remove(heart)
            app.numHearts += 1
            if len(app.enemies) > 0: app.enemies.pop()


def enemyCollision(app, enemy):
    if enemy.x == app.player.x and enemy.y == app.player.y:
        return True
    return False


# Causes the goal dot to pulse / change (makes it stand out as a target / goal)
def game_animateGoal(app):
    if app.goalMargin > app.playerMargin:
        app.goalMargin = -1
    app.goalMargin += 1


# Increases score by 1 and creates new maze if player completes current one
def checkForWin(app):
    if app.player.x == app.goal.x and app.player.y == app.goal.y:
        app.player.score += 1
        appReset(app)


def collisionAnimation(app):
    animationTime = app.elapsedTime - app.collideTime
    app.collideAnimation = True
    app.explosionRadius += app.timeLimit//10
    if animationTime < 0.25:
        app.explosionStipple = "gray25"
    elif animationTime < 0.5:
        app.explosionStipple = "gray50"
    elif animationTime < 1:
        app.explosionStipple = "gray75"
    elif animationTime < 1.25:
        app.explosionStipple = ""
    elif animationTime < 1.5:
        app.explosionStipple = ""
    elif animationTime < 1.75:
        app.explosionStipple = "gray75"
    elif animationTime < 2:
        app.explosionStipple = "gray50"
    else:
        app.explosionStipple = "gray25"
    
# Defines how our game view will change according to certain keyboard inputs
def game_keyPressed(app, event):
    if event.key.lower() == "p":
        app.paused = not app.paused
        if app.paused:
            app.startPause = time.time()
        else:
            app.endPause = time.time()
            app.pausedTime += app.endPause - app.startPause
    
    elif event.key.lower() == "r":
        appReset(app)

    elif event.key.lower() == "e":
        app.gameOver = True
    
    if not app.paused and not app.collideAnimation:
        if event.key == "Up":
            app.player.move(0, -1)

        elif event.key == "Down":
            app.player.move(0, 1)

        elif event.key == "Right":
            app.player.move(1, 0)

        elif event.key == "Left":
            app.player.move(-1, 0)


# View functions for game mode
def game_redrawAll(app, canvas):
    # Background
    canvas.create_rectangle(0, 0, app.width, app.height, 
                        fill = app.backgroundColour)
    
    drawPlayerAndScore(app, canvas)
    drawMaze(app, canvas)
   
    if app.isTimed:
        drawTimer(app, canvas)
    if app.hasEnemies:
        drawEnemies(app, canvas)
    
    if app.hasHappinessLevel:
        drawHappinessMeterAndHearts(app, canvas)
    
    drawGoal(app, canvas)

    if app.collideAnimation:
        drawCollision(app, canvas)

# Displays the current time left in the top-right
def drawTimer(app, canvas):
    # Idea to calculate time like this from TP mentor during check-in 2 (08/11)
    if app.collideAnimation:
        currentTime = app.timeLimit - int(app.collideTime)
    else:
        currentTime = app.timeLimit - int(app.elapsedTime)
    canvas.create_text(app.width - app.margin, 25, anchor = "e", fill = "white",
                        text = f"Time: {currentTime}", 
                        font = "Arial 15 bold")


# Draws the player piece and displays the current score in the top-left
def drawPlayerAndScore(app, canvas):
    canvas.create_text(app.margin, 25, text = f"Score: {app.player.score}", 
                        anchor = "w", font = "Arial 15 bold", fill = "white")

    x0, y0, x1, y1 = getCellBounds(app, app.player.y, app.player.x)
    x0 += app.playerMargin
    y0 += app.playerMargin
    x1 -= app.playerMargin
    y1 -= app.playerMargin
    
    if app.currentMode == "Absolutism":
        margin = max(7, app.playerMargin)
        canvas.create_polygon(x0, y1, x1, y1, (x0+x1)//2, y0,
                             fill = "white", width = 0)
        canvas.create_polygon(x0 + margin, y0 + margin,
                             x1 - margin, y0 + margin,
                             (x0+x1)//2, y1 - 0.5*margin,
                             fill = app.backgroundColour, width = 0)

    elif app.currentMode == "Eternalism":
        margin = 3
        canvas.create_polygon(x0, y0, x1, y0, (x0+x1)//2, (y0+y1)//2, 
                            fill = "sandy brown", width = 0)
        canvas.create_polygon(x0, y1, x1, y1, (x0+x1)//2, (y0+y1)//2, 
                            fill = "white", width = 0)
        canvas.create_polygon(x0 + 2*margin, y0 + margin,
                            x1 - 2*margin, y0 + margin,
                            (x0+x1)//2, (y0+y1)//2 - margin, 
                            fill = app.backgroundColour, width = 0)
        canvas.create_polygon(x0 + 2*margin, y1 - margin,
                            x1 - 2*margin, y1 - margin,
                            (x0+x1)//2, (y0+y1)//2 + margin, 
                            fill = app.backgroundColour, width = 0)

    else:
        margin = min(5, app.playerMargin)
        canvas.create_oval(x0, y0, x1, y1, fill = "light salmon", width = 0)
        canvas.create_oval(x0 + margin, y0 + margin, x1 - margin, y1 - margin, 
                            fill = "peach puff", width = 0)

        canvas.create_oval(x1 - 1.2*margin, y0 + 1.5*margin, 
                        (x0+x1)//2 - 0.2*margin, y1 - (y1-y0)//2 + margin//2,
                        fill = "orange red", width = 0)
        
        canvas.create_oval(x0 + 1.2*margin, y0 + 1.5*margin, 
                        (x0+x1)//2 + 0.2*margin, y1 - (y1-y0)//2 + margin//2, 
                        fill = "orange red", width = 0)

        canvas.create_polygon(x0 + 0.9*margin, 
                        (y0 + (y1 + y0)//2 + 2.7*margin)//2,
                        x1 - margin, 
                        (y0 + (y1 + y0)//2 + 2.7*margin)//2, 
                        (x0+x1)//2, y1 - margin, fill = "orange red")


# Loops through list app.maze (stores instances of Maze Class) & draws cell
def drawMaze(app, canvas):
    for mazeCell in app.maze:
        x0, y0, x1, y1 = getCellBounds(app, mazeCell.row, mazeCell.col)
        if mazeCell.leftBound:
            canvas.create_line(x0, y0, x0, y1, fill = mazeCell.colour)
        if mazeCell.rightBound:
            canvas.create_line(x1, y0, x1, y1, fill = mazeCell.colour)
        if mazeCell.upBound:
            canvas.create_line(x0, y0, x1, y0, fill = mazeCell.colour)
        if mazeCell.downBound:
            canvas.create_line(x0, y1, x1, y1, fill = mazeCell.colour)


# Draws pulsing dot in random location (marks our goal for that round)
def drawGoal(app, canvas):
    x0, y0, x1, y1 = getCellBounds(app, app.goal.y, app.goal.x)
    x0 += 3*app.playerMargin
    y0 += 3*app.playerMargin
    x1 -= 3*app.playerMargin
    y1 -= 3*app.playerMargin
    canvas.create_oval(x0, y0, x1, y1, fill = app.goal.colour, width = 0)
    canvas.create_oval(x0 + app.goalMargin, y0 + app.goalMargin,
                      x1 - app.goalMargin, y1 - app.goalMargin, 
                      fill = app.backgroundColour, width = 0)
    canvas.create_oval(x0 + 2*app.goalMargin, y0 + 2*app.goalMargin,
                      x1 - 2*app.goalMargin, y1 - 2*app.goalMargin,
                      fill = app.goal.colour, width = 0)


# Draws the white enemy rings (if collide with player, game is over)
def drawEnemies(app, canvas):
    margin = 5
    for enemy in app.enemies:
        x0, y0, x1, y1 = getCellBounds(app, enemy.y, enemy.x)
        x0 += app.playerMargin
        y0 += app.playerMargin
        x1 -= app.playerMargin
        y1 -= app.playerMargin
        canvas.create_oval(x0, y0, x1, y1, fill = enemy.colour, width = 0)
        canvas.create_oval(x0 + margin, y0 + margin, x1 - margin, y1 - margin,
                        fill = app.backgroundColour, width = 0)


# In Idealism mode, draws happiness meter (top of screen) & hearts (in the maze)
def drawHappinessMeterAndHearts(app, canvas):
    if app.collideAnimation:
        currentTime = app.timeLimit - int(app.collideTime)
    else:
        currentTime = app.timeLimit - int(app.elapsedTime)
    currentHappiness = min(app.timeLimit, currentTime + app.numHearts)
    happinessMeter = [0 for i in range(currentHappiness)]
    unitSize = 100/app.timeLimit

    for i in range(len(happinessMeter)):
        x0 = app.width//2 - 50 + (i*unitSize)
        y0 = 15
        x1 = x0 + unitSize
        y1 = 35
        canvas.create_rectangle(x0, y0, x1, y1, fill = "peach puff", width = 0)
    canvas.create_rectangle(app.width//2 - 50, 15, app.width//2 + 50, 35,
                            width = 2, outline = "white")
    
    margin = min(5, app.playerMargin)
    for heart in app.hearts:
        x0, y0, x1, y1 = getCellBounds(app, heart.y, heart.x)
        x0 += app.playerMargin
        y0 += app.playerMargin
        x1 -= app.playerMargin
        y1 -= app.playerMargin
        canvas.create_oval(x1 - 1.2*margin, y0 + 1.5*margin, 
                        (x0+x1)//2 - 0.2*margin, y1 - (y1-y0)//2 + margin//2,
                        fill = heart.colour, width = 0)
        
        canvas.create_oval(x0 + 1.2*margin, y0 + 1.5*margin, 
                        (x0+x1)//2 + 0.2*margin, y1 - (y1-y0)//2 + margin//2, 
                        fill = heart.colour, width = 0)

        canvas.create_polygon(x0 + 0.9*margin, 
                        (y0 + (y1 + y0)//2 + 2.7*margin)//2,
                        x1 - margin, 
                        (y0 + (y1 + y0)//2 + 2.7*margin)//2, 
                        (x0+x1)//2, y1 - margin, fill = heart.colour)


def drawCollision(app, canvas):
    r = 1.4*app.explosionRadius
    r1 = 1.2*app.explosionRadius
    r2 = app.explosionRadius
    bitmap = app.explosionStipple

    (x0, y0, x1, y1) = getCellBounds(app, app.player.y, app.player.x)
    cx = (x0+x1)//2
    cy = (y0+y1)//2
    fontSize = max(int(2*r2/3), 5)
    if app.collideAnimation:
        if app.currentMode == "Eternalism":
            explosionColour = "sandy brown"
            textColour = "saddle brown"
        else:
            explosionColour = "white"
            textColour = "red"
        canvas.create_polygon(cx, cy - 2*r, cx - 2*r, cy + r, cx + 2*r, cy + r,
                            fill = explosionColour, stipple = bitmap)
        canvas.create_polygon(cx, cy + 2*r, cx - 2*r, cy - r, cx + 2*r, cy - r,
                            fill = explosionColour, stipple = bitmap)
        canvas.create_polygon(cx, cy - 2*r1, cx - 2*r1, 
                            cy + r1, cx + 2*r1, cy + r1,
                            fill = app.backgroundColour, stipple = bitmap)
        canvas.create_polygon(cx, cy + 2*r1, cx - 2*r1, cy - r1, 
                            cx + 2*r1, cy - r1,
                            fill = app.backgroundColour, stipple = bitmap)
        canvas.create_polygon(cx, cy - 2*r2, cx - 2*r2, cy + r2, 
                            cx + 2*r2, cy + r2,
                            fill = explosionColour, stipple = bitmap)
        canvas.create_polygon(cx, cy + 2*r2, cx - 2*r2, cy - r2,
                            cx + 2*r2, cy - r2,
                            fill = explosionColour, stipple = bitmap)
        canvas.create_text(cx, cy, text = "BANG!", 
                            font = f"Arial {fontSize} bold",fill = textColour)

#################################################
# Maze Generation & Class
#################################################

def createMaze(app):
    app.mazeDict = createMazeDict(app.rows, app.cols)
    createMazeClassInstances(app)


# Created using Prim's algorithm, from the explanations seen on:
    # https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
    # https://en.wikipedia.org/wiki/Maze_generation_algorithm

def createMazeDict(colNum, rowNum):
    gridCoords = []
    frontierCells = list()
    mazeD = dict()
    # Using a dict inspired by Graph mini-lecture during TP Kickoff (08/08/21)

    for row in range(rowNum):
        for col in range(colNum):
            coord = (row,col)
            gridCoords.append(coord)

    cellIndex = random.randint(0, len(gridCoords) - 1)
    currentCell = gridCoords.pop(cellIndex)
    mazeD[currentCell] = set()

    while len(gridCoords) > 0:
        frontierCells = adjacentCells(mazeD, colNum, rowNum, frontierCells)
        currentFrontierCell = random.choice(frontierCells)
        frontierCells.remove(currentFrontierCell)
        currentCell = adjacentToFrontierCell(mazeD, currentFrontierCell)
        mazeD[currentCell].add(currentFrontierCell)

        if currentFrontierCell not in mazeD:
            mazeD[currentFrontierCell] = set()
        mazeD[currentFrontierCell].add(currentCell)

        gridCoords.remove(currentFrontierCell)
    
    return mazeD


# Returns a cell that is adjacent to the chosen frontier cell
def adjacentToFrontierCell(dictionary, frontier):
    (row, col) = frontier
    for cell in dictionary:
        if (cell == (row, col-1) or cell == (row, col+1) 
            or cell == (row-1,col) or cell == (row+1, col)):
            return cell


# When new cell added to the maze (i.e. dictionary), adds the cells adjacent
# to it to the list of frontier cells
def adjacentCells(dictionary, maxCol, maxRow, frontierCells):
    for startCell in dictionary:
        (row,col) = startCell
        for (drow, dcol) in [(0,-1), (0, 1), (-1,0), (1, 0)]:
            adjacentCell = (row+drow, col+dcol)
            if (drow != dcol and row + drow > -1 and row + drow < maxRow
                    and col + dcol > -1 and col + dcol < maxCol
                    and adjacentCell not in frontierCells
                    and adjacentCell not in dictionary):
                frontierCells.append(adjacentCell)

    return frontierCells


# Loops through key-value pairs in maze dict and creates Maze class instances 
# for each cell (each cell has boolean values for the state of their boundaries)
def createMazeClassInstances(app):
    for coord in app.mazeDict:
        (row1, col1) = coord
        left, right, up, down = True, True, True, True

        for adjacentCell in app.mazeDict[coord]:
            (row2, col2) = adjacentCell

            if row2 == row1 + 1: down = False
            elif row2 == row1 - 1: up = False
            if col2 == col1 + 1: right = False
            elif col2 == col1 - 1: left = False

        app.maze.append(MazeCells(app, row1, col1, left, right, up, down))


# Maze Class: inspired by the OOP mini-lecture during TP Kickoff (08/08/21)
class MazeCells(object):
    def __init__(self, app, r, c, leftBound, rightBound, upBound, downBound):
        self.app = app
        self.row, self.col = r, c
        self.leftBound, self.rightBound = leftBound, rightBound
        self.upBound, self.downBound = upBound, downBound

        if app.currentMode == "Eternalism": self.colour = "sandy brown"
        else: self.colour = "white"



#################################################
# Player and Enemy Classes
#################################################

# Player Class: inspired by the OOP mini-lecture during TP Kickoff (08/08/21)
class Player(object):
    def __init__(self, app):
        self.app = app
        self.radius = app.cellSize//2
        self.score = 0
        self.x, self.y = 0, 0
        self.currentCell = (self.y,self.x)


    def move(self, x, y):
        self.prevCell = (self.y, self.x)
        self.y += y
        self.x += x
        if not self.validMove():
            self.y -= y
            self.x -= x

    # Checks if move within grid bounds & player isn't crossing a maze barrier
    def validMove(self):
        self.currentCell = (self.y, self.x)
        if (self.x < 0 or self.x > self.app.cols - 1 
            or self.y < 0 or self.y > self.app.rows - 1
            or self.currentCell not in self.app.mazeDict[self.prevCell]):
            return False
        return True


# Enemy Class: inspired by the OOP mini-lecture during TP Kickoff (08/08/21)
class Enemy(Player):
    def __init__(self, app):
        super().__init__(app)
        # Enemies move randomly (but validly)
        self.x = random.randint(0, app.cols - 1)
        self.y = random.randint(app.rows//3, app.rows - 1)
        self.colour = "white"



#################################################
# Heart Class (for Idealism mode) & Goal Class
#################################################
class Heart(object):
    def __init__(self, app):
        self.colour = "light salmon"
        self.radius = app.cellSize//2
        self.x = random.randint(0, app.cols - 1)
        self.y = random.randint(0, app.rows - 1)
        
# inspired by the OOP mini-lecture during TP Kickoff (08/08/21)
class Goal(object):
    def __init__(self, app):
        self.app = app
        self.colour = "white"
        self.radius = app.cellSize//2
        self.x = random.randint(app.cols//2, app.cols - 1)
        self.y = random.randint(app.rows//2, app.rows - 1)



#################################################
# Game Over Functions
#################################################

# View functions for gameOver mode
def gameOver_redrawAll(app, canvas):
    # Background colour
    canvas.create_rectangle(0, 0, app.width, app.height, 
                        fill = app.backgroundColours[app.modeSelectionIndex])
    
    # Title of the game
    canvas.create_text(100, 250, text = "GAME\nOVER", anchor = 'w',
                        fill = "white", font = "Arial 140 bold")
    
    # Player Score
    canvas.create_text(100, 550, fill = "white", font = "Arial 50",
                        text = f"Score {app.player.score}", anchor = "nw")
    
    # High Score
    canvas.create_text(100, 650, fill = "white", font = "Arial 50",
                        text = f"High Score {app.highScore}", anchor = "nw")
    
    # Buttons
    fontStyle = "Arial 15 bold"
    canvas.create_rectangle(app.width - 3.5*app.margin, 560,
                        app.width - 25, 600,
                        fill = app.rButton, outline = "white", width = 3)
    canvas.create_text(656, 580, fill = app.rText, font = fontStyle,
                       text = "RESTART")


    canvas.create_rectangle(app.width - 3.5*app.margin, 617,
                        app.width - 25, 657,
                        fill = app.dButton, outline = "white", width = 3)
    canvas.create_text(656, 637, fill = app.dText, font = fontStyle,
                       text = "CHANGE DIFFICULTY")


    canvas.create_rectangle(app.width - 3.5*app.margin, 674,
                        app.width - 25, 714,
                        fill = app.mButton, outline = "white", width = 3)
    canvas.create_text(656, 694, fill = app.mText, font = fontStyle,
                       text = "CHANGE MODE")


# Creates a hover effect for the buttons. Syntax from course website at:
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#events
def gameOver_mouseMoved(app, event):
    btnColr = app.backgroundColour
    buttonXCoord = app.width - 3.5*app.margin < event.x < app.width - 25
    if buttonXCoord and 560 < event.y < 600:
        app.rText, app.mButton, app.dButton = btnColr, btnColr, btnColr
        app.rButton, app.mText, app.dText = "white", "white", "white"
        
    elif buttonXCoord and 617 < event.y < 657:
        app.rButton, app.mButton, app.dText = btnColr, btnColr, btnColr
        app.rText, app.mText, app.dButton = "white", "white", "white"
        
    elif buttonXCoord and 674 < event.y < 714:
        app.rButton, app.mText, app.dButton = btnColr, btnColr, btnColr
        app.rText, app.mButton, app.dText = "white", "white", "white"
        
    else:
        app.rButton, app.mButton, app.dButton = btnColr, btnColr, btnColr
        app.rText, app.mText, app.dText = "white", "white", "white"


# Changes the app mode if a button is pressed 
def gameOver_mousePressed(app, event):
    if app.width - 3.5*app.margin <= event.x <= app.width - 25:
        app.player.score = 0
        if 560 <= event.y <= 600:
            app.mode = "game"
        elif 617 <= event.y <= 657:
            app.mode = "chooseDifficulty"            
        elif 674 <= event.y <= 714:
            app.mode = "chooseMode"
    appReset(app)



#################################################
# High Score Functions (Using file IO)
#################################################

# readFile and writeFile are taken from the course website at: 
    # https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)


# Returns the current high score for the current mode and difficulty level
def highScoreFromFile(app):
    highScore = ""
    highScoreString = (readFile("highScores.txt"))
    for line in highScoreString.splitlines():
        if (line.startswith(app.currentMode) and
            line.endswith(app.currentDifficulty)):
            for char in line:
                if char.isdigit(): highScore += char
            return int(highScore)
    return 0


# When player beats current high score, file is updated with the new score
def updateHighScores(app, prevHighScore):
    highScoreString = (readFile("highScores.txt"))
    updatedScoreList = []
    for line in highScoreString.splitlines():
        if (line.startswith(app.currentMode) and 
            line.endswith(app.currentDifficulty)):
            line = line.replace(str(prevHighScore),str(app.highScore))
        updatedScoreList.append(line)
    
    highScoreString = "\n".join(updatedScoreList)
    writeFile("highScores.txt", highScoreString)



#################################################
# Running the app
#################################################
runApp(width = 800, height = 800)
