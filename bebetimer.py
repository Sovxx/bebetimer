import sys
import time
import threading
import termios
import tty

# Codes d'échappement ANSI pour les couleurs
BLUE = "\033[94m"
PINK = "\033[95m"
RESET = "\033[0m"
# Code d'échappement ANSI pour effacer l'écran et revenir au début
CLEAR_SCREEN = "\033[2J"
HOME_CURSOR = "\033[H"

# Variables globales pour les compteurs
blue_time = 0
pink_time = 0
blue_symbol = ""
pink_symbol = ""

# Variables pour indiquer si les compteurs sont en cours d'exécution
running_blue = False
running_pink = False
running = True

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}h{minutes:02d}m{seconds:02d}s"

def update_timers():
    global blue_time, pink_time, running_blue, running_pink, running
    while running:
        if running_blue:
            blue_time += 1
        if running_pink:
            pink_time += 1
        time.sleep(1)

def display_timers():
    while running:
        blue_display = f"{BLUE}{format_time(blue_time)}{blue_symbol}{RESET}"
        pink_display = f"{PINK}{format_time(pink_time)}{pink_symbol}{RESET}"
        # Effacer l'écran et déplacer le curseur au début
        sys.stdout.write(f"{CLEAR_SCREEN}{HOME_CURSOR}")
        sys.stdout.write(f"bebetimer : appuyez sur '{BLUE}p{RESET}' ou '{PINK}m{RESET}' (ou 'x' pour quitter)\r\n")
        sys.stdout.write(f"{blue_display}\r\n{pink_display}\r\n")
        sys.stdout.flush()
        time.sleep(0.2)

def key_listener():
    global running_blue, running_pink, blue_symbol, pink_symbol, running
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        while running:
            ch = sys.stdin.read(1)
            if ch == 'p':
                running_blue = not running_blue
                blue_symbol = " <" if running_blue else ""
                running_pink = False
                pink_symbol = ""
            elif ch == 'm':
                running_pink = not running_pink
                pink_symbol = " <" if running_pink else ""
                running_blue = False
                blue_symbol = ""
            elif ch == 'x':
                running = False
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Création et démarrage des threads
timer_thread = threading.Thread(target=update_timers)
display_thread = threading.Thread(target=display_timers)
key_thread = threading.Thread(target=key_listener)

timer_thread.daemon = True
display_thread.daemon = True
key_thread.daemon = True

timer_thread.start()
display_thread.start()
key_thread.start()

# Boucle principale pour garder le script en cours d'exécution
try:
    while running:
        time.sleep(1)
except KeyboardInterrupt:
    running = False
