import os
import argparse
import multiprocessing
import functools
                                                                 

def execute(process):                                                             
    os.system(f'python {process}')
                                                                                                        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--state')
    args, unknown = parser.parse_known_args()
    #args = parser.parse_args()


    all_processes = [f'continuous_collection_scripts/mouse_dynamics.py {bool(unknown[0])}', f'continuous_collection_scripts/desktop_data_collector.py {bool(unknown[0])}', f'continuous_collection_scripts/key_stroke_dynamics.py {bool(unknown[0])}'] 
    

    process_pool = multiprocessing.Pool(processes = len(all_processes))                                                     
    process_pool.map(execute, all_processes)                                                         
        

