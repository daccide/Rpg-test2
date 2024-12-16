#pgzero

import pgzrun
import random
import pygame.mouse
from pgzero.keyboard import keyboard
from pgzhelper import *

WIDTH = 600
HEIGHT = 150

TITLE = "RPG"  # Titolo della finestra di gioco
FPS = 30  # Numero di frame per secondo

background = Actor("background_layer_1.png", size=320)
background1 = Actor("background_layer_2.png", size=320)
background2 = Actor("background_layer_3.png", size=320)
Health = Actor("health",(25,20))
background_width = 320

yeninja = Actor("enemyyeidle1", (350, 120))
yeninja.health = 50
yeninja.attack = 10

is_hit = False
hit_timer = 0
hit_duration = 30
hit_animation_frame = 0

protagonist = Actor("skidleow2.png", (10, 120))
protagonist.health = 100
protagonist.attack = 20


skeleton = Actor("ready_1", (50, 132))
# Le animazioni di idle, run, e runow
idle_animation = ["idle0", "idle1", "idle2", "idle3", "idle4", "idle5", "idle6", "idle7", "idle8", "idle9"]
run_animation = ["run{}".format(i) for i in range(16)]  # da 0 a 15
runow_animation = ["runow{}".format(i) for i in range(16)]  # da 0 a 15
attack_animation = ["attacco2", "attacco3", "attacco4", "attacco5", "attacco6", "attacco7"]
idle_skeleton_animation = ["ready_{}".format(i) for i in range(4)]
idle_skeleton_animation_ow = ["skidleow{}".format(i) for i in range(4)]
is_attacking = False
last_direction = ""

# Variabili per le animazioni
idle_frame = 0
run_frame = 0
runow_frame = 0
attack_frame = 0
idle_delay = 5  # Quante volte deve passare prima di cambiare frame (animazione idle)
run_delay = 3  # Ritardo per l'animazione "run"
runow_delay = 3  # Ritardo per l'animazione "runow"
attack_delay = 3
frame_counter = 0  # Contatore generale dei frame
attack_frame_counter = 0
yeninja_frame_counter = 0

def enemyyellowninja():
    global yeninja, yeninja_frame_counter, is_hit, hit_timer, hit_animation_frame
    yeninja_idle_animation = [
        "enemyyeidle1", "enemyyeidle2", "enemyyeidle3", "enemyyeidle4",
        "enemyyeidle5", "enemyyeidle6", "enemyyeidle7", "enemyyeidle8"
    ]
    yeninja_whenhit_animation = ["whenenemyyeishit1", "whenenemyyeishit2", "whenenemyyeishit3", "whenenemyyeishit4"]
    yeninja_walking_animation = ["enwalkye1", "enwalkye2", "enwalkye3", "enwalkye4", "enwalkye5", "enwalkye6",
                                 "enwalkye7", "enwalkye8", "enwalkye9", "enwalkye10"]

    walking_distance = 100
    yeninja_idle_delay = 6
    yeninja_walk_delay = 4
    distance_to_protagonist = protagonist.x - yeninja.x
    if is_hit:
        yeninja.image = yeninja_whenhit_animation[hit_animation_frame]
        hit_timer += 1
        if hit_timer % 8 == 0:
            hit_animation_frame = (hit_animation_frame + 1) % len(yeninja_whenhit_animation)
        if hit_timer >= hit_duration:
            is_hit = False
            hit_timer = 0
            hit_animation_frame = 0
        return
    if distance_to_protagonist <= walking_distance:
        yeninja_frame_counter += 1
        if yeninja_frame_counter >= yeninja_walk_delay:
            yeninja_frame_counter = 0
            if yeninja.image in yeninja_walking_animation:
                current_image = yeninja_walking_animation.index(yeninja.image)
                next_image = (current_image + 1) % len(yeninja_walking_animation)
                yeninja.image = yeninja_walking_animation[next_image]
            else:
                yeninja.image = yeninja_walking_animation[0]
        return
    yeninja_frame_counter += 1
    if yeninja_frame_counter >= yeninja_idle_delay:
        yeninja_frame_counter = 0
        if yeninja.image in yeninja_idle_animation:
            current_image = yeninja_idle_animation.index(yeninja.image)
            next_image = (current_image + 1) % len(yeninja_idle_animation)
            yeninja.image = yeninja_idle_animation[next_image]
        else:
            yeninja.image = yeninja_idle_animation[0]

def check_collision():
    """Controlla se il giocatore colpisce yeninja."""
    global is_hit
    if is_attacking and protagonist.colliderect(yeninja) and not is_hit:
        is_hit = True


def draw():
    global background, background1, background2
    # Disegna i personaggi
    repetitions = WIDTH // background_width + 1
    for i in range(repetitions):
        x_pos = i * background_width

        background.x = x_pos + background_width // 2
        background.y = HEIGHT // 2
        background.draw()

        background1.x = x_pos + background_width // 2
        background1.y = HEIGHT // 2
        background1.draw()

        background2.x = x_pos + background_width // 2
        background2.y = HEIGHT // 2
        background2.draw()
    yeninja.draw()
    protagonist.draw()
    Health.draw()
    screen.draw.text(str(protagonist.health), center=(30, 20), color="pink", fontsize=15)

def character():
    global protagonist



def handle_movement():
    global protagonist, idle_frame, run_frame, runow_frame, attack_frame, frame_counter, last_direction

    # Controllo del movimento e delle animazioni
    if keyboard.D or keyboard.right:  # Controlla se la freccia destra è premuta
        protagonist.x += 3
        # Esegui animazione "run"
        frame_counter += 1  # Incrementa il contatore per la gestione dei frame
        last_direction = "est"
        if frame_counter >= run_delay:  # Cambia il frame ogni run_delay
            frame_counter = 0  # Reset del contatore
            run_frame = (run_frame + 1) % len(run_animation)  # Cicla tra i frame di "run"
            protagonist.image = run_animation[run_frame]  # Aggiorna l'immagine


    elif keyboard.A or keyboard.left:  # Controlla se la freccia sinistra è premuta
        protagonist.x -= 3
        # Esegui animazione "runow"
        frame_counter += 1  # Incrementa il contatore per la gestione dei frame
        last_direction = "ovest"
        if frame_counter >= runow_delay:  # Cambia il frame ogni runow_delay
            frame_counter = 0  # Reset del contatore
            runow_frame = (runow_frame + 1) % len(runow_animation)  # Cicla tra i frame di "runow"
            protagonist.image = runow_animation[runow_frame]  # Aggiorna l'immagine
    else:
        # Animazione idle
        frame_counter += 1  # Incrementa il contatore per la gestione dei frame
        if frame_counter >= idle_delay:  # Cambia il frame ogni idle_delay
            frame_counter = 0  # Reset del contatore
            idle_frame = (idle_frame + 1) % len(idle_animation)  # Cicla tra i frame di "idle"
            protagonist.image = idle_animation[idle_frame]  # Aggiorna l'immagine


def on_mouse_down(button, pos):
    """Inizio dell'animazione attacco quando il mouse viene premuto."""
    global is_attacking, current_frame, frame_counter
    if button == mouse.LEFT:  # Rileva il clic del pulsante sinistro
        is_attacking = True
        current_frame = 0  # Ripristina l'animazione dal primo frame
        frame_counter = 0  # Ripristina il contatore del delay


def attack_sequence():
    global current_frame, is_attacking, frame_counter
    frame_counter += 1  # Incrementa il contatore dei frame

    # Cambia il frame solo dopo che ha raggiunto il delay previsto
    if frame_counter >= attack_delay:
        frame_counter = 0  # Resetta il contatore
        current_frame += 1  # Passa al prossimo frame

        # Controlla se ci sono ancora frame da mostrare
        if current_frame < len(attack_animation):
            protagonist.image = attack_animation[current_frame]  # Cambia immagine
        else:
            is_attacking = False  # Fine dell'animazione
            protagonist.image = "idle0"  # Torna all'immagine di default


def update(dt):
    global is_attacking
    enemyyellowninja()
    check_collision()

    if is_attacking:
        attack_sequence()
    else:
        handle_movement()


pgzrun.go()
