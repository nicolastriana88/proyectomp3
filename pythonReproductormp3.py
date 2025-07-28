#Librerias
import pygame 
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import time #Futuro uso para nuevas funcionalidades
import os

#Iniciar pygame y pygamemixer
pygame.init()
pygame.mixer.init()

# Tkinter parametros

root = Tk()
root.title("ReproductorMP3")
frm = ttk.Frame(root, padding=10)
frm.grid() #Podria ser reemplazdo por PACk

# Variables Globales
current_song = None
volume_var = DoubleVar(value=70)
progress_var = DoubleVar(value=0)
is_playing = False
song_length = 0 
song_name_var = StringVar(value="No song loaded") 
folder_path = None
playlist = []
current_song_index = 0
progress_updating = False


#Funciones


def add_song(): 
    files = filedialog.askopenfilenames(
        title = "Select new song",
        initialdir=os.path.expanduser("~"),
        filetypes=[("MP3 Files", "*.mp3"), ("All Files", "*.*")]
    )

    if files:
        global playlist
        playlist.extend(files)
        if not current_song: 
            load_song(0)

def add_folder():
    global folder_path, playlist
    folder_path = filedialog.askdirectory(
        title="Select folder with songs",
        initialdir=os.path.expanduser("~")
    )

    if folder_path:
        playlist = [
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if file.lower().endswith(".mp3")
        ]
        if playlist:
            load_song(0)
        else:
            messagebox.showinfo("Info", "No MP3 files found in the selected folder")

def get_song_length(file_path):
    try:
        sound = pygame.mixer.Sound(file_path)
        return sound.get_length()
    except:
        return 0  

def load_song(index):
    global current_song,is_playing, song_length, current_song_index
    if 0 <= index < len(playlist):
        current_song_index = index
        current_song = playlist[current_song_index]
        pygame.mixer.music.load(current_song)
        song_length = get_song_length(current_song)
        song_name_var.set(os.path.basename(current_song))
        progress_var.set(0)
        if is_playing:
            pygame.mixer.music.play()
            update_progress()

        
def play_and_pause():
    global is_playing
    if current_song:
        if not is_playing:
            pygame.mixer.music.play()
            is_playing = True
            update_progress()
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            is_playing = not is_playing

def stop_song():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    progress_var.set(0)

#try


def next_song():
    if playlist:
        new_index = (current_song_index + 1) % len(playlist)
        load_song(new_index)
        if is_playing:
            pygame.mixer.music.play()

def prev_song():
    if playlist:
        new_index = (current_song_index - 1) % len(playlist)
        load_song(new_index)
        if is_playing:
            pygame.mixer.music.play()

def set_volume(val):
    volume = float(val)/100.0 
    pygame.mixer.music.set_volume(volume)

def update_progress():
    global progress_updating
    if is_playing and pygame.mixer.music.get_busy():
        current_pos = pygame.mixer.music.get_pos() / 1000
        if song_length > 0:
            progress = min((current_pos / song_length) * 100, 100)
            progress_var.set(progress)
            if progress >= 100:
                next_song()
        root.after(100, update_progress)
    else:
        progress_updating = False


# Widgets
ttk.Label(frm, textvariable=song_name_var).grid(column=1, row=1) 

# Botones con Comandos
ttk.Button(frm, text="Play/Pause", command=play_and_pause).grid(column=1, row=2)
ttk.Button(frm, text="Next", command=next_song).grid(column=2, row=2)
ttk.Button(frm, text="Back", command=prev_song).grid(column=0, row=2)
ttk.Button(frm, text="Stop", command=stop_song).grid(column=1, row=3)
ttk.Button(frm, text="Add song", command=add_song).grid(column=0, row=1)
ttk.Button(frm, text="Add Folder", command=add_folder).grid(column=2, row=1)

# Boton de Volumen
ttk.Label(frm,text="Volume").grid(column=4,row=0)
ttk.Scale(frm, from_=100, to=0, orient=VERTICAL, variable=volume_var, command=set_volume).grid(column=4, row=2)

#progress bar - Boton barra de progreso
ttk.Progressbar(frm, length=400,orient=HORIZONTAL, variable=progress_var, maximum=100).grid(column=1, row=5)


# Main loop
root.mainloop()