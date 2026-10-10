import linecache
import random
import math
import time
import turtle
import hashlib  # Added for secure password hashing


# ============================================================
# SECURITY FUNCTIONS
# ============================================================

def hash_password(password):
    """Converts a plain text password into a secure SHA-256 hash."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def obfuscate_data(data_string, key="toilet_secret_key"):
    """Simple character shift to disguise human-readable text files."""
    output = []
    for i, char in enumerate(data_string):
        key_char = key[i % len(key)]
        encoded_char = chr((ord(char) + ord(key_char)) % 1114112)
        output.append(encoded_char)
    return "".join(output)

def deobfuscate_data(encoded_string, key="toilet_secret_key"):
    """Reverses the character shift to read data back into the game."""
    output = []
    for i, char in enumerate(encoded_string):
        key_char = key[i % len(key)]
        decoded_char = chr((ord(char) - ord(key_char)) % 1114112)
        output.append(decoded_char)
    return "".join(output)

def make_game_fullscreen():
    """Safely forces the window to fullscreen if it exists."""
    if 'window' in globals():
        root = window._root
        root.lift()
        root.attributes("-topmost", True)
        root.attributes("-topmost", False)
        try:
            root.state("zoomed") 
        except:
            root.attributes("-fullscreen", True)
            
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        window.setup(width=screen_w, height=screen_h)

# ============================================================
# LOGIN / SIGNUP SYSTEM
# ============================================================

ucreated = 0
pos = 0
startq = ["would you like to login or sign up? \n", "Type 'l' or 'login' to login \n"]
while ucreated == 0:
    print("-------------------------------------------------------")
    time.sleep(0.5)
    los = input(f"{startq[pos]}").lower().strip()
    if los == "sign up" or los == "s":
        eloop = 0
        while eloop == 0:
            username = input("what would you like your username to be? ")
            time.sleep(0.1)
            print("checking availability...")
            try:
                with open("usernames.txt", "r") as file:
                    existing_usernames = [line.strip() for line in file.readlines()]
            except FileNotFoundError:
                existing_usernames = []
                
            if username in existing_usernames:
                time.sleep(1)
                print("Username in use. Please try another one.")
                time.sleep(1)
            else:
                time.sleep(1)
                print("Username Accepted.")
                time.sleep(1)
                yloop = 0
                while yloop == 0:
                    password = input("Choose a password: ")
                    if password == username:
                        time.sleep(1)
                        print("Password cannot be the same as username")
                        time.sleep(1)
                    else:
                        time.sleep(1)
                        print("saving user and pass...")
                        
                        # Securely hash the password before writing it to passwords.txt
                        hashed_password = hash_password(password)
                        
                        with open("passwords.txt", "a") as file:
                            file.write(hashed_password + "\n")
                        with open("usernames.txt", "a") as file:
                            file.write(username + "\n")
                        time.sleep(2.5)
                        print("saved!")
                        time.sleep(1)
                        print("Creating personalised data file...")
                        time.sleep(2)
                        
                        # Obfuscate the initial save data file using the .dat extension
                        initial_data = "Placeholder\n"
                        encrypted_initial_data = obfuscate_data(initial_data)
                        with open(f"{username}.dat", "w", encoding="utf-8") as file:
                            file.write(encrypted_initial_data)

                        print(f"Created {username}.dat user data")
                        print("please login with the username and password just created.")
                        eloop = 1
                        yloop = 1
                        pos = 1
                        time.sleep(1)
    elif los == "login" or los == "l":
        xloop = 0
        while xloop == 0:
            loginu = input("Enter username... ")
            userlinenumber = None
            try:
                with open("usernames.txt", "r") as file: #searches for the line number and stores it as a variable
                    for line_num, line in enumerate(file, 1):
                        if line.strip() == loginu:
                            userlinenumber = line_num
                            break
            except FileNotFoundError:
                print("No users registered yet. Please sign up first.")
                break
                
            if userlinenumber is not None:
                time.sleep(0.5)
                attempts=0 #this is the real attempts
                dattempts=3 #dattempts is the displayed attempts
                while attempts<3:
                    loginp = input("Enter password... ")
                    linecache.checkcache("passwords.txt")
                    userp = linecache.getline("passwords.txt", userlinenumber).strip()
                    
                    # Hash the entered password to match against the stored hash
                    if hash_password(loginp) == userp:
                        print("Login successful!")
                        xloop = 1
                        ucreated = 1
                        break
                    else:
                        print("Incorrect password. Please try again.")
                        attempts=attempts+1
                        dattempts=dattempts-1
                        time.sleep(1)
                        print("[You have", dattempts, "more attempts]")
                        time.sleep(1)
                if attempts == 3:
                    print("Too many attempts, please try again later")
                else:
                    print()
            else:
                print("Username does not exist, please try again or signup")
    elif los == "test":
        print("--test mode--")
        loginu="admin"
        ucreated = 1
# ============================================================
# GAME SETTINGS
# ============================================================

score = 0
game_active = True

DRAIN_RADIUS = 70
WATER_RADIUS = 200
RIM_RADIUS = 250

current_mode = "FART"

# Used for pee scoring
last_pee_score_time = time.time()


# ============================================================
# FART TYPES
# ============================================================

fartTypes = [
    "Wet",
    "Squelchy",
    "Dry",
    "Smelly",
    "Deadly",
    "Atomic"
]


# ============================================================
# FART SHOP
# ============================================================

fart_shop = {

    "Wet": {
        "cost": 0,
        "points": 2
    },

    "Squelchy": {
        "cost": 100,
        "points": 5
    },

    "Dry": {
        "cost": 2000,
        "points": 20
    },

    "Smelly": {
        "cost": 5000,
        "points": 75
    },

    "Deadly": {
        "cost": 25000,
        "points": 200
    },

    "Atomic": {
        "cost": 100000,
        "points": 1000
    },

    "Pee": {
        "cost": 200000,
        "points": 100
    },

    "GoldenToilet": {
        "cost": 1000000,
        "points": 0
    }
}



# ============================================================
# FART PROFILES
# ============================================================

fart_profiles = {

    "Wet": {
        "multiplier": 0.8,
        "colors": ["#76b322", "#5c8c16"]
    },

    "Squelchy": {
        "multiplier": 0.9,
        "colors": ["#8fa321", "#acc429"]
    },

    "Dry": {
        "multiplier": 0.7,
        "colors": ["#c2b078", "#d6c594"]
    },

    "Smelly": {
        "multiplier": 1.2,
        "colors": ["#8ae63c", "#a6f062"]
    },

    "Deadly": {
        "multiplier": 1.6,
        "colors": ["#4d6e28", "#334a1b"]
    },

    "Atomic": {
        "multiplier": 3.5,
        "colors": ["#5a3d28", "#ffd700"]
    }
}


# ============================================================
# UNLOCK SYSTEM
# ============================================================

unlocked_farts = ["Wet"]

current_fart_index = 0

current_fart = "Wet"

shop_message = ""

# ============================================================
# WINDOW
# ============================================================

window = turtle.Screen()

window.setup(width=0.98, height=0.94)

window.bgcolor(
    "#3a3a3a"
)

# Draw very quickly
window.tracer(
    0,
    0
)

# ============================================================
# PLAYER PROGRESS SAVE / LOAD
# ============================================================

def save_progress():
    global game_active

    if not game_active:
        return

    game_active = False

    try:
        # Build plain text data string
        raw_data = (
            f"score={score}\n"
            f"unlocked={','.join(unlocked_farts)}\n"
            f"current_fart={current_fart}\n"
            f"current_mode={current_mode}\n"
        )
        
        # Scramble the content
        encrypted_data = obfuscate_data(raw_data)
        
        # Write to .dat file with utf-8 encoding
        with open(f"{loginu}.dat", "w", encoding="utf-8") as file:
            file.write(encrypted_data)

        print(f"Progress saved to {loginu}.dat!")

    except OSError as error:
        print(f"Could not save progress: {error}")

    # Clear active effects
    for fart in active_farts:
        fart["turtle"].clear()
        fart["turtle"].hideturtle()
    active_farts.clear()

    for pee in active_pee:
        pee["turtle"].clear()
        pee["turtle"].hideturtle()
    active_pee.clear()

    # Display the final score
    score_drawer.clear()
    shop_drawer.clear()

    score_drawer.goto(-2, 318)
    score_drawer.color("#ffffff")
    score_drawer.write(
        "GAME ENDED",
        align="center",
        font=("Arial", 36, "bold")
    )

    score_drawer.goto(-2, 278)
    score_drawer.color("white")
    score_drawer.write(
        f"Final Score: {score}",
        align="center",
        font=("Arial", 20, "bold")
    )
    
    score_drawer.goto(0, 320)
    score_drawer.color("#000000")
    score_drawer.write(
        "GAME ENDED",
        align="center",
        font=("Arial", 36, "bold")
    )

    score_drawer.goto(0, 280)
    score_drawer.color("black")
    score_drawer.write(
        f"Final Score: {score}",
        align="center",
        font=("Arial", 20, "bold")
    )

    score_drawer.goto(0, 255)
    score_drawer.color("#ffd92f")
    score_drawer.write(
        "Score saved to your profile!",
        align="center",
        font=("Arial", 14, "normal")
    )

    window.update()
    time.sleep(3)
    window.bye()


def load_progress():
    global score, unlocked_farts
    global current_fart, current_fart_index, current_mode

    try:
        # Load and decrypt the .dat save file
        with open(f"{loginu}.dat", "r", encoding="utf-8") as file:
            encrypted_content = file.read()
            
        decrypted_content = deobfuscate_data(encrypted_content)
        lines = decrypted_content.splitlines()
        
        data = {}
        for line in lines:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                data[key] = value

        score = max(0, int(data.get("score", 0)))

        # Only restore valid, sequentially unlockable items
        saved = data.get("unlocked", "Wet").split(",")
        unlocked_farts = ["Wet"]

        for fart in fartTypes[1:]:
            if fart in saved:
                unlocked_farts.append(fart)
            else:
                break

        if "Pee" in saved and "Atomic" in unlocked_farts:
            unlocked_farts.append("Pee")

        # GoldenToilet is a separate cosmetic, not part of the fart unlock chain.
        if "GoldenToilet" in saved:
            unlocked_farts.append("GoldenToilet")

        # Restore the selected fart
        saved_fart = data.get("current_fart", "Wet")

        if saved_fart in unlocked_farts and saved_fart in fartTypes:
            current_fart = saved_fart
        else:
            current_fart = "Wet"

        current_fart_index = (
            unlocked_farts.index(current_fart)
        )

        # Restore the mode
        saved_mode = data.get("current_mode", "FART")

        if saved_mode == "PEE" and "Pee" in unlocked_farts:
            current_mode = "PEE"
        else:
            current_mode = "FART"

        print("Player progress loaded!")

    except (OSError, ValueError, Exception):
        print("No previous progress found. Starting fresh.")

# ============================================================
# ACTIVE EFFECTS
# ============================================================

active_farts = []
active_pee = []





# ============================================================
# WHITE AND DARK CHECKERED TILE FLOOR
# ============================================================

floor_drawer = turtle.Turtle()
floor_drawer.hideturtle()
floor_drawer.speed(0)
floor_drawer.penup()

def draw_tiled_floor():
    """Draw checkerboard tiles beyond every edge of the current game window."""
    floor_drawer.clear()
    tile = 70
    half_w = window.window_width() / 2 + tile
    half_h = window.window_height() / 2 + tile
    left = -half_w
    bottom = -half_h
    cols = int((2 * half_w) // tile) + 2
    rows = int((2 * half_h) // tile) + 2
    for row in range(rows):
        y = bottom + row * tile
        for col in range(cols):
            x = left + col * tile
            color = "#f5f4ef" if (row + col) % 2 == 0 else "#292929"
            floor_drawer.goto(x, y)
            floor_drawer.setheading(0)
            floor_drawer.color("#777777", color)
            floor_drawer.pendown()
            floor_drawer.begin_fill()
            for _ in range(4):
                floor_drawer.forward(tile)
                floor_drawer.left(90)
            floor_drawer.end_fill()
            floor_drawer.penup()

draw_tiled_floor()


# ============================================================
# BACKGROUND DRAWER
# ============================================================

bg_drawer = turtle.Turtle()

bg_drawer.hideturtle()
bg_drawer.speed(0)
bg_drawer.penup()


# ============================================================
# SCORE DRAWER
# ============================================================

score_drawer = turtle.Turtle()

score_drawer.hideturtle()
score_drawer.speed(0)
score_drawer.penup()

# Dedicated top HUD layer, drawn above the tiled floor.
hud_drawer = turtle.Turtle()
hud_drawer.hideturtle()
hud_drawer.speed(0)
hud_drawer.penup()


def draw_hud_bar():
    hud_drawer.clear()
    half_w = window.window_width() / 2
    half_h = window.window_height() / 2
    bar_h = 92
    hud_drawer.goto(-half_w, half_h - bar_h)
    hud_drawer.setheading(0)
    hud_drawer.color("#000000", "#000000")
    hud_drawer.pendown()
    hud_drawer.begin_fill()
    for distance in (2 * half_w, bar_h, 2 * half_w, bar_h):
        hud_drawer.forward(distance)
        hud_drawer.left(90)
    hud_drawer.end_fill()
    hud_drawer.penup()


draw_hud_bar()


# ============================================================
# SHOP DRAWER
# ============================================================

shop_drawer = turtle.Turtle()

shop_drawer.hideturtle()
shop_drawer.speed(0)
shop_drawer.penup()


# ============================================================
# SHOP AREA
# ============================================================

SHOP_WIDTH = 120
SHOP_HEIGHT = 600
SHOP_RIGHT = window.window_width() / 2 - 10
SHOP_LEFT = SHOP_RIGHT - SHOP_WIDTH
SHOP_BOTTOM = -SHOP_HEIGHT / 2
SHOP_TOP = SHOP_HEIGHT / 2
SHOP_X_OFFSET = SHOP_LEFT - 270

# Scrollable shop settings
shop_scroll_offset = 0
SHOP_SCROLL_STEP = 35
SHOP_CONTENT_TOP = 235
SHOP_CONTENT_BOTTOM = -235


# ============================================================
# DRAW TOILET BOWL
# ============================================================

def draw_toilet():
    """Draw the bowl; owning GoldenToilet changes the porcelain to gold."""
    bg_drawer.clear()
    gold_owned = "GoldenToilet" in unlocked_farts

    outer_porcelain = "#ffd700" if gold_owned else "#f5f5f5"
    inner_porcelain = "#d4a900" if gold_owned else "#d1d5db"

    bg_drawer.penup()
    bg_drawer.goto(0, 0)
    bg_drawer.dot(500, outer_porcelain)

    bg_drawer.goto(0, 5)
    bg_drawer.dot(430, inner_porcelain)

    # Keep the water and drain blue/dark even when the toilet is gold.
    bg_drawer.goto(0, 0)
    bg_drawer.dot(400, "#a0e1fa")

    bg_drawer.goto(0, 0)
    bg_drawer.dot(340, "#73c2fb")

    bg_drawer.goto(0, -10)
    bg_drawer.dot(140, "#212d33")


draw_toilet()


# ============================================================
# YELLOW PIPE
# TOUCHES BOTTOM OF SCREEN
# ============================================================

pipe_drawer = turtle.Turtle()

pipe_drawer.hideturtle()
pipe_drawer.speed(0)
pipe_drawer.penup()

pipe_drawer.goto(
    -24,
    -400
)

pipe_drawer.setheading(
    90
)

pipe_color = "#ffd700" if "GoldenToilet" in unlocked_farts else "#f5f5f5"

pipe_drawer.color(
    pipe_color
)

pipe_drawer.fillcolor(
    pipe_color
)

pipe_drawer.begin_fill()

pipe_drawer.forward(170)

pipe_drawer.right(90)

pipe_drawer.forward(48)

pipe_drawer.right(90)

pipe_drawer.forward(170)

pipe_drawer.right(90)

pipe_drawer.forward(48)

pipe_drawer.end_fill()


# ============================================================
# PINK SEMICIRCLE
# ============================================================

pink_drawer = turtle.Turtle()

pink_drawer.hideturtle()
pink_drawer.speed(0)
pink_drawer.penup()

pink_drawer.goto(
    -25,
    -245
)

pink_drawer.setheading(
    0
)

pink_drawer.color(
    "#ff69b4"
)

pink_drawer.fillcolor(
    "#ff69b4"
)

pink_drawer.begin_fill()

pink_drawer.forward(50)

pink_drawer.left(90)

pink_drawer.circle(
    25,
    180
)

pink_drawer.end_fill()

# ============================================================
# SCOREBOARD
# ============================================================

def update_score(hit_type="", points_changed=0, fart_name=""):
    """Draw score at top-left, hit/miss feedback at top-centre, and mode at top-right."""
    score_drawer.clear()

    half_w = window.window_width() / 2
    half_h = window.window_height() / 2
    hud_y = half_h - 38

    # Score: top-left
    score_drawer.goto(-half_w + 18, hud_y)
    score_drawer.color("white")
    score_drawer.write(
        f"STINK SCORE: {score}",
        align="left",
        font=("Arial", 16, "bold")
    )

    # Hit/miss feedback: top-middle
    score_drawer.goto(0, hud_y)
    if fart_name and game_active:
        if hit_type == "critical":
            color, message, size = "#ffd700", f"CRITICAL HIT! {fart_name} (+{points_changed} pts)", 12
        elif hit_type == "hit":
            color, message, size = "#a6f062", f"DIRECT HIT! {fart_name} (+{points_changed} pts)", 12
        elif hit_type == "near_miss":
            color, message, size = "#ff9933", f"NEAR MISS! {fart_name} (-{points_changed} pts)", 12
        else:
            color, message, size = "#ff4d4d", f"TOTAL MISS! {fart_name} (-{points_changed} pts)", 12
    else:
        color, message, size = "#d1d5db", "HIT / MISS", 12
    score_drawer.color(color)
    score_drawer.write(message, align="center", font=("Arial", size, "bold"))

    # Mode: top-right
    score_drawer.goto(half_w - 18, hud_y)
    if current_mode == "FART":
        score_drawer.color("#a6f062")
        mode_text = f"MODE: FART ({current_fart})  [F] FART [P] PEE"
    else:
        score_drawer.color("#ffe45c")
        mode_text = "MODE: PEE  [F] FART [P] PEE"
    score_drawer.write(mode_text, align="right", font=("Arial", 10, "bold"))


# ============================================================
# DRAW SHOP
# ============================================================

def draw_shop():
    """Draw the shop panel, item cards, and scroll bar."""
    shop_drawer.clear()

    # Main shop panel
    shop_drawer.penup()
    shop_drawer.goto(SHOP_LEFT, SHOP_BOTTOM)
    shop_drawer.setheading(0)
    shop_drawer.color("#111827", "#111827")
    shop_drawer.pendown()
    shop_drawer.begin_fill()
    for distance, turn in [
        (SHOP_RIGHT - SHOP_LEFT, 90),
        (SHOP_TOP - SHOP_BOTTOM, 90),
        (SHOP_RIGHT - SHOP_LEFT, 90),
        (SHOP_TOP - SHOP_BOTTOM, 90),
    ]:
        shop_drawer.forward(distance)
        shop_drawer.left(turn)
    shop_drawer.end_fill()
    shop_drawer.penup()

    # Header
    shop_drawer.goto(330 + SHOP_X_OFFSET, 274)
    shop_drawer.color("#ffd92f")
    shop_drawer.write("FART SHOP", align="center", font=("Arial", 15, "bold"))

    shop_drawer.goto(330 + SHOP_X_OFFSET, 253)
    shop_drawer.color("#d1d5db")
    shop_drawer.write(f"Score: {score}", align="center", font=("Arial", 9, "bold"))

    shop_drawer.goto(330 + SHOP_X_OFFSET, 238)
    shop_drawer.color("#9ca3af")
    shop_drawer.write("Scroll to browse", align="center", font=("Arial", 7, "normal"))

    items = fartTypes + ["Pee", "GoldenToilet"]
    row_height = 78
    first_y = 200
    card_half_height = 30
    shop_scroll_max = max(
        0,
        SHOP_CONTENT_BOTTOM + card_half_height
        - (first_y - row_height * (len(items) - 1))
    )

    # Keep the offset in range even if the item list changes.
    global shop_scroll_offset
    shop_scroll_offset = max(0, min(shop_scroll_offset, shop_scroll_max))

    for i, item in enumerate(items):
        item_y = first_y - i * row_height + shop_scroll_offset

        # Only draw cards inside the scrolling content area.
        if not (SHOP_CONTENT_BOTTOM + card_half_height <= item_y <= SHOP_CONTENT_TOP - card_half_height):
            continue

        if item == "GoldenToilet":
            unlocked = "GoldenToilet" in unlocked_farts
            selected = unlocked
            cost = fart_shop["GoldenToilet"]["cost"]
            points_text = "Gold skin + PERMANENT 2x points"
        elif item == "Pee":
            unlocked = "Pee" in unlocked_farts
            selected = current_mode == "PEE"
            cost = fart_shop["Pee"]["cost"]
            points_text = "Stream mode"
        else:
            unlocked = item in unlocked_farts
            selected = current_mode == "FART" and item == current_fart
            cost = fart_shop[item]["cost"]
            points_text = f"+{fart_shop[item]['points']} pts"

        if selected:
            card_color = "#244b2c"
            edge_color = "#a6f062"
            status = "SELECTED"
        elif unlocked:
            card_color = "#263244"
            edge_color = "#60a5fa"
            status = "UNLOCKED"
        else:
            card_color = "#20242c"
            edge_color = "#4b5563"
            status = f"{cost:,} pts"

        # Card background
        card_left = SHOP_LEFT + 8
        card_width = 100
        card_height = 60
        shop_drawer.goto(card_left, item_y - card_height / 2)
        shop_drawer.setheading(0)
        shop_drawer.color(edge_color, card_color)
        shop_drawer.pendown()
        shop_drawer.begin_fill()
        for distance, turn in [
            (card_width, 90),
            (card_height, 90),
            (card_width, 90),
            (card_height, 90),
        ]:
            shop_drawer.forward(distance)
            shop_drawer.left(turn)
        shop_drawer.end_fill()
        shop_drawer.penup()

        shop_drawer.goto(328 + SHOP_X_OFFSET, item_y + 8)
        shop_drawer.color("#ffd700" if item == "GoldenToilet" else ("#ffffff" if unlocked or item == "Pee" else "#b6beca"))
        display_name = "GOLDEN TOILET" if item == "GoldenToilet" else item.upper()
        shop_drawer.write(display_name, align="center", font=("Arial", 8 if item == "GoldenToilet" else 9, "bold"))

        shop_drawer.goto(328 + SHOP_X_OFFSET, item_y - 7)
        shop_drawer.color(edge_color if selected else "#d1d5db")
        shop_drawer.write(status, align="center", font=("Arial", 7, "bold"))

        shop_drawer.goto(328 + SHOP_X_OFFSET, item_y - 20)
        shop_drawer.color("#9ca3af")
        shop_drawer.write(points_text, align="center", font=("Arial", 7, "normal"))

    # Scroll bar track and thumb
    track_x = SHOP_RIGHT - 6
    track_top = SHOP_CONTENT_TOP - 3
    track_bottom = SHOP_CONTENT_BOTTOM + 3
    shop_drawer.goto(track_x, track_bottom)
    shop_drawer.setheading(90)
    shop_drawer.color("#374151")
    shop_drawer.pensize(4)
    shop_drawer.pendown()
    shop_drawer.forward(track_top - track_bottom)
    shop_drawer.penup()
    shop_drawer.pensize(1)

    content_height = track_top - track_bottom
    thumb_height = max(28, content_height * (content_height / (content_height + shop_scroll_max)))
    thumb_range = content_height - thumb_height
    thumb_y = track_top - thumb_height / 2
    if shop_scroll_max:
        thumb_y -= (shop_scroll_offset / shop_scroll_max) * thumb_range
    shop_drawer.goto(track_x, thumb_y - thumb_height / 2)
    shop_drawer.setheading(90)
    shop_drawer.color("#ffd92f")
    shop_drawer.pensize(4)
    shop_drawer.pendown()
    shop_drawer.forward(thumb_height)
    shop_drawer.penup()
    shop_drawer.pensize(1)

    # Footer message
    shop_drawer.goto(330 + SHOP_X_OFFSET, -263)
    shop_drawer.color("#ffd92f")
    shop_drawer.write(shop_message[:20], align="center", font=("Arial", 8, "bold"))

    shop_drawer.goto(330 + SHOP_X_OFFSET, -283)
    shop_drawer.color("#9ca3af")
    shop_drawer.write("Click a card to select/buy", align="center", font=("Arial", 7, "normal"))


# ============================================================
# SHOP CLICK
# ============================================================

def shop_click(x, y):
    global score
    global current_fart
    global current_fart_index
    global current_mode
    global shop_message

    if not (SHOP_LEFT <= x <= SHOP_RIGHT and SHOP_BOTTOM <= y <= SHOP_TOP):
        return False

    # Header and footer aren't clickable item cards.
    if y > SHOP_CONTENT_TOP or y < SHOP_CONTENT_BOTTOM:
        return True

    items = fartTypes + ["Pee", "GoldenToilet"]
    row_height = 78
    first_y = 200
    card_half_height = 30

    for i, item in enumerate(items):
        item_y = first_y - i * row_height + shop_scroll_offset
        if not (SHOP_CONTENT_BOTTOM + card_half_height <= item_y <= SHOP_CONTENT_TOP - card_half_height):
            continue
        if not (item_y - card_half_height <= y <= item_y + card_half_height):
            continue

        if item == "GoldenToilet":
            if "GoldenToilet" in unlocked_farts:
                shop_message = "Golden toilet owned!"
            else:
                cost = fart_shop["GoldenToilet"]["cost"]
                if score >= cost:
                    score -= cost
                    unlocked_farts.append("GoldenToilet")
                    shop_message = "Golden toilet unlocked!"
                    draw_toilet()
                else:
                    shop_message = f"Need {cost - score} more points!"
        elif item == "Pee":
            if "Pee" in unlocked_farts:
                current_mode = "PEE"
                shop_message = "PEE selected!"
            elif "Atomic" not in unlocked_farts:
                shop_message = "Unlock Atomic first!"
            else:
                cost = fart_shop["Pee"]["cost"]
                if score >= cost:
                    score -= cost
                    unlocked_farts.append("Pee")
                    current_mode = "PEE"
                    shop_message = "PEE unlocked!"
                else:
                    shop_message = f"Need {cost - score} more points!"
        else:
            if item in unlocked_farts:
                current_fart = item
                current_fart_index = unlocked_farts.index(item)
                current_mode = "FART"
                shop_message = f"{item} selected!"
            else:
                # Count only fart types; Pee and GoldenToilet are special items.
                next_index = sum(1 for fart_name in fartTypes if fart_name in unlocked_farts)
                if next_index >= len(fartTypes) or fartTypes[next_index] != item:
                    shop_message = "Buy the previous fart first!"
                else:
                    cost = fart_shop[item]["cost"]
                    if score >= cost:
                        score -= cost
                        unlocked_farts.append(item)
                        current_fart = item
                        current_fart_index = unlocked_farts.index(item)
                        current_mode = "FART"
                        shop_message = f"{item} unlocked!"
                    else:
                        shop_message = f"Need {cost - score} more points!"

        update_score()
        draw_shop()
        return True

    return True


# ============================================================
# GAME OVER
# ============================================================

def trigger_game_over():

    global game_active

    game_active = False

    for fart in active_farts:

        fart["turtle"].clear()
        fart["turtle"].hideturtle()

    active_farts.clear()

    for pee in active_pee:

        pee["turtle"].clear()
        pee["turtle"].hideturtle()

    active_pee.clear()

    score_drawer.clear()
    shop_drawer.clear()

    score_drawer.goto(
        0,
        70
    )

    score_drawer.color(
        "#ff3333"
    )

    score_drawer.write(
        "GAME OVER",
        align="center",
        font=("Arial", 48, "bold")
    )

    score_drawer.goto(
        0,
        10
    )

    score_drawer.color(
        "white"
    )

    score_drawer.write(
        f"Final Score: {score}",
        align="center",
        font=("Arial", 20, "bold")
    )

    score_drawer.goto(
        0,
        -40
    )

    score_drawer.color(
        "#b0bec5"
    )

    score_drawer.write(
        "You made too much of a mess outside the bowl!",
        align="center",
        font=("Arial", 14, "italic")
    )

    window.update()


# ============================================================
# CREATE FART
# ============================================================

def visualFart(x, y):

    global score

    if not game_active:
        return

    # Don't allow farting in the shop LOLLLLL
    if (
        SHOP_LEFT <= x <= SHOP_RIGHT
        and
        SHOP_BOTTOM <= y <= SHOP_TOP
    ):
        return

    # --------------------------------------------------------
    # DISTANCE FROM DRAIN
    # --------------------------------------------------------

    distance = math.sqrt(
        x ** 2 +
        y ** 2
    )

    chosen_type = current_fart

    if chosen_type not in fart_profiles:
        chosen_type = "Wet"

    base_points = fart_shop[
        chosen_type
    ]["points"]
    # Golden Toilet permanently doubles points earned from successful hits.
    points_multiplier = 2 if "GoldenToilet" in unlocked_farts else 1

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    if distance <= DRAIN_RADIUS:

        hit_status = "critical"

        points_applied = base_points * 2 * points_multiplier

        score += points_applied

    elif distance <= WATER_RADIUS:

        hit_status = "hit"

        points_applied = base_points * points_multiplier

        score += points_applied

    elif distance <= RIM_RADIUS:

        hit_status = "near_miss"

        points_applied = 1

        score -= points_applied

    else:

        hit_status = "total_miss"

        points_applied = base_points

        score -= points_applied

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------

    if score < 0:

        trigger_game_over()

        return

    update_score(
        hit_status,
        points_applied,
        chosen_type
    )

    # --------------------------------------------------------
    # FART PROFILE
    # --------------------------------------------------------

    profile = fart_profiles[
        chosen_type
    ]

    mult = profile[
        "multiplier"
    ]

    base_color = profile[
        "colors"
    ][0]

    highlight_color = profile[
        "colors"
    ][1]

    # --------------------------------------------------------
    # CREATE FART TURTLE
    # --------------------------------------------------------

    fart_turtle = turtle.Turtle()

    fart_turtle.hideturtle()
    fart_turtle.speed(0)
    fart_turtle.penup()

    dots = []

    num_puffs = random.randint(
        4,
        7
    )

    for i in range(
        num_puffs
    ):

        scatter_x = random.randint(
            int(-20 * mult),
            int(20 * mult)
        )

        scatter_y = random.randint(
            int(-20 * mult),
            int(20 * mult)
        )

        puff_size = random.randint(
            int(20 * mult),
            int(40 * mult)
        )

        dots.append({

            "x":
                x + scatter_x,

            "y":
                y + scatter_y,

            "size":
                puff_size,

            "color":
                base_color
        })

    # --------------------------------------------------------
    # ATOMIC PARTICLES
    # --------------------------------------------------------

    if chosen_type == "Atomic":

        for i in range(
            random.randint(
                7,
                12
            )
        ):

            yellow_x = (
                x +
                random.randint(
                    int(-35 * mult),
                    int(35 * mult)
                )
            )

            yellow_y = (
                y +
                random.randint(
                    int(-35 * mult),
                    int(35 * mult)
                )
            )

            yellow_size = random.randint(
                8,
                18
            )

            dots.append({

                "x":
                    yellow_x,

                "y":
                    yellow_y,

                "size":
                    yellow_size,

                "color":
                    highlight_color
            })

        lifetime = 8.0

    else:

        center_size = int(
            25 * mult
        )

        dots.append({

            "x":
                x +
                random.randint(
                    -5,
                    5
                ),

            "y":
                y +
                random.randint(
                    -5,
                    5
                ),

            "size":
                center_size,

            "color":
                highlight_color
        })

        lifetime = 3.0

    # --------------------------------------------------------
    # DRAW FART
    # --------------------------------------------------------

    for dot in dots:

        fart_turtle.goto(
            dot["x"],
            dot["y"]
        )

        fart_turtle.dot(
            dot["size"],
            dot["color"]
        )

    active_farts.append({

        "turtle":
            fart_turtle,

        "dots":
            dots,

        "start_time":
            time.time(),

        "lifetime":
            lifetime
    })

    window.update()


# ============================================================
# CREATE PEE
# ============================================================

def make_pee(x, y):

    if not game_active:
        return

    # --------------------------------------------------------
    # Pee must be unlocked
    # --------------------------------------------------------

    if "Pee" not in unlocked_farts:
        return

    # --------------------------------------------------------
    # Don't allow pee in shop #LOLLLLLLLLLL jfl
    # --------------------------------------------------------

    if (
        SHOP_LEFT <= x <= SHOP_RIGHT
        and
        SHOP_BOTTOM <= y <= SHOP_TOP
    ):
        return

    pee_turtle = turtle.Turtle()

    pee_turtle.hideturtle()
    pee_turtle.speed(0)
    pee_turtle.penup()

    droplets = []

    # --------------------------------------------------------
    # START OF STREAM
    # --------------------------------------------------------

    start_x = 0
    start_y = -220

    dx = x - start_x
    dy = y - start_y

    distance = math.sqrt(
        dx ** 2 +
        dy ** 2
    )

    if distance == 0:
        distance = 1

    direction_x = dx / distance
    direction_y = dy / distance

    stream_steps = max(
        1,
        int(distance / 6)
    )

    # --------------------------------------------------------
    # STREAM
    # --------------------------------------------------------

    for i in range(
        stream_steps
    ):

        progress = (
            i /
            stream_steps
        )

        stream_x = (
            start_x +
            dx * progress
        )

        stream_y = (
            start_y +
            dy * progress
        )

        wobble = random.randint(
            -4,
            4
        )

        side_x = -direction_y
        side_y = direction_x

        stream_x += (
            side_x *
            wobble
        )

        stream_y += (
            side_y *
            wobble
        )

        droplets.append({

            "x":
                stream_x,

            "y":
                stream_y,

            "size":
                random.randint(
                    5,
                    9
                ),

            "color":
                random.choice([

                    "#fff176",
                    "#ffe45c",
                    "#ffd92f",
                    "#fbc02d"

                ])
        })

    # --------------------------------------------------------
    # SPLASH
    # --------------------------------------------------------

    for i in range(8):

        splash_x = (
            x +
            random.randint(
                -18,
                18
            )
        )

        splash_y = (
            y +
            random.randint(
                -18,
                18
            )
        )

        droplets.append({

            "x":
                splash_x,

            "y":
                splash_y,

            "size":
                random.randint(
                    5,
                    11
                ),

            "color":
                random.choice([

                    "#fff176",
                    "#ffe45c",
                    "#ffd92f",
                    "#fbc02d"

                ])
        })

    # --------------------------------------------------------
    # PEE AREA
    # --------------------------------------------------------

    target_distance = math.sqrt(
        x ** 2 +
        y ** 2
    )

    if target_distance <= RIM_RADIUS:

        pee_area = "bowl"

    else:

        pee_area = "floor"

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    for drop in droplets:

        pee_turtle.goto(
            drop["x"],
            drop["y"]
        )

        pee_turtle.dot(
            drop["size"],
            drop["color"]
        )

    active_pee.append({

        "turtle":
            pee_turtle,

        "droplets":
            droplets,

        "start_time":
            time.time(),

        "lifetime":
            2.5,

        "area":
            pee_area
    })

    window.update()


# ============================================================
# SCORE PEE
# ============================================================

def score_pee():

    global score
    global last_pee_score_time

    if not game_active:
        return

    current_time = time.time()

    elapsed = (
        current_time -
        last_pee_score_time
    )

    if elapsed >= 1.0:

        seconds_passed = int(
            elapsed
        )

        last_pee_score_time = (
            last_pee_score_time +
            seconds_passed
        )

        total_change = 0

        # ----------------------------------------------------
        # Only pee that is still active counts
        # ----------------------------------------------------

        for pee in active_pee:

            age = (
                current_time -
                pee["start_time"]
            )

            if age < 1.0:
                continue

            if pee["area"] == "floor":
                total_change += 100 * seconds_passed
            else:
                total_change -= 100 * seconds_passed

        if total_change != 0:

            # Golden Toilet doubles positive points!
            if total_change > 0 and "GoldenToilet" in unlocked_farts:
                total_change *= 2

            score += total_change

            if score < 0:
                trigger_game_over()
                return

            update_score()

    window.ontimer(
        score_pee,
        100
    )


# ============================================================
# FADE FARTS
# ============================================================

def fade_farts():

    current_time = time.time()

    remaining_farts = []

    for fart in active_farts:

        age = (
            current_time -
            fart["start_time"]
        )

        progress = (
            age /
            fart["lifetime"]
        )

        if progress >= 1.0:

            fart["turtle"].clear()
            fart["turtle"].hideturtle()

            continue

        visibility = (
            1.0 -
            progress
        )

        fart["turtle"].clear()

        for dot in fart["dots"]:

            size = int(
                dot["size"] *
                visibility
            )

            if size > 0:

                fart["turtle"].goto(
                    dot["x"],
                    dot["y"]
                )

                fart["turtle"].dot(
                    size,
                    dot["color"]
                )

        remaining_farts.append(
            fart
        )

    active_farts[:] = remaining_farts

    window.ontimer(
        fade_farts,
        40
    )


# ============================================================
# FADE PEE
# ============================================================

def fade_pee():

    current_time = time.time()

    remaining_pee = []

    for pee in active_pee:

        age = (
            current_time -
            pee["start_time"]
        )

        progress = (
            age /
            pee["lifetime"]
        )

        if progress >= 1.0:

            pee["turtle"].clear()
            pee["turtle"].hideturtle()

            continue

        visibility = (
            1.0 -
            progress
        )

        pee["turtle"].clear()

        for drop in pee["droplets"]:

            size = int(
                drop["size"] *
                visibility
            )

            if size > 0:

                pee["turtle"].goto(
                    drop["x"],
                    drop["y"]
                )

                pee["turtle"].dot(
                    size,
                    drop["color"]
                )

        remaining_pee.append(
            pee
        )

    active_pee[:] = remaining_pee

    window.ontimer(
        fade_pee,
        40
    )


# ============================================================
# MOUSE CLICK
# ============================================================

# Mouse-hold state for continuous pee mode.
pee_stream_held = False
pee_stream_target = (0, 0)


def canvas_to_turtle_coords(event):
    """Convert Tk mouse events using the same mapping as Turtle's click handler."""
    canvas = window.getcanvas()
    return (
        canvas.canvasx(event.x) / window.xscale,
        -canvas.canvasy(event.y) / window.yscale
    )


def start_pee_stream(event):
    global pee_stream_held, pee_stream_target

    if not game_active or current_mode != "PEE":
        return

    x, y = canvas_to_turtle_coords(event)

    # Don't start a stream when the mouse is pressed on the shop.
    if SHOP_LEFT <= x <= SHOP_RIGHT and SHOP_BOTTOM <= y <= SHOP_TOP:
        return

    if "Pee" not in unlocked_farts:
        return

    pee_stream_target = (x, y)
    pee_stream_held = True
    make_pee(x, y)
    window.ontimer(pee_stream_tick, 90)


def move_pee_stream(event):
    global pee_stream_target

    if pee_stream_held:
        pee_stream_target = canvas_to_turtle_coords(event)


def stop_pee_stream(event=None):
    global pee_stream_held
    pee_stream_held = False


def pee_stream_tick():
    """Add another short stream segment while the left mouse button is held."""
    if not pee_stream_held or not game_active or current_mode != "PEE":
        return

    x, y = pee_stream_target
    make_pee(x, y)
    window.ontimer(pee_stream_tick, 90)


def mouse_click(x, y):

    if not game_active:
        return

    # --------------------------------------------------------
    # SHOP GETS FIRST PRIORITY
    # --------------------------------------------------------

    if shop_click(x, y):

        return

    # --------------------------------------------------------
    # FART
    # --------------------------------------------------------

    if current_mode == "FART":

        visualFart(
            x,
            y
        )

    # --------------------------------------------------------
    # PEE
    # --------------------------------------------------------

    elif current_mode == "PEE":

        make_pee(
            x,
            y
        )


# ============================================================
# FART MODE
# ============================================================

def fart_mode():

    global current_mode

    if not game_active:
        return

    if current_fart in fartTypes:

        current_mode = "FART"

        update_score()


# ============================================================
# PEE MODE
# ============================================================

def pee_mode():

    global current_mode

    if not game_active:
        return

    if "Pee" not in unlocked_farts:

        return

    current_mode = "PEE"

    update_score()


# ============================================================
# CLEAR ALL POO AND PEE
# ============================================================

def clear_shit():
    """Remove all active fart and pee effects from the screen."""
    global last_pee_score_time

    for fart in active_farts:
        fart["turtle"].clear()
        fart["turtle"].hideturtle()
    active_farts.clear()

    for pee in active_pee:
        pee["turtle"].clear()
        pee["turtle"].hideturtle()
    active_pee.clear()

    last_pee_score_time = time.time()
    update_score()
    draw_shop()
    window.update()
    
# ============================================================
# TEST CHEATS - GIVE 9999999999 SCORE
# ============================================================

#def test_cheat():
#    print("This is just to be used during test gameplay, will be hashed out during the full game")
#    
#    global score
#    score += 9999999999
#    update_score()
# ============================================================
# KEYBOARD CONTROLS
# ============================================================

window.onkey(fart_mode, "f")

window.onkey(fart_mode, "F")

window.onkey(pee_mode, "p")

window.onkey(pee_mode, "P")

window.onkey(clear_shit, "e")

window.onkey(clear_shit, "E")

window.onkey(save_progress, "s")

window.onkey(save_progress, "S")

#window.onkey(test_cheat, "t")

#window.onkey(test_cheat, "T")

window.listen()


# ============================================================
# MOUSE CONTROL
# ============================================================

window.onscreenclick(
    mouse_click,
    btn=1
)

# Tk canvas bindings let pee mode detect a held mouse button and pointer movement.
# add="+" keeps Turtle's existing click handler working for normal fart/shop clicks.
pee_canvas = window.getcanvas()
pee_canvas.bind("<ButtonPress-1>", start_pee_stream, add="+")
pee_canvas.bind("<B1-Motion>", move_pee_stream, add="+")
pee_canvas.bind("<ButtonRelease-1>", stop_pee_stream, add="+")


def shop_scroll(event):
    """Scroll the shop when the pointer is over its panel."""
    global shop_scroll_offset

    x, y = canvas_to_turtle_coords(event)
    if not (SHOP_LEFT <= x <= SHOP_RIGHT and SHOP_BOTTOM <= y <= SHOP_TOP):
        return

    if getattr(event, "num", None) == 4:
        direction = -1
    elif getattr(event, "num", None) == 5:
        direction = 1
    else:
        direction = -1 if getattr(event, "delta", 0) > 0 else 1

    shop_scroll_offset += direction * SHOP_SCROLL_STEP
    draw_shop()
    window.update()


pee_canvas.bind("<MouseWheel>", shop_scroll, add="+")
pee_canvas.bind("<Button-4>", shop_scroll, add="+")
pee_canvas.bind("<Button-5>", shop_scroll, add="+")


# ============================================================
# START SYSTEMS
# ============================================================

window.ontimer(
    fade_farts,
    40
)

window.ontimer(
    fade_pee,
    40
)

window.ontimer(
    score_pee,
    100
)


# ============================================================
# LOAD PLAYER AND START GAME
# ============================================================

load_progress()

make_game_fullscreen()

draw_hud_bar()
draw_toilet()
update_score()

draw_shop()

window.update()

window.mainloop()



