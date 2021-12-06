import os
import argparse
import multiprocessing
import functools
                                                                 

def execute(process):                                                             
    os.system(f'python {process}')
                                                                                                        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--days')
    args, unknown = parser.parse_known_args()
    #args = parser.parse_args()

    #
    
    all_processes = [f'initial_collection_scripts/mouse_dynamics.py {int(unknown[0])}', f'initial_collection_scripts/desktop_data_collector.py {int(unknown[0])}', f'initial_collection_scripts/key_stroke_dynamics.py {int(unknown[0])}'] #
    

    process_pool = multiprocessing.Pool(processes = len(all_processes))                                                        
    process_pool.map(execute, all_processes)                                                         
        



# https://datasciencebeginners.com/2018/10/24/running-python-processes-in-parallel-getting-started/

#The 'freeze_support()' line can be ommited if the program is not going to be frozen to produce an executable