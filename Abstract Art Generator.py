import pygame, random, time, webbrowser, ctypes
pygame.init()

# Loads all the photos
save = pygame.image.load('photos/save.png')
menu_icon = pygame.image.load('photos/menu.png')
redo = pygame.image.load('photos/repeat.png')
pause = pygame.image.load('photos/pause.png')
play = pygame.image.load('photos/play.png')

github_icon_normal, github_icon_big = pygame.image.load('photos/github_logo.png'), pygame.image.load('photos/github_logo_big.png')
twitter_icon_normal, twitter_icon_big = pygame.image.load('photos/twitter_logo.png'), pygame.image.load('photos/twitter_logo_big.png')
discord_icon_normal, discord_icon_big = pygame.image.load('photos/discord_logo.png'), pygame.image.load('photos/discord_logo_big.png')

# Sets program icon
programIcon = pygame.image.load('photos/icon.png')
pygame.display.set_icon(programIcon)

# Gets the monitors screenwidth and height
screenwidth = ctypes.windll.user32.GetSystemMetrics(0)
screenheight = ctypes.windll.user32.GetSystemMetrics(1)

# Defines shapes list
shapes = ["circle", "line"]


class CreateShape:
    def __init__(self, x, y, size, color, xy1=(random.randint(0, screenwidth), random.randint(0, screenheight)), xy2=(random.randint(0, screenwidth), random.randint(0, screenheight)), width=1):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.xy1 = xy1
        self.xy2 = xy2
        self.width = width

    def spawn(self, win):
        """
        Creates an object and draws it on the screen
        :param win:
        :return: None
        """

        if shape == "circle":
            pygame.draw.circle(win, self.color, (self.x, self.y), self.size)
        elif shape == "line":
            pygame.draw.line(win, self.color, (random.randint(0, screenwidth), random.randint(0, screenheight)), (random.randint(0, screenwidth), random.randint(0, screenheight)), self.width)
        else:
            if "circle" in shapes:
                pygame.draw.circle(win, self.color, (self.x, self.y), self.size)
            if "line" in shapes:
                pygame.draw.line(win, self.color, self.xy1, self.xy2, self.width)


class Button:
    def __init__(self, color, x, y, width, height, opacity, text='', font_size = 100):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.opacity = opacity
        self.text = text
        self.font_size = font_size

    def draw(self, win):
        """
        Draws the button
        :param win:
        :return: None
        """
        s = pygame.Surface((self.width+4, self.height+4))  # the size of your rect
        s.set_alpha(self.opacity)  # alpha level
        s.fill(self.color)  # this fills the entire surface
        win.blit(s, (round(self.x - 2), round(self.y - 2)))

        if self.text != '':
            font = pygame.font.SysFont('main_menu_font.ttf', self.font_size)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (
                round(self.x + (self.width / 2 - text.get_width() / 2)), round(self.y + (self.height / 2 - text.get_height() / 2))))


    def isOver(self, pos):
        """
        Checks if the mouse is over the button
        :param pos:
        :return: True or False
        """
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def isOver(x, y, width, height, pos):
    """
    Checks if the mouse is over the button
    :return: True or False
    """
    # Pos is the mouse position or a tuple of (x,y) coordinates
    if x < pos[0] < x + width:
        if y < pos[1] < y + height:
            return True

    return False

def blurSurf(surface, amt):
    """
    Blurs the given surface by the given 'amount'.
    """

    scale = 1.0/float(amt)

    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))

    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)

    return surf

def draw_text(text, font, color, surface, x, y):
    """
    Creates a text object and writes it on the screen
    :return: None
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)

    surface.blit(textobj, textrect)

def draw_text2(text, font, color, surface, x, y):
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    surface.blit(text, text_rect)

def menu():
    """
    A really ugly and bad line of text that I want to forget and is basically is the entire menu.
    This was my first time making a menu with pygame so bare with me here lol.
    WARNING: SEVERE SPAGHETTI CODE AHEAD. PROCEED WITH CAUTION!
    :return: None
    """

    global count, random_int, shape, prefix_shape, shape_list, screen, enable_timer, enable_advanced, enable_small, enable_med, enable_big

    first = True

    color = (255,255,255)

    # Defines everything needed
    start_button_opacity, stop_button_opacity, settings_button_opacity, info_button_opacity = 0,0,0,0

    circle_button_opacity, line_button_opacity, timer_button_opacity, advanced_generator_opacity = 40, 40, 0, 40
    enable_timer, enable_circle, enable_line, enable_advanced = False, True, True, True

    gen_small_opacity, gen_med_opacity, gen_big_opacity = 0, 40, 0
    enable_small, enable_med, enable_big = False, True, False

    is_settings, is_info = False, False

    github_icon, twitter_icon, discord_icon = github_icon_normal, twitter_icon_normal, discord_icon_normal
    github_icon_x, github_icon_y = 40, 900
    twitter_icon_x, twitter_icon_y = 240, 930
    discord_icon_x, discord_icon_y = 405, 920

    # Checks if the current screen is menu
    while screen == "menu":
        # Makes a black obj between the menu and the generation
        win.fill((255, 255, 255))
        for obj in shape_list:
            obj.spawn(win)

        win.blit(blurSurf(win, 5), (0, 0))
        win.blit(black, (0, 0))

        # Checks to see if to keep going generating or stop for 2 seconds and start a new one
        if count < random_int:
            prefix_shape = CreateShape(x=random.randint(0, screenwidth), y=random.randint(0, screenheight),
                                        size=random.randint(10, 100),
                                        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                        width=random.randint(5, 10))

            shape = "circle"
            shape_list.append(prefix_shape)

        else:
            if first:
                start_time = time.time()
                first = False
            elif time.time() - start_time > 2:
                random_int = random.randint(400, 1200)
                shape_list = []
                count = -1
                first = True

        # Checks to see if current screen is not the info tab or the settings tab
        if not is_settings and not is_info:

            font = pygame.font.Font("main_menu_font.ttf", 100)
            text = font.render("Abstract Art Generator", True, (255, 255, 255))
            text_rect = text.get_rect(center=(round(screenwidth / 2), 50))
            win.blit(text, text_rect)

            draw_text2("V1.232", pygame.font.SysFont('main_menu_font.ttf', 30), (255,255,255), win, 1860, 1060)

            # Draws photos
            win.blit(github_icon, (github_icon_x, github_icon_y))
            win.blit(twitter_icon, (twitter_icon_x, twitter_icon_y))
            win.blit(discord_icon, (discord_icon_x, discord_icon_y))

            # Defines buttons
            start_button = Button(color, (screenwidth / 2) - 100, 300, 200, 100, start_button_opacity, "Start")
            settings_button = Button(color, (screenwidth / 2) - 160, 400, 320, 100, settings_button_opacity, "Settings")
            info_button = Button(color, (screenwidth / 2) - 85, 500, 170, 100, info_button_opacity, "Info")
            stop_button = Button(color, (screenwidth / 2) - 100, 600, 200, 100, stop_button_opacity, "Quit")

            # Draws buttons
            start_button.draw(win)
            settings_button.draw(win)
            info_button.draw(win)
            stop_button.draw(win)

            # Checks for events
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    quit()

                # Checks if left mouse button is pressed
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.isOver(pos):
                        screen = "game"
                    elif settings_button.isOver(pos):
                        is_settings = True
                    elif info_button.isOver(pos):
                        is_info = True
                    elif stop_button.isOver(pos):
                        quit()

                    elif isOver(40, 900, 170, 170, pos): webbrowser.open("https://github.com/FirePlank", autoraise=True)
                    elif isOver(240, 930, 130, 106, pos): webbrowser.open("https://twitter.com/FirePlank", autoraise=True)
                    elif isOver(405, 920, 130, 130, pos): webbrowser.open("https://discord.gg/K2Cf6ma", autoraise=True)


                # Checks for mose movement
                elif event.type == pygame.MOUSEMOTION:
                    if start_button.isOver(pos): start_button_opacity = 25
                    else: start_button_opacity = 0

                    if stop_button.isOver(pos): stop_button_opacity = 25
                    else: stop_button_opacity = 0

                    if settings_button.isOver(pos): settings_button_opacity = 25
                    else: settings_button_opacity = 0

                    if info_button.isOver(pos): info_button_opacity = 25
                    else: info_button_opacity = 0

                    if isOver(40, 900, 170, 170, pos): github_icon, github_icon_x, github_icon_y = github_icon_big, 20, 880
                    else: github_icon, github_icon_x, github_icon_y = github_icon_normal, 40, 900
                    if isOver(240, 930, 130, 106, pos): twitter_icon, twitter_icon_x, twitter_icon_y = twitter_icon_big, 220, 916
                    else: twitter_icon, twitter_icon_x, twitter_icon_y = twitter_icon_normal, 240, 930
                    if isOver(405, 920, 130, 130, pos): discord_icon, discord_icon_x, discord_icon_y = discord_icon_big, 385, 900
                    else: discord_icon, discord_icon_x, discord_icon_y = discord_icon_normal, 405, 920

        # Checks if current screen is settings
        elif is_settings:
            draw_text2("Settings", pygame.font.Font("main_menu_font.ttf", 100), (255,255,255), win, round(screenwidth / 2), 50)
            draw_text2("Generation Amount", pygame.font.Font("main_menu_font.ttf", 55), (255,255,255), win, round(screenwidth / 2), 545)

            # Defines buttons
            include_circle = Button((255, 255, 255), (screenwidth / 2) - 150, 170, 300, 50, circle_button_opacity, "Include Circles", 50)
            include_line = Button((255, 255, 255), (screenwidth / 2) - 150, 225, 300, 50, line_button_opacity, "Include Lines", 50)
            advanced_generation = Button((255, 255, 255), (screenwidth / 2) - 300, 340, 600, 75, advanced_generator_opacity, "Advanced Generation", 75)
            include_timer = Button((255, 255, 255), (screenwidth / 2) - 82, 420, 165, 75, timer_button_opacity, "Timer", 75)

            gen_small = Button((255,255,255), (screenwidth / 2) - 82, 605, 165, 75, gen_small_opacity, "Small", 75)
            gen_med = Button((255,255,255), (screenwidth / 2) - 115, 685, 230, 75, gen_med_opacity, "Medium", 75)
            gen_big = Button((255,255,255), (screenwidth / 2) - 65, 765, 130, 75, gen_big_opacity, "Big", 75)

            back_button = Button(color, (screenwidth / 2) - 100, 900, 200, 100, stop_button_opacity, "Back")

            # Draw everything to screen
            include_circle.draw(win)
            include_line.draw(win)
            include_timer.draw(win)
            advanced_generation.draw(win)

            gen_small.draw(win)
            gen_med.draw(win)
            gen_big.draw(win)

            back_button.draw(win)

            # Checks for events
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Checks what button is pressed if any
                    if include_circle.isOver(pos) and shapes != ["circle"]:
                        if enable_circle:
                            circle_button_opacity = 0
                            shapes.remove("circle")
                            enable_circle = False
                        else:
                            circle_button_opacity = 50
                            shapes.append("circle")
                            enable_circle = True

                    elif include_line.isOver(pos) and shapes != ["line"]:
                        if enable_line:
                            line_button_opacity = 0
                            shapes.remove("line")
                            enable_line = False
                        else:
                            line_button_opacity = 50
                            shapes.append("line")
                            enable_line = True

                    elif advanced_generation.isOver(pos):
                        if enable_advanced:
                            advanced_generator_opacity = 0
                            enable_advanced = False
                        else:
                            advanced_generator_opacity = 50
                            enable_advanced = True

                    elif include_timer.isOver(pos):
                        if enable_timer:
                            timer_button_opacity = 0
                            enable_timer = False
                        else:
                            timer_button_opacity = 50
                            enable_timer = True


                    elif gen_small.isOver(pos):
                        if not enable_small:
                            gen_small_opacity = 50
                            enable_small, enable_med, enable_big  = True, False, False
                            gen_med_opacity, gen_big_opacity = 0,0

                    elif gen_med.isOver(pos):
                        if not enable_med:
                            gen_med_opacity = 50
                            enable_small, enable_med, enable_big  = False, True, False
                            gen_small_opacity, gen_big_opacity = 0, 0

                    elif gen_big.isOver(pos):
                        if not enable_big:
                            gen_big_opacity = 50
                            enable_small, enable_med, enable_big  = False, False, True
                            gen_med_opacity, gen_small_opacity = 0, 0

                    elif back_button.isOver(pos):
                        start_button_opacity = 0
                        settings_button_opacity = 0
                        stop_button_opacity = 0
                        info_button_opacity = 0
                        is_settings = False

                elif event.type == pygame.MOUSEMOTION:
                    # Checks to see if mouse is over any buttons to change the opacity of them
                    if include_circle.isOver(pos):
                        if enable_circle: circle_button_opacity = 75
                        else: circle_button_opacity = 25
                    else:
                        if enable_circle: circle_button_opacity = 50
                        else: circle_button_opacity = 0

                    if include_line.isOver(pos):
                        if enable_line: line_button_opacity = 75
                        else: line_button_opacity = 25
                    else:
                        if enable_line: line_button_opacity = 50
                        else: line_button_opacity = 0

                    if advanced_generation.isOver(pos):
                        if enable_advanced: advanced_generator_opacity = 75
                        else: advanced_generator_opacity = 25
                    else:
                        if enable_advanced: advanced_generator_opacity = 50
                        else: advanced_generator_opacity = 0

                    if include_timer.isOver(pos):
                        if enable_timer: timer_button_opacity = 75
                        else: timer_button_opacity = 25
                    else:
                        if enable_timer: timer_button_opacity = 50
                        else: timer_button_opacity = 0

                    if back_button.isOver(pos):
                        stop_button_opacity = 25
                    else:
                        stop_button_opacity = 0

                    if gen_small.isOver(pos):
                        if enable_small: gen_small_opacity = 75
                        else: gen_small_opacity = 25
                    else:
                        if enable_small: gen_small_opacity = 50
                        else: gen_small_opacity = 0
                    if gen_med.isOver(pos):
                        if enable_med: gen_med_opacity = 75
                        else: gen_med_opacity = 25
                    else:
                        if enable_med: gen_med_opacity = 50
                        else: gen_med_opacity = 0
                    if gen_big.isOver(pos):
                        if enable_big: gen_big_opacity = 75
                        else: gen_big_opacity = 25
                    else:
                        if enable_big: gen_big_opacity = 50
                        else: gen_big_opacity = 0
        # Info Menu
        else:
            font = pygame.font.Font("main_menu_font.ttf", 100)
            text = font.render("Info", True, (255, 255, 255))
            text_rect = text.get_rect(center=(round(screenwidth / 2), 50))
            win.blit(text, text_rect)

            # Text to display in info menu
            draw_text2("Hello! This is my first ever code jam that I have ever participated in", pygame.font.Font("main_menu_font.ttf", 50), (255, 255, 255), win, round(screenwidth / 2), 140)
            draw_text2("So I hope you like what I made (:", pygame.font.Font("main_menu_font.ttf", 50), (255, 255, 255), win, round(screenwidth / 2), 210)
            draw_text2("I know this project is not the most advanced but I sure had fun making this!", pygame.font.Font("main_menu_font.ttf", 50), (255, 255, 255), win, round(screenwidth / 2), 330)
            draw_text2("This app basically generates abstract art if you", pygame.font.Font("main_menu_font.ttf", 50), (255, 255, 255), win, round(screenwidth / 2), 430)
            draw_text2("didn't pick it up from the name already.", pygame.font.Font("main_menu_font.ttf", 50), (255, 255, 255), win, round(screenwidth / 2), 500)
            draw_text2("This apps basically runs with any screen resolution", pygame.font.Font("main_menu_font.ttf", 50), (255, 255, 255), win, round(screenwidth / 2), 600)
            draw_text2("but 1920x1080 is recommended.", pygame.font.Font("main_menu_font.ttf", 50), (255, 255, 255), win, round(screenwidth / 2), 670)
            draw_text2("With Love, FirePlank", pygame.font.Font("main_menu_font.ttf", 50), (255, 255, 255), win, round(screenwidth / 2), 820)

            back_button = Button(color, (screenwidth / 2) - 100, 900, 200, 100, stop_button_opacity, "Back")
            back_button.draw(win)

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Checks to see if the user presses the back button
                    if back_button.isOver(pos):
                        is_info = False
                        start_button_opacity = 0
                        settings_button_opacity = 0
                        stop_button_opacity = 0
                        info_button_opacity = 0

                elif event.type == pygame.MOUSEMOTION:
                    # Checks to see if mouse is over back button
                    if back_button.isOver(pos):
                        stop_button_opacity = 25
                    else:
                        stop_button_opacity = 0

        count += 1
        pygame.display.update()


def redrawWindow():
    """
    Redraws the window so the player can see all the changes
    :return: None
    """
    global shape, enable_timer, stopped
    shape = "all"
    # Checks if timer is enabled
    if enable_timer:
        win.fill((255, 255, 255))
        for obj in shape_list: obj.spawn(win)
        # Draws the timer
        draw_text(f"Time Took: {round(time.time()-timer, 2)}", pygame.font.SysFont(None, 50), (0, 0, 0), win, 800, 15)

    pygame.display.update()

# Sets the app window
win = pygame.display.set_mode((screenwidth, screenheight), pygame.FULLSCREEN)
win.fill((255,255,255))
pygame.display.set_caption("Abstract Art")


# Sets some vars
screen = "menu"
shape_list = []
count = 0
one = True

circle_count = 0
lines_count = 0
xy_list = []

random_int = random.randint(400, 1000)

# Main Loop
while True:
    black = pygame.Surface((screenwidth, screenheight))
    black.set_alpha(130)
    if screen == "menu":
        menu()
    if one:
        one = False
        timer = time.time()

        # Checks which option was picked to generate the right amount of shapes
        if enable_small: random_int = random.randint(100, 400)
        elif enable_med: random_int = random.randint(500, 800)
        else: random_int = random.randint(900, 1300)

        shape_list = []
        count = 0
        win.fill((255,255,255))

    # Draws icons to screen
    win.blit(menu_icon, (1800, 10))
    win.blit(save, (1690, 10))
    win.blit(redo, (1580, 10))

    for event in pygame.event.get():
        # Get the mouse pos
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            quit()

        # Check if user left clicks
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Checks if menu button is pressed
            if isOver(1800, 10, 80, 80, pos):
                screen = "menu"
                one = True
                shape_list = []
                xy_list = []
                count = 0
                circle_count = 0
                lines_count = 0
                menu()

            # Checks if reset button is pressed
            elif isOver(1580, 10, 80, 80, pos):
                one = True
                timer = time.time()
                circle_count = 0
                lines_count = 0
                xy_list = []
                shape_list = []

            # Checks if save button is pressed
            elif isOver(1690, 10, 80, 80, pos):
                try:
                    from tkinter import filedialog
                    import tkinter

                    win.fill((255, 255, 255))
                    for obj in shape_list: obj.spawn(win)

                    root = tkinter.Tk()
                    root.withdraw()
                    img_name = filedialog.asksaveasfilename(initialdir="/", title="Save Abstract Art To...", filetypes=(
                    ("PNG Files", "png.*"), ("JPEG Files", "jpg.*"), ("GIF Files", "gif.*"), ("All Files", "*.*")))
                    root.destroy()

                    pygame.image.save(win, img_name)

                    if enable_timer: draw_text(f"Time Took: {round(time.time() - timer, 2)}", pygame.font.SysFont(None, 50), (0, 0, 0), win,800, 15)
                    win.blit(menu_icon, (1800, 10))
                    win.blit(save, (1690, 10))
                    win.blit(redo, (1580, 10))
                except Exception as e: print(e)


    # Checks to see if to keep going generating or stop
    if count < random_int:
        # Checks if advanced generation is checked
        if enable_advanced:
            good = True
            xy_count = 0
            if len(xy_list) > 400: xy_list=[]
            while xy_count < 500:
                x = random.randint(0, screenwidth)
                y = random.randint(0, screenheight)

                # Checks if shape is too close to an another shape already present
                for i in xy_list:
                    if x-10<=i<=x+10:
                        if y - 10 <= i <= y + 10:
                            good = False
                            break

                if good:
                    xy_list.append(x)
                    xy_list.append(y)
                    break
                else:
                    xy_count += 1
                    continue

            # Creates the shape obj
            prefix_shape = CreateShape(x=x, y=y,
                                        size=random.randint(10, 100),
                                        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                        xy1=(random.randint(0, screenwidth), random.randint(0, screenheight)), xy2=(random.randint(0, screenwidth), random.randint(0, screenheight)),
                                        width=random.randint(5, 10))
            if lines_count > circle_count:
                shape = "circle"
                circle_count += 1
            else:
                shape = "line"
                lines_count += 1

        else:
            # Creates the shape obj
            prefix_shape = CreateShape(x=random.randint(0, screenwidth), y=random.randint(0, screenheight),
                                       size=random.randint(10, 100),
                                       color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                       xy1=(random.randint(0, screenwidth), random.randint(0, screenheight)),
                                       xy2=(random.randint(0, screenwidth), random.randint(0, screenheight)),
                                       width=random.randint(5, 10))
            # Picks a random shape from the shapes list
            shape = random.choice(shapes)

        # Appends the new obj to the shape list
        shape_list.append(prefix_shape)

        # Checks if timer is enabled
        if not enable_timer:
            prefix_shape.spawn(win)

        # Redraws the window and adds one to the counter
        count += 1
        redrawWindow()

