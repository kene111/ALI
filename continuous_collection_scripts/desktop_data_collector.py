from win32gui import GetForegroundWindow
import psutil
import argparse
import time
from collections import defaultdict
import win32process
from datetime import date, datetime
import pandas as pd

def get_minute(data):
    minute = getattr(data,'minute')
    return minute

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

def get_process_information(state):
    
    current_app = []
    activation_time = []
    
    minute = -1

    while state:

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
                        
                        if minute == 0:
                            # add the last running time of application before breaking out of code.
                            a_time = datetime.now()
                            activation_time.append(a_time)
                            state = False
                            break


                        date = datetime.now()
                        minute = get_minute(date)
                        
                    else:
                        pass

                except ValueError as ve:
                    pass
                           
        except psutil.NoSuchProcess:
            pass
    
    duration = create_duration(activation_time)
    s1 = pd.Series(current_app, name='Application')
    s2 = pd.Series(activation_time[:-1], name='Activation_time')
    s3 = pd.Series(duration, name='Duration')

    process_info = pd.concat([s1,s2,s3], axis=1)

    current_app = []
    activation_time = []
    
        
    return process_info


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--state')
    args, unknown = parser.parse_known_args()

    print('Script 2b is running ...')
    processes =  get_process_information(bool(unknown[0]))
    dataframe = handle_datetime(processes)
    dataframe.to_csv('data_storage/application_usage_data.csv',index=False)
    print('Script 2b is done.')