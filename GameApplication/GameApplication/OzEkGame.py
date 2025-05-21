#importlar
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from turtle import TurtleScreen, RawTurtle
from datetime import datetime
import random
import sqlite3
"""
conn = sqlite3.connect('ozekGame.db')
cursor = conn.cursor()
command1 = "CREATE TABLE IF NOT EXISTS Users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT, Level INTEGER)"
cursor.execute(command1)
command2 = "CREATE TABLE IF NOT EXISTS Games(game_id INTEGER PRIMARY KEY AUTOINCREMENT, Game_Name TEXT)"
cursor.execute(command2)
command3 = "CREATE TABLE IF NOT EXISTS Scores(score_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, game_id INTEGER, Score FLOAT, FOREIGN KEY(user_id) REFERENCES Users(user_id), FOREIGN KEY(game_id) REFERENCES Games(game_id))"
cursor.execute(command3)

cursor.execute("INSERT INTO Users VALUES (0, 'admin', 1234, 1)")
cursor.execute("INSERT INTO Users VALUES (1, 'ekin', 3124, 1)")
cursor.execute("INSERT INTO Users VALUES (2, 'yuki', 1632, 1)")

cursor.execute("INSERT INTO Games VALUES (1, 'Memory Game')")
cursor.execute("INSERT INTO Games VALUES (2, 'Hangman')")
cursor.execute("INSERT INTO Games VALUES (3, 'Fast Typing')")

cursor.execute("INSERT INTO Scores VALUES (1, 0, 1, 30.0)")
conn.commit()
"""
#ilk pencere açılımı
window = Tk()
window.title("Kullanıcı Giriş Ekranı")
window.geometry("390x220")
window.resizable(width=False, height=False)

#background
bgPath = "Images\\MemoryGame\\bg.jpg"
bg = ImageTk.PhotoImage(Image.open(bgPath))
bgLabel = Label(window, image=bg)
bgLabel.place(relwidth=1, relheight=1)

#yandaki resim
resim = ImageTk.PhotoImage(Image.open("Images\\Icons\\login.png").resize((100, 100)))
lresim = Label(window, image=resim)
lresim.place(x=250, y=10)

#girilen değerlerin doğruluğunu kontrol eder
def giris():
    username = E1.get()
    password = E2.get()
    if username and password:  # Ensure both fields are filled
        conn = sqlite3.connect('ozekGame.db')
        cur = conn.cursor()

        # Query the database to check if the username and password match
        cur.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
        user = cur.fetchone()  # Fetch the result

        conn.close()

        if user:
            messagebox.showinfo("Login Success", "Login successful!")
            getUserInfo(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    else:
        messagebox.showwarning("Input Error", "Please enter both a username and a password.")
def getUserInfo(user):
    global usn, uid, lvl
    user_id, username, password, level = user
    uid = user_id
    usn = username
    lvl = level
    toMenu()
usn = ""
lvl = 0
uid = 0
def signup():
    window.withdraw()
    signupWin = Toplevel()
    signupWin.title("Sign Up")
    signupWin.geometry("390x220")
    signupWin.resizable(width=False, height=False)

    def toLogin():
        signupWin.destroy()
        window.deiconify()

    def on_click_signupButton():
        username = usernameEntry.get()
        password = passwordEntry.get()
        if username and password:  # Ensure both fields are filled
            registerUser(username, password)
        else:
            messagebox.showwarning("Input Error", "Please enter both a username and a password.")

    def registerUser(u, p):
        conn = sqlite3.connect('ozekGame.db')
        cur = conn.cursor()

        # Insert new user into the users table (password is stored in plaintext)
        cur.execute("INSERT INTO users (Username, Password, Level) VALUES (?, ?, 1)", (u, p))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"User {u} registered successfully.")

    bgPath = "Images\\MemoryGame\\bg.jpg"
    bg = ImageTk.PhotoImage(Image.open(bgPath))
    bgLabel = Label(signupWin, image=bg)
    bgLabel.place(relwidth=1, relheight=1)

    welcomeLabel = Label(signupWin, text="Welcome to OzEk Games!", font=("Arial", 16), bg="#1470B9", foreground="white")
    welcomeLabel.grid(row=0, column=0, columnspan=2, sticky="wen", padx=30, pady=10)

    usernameLabel = Label(signupWin, text="Username: ", bg="#1470B9", foreground="white", font=("Arial", 12))
    passwordLabel = Label(signupWin, text="Password: ", bg="#1470B9", foreground="white", font=("Arial", 12))
    usernameLabel.grid(row=1, column=0, sticky="w", padx=(50, 30), pady=(10, 10))
    passwordLabel.grid(row=2, column=0, sticky="w", padx=(50, 30))

    usernameEntry = Entry(signupWin, width=30)
    passwordEntry = Entry(signupWin, width=30)
    usernameEntry.grid(row=1, column=1, sticky="w", padx=30)
    passwordEntry.grid(row=2, column=1, sticky="w", padx=30)

    signupButton = Button(signupWin, text="Sign Up", width=8, command=on_click_signupButton)  # Set smaller width
    signupButton.grid(row=3, column=0, columnspan=2, pady=(20, 0))  # Center it horizontally
    signupWin.grid_columnconfigure(0, weight=1)  # Center contents in column 0
    signupWin.grid_columnconfigure(1, weight=1)  # Center contents in column 1

    backPath = "Images\\Icons\\back.png"
    backIcon = ImageTk.PhotoImage(Image.open(backPath).resize((50, 50)))
    backButton = Button(signupWin, image=backIcon, command=toLogin)
    backButton.grid(row=4, column=0, sticky="ws", padx=20, pady=(0, 15))
    signupWin.grid_rowconfigure(4, weight=1)

    signupWin.mainloop()

def toMenu():
    global usn, uid
    window.withdraw()
    menu = Toplevel()
    menu.title("Kullanıcı Giriş Ekranı")
    menu.geometry("400x400")
    menu.attributes('-fullscreen',True)

    bgPath = "Images\\MemoryGame\\bg.jpg"
    partbgPath = "Images\\MemoryGame\\partbg.png"
    bg = ImageTk.PhotoImage(Image.open(bgPath))
    partbg = ImageTk.PhotoImage(Image.open(partbgPath))
    bgLabel = Label(menu, image=bg)
    bgLabel.place(relwidth=1, relheight=1)

    def saveScore(user_id, game_id, score):
        conn = sqlite3.connect('ozekGame.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO Scores (user_id, game_id, score_time, score_moves) VALUES (?, ?, ?, ?)",
                    (user_id, game_id, score))
        conn.commit()
        conn.close()

    def toMemoryGameMenu():
        global usn, uid
        menu.destroy()
        memoryMenu = Toplevel()

        memoryMenu.title("Memory Game Menu")
        memoryMenu.geometry("1920x1200")
        memoryMenu.attributes('-fullscreen',True)

        bgPath = "Images\\MemoryGame\\bg.jpg"
        partbgPath = "Images\\MemoryGame\\partbg.png"
        bg = ImageTk.PhotoImage(Image.open(bgPath))
        partbg = ImageTk.PhotoImage(Image.open(partbgPath))
        bgLabel = Label(memoryMenu, image=bg)
        bgLabel.place(relwidth=1, relheight=1)

        chosenTheme = ""

        def selectTheme(theme):
            global chosenTheme
            themeLabel["text"] = f"Selected Theme : {theme}"
            chosenTheme = theme

        def play():
            global chosenTheme
            memoryMenu.destroy()
            playMemory = Toplevel()

            playMemory.title("Memory Game")
            playMemory.geometry("1920x1200")
            playMemory.attributes('-fullscreen',True)
            playMemory.rowconfigure(0, weight=1)
            playMemory.columnconfigure(0, weight=1)

            bgLabel = Label(playMemory, bg="black")
            bgLabel.place(relwidth=1, relheight=1)

            def showTheImageBehind(row, col):
                global selectedCardNumber, selectedButtons, matchedCards, moveCount

                startTimer()

                # aynı butona mı basılmış diye bakıyor
                if any(button["row"] == row and button["col"] == col for button in selectedButtons.values()):
                    return

                # açılmış kartlara mı basılmış diye bakıyor
                card_index = row * cols + col
                if gameCards[card_index] in matchedCards:
                    return

                # Reveal the selected card
                selectedButtons[selectedCardNumber] = {"row": row, "col": col, "image": gameCards[card_index]}
                buttons[row][col].config(image=cardImages[card_index])

                selectedCardNumber += 1
                if selectedCardNumber == 2:
                    moveCount += 1
                    # Check if the selected cards match
                    if selectedButtons[0]["image"] == selectedButtons[1]["image"]:
                        matchedCards.append(selectedButtons[0]["image"])
                        checkGameEnds()
                        selectedButtons = {}
                    else:
                        playMemory.after(500, resetCards)
                    selectedCardNumber = 0

            def resetCards():
                for i in range(2):
                    buttons[selectedButtons[i]["row"]][selectedButtons[i]["col"]].config(image=backofCard)
                selectedButtons.clear()

            def checkGameEnds():
                global timerRunning
                if len(matchedCards) == len(gameCards) / 2:
                    print("game ended")
                    timerRunning = False
                    timerLabel.config(text=f"Game Over! Time: {timeElapsed}s Move Count: {moveCount}")
                    print(moveCount)
                    gameOver()
                else:
                    print("continue")

            def startTimer():
                global timerStarted, timerRunning
                if not timerStarted:
                    timerStarted = True
                    timerRunning = True
                    updateTimer()

            def updateTimer():
                global timeElapsed, timerRunning
                if timerRunning:
                    timeElapsed += 1
                    timerLabel.config(text=f"Time: {timeElapsed}s")
                    playMemory.after(1000, updateTimer)

            def restartGame():
                global selectedCardNumber, selectedButtons, matchedCards, moveCount, timeElapsed, timerRunning, timerStarted
                selectedCardNumber = 0
                selectedButtons = {}
                matchedCards = []
                moveCount = 0
                timeElapsed = 0
                timerRunning = False
                timerStarted = False
                timerLabel.config(text="Time: 0s")
                random.shuffle(gameCards)
                for r in range(rows):
                    for c in range(cols):
                        buttons[r][c].config(image=backofCard)

            def gameOver():
                global uid
                resultplayMemory = Toplevel()
                resultplayMemory.title("Game Over")
                resultplayMemory.geometry("300x300")
                resultplayMemory.configure(bg="lightblue")

                saveScore(uid, 1, timeElapsed)

                messageLabel = Label(resultplayMemory, text="Congrats!", font=("Arial", 18), bg="lightblue")
                restartButton = Button(resultplayMemory, image=restartIcon, font=("Arial", 14), command=restartGame,
                                       bg="lightblue")
                mainMenuButton = Button(resultplayMemory, image=homeIcon, font=("Arial", 14), command=toMainMenu,
                                        bg="lightblue")
                timePassedLabel = Label(resultplayMemory, text=f"Time : {timeElapsed}", font=("Arial", 14), bg="lightblue")
                attemptsLabel = Label(resultplayMemory, text=f"Move : {moveCount}", font=("Arial", 14), bg="lightblue")

                timePassedLabel.grid(row=1, column=0, sticky="e", pady=30, padx=10)
                attemptsLabel.grid(row=1, column=1, sticky="w", pady=30, padx=10)
                messageLabel.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=30)
                restartButton.grid(row=2, column=0, sticky="e", pady=30, padx=10)
                mainMenuButton.grid(row=2, column=1, sticky="w", pady=30, padx=10)

                resultplayMemory.grid_rowconfigure(0, weight=1)  # Center vertically
                resultplayMemory.grid_rowconfigure(1, weight=1)  # Adjust button alignment
                resultplayMemory.grid_columnconfigure(0, weight=1)  # Center horizontally
                resultplayMemory.grid_columnconfigure(1, weight=1)
                resultplayMemory.mainloop()

            def toMainMenu():
                playMemory.destroy()
                toMenu()
                print("Main menu is under construction")

            def getHighestScore(user_id, game_id):
                conn = sqlite3.connect('ozekGame.db')
                cur = conn.cursor()

                cur.execute("select Score from Scores where user_id = ? and game_id = ? order by Score desc limit 1",
                            (user_id, game_id))
                return cur.fetchall()

            global selectedCardNumber, selectedButtons, moveCount, matchedCards
            selectedCardNumber = 0
            selectedButtons = {}
            matchedCards = []
            moveCount = 0

            backofCard = ImageTk.PhotoImage(Image.open("Images\\MemoryGame\\backofcard.jpg").resize((177, 384)))


            if chosenTheme == "TKDB":
                cards = ["Amoral_Attorney",
                         "Cosmic_Carnation",
                         "Hazy_Spectacle",
                         "Incongruous_Bones",
                         "Indomitable_Outlaw",
                         "Languid_Prisoner",
                         "Neon_Night",
                         "Ordinary_Happiness",
                         "Perfect_Mirror",
                         "Poetic_Promenade",
                         "Riverside_Gloaming",
                         "Sadistic_Warden",
                         "The_Fool",
                         "Unearthly_Bohemian",
                         "Unworldly_Respite",
                         "Witty_Priest"]
            elif chosenTheme == "DBD":
                cards = ["TheClown",
                         "TheDemogorgon",
                         "TheDoctor",
                         "TheExecutioner",
                         "TheGhostFace",
                         "TheHag",
                         "TheHillbilly",
                         "TheHuntress",
                         "TheLegion",
                         "TheNightmare",
                         "TheNurse",
                         "TheOni",
                         "ThePig",
                         "ThePlague",
                         "TheShape",
                         "TheSpirit",
                         "TheTrapper",
                         "TheTrickster",
                         "TheWraith",
                         "TheXenomorph"]
            elif chosenTheme == "E7":
                cards = ["Astromancer-Elena",
                         "Baal-Sezan",
                         "Beehoo",
                         "Blood-Moon-Haste",
                         "Briar-Witch-Iseria",
                         "Brieg",
                         "Byblis",
                         "Celine",
                         "Death-Dealer-Ray",
                         "Eda",
                         "Jenua",
                         "Lionheart-Cermia",
                         "Mort",
                         "Operator-Sigret",
                         "Schniel",
                         "Sea-Phantom-Politis"]
            elif chosenTheme == "BG3":
                cards = ["Astarion",
                         "Gale",
                         "Halsin",
                         "Jaheira",
                         "Karlach",
                         "Laezel",
                         "Minsc",
                         "Minthara",
                         "Shadowheart",
                         "Wyll"]
            elif chosenTheme == "LoL":
                cards = ["Amumu",
                         "Blitzcrank",
                         "Caitlyn",
                         "Ekko",
                         "Hecarim",
                         "Illaoi",
                         "Irelia",
                         "Jinx",
                         "Vayne",
                         "Vex",
                         "Yuumi",
                         "Ambessa",
                         "Mordekaiser",
                         "Teemo"]
            elif chosenTheme == "Undertale":
                cards = ["Alphys",
                         "Asgore_Dreemurr",
                         "Asriel_Dreemurr",
                         "Chara",
                         "Flowey",
                         "Frisk",
                         "Mettaton",
                         "Papyrus",
                         "Sans",
                         "Toriel",
                         "Undyne"]
            elif chosenTheme == "Valorant":
                cards = ["Astra",
                         "Breach",
                         "Brimstone",
                         "Chamber",
                         "Clove",
                         "Cypher",
                         "Deadlock",
                         "Fade",
                         "Gekko",
                         "Harbor",
                         "Iso",
                         "Jett",
                         "KAYO",
                         "Killjoy",
                         "Neon",
                         "Omen",
                         "Phoenix",
                         "Raze",
                         "Reyna",
                         "Sage",
                         "Skye",
                         "Sova",
                         "Viper",
                         "Vyse",
                         "Yoru"]
            else:
                print("Some problems acquired")

            cardsPath = f"Images\\MemoryGame\\{chosenTheme}\\"
            gameCards = random.sample(cards, 10) * 2
            random.shuffle(gameCards)

            cardImages = []
            for card in gameCards:
                path = f"{cardsPath}{card}.png"
                img = ImageTk.PhotoImage(Image.open(path).resize((177, 384)))
                cardImages.append(img)

            # Top frame
            topFrame = Frame(playMemory, bg="lightblue")
            topFrame.grid(row=0, column=0, sticky="new", pady=10)
            topFrame.grid_columnconfigure(0, weight=1)
            topFrame.grid_columnconfigure(1, weight=2)
            topFrame.grid_columnconfigure(2, weight=1)

            bestTime = getHighestScore(uid, 1)
            gameTheme = chosenTheme

            # sol üstteki üçlü
            titleLabel = Label(topFrame, text="Memory Game", font=("Arial", 18), bg="lightblue")
            themeLabel = Label(topFrame, text=f"Theme: {gameTheme}", font=("Arial", 18), bg="lightblue")
            bestTimeLabel = Label(topFrame, text=f"Best Time: {bestTime}", font=("Arial", 18), bg="lightblue")
            titleLabel.grid(row=0, column=0, sticky="nws", padx=10, ipady=10)
            themeLabel.grid(row=1, column=0, sticky="nws", padx=10, ipady=10)
            bestTimeLabel.grid(row=2, column=0, sticky="nws", padx=10, ipady=10)

            # ortadaki timer
            timerLabel = Label(topFrame, text="Time: 0s", font=("Arial", 24), bg="lightblue")
            timerLabel.grid(row=0, column=1, rowspan=3, padx=10, sticky="ns")

            homeIconPath = "Images\\Icons\\home.png"
            homeIcon = ImageTk.PhotoImage(Image.open(homeIconPath).resize((50, 50)))
            homeButton = Button(topFrame, image=homeIcon, font=("Arial", 14), bg="lightblue", command=toMenu)
            homeButton.grid(row=1, column=3, padx=10, pady=10, sticky="nse")

            restartIconPath = "Images\\Icons\\restart.png"
            restartIcon = ImageTk.PhotoImage(Image.open(restartIconPath).resize((50, 50)))
            restartButton = Button(topFrame, image=restartIcon, font=("Arial", 14), command=restartGame, bg="lightblue")
            restartButton.grid(row=1, column=2, padx=10, pady=10, sticky="nes")

            # Game frame
            gameFrame = Frame(playMemory, bg="black")
            gameFrame.grid(row=1, column=0, pady=50, padx=10)
            gameFrame.grid_rowconfigure(0, weight=1)
            gameFrame.grid_columnconfigure(0, weight=1)

            global timerStarted, timerRunning, timeElapsed  # Declare global variables
            timeElapsed = 0
            timerRunning = False
            timerStarted = False

            buttons = []
            rows, cols = 2, 10
            for r in range(rows):
                row_buttons = []
                for c in range(cols):
                    button = Button(gameFrame, image=backofCard, command=lambda r=r, c=c: showTheImageBehind(r, c))
                    button.grid(row=r, column=c, padx=5, pady=5)
                    row_buttons.append(button)
                buttons.append(row_buttons)
            playMemory.mainloop()


        themes = ["DBD",
                  "E7",
                  "LoL",
                  "TKDB",
                  "Undertale",
                  "Valorant",
                  "BG3"]

        themeImages = []
        for theme in themes:
            path = f"Images\\MemoryGame\\{theme}\\{theme}Theme.png"
            img = ImageTk.PhotoImage(Image.open(path).resize((250, 400)))
            themeImages.append(img)

        backIcon = ImageTk.PhotoImage(Image.open("Images\\Icons\\back.png").resize((50, 50)))
        pfpIcon = ImageTk.PhotoImage(Image.open("Images\\Icons\\profilePic.png").resize((100, 100)))

        menuFrame = Frame(memoryMenu, bg="#7AAADA")
        themeSelectorFrame = Frame(memoryMenu, bg="black")
        playFrame = Frame(memoryMenu, bg="#0364B1")

        memoryMenu.grid_rowconfigure(1, weight=1)
        memoryMenu.grid_columnconfigure(0, weight=1)

        menuFrame.grid(row=0, column=0, sticky="new", pady=50)
        themeSelectorFrame.grid(row=1, column=0, padx=10)
        playFrame.grid(row=2, column=0, pady=(50, 220))

        menuFrame.grid_columnconfigure(0, weight=1)  # Back button column
        menuFrame.grid_columnconfigure(1, weight=2)  # Spacer
        menuFrame.grid_columnconfigure(2, weight=1)  # Profile section column

        # menuFrame
        bg_label = Label(menuFrame, image=partbg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        backButton = Button(menuFrame, image=backIcon, command=toMenu)
        profilePicture = Button(menuFrame, image=pfpIcon)
        nameLabel = Label(menuFrame, text=f"{usn}")
        levelLabel = Label(menuFrame, text=f"lvl {lvl}")

        backButton.grid(row=0, column=0, sticky="w", padx=30)
        profilePicture.grid(row=0, rowspan=2, column=7, sticky="e", padx=30)
        nameLabel.grid(row=0, column=6, sticky="e", pady=(20, 0))
        levelLabel.grid(row=1, column=6, sticky="e", pady=(0, 20))

        # themeSelectorFrame
        for idx, theme in enumerate(themes):
            themeButton = Button(themeSelectorFrame, image=themeImages[idx],
                                 command=lambda theme=theme: selectTheme(theme))
            themeButton.grid(row=2, column=idx)

        # playFrame
        themeLabel = Label(playFrame, text="", font=("Arial", 24), bg="#0364B1", fg="White")
        playButton = Button(playFrame, text="Start", font=("Arial", 20), bg="#0364B1", fg="White", command=play)

        themeLabel.grid(row=0, column=0, columnspan=len(themes), sticky="ew", padx=10, pady=10)
        playButton.grid(row=1, column=0, columnspan=len(themes), sticky="ew", padx=10, pady=10)

        memoryMenu.mainloop()

    def toHangmanGame():
        global uid
        menu.destroy()
        playHangman = Toplevel()

        playHangman.title("Hangman")
        playHangman.geometry("1920x1200")
        # playHangman.attributes('-fullscreen',True)
        playHangman.rowconfigure(0, weight=1)  # Space for menuFrame
        playHangman.rowconfigure(1, weight=3)  # Space for guessFrame
        playHangman.rowconfigure(2, weight=5)  # Space for turtleFrame
        playHangman.rowconfigure(3, weight=2)  # Space for wordFrame
        playHangman.columnconfigure(0, weight=1)

        def restartGame():
            global guessCount, theWord, letters, current_word_display, result, wrongGuessCount
            theWord = random.choice(words)
            guessCount = 0
            wrongGuessCount = 0
            letters = []
            current_word_display = ["_" for _ in theWord]
            turtle.clear()
            guessALetterButton.config(state=NORMAL)
            result = ""
            updateDisplay()

        def updateDisplay():
            """Update the displayed word and remaining attempts."""
            wordLabel.config(text=" ".join(current_word_display))
            attemptsLabel.config(text=f"Attempts: {guessCount}")

        def checkGuess():
            """Check the guessed letter and update the game state."""
            global guessCount, result, wrongGuessCount

            guess = letterEntry.get().lower()
            letterEntry.delete(0, END)

            if len(guess) != 1 or not guess.isalpha():
                return

            if guess in letters:
                return

            letters.append(guess)

            if guess in theWord.lower():
                for idx, letter in enumerate(theWord):
                    if letter.lower() == guess:
                        current_word_display[idx] = letter
            else:
                wrongGuessCount += 1
                drawHangman()
            guessCount += 1
            updateDisplay()

            if "_" not in current_word_display:
                guessALetterButton.config(state=DISABLED)
                guessTheWordButton.config(state=DISABLED)
                guessEntry.config(state=DISABLED)
                letterEntry.config(state=DISABLED)
                result = "WON"
                gameOver()
            elif wrongGuessCount == 10:
                guessALetterButton.config(state=DISABLED)
                guessTheWordButton.config(state=DISABLED)
                guessEntry.config(state=DISABLED)
                letterEntry.config(state=DISABLED)
                result = "LOST"
                gameOver()

        def checkWordGuess():
            global guessCount, result, wrongGuessCount
            guess = guessEntry.get()

            guessCount += 1
            if guess.lower() == theWord.lower():  # Check if the entire word is correct
                current_word_display[:] = list(theWord)  # Reveal the full word
                updateDisplay()
                guessALetterButton.config(state=DISABLED)
                guessTheWordButton.config(state=DISABLED)
                guessEntry.config(state=DISABLED)
                letterEntry.config(state=DISABLED)
                result = "WON"
                gameOver()
            else:
                wrongGuessCount += 1
                drawHangman()
                updateDisplay()

        def drawHangman():
            """Draw parts of the hangman, centered on the canvas."""
            turtle.penup()
            if wrongGuessCount == 1:
                turtle.goto(550, -150)  # Base (horizontal line centered)
                turtle.pendown()
                turtle.goto(750, -150)
            elif wrongGuessCount == 2:
                turtle.goto(650, -150)  # Pole (vertical line upwards)
                turtle.pendown()
                turtle.goto(650, 100)
            elif wrongGuessCount == 3:
                turtle.goto(650, 100)  # Beam (horizontal line to the right)
                turtle.pendown()
                turtle.goto(700, 100)
            elif wrongGuessCount == 4:
                turtle.goto(700, 100)  # Rope (short vertical line down)
                turtle.pendown()
                turtle.goto(700, 75)
            elif wrongGuessCount == 5:
                turtle.goto(700, 50)  # Head (circle)
                turtle.pendown()
                turtle.circle(25)
            elif wrongGuessCount == 6:
                turtle.goto(700, 50)  # Body (vertical line down)
                turtle.pendown()
                turtle.goto(700, -25)
            elif wrongGuessCount == 7:
                turtle.goto(700, 35)  # Left Arm
                turtle.pendown()
                turtle.goto(670, 10)
            elif wrongGuessCount == 8:
                turtle.goto(700, 35)  # Right Arm
                turtle.pendown()
                turtle.goto(730, 10)
            elif wrongGuessCount == 9:
                turtle.goto(700, -25)  # Left Leg
                turtle.pendown()
                turtle.goto(680, -70)
            elif wrongGuessCount == 10:
                turtle.goto(700, -25)  # Right Leg
                turtle.pendown()
                turtle.goto(720, -70)

        def gameOver():
            resultWin = Toplevel()
            resultWin.title(f"You {result}")
            resultWin.geometry("300x300")
            resultWin.configure(bg="lightblue")
            messageLabel = Label(resultWin, text="", font=("Arial", 18), bg="lightblue")
            restartButton = Button(resultWin, image=restartIcon, font=("Arial", 14), command=restartGame,
                                   bg="lightblue")
            mainMenuButton = Button(resultWin, image=homeIcon, font=("Arial", 14), command=toMainMenu, bg="lightblue")
            if result == "WON":
                messageLabel["text"] = "Congrats on your WIN!"
                attemptLabel = Label(resultWin, text=guessCount, font=("Arial", 14))
                attemptLabel.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=30, bg="lightblue")
            else:
                messageLabel["text"] = "Damn you SUCK!"
            messageLabel.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=30)
            restartButton.grid(row=2, column=0, sticky="e", pady=30, padx=10)
            mainMenuButton.grid(row=2, column=1, sticky="w", pady=30, padx=10)

            saveScore(uid, 2, guessCount)

            resultWin.grid_rowconfigure(0, weight=1)  # Center vertically
            resultWin.grid_rowconfigure(1, weight=1)  # Adjust button alignment
            resultWin.grid_columnconfigure(0, weight=1)  # Center horizontally
            resultWin.grid_columnconfigure(1, weight=1)
            resultWin.mainloop()

        def toMainMenu():
            playHangman.destroy()
            toMenu()

        words = ["python",
                 "java",
                 "hangman",
                 "epic seven",
                 "valorant",
                 "LeagueOfLegends",
                 "tokyo",
                 "avallum",
                 "ravanis",
                 "CassianFloros",
                 "computer"]

        global wrongGuessCount, guessCount, letters

        theWord = random.choice(words)
        guessCount = 0
        wrongGuessCount = 0
        letters = []
        current_word_display = ["_" for _ in theWord]
        result = ""

        menuFrame = Frame(playHangman, bg="lightblue")
        guessFrame = Frame(playHangman)
        turtleFrame = Frame(playHangman)
        wordFrame = Frame(playHangman)

        menuFrame.grid(row=0, column=0, sticky="ew", pady=10)
        guessFrame.grid(row=1, column=0, sticky="nsew", pady=10)
        turtleFrame.grid(row=2, column=0, sticky="nsew", pady=20)
        wordFrame.grid(row=3, column=0, sticky="nsew", pady=10)

        menuFrame.columnconfigure(0, weight=1)
        menuFrame.columnconfigure(1, weight=2)
        menuFrame.columnconfigure(2, weight=1)

        turtleFrame.columnconfigure(0, weight=1)
        wordFrame.columnconfigure(0, weight=1)
        guessFrame.grid(row=1, column=0, sticky="nsew", pady=10)
        guessFrame.columnconfigure(0, weight=1)
        guessFrame.columnconfigure(1, weight=1)

        # sol üstteki
        titleLabel = Label(menuFrame, text="Game : Hangman", font=("Arial", 18), bg="lightblue")
        titleLabel.grid(row=0, column=0, sticky="ew", padx=10, ipady=10)

        # ortadaki attemptLabel
        attemptsLabel = Label(menuFrame, text=f"Remaining attempts: {guessCount}", font=("Helvetica", 14))
        attemptsLabel.grid(row=0, column=1, sticky="ew", padx=10)

        # ayarlar ve restart butonları
        homeIconPath = "Images\\Icons\\home.png"
        homeIcon = ImageTk.PhotoImage(Image.open(homeIconPath).resize((50, 50)))
        homeButton = Button(menuFrame, image=homeIcon, font=("Arial", 14), bg="lightblue", command=toMenu)

        restartIconPath = "Images\\Icons\\restart.png"
        restartIcon = ImageTk.PhotoImage(Image.open(restartIconPath).resize((50, 50)))
        restartButton = Button(menuFrame, image=restartIcon, font=("Arial", 14), command=restartGame, bg="lightblue")


        homeButton.grid(row=0, column=3, sticky="e", padx=10, pady=10)
        restartButton.grid(row=0, column=2, sticky="e", padx=10, pady=10)

        # Set up the canvas for Turtle graphics
        canvas = Canvas(turtleFrame, width=600, height=400)  # Larger canvas
        canvas.grid(row=0, column=0, sticky="nsew")  # Ensure it expands and centers
        turtleFrame.grid(row=2, column=0, sticky="nsew", pady=10)
        turtleFrame.columnconfigure(0, weight=1)
        turtleFrame.rowconfigure(0, weight=1)
        screen = TurtleScreen(canvas)
        turtle = RawTurtle(screen)
        turtle.speed(0)
        turtle.hideturtle()

        guessEntry = Entry(guessFrame, width=15, font=("Helvetica", 14))
        guessEntry.grid(row=4, column=0, padx=(740, 0), pady=10, sticky="w")

        # Tkinter Widgets
        wordLabel = Label(wordFrame, text=" ".join(current_word_display), font=("Helvetica", 18))
        wordLabel.grid(row=0, column=0, sticky="nsew", pady=10)

        letterEntry = Entry(guessFrame, width=2, font=("Helvetica", 14))
        letterEntry.grid(row=0, column=0, padx=(882, 0), pady=10, sticky="w")

        guessALetterButton = Button(guessFrame, text="Guess A Letter", command=checkGuess, font=("Helvetica", 14))
        guessALetterButton.grid(row=0, column=1, padx=(0, 650), pady=10, sticky="w")

        guessTheWordButton = Button(guessFrame, text="Guess The Word", command=checkWordGuess, font=("Helvetica", 14))
        guessTheWordButton.grid(row=4, column=1, padx=(0, 650), pady=10, sticky="w")

        updateDisplay()
        playHangman.mainloop()

    def toFastTypingGame():
        menu.destroy()
        playTyping = Toplevel()

        def restartGame():
            global baslangic, saniye, hata_sayisi
            timerLabel["text"] = f"Time : {saniye}"
            baslangic = None
            saniye = 0
            hata_sayisi = 0

        playTyping.title("Hızlı Yazma Testi")
        playTyping.geometry("500x400")

        # Top frame
        topFrame = Frame(playTyping, bg="lightblue")
        topFrame.grid(row=0, column=0, sticky="new", pady=0)
        topFrame.grid_columnconfigure(0, weight=1)
        topFrame.grid_columnconfigure(1, weight=2)
        topFrame.grid_columnconfigure(2, weight=1)

        bestTime = 2.10

        # sol üstteki üçlü
        titleLabel = Label(topFrame, text="Fast Typing Game", font=("Arial", 14), bg="lightblue")
        bestTimeLabel = Label(topFrame, text=f"Best Time: {bestTime}s", font=("Arial", 14), bg="lightblue")
        titleLabel.grid(row=0, column=0, sticky="nws", padx=10, pady=(10, 0))
        bestTimeLabel.grid(row=1, column=0, sticky="nws", padx=10, pady=(0, 10))

        # ortadaki timer
        timerLabel = Label(topFrame, text="Time: 0s", font=("Arial", 20), bg="lightblue")
        timerLabel.grid(row=0, column=1, rowspan=2, padx=(10, 50), sticky="nsew")

        homeIconPath = "Images\\Icons\\home.png"
        homeIcon = ImageTk.PhotoImage(Image.open(homeIconPath).resize((30, 30)))

        restartIconPath = "Images\\Icons\\restart.png"
        restartIcon = ImageTk.PhotoImage(Image.open(restartIconPath).resize((30, 30)))

        # Restart butonu
        restartButton = Button(topFrame, image=restartIcon, font=("Arial", 14), bg="lightblue", command=restartGame)
        restartButton.grid(row=0, column=2, rowspan=2, padx=10, sticky="ns", pady=25)  # rowspan ve sticky ayarlandı

        homeButton = Button(topFrame, image=homeIcon, font=("Arial", 14), bg="lightblue", command=toMenu)
        homeButton.grid(row=0, column=3, rowspan=2, padx=10, sticky="ns", pady=25)  # rowspan ve sticky ayarlandı

        # Başlangıç değişkenleri
        baslangic = None
        saniye = 0
        hata_sayisi = 0

        metinler = [
            "Say hello to my little friend.",
            "Python is awesome.",
            "Welcome to the world of programming.",
            "Hangman is a fun game.",
            "Fast typing is a useful skill."
        ]

        metin = random.choice(metinler)
        def basla():
            global baslangic, saniye, hata_sayisi, metin
            baslangic = datetime.now()
            saniye = 0
            hata_sayisi = 0
            metin = random.choice(metinler)
            print(metin)
            metin_alani.delete(0, END)
            test_metni.config(text=metin)
            zaman_label.config(text="Geçen Zaman: 0 sn")
            hata_label.config(text="Hata Sayısı: 0")
            metin_alani.config(state=NORMAL)
            tamamla_button.config(state=NORMAL)

        def tamamla():
            global baslangic, saniye, hata_sayisi

            bitis = datetime.now()
            sure = bitis - baslangic
            saniye = int(sure.total_seconds())

            kullanici_girdisi = metin_alani.get().strip()  # Kullanıcı girişindeki baştaki ve sondaki boşlukları temizle
            metin_listesi = metin.strip().split()  # Metnin baştaki ve sondaki boşlukları temizle ve kelimelere ayır
            kullanici_listesi = kullanici_girdisi.split()  # Kullanıcı girdisini kelimelere ayır

            hata_sayisi = 0

            # En az uzunluktaki kelime listesi kadar karşılaştırma yapalım
            for i in range(len(kullanici_listesi)):
                if metin_listesi[i] == kullanici_listesi[i]:
                    break
                else:
                    hata_sayisi += 1

            # Sonuçları güncelle
            zaman_label.config(text=f"Geçen Zaman: {saniye} sn")
            hata_label.config(text=f"Hata Sayısı: {hata_sayisi}")
            timerLabel["text"] = f"Time : {saniye}"
            metin_alani.config(state=DISABLED)
            tamamla_button.config(state=DISABLED)

            messagebox.showinfo("Sonuç",
                                f"Test tamamlandı!\n\n"
                                f"Geçen Zaman: {saniye} sn\n"
                                f"Hata Sayısı: {hata_sayisi}")

            #saveScore(user_id, 2, saniye)

        frame = Frame(playTyping)
        frame.grid(row=1, column=0, pady=20)  # pack yerine grid kullanıyoruz

        zaman_label = Label(frame, text="Geçen Zaman: 0 sn", width=20, height=2, relief="solid", anchor="center")
        zaman_label.grid(row=0, column=0, padx=10)

        hata_label = Label(frame, text="Hata Sayısı: 0", width=20, height=2, relief="solid", anchor="center")
        hata_label.grid(row=0, column=1, padx=10)

        test_metni = Label(playTyping, text=metin, font=("Arial", 14), wraplength=450, justify="center")

        metin_alani = Entry(playTyping, font=("Arial", 14), width=40)  # Yeni bir frame oluşturup butonları bu frame'e ekliyoruz
        buton_frame = Frame(playTyping)
        buton_frame.grid(row=4, column=0, columnspan=3, pady=10)  # Ortalamak için columnspan

        basla_button = Button(buton_frame, text="Başla", font=("Arial", 14), command=basla)
        tamamla_button = Button(buton_frame, text="Tamamla", font=("Arial", 14), command=tamamla, state=DISABLED)

        basla_button.grid(row=0, column=0, padx=5)  # Butonların arasında boşluk için padx kullanıyoruz
        tamamla_button.grid(row=0, column=1, padx=5)

        test_metni.grid(row=2, column=0, columnspan=3, pady=10)  # wraplength ayarı için columnspan ile tüm sütunları kapsıyor
        metin_alani.grid(row=3, column=0, columnspan=3, pady=10)

        playTyping.mainloop()

    def logout():
        window.destroy()

    logoutIcon = ImageTk.PhotoImage(Image.open("Images\\Icons\\logout.jpg").resize((50, 50)))
    pfpIcon = ImageTk.PhotoImage(Image.open("Images\\Icons\\profilePic.png").resize((100, 100)))

    menuFrame = Frame(menu, bg="#7AAADA")
    labelFrame = Frame(menu, bg="#2D7EBF")
    gameFrame = Frame(menu, bg="#0364B1")

    menu.grid_rowconfigure(1, weight=1)
    menu.grid_columnconfigure(0, weight=1)

    menuFrame.grid(row=0, column=0, sticky="new", pady=50)
    labelFrame.grid(row=1, column=0, padx=10)
    gameFrame.grid(row=2, column=0, pady=(50, 220))

    menuFrame.grid_columnconfigure(0, weight=1)  # Back button column
    menuFrame.grid_columnconfigure(1, weight=2)  # Spacer
    menuFrame.grid_columnconfigure(2, weight=1)  # Profile section column

    # menuFrame
    bg_label = Label(menuFrame, image=partbg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    logoutButton = Button(menuFrame, image=logoutIcon, command=logout)
    profilePicture = Button(menuFrame, image=pfpIcon)
    nameLabel = Label(menuFrame, text=f"{usn}", font=("Arial", 14))
    levelLabel = Label(menuFrame, text=f"lvl {lvl}", font=("Arial", 14))

    logoutButton.grid(row=0, column=0, sticky="wns", padx=30, pady=10)
    profilePicture.grid(row=0, rowspan=2, column=7, sticky="e", padx=30)
    nameLabel.grid(row=0, column=6, sticky="e", pady=(20, 0))
    levelLabel.grid(row=1, column=6, sticky="e", pady=(0, 20))

    ozekGameLabel = Label(labelFrame, text="OzEk Game", font=("Arial", 70), bg="#2D7EBF", fg="White")
    welcomeLabel = Label(labelFrame, text="Welcome!", font=("Arial", 24), bg="#2D7EBF", fg="White")
    ozekGameLabel.grid(row=0, column=0, sticky="ew", pady=30)
    welcomeLabel.grid(row=1, column=0, sticky="ew", pady=30)

    memoryGameButton = Button(gameFrame, text="Memory Game", command=toMemoryGameMenu, font=("Arial", 22))
    hangmanGameButton = Button(gameFrame, text="Hangman", command=toHangmanGame, font=("Arial", 22))
    fastTypingGameButton = Button(gameFrame, text="Fast Typing Game", command=toFastTypingGame, font=("Arial", 22))

    memoryGameButton.grid(row=0, column=0, padx=20)
    hangmanGameButton.grid(row=0, column=2, padx=20)
    fastTypingGameButton.grid(row=0, column=3, padx=20)

    menu.mainloop()

L1 = Label(window, text="Kullanıcı Adı")
L1.grid(row=0, column=0, pady=(15, 5), sticky="nw", padx=15)

E1 = Entry(window, width=25)
E1.grid(row=1, column=0, pady=5, sticky="nw", padx=15)

L2 = Label(window, text="Şifre")
L2.grid(row=2, column=0, pady=5, sticky="nw", padx=15)

E2 = Entry(window, textvariable=StringVar(), show='*', width=25)
E2.grid(row=3, column=0, pady=5, sticky="nw", padx=15)

bt = Button(window, text="Giriş Yap", padx="20", pady="5", command=giris)
bt.grid(row=4, column=0, pady=5, sticky="nw", padx=15)

btuye = Button(window, text="Üye Ol", padx="20", pady="5", command=signup)
btuye.grid(row=4, column=1, pady=5, sticky="ne", padx=(75, 15))

window.mainloop()