import pyautogui
import argparse
import time
import mouse
import pandas as pd
from datetime import datetime


x = []
y = []
clicks = []
coor = set()

def get_minute(data):
    minute = getattr(data,'minute')
    return minute


def click_left():
    hold = mouse.get_position()
    coor.add((hold[0],hold[1],1))

def click_right():
    hold = mouse.get_position()
    coor.add((hold[0],hold[1],0))


def get_mouse_dynamics(state):

    
    minute = -1

    while state:

        if  minute == 0:
            state = False
    

        mouse.on_click(click_left)   
        mouse.on_right_click(click_right)
        time.sleep(1)
        
        
        date = datetime.now()
        minute = get_minute(date)

    for i,j,k in list(coor):
        x.append(i)
        y.append(j)
        clicks.append(k)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--state')
    args, unknown = parser.parse_known_args()


    print('Script 1b is running ...')
    get_mouse_dynamics(bool(unknown[0]))
    mouse_coordinates = pd.DataFrame(list(zip(x, y, clicks)),columns = ['x_coordinates', 'y_coordinates', 'clicks'])
    mouse_coordinates.drop_duplicates(keep='first', inplace=True)
    mouse_coordinates.to_csv('data_storage/mouse_data.csv',index=False)
    x = []
    y = []
    clicks = []
    coor = set()
    print('Script 1b is done.')