from keras.models import load_model
from datetime import datetime
import argparse
from subprocess import call
import threading
import os
import ctypes
from threading import Thread

from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer, MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import FeatureUnion
import tensorflow as tf
import pickle
import joblib


# libraries imported 

from collections import defaultdict
from time import time as ttt
import time as tt
from pynput.keyboard import Listener
from pynput import keyboard
from datetime import datetime
import pandas as pd
import numpy as np

#

import pyautogui
import time
import mouse
import pandas as pd
from datetime import datetime

#

from win32gui import GetForegroundWindow
import psutil
import time
from collections import defaultdict
import win32process
from datetime import date, datetime
import pandas as pd

#





#####################################################################################################

x = []
y = []
clicks = []
coor = set()
all_keys = defaultdict(list)
pending = {}
last_key = None
current_app = []
activation_time = []

##################################### Key stroke data #####################################################

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
        
                t = pending[key] = ttt()
                #print(f'this is {t}')
                #print(all_keys)

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

                        t = ttt()
                        # calculate the holdtime
                        try:
                                all_keys[key].append(t - pending.pop(key))
                        except KeyError:
                                pass
                        last_key = [key, t]


def get_keys():

        condition = True

        with keyboard.Events() as events:

                while condition:
                        event = events.get(1.0)

                        if event is None:
                                pass

                        else:
                                
                                keystroke_dynamics(event)

                        if len(all_keys.keys()) == 30 and len(all_keys[f'{max(all_keys, key= lambda n: len(all_keys[n]))}']) == 10:
                                condition = False
                                break



############################################### data collection #######################################################################
# correct the data types

def correct_datatype(data):

        date_cols = ['Activation_time']
        cat_cols = ['Application']

        for col in data.columns:
                if col in date_cols:
                        data[col] = pd.to_datetime(data[col])
                elif col in cat_cols:
                        data[col] = data[col].astype('category')
                
        return data


# get important features 
def get_features(data):
    
        #day = getattr(data,'day')
        hour = getattr(data,'hour')
        minute = getattr(data,'minute')
        
        return hour, minute

def extract_time(data):


        day = []
        hour = []
        minute = []
        
        time_data = data['Activation_time'].tolist()
        
        for data in time_data:
                
                
                hourx, minutex = get_features(data) #dayx,
        
                day.append(data.isoweekday())
                hour.append(hourx)
                minute.append(minutex)
                
        return day, hour, minute





def create_duration(list_):
    duration = []
    for i in range(len(list_)-1):
        difference = (list_[i + 1] - list_[i])
        duration.append(difference.total_seconds())
        
    return duration

def handle_datetime(processes_df):

    # convert to proper date format
    processes_df['Activation_time'] = processes_df['Activation_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))

    return processes_df


def get_process_information():
    
    
    condition =True
    
    while condition:

        try:
        
            if win32process.GetWindowThreadProcessId(GetForegroundWindow())[1] > 0 :
            
                # Get Name of current app
                app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")           

                # Get date and time of useage
                a_time = datetime.now()
                
                # add the name of the current application and active start time to a list.
                current_app.append(app)
                activation_time.append(a_time)

                try: 

                    while app == psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "") and win32process.GetWindowThreadProcessId(GetForegroundWindow())[1] > 0:
                        #and len(all_keys[f'{max(all_keys, key= lambda x: len(all_keys[x]))}']) == 10
                        # len(all_keys.keys()) == 30
                        if len(all_keys.keys()) >= 30 and len(all_keys[f'{max(all_keys, key= lambda n: len(all_keys[n]))}']) >= 10:
                            # add the last running time of application before breaking out of code.
                            print('i got here 333')
                            a_time = datetime.now()
                            activation_time.append(a_time)
                            condition = False
                            break
                        
                    else:
                        pass

                except ValueError as ve:
                    pass
                           
        except psutil.NoSuchProcess:
            pass
    
    #duration = create_duration(activation_time)
    #s1 = pd.Series(current_app, name='Application')
    #s2 = pd.Series(activation_time[:-1], name='Activation_time')
    #s3 = pd.Series(duration, name='Duration')

    #process_info = pd.concat([s1,s2,s3], axis=1)
    
        
    #return process_info

########################################### Mouse Data #########################################################################################

def click_left():

        hold = mouse.get_position()
        coor.add((hold[0],hold[1],1))

def click_right():

        hold = mouse.get_position()
        coor.add((hold[0],hold[1],0))


def get_mouse_dynamics():
        condition = True
        while condition:

                if  len(all_keys.keys()) == 30 and len(all_keys[f'{max(all_keys, key= lambda n: len(all_keys[n]))}']) == 10:
                        condition = False

                mouse.on_click(click_left)   
                mouse.on_right_click(click_right)
                time.sleep(3)




########################################################################################################################################

def mad_score(points):

        """https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm """
        m = np.median(points)
        ad = np.abs(points - m)
        mad = np.median(ad)
        return 0.6745 * ad / mad


def get_minute(data):

        minute = getattr(data,'minute')
        return minute

def collect_data():
        Thread(target = get_keys).start()
        Thread(target = get_process_information).start()
        Thread(target = get_mouse_dynamics).start() 



def protect_system(state):
        global all_keys, clicks, x, y, current_app, pending , activation_time, coor

        m1 = load_model('models/autoencoder1_best_weights.h5') # keys
        m2 = load_model('models/autoencoder2_best_weights.h5') # apps
        m3 = load_model('models/autoencoder3_best_weights.h5') # mouse

        minute = -1
        already_true = 0

        collect_data()

        while state:
                           

                print(f'This is the number of clicks {len(coor)}')
                #print(f'This is the number of mouse x - coor {len(x)}')
                print(f'This is the number of current applications {len(current_app)}')
                print(f'This is the number of applications keys {len(all_keys.keys())}')

                if len(all_keys.values()) != 0:
                        print(len(all_keys[f'{max(all_keys, key= lambda n: len(all_keys[n]))}']))
                        

                time.sleep(3)
                

                if len(all_keys.keys()) >= 30 and len(all_keys[f'{max(all_keys, key= lambda n: len(all_keys[n]))}']) >= 11 and len(coor) >=6  and len(current_app) >= 3:

                        print('I AM HERE')

                        

                        ### Application data #####

                        # creating a dataframe for the applications used
        
                        duration = create_duration(activation_time)
                        s1 = pd.Series(current_app, name='Application')
                        s2 = pd.Series(activation_time[:-1], name='Activation_time')
                        s3 = pd.Series(duration, name='Duration')
                        test_info = pd.concat([s1,s2,s3], axis=1)

                        apps = correct_datatype(test_info)
                        day, hour, minute = extract_time(apps)

                        apps['activation_day'] =  day
                        apps['activation_hour'] = hour
                        apps['activation_minute'] = minute
                        apps.drop('Activation_time', axis=1, inplace=True)


                        scale = joblib.load('models/apps_pipeline.pkl')

                        print(apps)

                        #enc = OneHotEncoder()
                        #pipeline = Pipeline([('normalizer', Normalizer()), ('scaler', MinMaxScaler())])

                        #ct1 = ColumnTransformer([("enc", enc,[0])], remainder="drop")   
                        #ct2 = ColumnTransformer([('scale_pipe', pipeline, slice(1, apps.shape[1]+1))], remainder="drop")

                        #columnTranfomers = FeatureUnion([
                        #('ct1', ct1),
                        #('ct2', ct2)
                        #])

                        #scale = Pipeline([
                        #('ct',columnTranfomers)
                        #])


                        test_apps_scaled = scale.fit_transform(apps)
                        print(test_apps_scaled.shape)
                        columns2 = [f'V{i}' for i in range(1,test_apps_scaled.shape[1] + 1)]
                        test_apps_scaled = pd.DataFrame(test_apps_scaled, columns=columns2) 

                        #.toarray()
                        #print(test_apps_scaled)
                        #print(yes_ooooo)
                        #print(test_apps_scaled.shape)

                        
                        ### keystroke data ###### 

                        keys = pd.DataFrame.from_dict(all_keys, orient='index')
                        keys = keys.transpose()
                        keys = fill_null(keys)
                        print(keys.shape)
                        print(keys)


                        pipeline1 = joblib.load('models/keys_pipeline.pkl')
                        pca = PCA(10) #pickle.load(open("models/keys_pca.pkl",'rb'))

                        keys = pca.fit_transform(keys)
                        columns = [f'V{i}' for i in range(1,keys.shape[1] + 1)]
                        keys = pd.DataFrame(keys,columns = columns)
                        keys = pipeline1.transform(keys)
                        test_keys_scaled = pd.DataFrame(keys, columns=columns)

                        #print(test_keys_scaled)
                        
                        ### mouse data ######
                        for i,j,k in list(coor):

                                x.append(i)
                                y.append(j)
                                clicks.append(k)

                        mouse_coordinates = pd.DataFrame(list(zip(x, y, clicks)),columns = ['x_coordinates', 'y_coordinates', 'clicks'])
                        #mouse_coordinates.drop_duplicates(keep='first', inplace=True)


                        pipeline3 = joblib.load('models/mouse_pipeline.pkl')


                        test_mouse_scaled = pipeline3.fit_transform(mouse_coordinates)
                        columns3 = [f'V{i}' for i in range(1,test_mouse_scaled.shape[1] + 1)]
                        test_mouse_scaled = pd.DataFrame(test_mouse_scaled, columns=columns3)

                        # Authenticate 

                        c1 = m1.predict(test_keys_scaled)
                        c2 = m2.predict(test_apps_scaled)
                        c3 = m3.predict(test_mouse_scaled)

                        mse1 = np.mean(np.power(test_keys_scaled - c1, 2), axis=1)
                        mse2 = np.mean(np.power(test_apps_scaled - c2, 2), axis=1)
                        mse3 = np.mean(np.power(test_mouse_scaled - c3, 2), axis=1)

                        z_scores1 = mad_score(mse1)
                        z_scores2 = mad_score(mse2)
                        z_scores3 = mad_score(mse3)

                        count  = 0
                        THRESHOLD = 3.5

                        outliers1 = z_scores1 > THRESHOLD
                        outliers2 = z_scores2 > THRESHOLD
                        outliers3 = z_scores3 > THRESHOLD


                        for i in outliers1: 
                                if i is True:
                                        count += 1
                                        
                        for i in outliers2: 
                                if i is True:
                                        count += 1
                                
                        for i in outliers3: 
                                if i is True:
                                        count += 1


                        print(len(outliers3))
                        print(len(outliers2))
                        print(len(outliers1))

                        print(count)
                        if count >= 30:
                        
                                ctypes.windll.user32.LockWorkStation()
                        
                                count = 0
                                pending = {}
                                current_app = []
                                activation_time = []
                                x = []
                                y = []
                                clicks = []
                                coor = set()
                                all_keys = defaultdict(list)
                                collect_data()

                        else:
                                # reset
                                all_keys = defaultdict(list)
                                count = 0
                                pending = {}
                                current_app = []
                                activation_time = []
                                x = []
                                y = []
                                clicks = []
                                coor = set()
                                collect_data()

                                print('I GOT HERE FINAL 1 ')

                                if  already_true == 1:
                                        print('I GOT HERE FINAL 2 ')
                                        pass

                                else:
                                        # continuous learning section
                                        state = True
                                        threading.Thread(target=call, args=(f"python run_script2.py {state}" ,), ).start()

                                        already_true = 1

                                        print('I GOT HERE FINAL 3')


                    

                # udate the model
                if minute == 3:

                        #threading.Thread(target=call, args=(f"python learning_script.py {state}" ,), ).start()
                        os.system("python learning_script.py")
                        m1 = load_model('models/autoencoder1_best_weights.h5')
                        m2 = load_model('models/autoencoder2_best_weights.h5')
                        m3 = load_model('models/autoencoder3_best_weights.h5')
                

                date = datetime.now()
                minute = get_minute(date)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--state')
    args, unknown = parser.parse_known_args()
    print(unknown[0])

    protect_system(bool(unknown[0]))