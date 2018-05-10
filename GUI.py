# (c) 2018 Tongyu Zhou, Tingda Wang
# GUI for a simple pokemon type guessing game played against the predictive model

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os, random
import sys
from queue import Queue

# -----------
# remove these lines if code not working
# for set TkAgg backend for compatibility between matplotlib and tkinter
import matplotlib
matplotlib.use("TkAgg")
# -----------

from preprocess import types, get_pokemon
from run import load_models, load_image, run, predict_single

class GUIData:
    #Attrs:
    #pd.AI_answer
    #pd.AI_counter
    #pd.classifier
    #pd.name_txt
    #pd.player_counter
    #pd.pokemon_id
    #pd.prediction
    #pd.test_set
    #pd.type_labels
    #pd.window
    #pd.multi
    #pd.net
    pass

class NetData:
    #pd.net.queue
    #pd.net.last_item
    pass

pd = GUIData()
pd.net = NetData()

# determines the outcome of a click
def clicked(correct_type):
    if correct_type:
        score = int(pd.player_counter.cget("text").split(": ")[1])
        pd.player_counter.configure(text="Player score: " + str(score+1))
    if pd.AI_answer:
        score = int(pd.AI_counter.cget("text").split(": ")[1])
        pd.AI_counter.configure(text="AI score: " + str(score+1))
    if not pd.multi:
        next_pokemon()
        labels()
    if pd.multi:
        pd.net.queue.put("click")


def random_sprite():
    path = "data/main-sprites/"

    game_vers = random.choice(os.listdir(path))
    while str(game_vers).endswith('.DS_Store'):
        game_vers = random.choice(os.listdir(path))
    img = random.choice(os.listdir(path + game_vers))
    while not str(img).endswith('png'):
        img = random.choice(os.listdir(path + game_vers))
    return (path + game_vers + '/' + img, img)

# Picks a random next pokemon to be guessed
def next_pokemon():
    (file_name, img) = random_sprite()
    set_pokemon(file_name, img)

def set_pokemon(file_name, img):
    pilImage = Image.open(file_name)
    pilImage = pilImage.resize((100, 100), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    p = Label(pd.window, image = image)
    p.photo = image
    p.place(x=150, y=130, anchor="center")
    pd.name_txt.set(get_pokemon(img).name)

    pd.prediction = predict_single(file_name, pd.classifier, pd.test_set)
    pd.pokemon_id = img

# Returns a random label
def rand():
    path = "data/type_labels/"
    name = path + random.choice(os.listdir(path))
    while str(name).endswith('.DS_Store'):
            name = path + random.choice(os.listdir(path))
    pilImage = Image.open(name)
    image = ImageTk.PhotoImage(pilImage)
    return image

# Labels the type buttons
def labels():
    typing = types('data/Pokemon-2.csv')
    path = "data/type_labels/"
    type = get_pokemon(pd.pokemon_id).type1
    pd.AI_answer = (type == pd.prediction)

    pd.type_labels[0] = (path + type + '.png', True)

    for i in range(1,4):
        name = path + random.choice(os.listdir(path))
        temp = [a for b in pd.type_labels for a in b]
        while str(name).endswith('.DS_Store') or name in temp:
            name = path + random.choice(os.listdir(path))
        pd.type_labels[i] = (name, False)

    for i in range(4):
        pilImage = Image.open(pd.type_labels[i][0])
        image = ImageTk.PhotoImage(pilImage)
        pd.type_labels[i] = (image,pd.type_labels[i][1])

    random.shuffle(pd.type_labels)


    btn1 = Button(pd.window, image=pd.type_labels[0][0], command=lambda:
                  clicked(pd.type_labels[0][1]))
    btn2 = Button(pd.window, image=pd.type_labels[1][0], command=lambda:
                  clicked(pd.type_labels[1][1]))
    btn3 = Button(pd.window, image=pd.type_labels[2][0], command=lambda:
                  clicked(pd.type_labels[2][1]))
    btn4 = Button(pd.window, image=pd.type_labels[3][0], command=lambda:
                  clicked(pd.type_labels[3][1]))

    btn1.place(x=100, y=200, anchor="center")
    btn2.place(x=100, y=250, anchor="center")
    btn3.place(x=200, y=200, anchor="center")
    btn4.place(x=200, y=250, anchor="center")


def gui():
    if pd.multi:
        pd.net.queue = Queue()

    window = Tk()
    pd.window = window
    pd.window.title("Pokemon Classification Game")
    pd.window.geometry('300x300')

    f = Frame(window,bg="white",width=400,height=400)
    f.grid(row=0,column=0,sticky="NW")
    f.grid_propagate(0)
    f.update()

    pd.type_labels = [(None, None), (None, None), (None, None), (None, None)]

    pd.player_counter = Label(window, text = "Player score: 0")
    pd.player_counter.place(x = 65, y = 10, anchor = "center")

    pd.AI_counter = Label(window, text = "AI score: 0")
    pd.AI_counter.place(x = 250, y = 10, anchor = "center")

    pd.classifier, pd.test_set = run(evaluate = False, predict = False)

    v = StringVar()
    name_label = Label(window, textvariable = v)
    name_label.place(x = 150, y = 30, anchor = "center")

    pd.name_txt = v
    if not pd.multi:
        next_pokemon()
        labels()

if __name__ == "__main__":
    pd.multi = False
    gui()
    window.mainloop()
