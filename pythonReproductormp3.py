#Librerias
import pygame 
from tkinter import *
from tkinter import ttk
import time #Futuro uso para nuevas funcionalidades

#Iniciar pygame y pygamemixer
pygame.init()
pygame.mixer.init()

# Tkinter parametros

root = Tk()
root.title("ReproductorMP3")
frm = ttk.Frame(root, padding=10)
frm.grid() #Podria ser reemplazdo por PACk

# Variables Globales
current_song = "anysong.mp3"  #Variable constante por definir, se añadira funcion buscar en el so la cancion
volume_var = DoubleVar(value=70)
progress_var = DoubleVar(value=0)
is_playing = False
song_length = 0 

#funciones

def get_song_length(file_path):
    sound = pygame.mixer.Sound(file_path)
    return sound.get_length() 

def load_song():
    global is_playing, song_length
    if not is_playing:
        pygame.mixer.music.load(current_song)
        song_length = get_song_length(current_song)
        is_playing = True

def play_and_pause():
    global is_playing,song_length
    if not is_playing:
        load_song()
        pygame.mixer.music.play()
        song_length = 156 #Modificar a futuro no puede ser un valor constante
        is_playing = True
        update_progress()
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

def stop_song():
    global is_playing
    pygame.mixer.music.pause()
    is_playing = False

def set_volume(val):
    volume = float(val)/100.0 
    pygame.mixer.music.set_volume(volume)

def update_progress():
    if is_playing:
        current_pos = pygame.mixer.music.get_pos() / 1000  
        if song_length > 0:
            progress = (current_pos / song_length) * 100
            progress_var.set(progress)
        root.after(100, update_progress)

# Widgets
ttk.Label(frm, text="Songs name").grid(column=1, row=0) #Progreso
ttk.Label(frm, text="Here should be the song photo").grid(column=1, row=1) #Progreso

# Botones con Comandos
ttk.Button(frm, text="play", command=play_and_pause).grid(column=1, row=2)
ttk.Button(frm, text="next").grid(column=2, row=2)
ttk.Button(frm, text="back").grid(column=0, row=2)
ttk.Button(frm, text="stop", command=stop_song).grid(column=1, row=3)

# Boton de Volumen
ttk.Label(frm,text="Volume").grid(column=4,row=0)
ttk.Scale(frm, from_=100, to=0, orient=VERTICAL, variable=volume_var, command=set_volume).grid(column=4, row=2)

#progress bar - Boton barra de progreso
ttk.Progressbar(frm, length=400,orient=HORIZONTAL, variable=progress_var, maximum=100).grid(column=1, row=5)


# Main loop
root.mainloop()