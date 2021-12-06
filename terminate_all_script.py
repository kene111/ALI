import os
import multiprocessing
import functools
                                                                 
                                                                                                        
#if __name__ == "__main__":
    

all_processes = [f'protection_script.py',f'continuous_collection_scripts/mouse_dynamics.py', f'continuous_collection_scripts/desktop_data_collector.py', f'continuous_collection_scripts/key_stroke_dynamics.py'] 

for processes in all_processes:
    print(f'Terminated {processes}.')
    processes.terminate()
