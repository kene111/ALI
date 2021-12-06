from collections import defaultdict
from time import time
import time as tt
from pynput.keyboard import Listener
from pynput import keyboard
from datetime import datetime
import pandas as pd
import numpy as np
import argparse


# Mapping a key pair to a list of holdtimes and digraphs
all_keys = defaultdict(list)

# Keys which have been pressed down, but not up yet.
pending = {}

# Last key to be de-pressed, corresponding time)
last_key = None


def get_hour(data):
    hour = getattr(data,'hour')
    return hour

def get_minute(data):
    minute = getattr(data,'minute')
    return minute


def key_fix(key):
    
    key_data =  str(key).replace("'","")
    
    if key_data == 'Key.space':
        key_data = 'space'
        
    if key_data == 'Key.shift_r':
        key_data = 'shift'

    if key_data == 'Key.shift':
        key_data = 'shift'
        
    if key_data == "Key.ctrl_l":
        key_data = "ctrl"
        
    if key_data == "Key.enter":
        key_data = "enter"
        
    if key_data == "Key.caps_lock":
        key_data = "capslock"
        
    if key_data == "Key.tab":
        key_data = "tab"
        
    if key_data == "Key.backspace":
        key_data = "backspace"
        
    if key_data == "Key.esc":
        key_data = "escape"
        
    if key_data == "Key.right":
        key_data = "right"
        
    if key_data == "Key.left":
        key_data = "left"
        
    if key_data == "Key.down":
        key_data = "down"
    
    if key_data == "Key.up":
        key_data = "up"
        
    if key_data == "Key.media_volume_up":
        key_data = "volumeUp"
        
    if key_data == "Key.media_volume_down":
        key_data = "volumeDown"
    
    if key_data == "Key.cmd":
        key_data = "cmd"
        
    if key_data == "Key.media_volume_mute":
        key_data = "volumeMute"
        
    if key_data == "Key.media_next":
        key_data = "next"
        
    if key_data == "Key.media_previous":
        key_data = "previous"
        
    if key_data == "Key.f1":
        key_data = "f1"
    
    if key_data == "Key.print_screen":
        key_data = "printScreen"
    
    if key_data == "Key.num_lock":
        key_data = "numlock"
        
    if key_data == "Key.end":
        key_data = "end"

    if key_data == "Key.page_down":
        key_data ="pageDown"
    
    if key_data == "Key.page_up":
        key_data ="pageUp"

    if key_data == "Key.delete":
        key_data ="delete"
        
    return key_data

# replace the null values with 0.
def fill_null(data):
    for i in range(len(data.columns)):
        data.iloc[:,i].fillna(0, inplace=True) 
    return data


def keystroke_dynamics(event):

    global last_key
    
    
    key = key_fix(event.key)
    
    if f'{event}'[:5] == 'Press':
     
        t = pending[key] = time()

        if last_key is not None:
            
            if key != "enter":
                # calculate the digraphs
                all_keys[f'{last_key[0]}_{key}'].append(t - last_key[1])           
            last_key = None
            
    elif f'{event}'[:7] == 'Release':

        if key == 'enter':
            try:
                pending.pop(key)
            except KeyError:
                pass
            last_key = None
        else:
            t = time()
            # calculate the holdtime
            try:
                all_keys[key].append(t - pending.pop(key))
            except KeyError:
                pass
            last_key = [key, t]


def get_keys(days):

    hour = -1
    minute = -1
    condition = 0 # 12 midnight
    num_days  = days
    num_days_count = 0
    

    with keyboard.Events() as events:

        while num_days_count != num_days:
            event = events.get(1.0)

            if event is None:
                pass

            else:

                keystroke_dynamics(event)

            if hour == condition and minute == 0:

                num_days_count += 1
                tt.sleep(70)

            date = datetime.now()
            hour = get_hour(date)
            minute = get_minute(date)




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--days')
    args, unknown = parser.parse_known_args()


    print('Script 3a is running ...')
    get_keys(int(unknown[0]))
    all_keys = pd.DataFrame.from_dict(all_keys, orient='index')
    all_keys = all_keys.transpose()
    all_keys = fill_null(all_keys)
    all_keys.to_csv('data_storage/all_keys_data.csv',index=False)
    print('Script 3a is done.')

# example : s is a holdtime, s_a is a digrapgh between s and a