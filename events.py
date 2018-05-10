import GUI
import time

def current_time():
    return int(round(time.time() * 1000))

def tick_update():
    if hasattr(GUI.pd.net, 'end_time'):
        time_diff = GUI.pd.net.end_time - current_time()
        if time_diff < 0:
            time_diff = 0
        GUI.pd.net.time_txt.set(int(time_diff / 100) / 10)

def set_timer(millis):
    time = current_time()
    GUI.pd.net.start_time = time
    GUI.pd.net.end_time = time + millis

def labels():
    GUI.labels()

def set_pokemon(file_name, img):
    GUI.set_pokemon(file_name, img)

def set_scores(scores):
    print("update score")
    GUI.pd.player_counter.configure(text="Player score: " + str(scores["self"]))
    GUI.pd.AI_counter.configure(text="Opponent score: " + str(scores["high"]))
