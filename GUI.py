# (c) 2018 Tongyu Zhou, Tingda Wang
# GUI for a simple pokemon type guessing game played against the predictive model

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os, random
import sys

# -----------
# remove these lines if code not working
# for set TkAgg backend for compatibility between matplotlib and tkinter
import matplotlib
matplotlib.use("TkAgg")
# -----------

from preprocess import types, get_pokemon
from run import load_models, load_image, run, predict_single

# determines the outcome of a click
def clicked(window, type_labels, correct_type, player_counter, AI_counter, AI_answer, classifier, test_set, name_txt):
    if correct_type:
        score = int(player_counter.cget("text").split(": ")[1])
        player_counter.configure(text="Player score: " + str(score+1))
    if AI_answer:
        score = int(AI_counter.cget("text").split(": ")[1])
        AI_counter.configure(text="AI score: " + str(score+1))

    pokemon_id, prediction = next_pokemon(window, classifier, test_set, name_txt)
    labels(window, type_labels, pokemon_id, player_counter, AI_counter, prediction, classifier, test_set, name_txt)

# Picks a random next pokemon to be guessed
def next_pokemon(window, classifier, test_set, name_txt):
    path = "data/main-sprites/"
    
    game_vers = random.choice(os.listdir(path))
    while str(game_vers).endswith('.DS_Store'):
        game_vers = random.choice(os.listdir(path))
    img = random.choice(os.listdir(path + game_vers))
    while not str(img).endswith('png'):
        img = random.choice(os.listdir(path + game_vers))
    file_name = path + game_vers + '/' + img

    pilImage = Image.open(file_name)
    pilImage = pilImage.resize((100, 100), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    p = Label(window, image = image)
    p.photo = image
    p.place(x=150, y=130, anchor="center")
    name_txt.set(get_pokemon(img).name)

    prediction = predict_single(file_name, classifier, test_set)

    return img, prediction

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
def labels(window, type_labels, pokemon_id, player_counter, AI_counter, prediction, classifier, test_set, name_txt):
    typing = types('data/Pokemon-2.csv')
    path = "data/type_labels/"
    type = get_pokemon(pokemon_id).type1
    AI_answer = (type == prediction)

    type_labels[0] = (path + type + '.png', True)

    for i in range(1,4):
        name = path + random.choice(os.listdir(path))
        temp = [a for b in type_labels for a in b]
        while str(name).endswith('.DS_Store') or name in temp:
            name = path + random.choice(os.listdir(path))
        type_labels[i] = (name, False)

    for i in range(4):
        pilImage = Image.open(type_labels[i][0])
        image = ImageTk.PhotoImage(pilImage)
        type_labels[i] = (image,type_labels[i][1])

    random.shuffle(type_labels)


    btn1 = Button(window, image=type_labels[0][0], command=lambda: 
                  clicked(window,type_labels,type_labels[0][1],player_counter,AI_counter,AI_answer,classifier, test_set, name_txt))
    btn2 = Button(window, image=type_labels[1][0], command=lambda: 
                  clicked(window,type_labels,type_labels[1][1],player_counter,AI_counter,AI_answer,classifier, test_set, name_txt))
    btn3 = Button(window, image=type_labels[2][0], command=lambda: 
                  clicked(window,type_labels,type_labels[2][1],player_counter,AI_counter,AI_answer,classifier, test_set, name_txt))
    btn4 = Button(window, image=type_labels[3][0], command=lambda: 
                  clicked(window,type_labels,type_labels[3][1],player_counter,AI_counter,AI_answer,classifier, test_set, name_txt))

    btn1.place(x=100, y=200, anchor="center")
    btn2.place(x=100, y=250, anchor="center")
    btn3.place(x=200, y=200, anchor="center")
    btn4.place(x=200, y=250, anchor="center")


if __name__ == "__main__":

    window = Tk()
    window.title("Pokemon Classification Game")
    window.geometry('300x300')

    f = Frame(window,bg="white",width=400,height=400)
    f.grid(row=0,column=0,sticky="NW")
    f.grid_propagate(0)
    f.update()

    type_labels = [(None, None), (None, None), (None, None), (None, None)]

    player_counter = Label(window, text = "Player score: 0")
    player_counter.place(x = 65, y = 10, anchor = "center")
    
    AI_counter = Label(window, text = "AI score: 0")
    AI_counter.place(x = 250, y = 10, anchor = "center")

    classifier, test_set = run(evaluate = False, predict = False)

    v = StringVar()
    name_label = Label(window, textvariable = v)
    name_label.place(x = 150, y = 30, anchor = "center")

    pokemon_id, prediction = next_pokemon(window, classifier, test_set, v)
    labels(window, type_labels, pokemon_id, player_counter, AI_counter, prediction, classifier, test_set, v)

    window.mainloop()

