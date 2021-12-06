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

def get_hour(data):
    hour = getattr(data,'hour')
    return hour

def get_minute(data):
    minute = getattr(data,'minute')
    return minute


def click_left():
    hold = mouse.get_position()
    coor.add((hold[0],hold[1],1))

def click_right():
    hold = mouse.get_position()
    coor.add((hold[0],hold[1],0))


def get_mouse_dynamics(days):

    hour = -1
    minute = -1
    condition = 0 # 12 midnight
    num_days  = days
    num_days_count = 0
        

    while num_days_count != num_days:

        if hour == condition and minute == 0:
            num_days_count += 1
    
            time.sleep(70)

        mouse.on_click(click_left)   
        mouse.on_right_click(click_right)
        time.sleep(1)
        
        
        date = datetime.now()
        hour = get_hour(date)
        minute = get_minute(date)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--days')
    args, unknown = parser.parse_known_args()

    print('Script 1a is running ...')
    get_mouse_dynamics(int(unknown[0]))

    for i,j,k in list(coor):
        x.append(i)
        y.append(j)
        clicks.append(k)
        
    mouse_coordinates = pd.DataFrame(list(zip(x, y, clicks)),columns = ['x_coordinates', 'y_coordinates', 'clicks'])
    #mouse_coordinates.drop_duplicates(keep='first', inplace=True)
    mouse_coordinates.to_csv('data_storage/mouse_data.csv',index=False)
    print('Script 1a is done.')