import os
import argparse
import multiprocessing
import functools
import pickle
from subprocess import check_output

                                       

def execute(process):                                                             
    os.system(f'python {process}')
                                                                                                        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--state')
    args, unknown = parser.parse_known_args()
    #args = parser.parse_args()
    file_name = "protect.pkl"
    open_file = open(file_name, "wb")
    
    all_processes = [] 

    process = multiprocessing.Process(target=execute, args=(f'protection_script.py {bool(unknown[0])}',))
    process.start()
    print(process.pid)
    all_processes.append(process.pid)

    pickle.dump(all_processes, open_file)
    open_file.close()
    

    #process_pool = multiprocessing.Pool(processes = len(all_processes))                                                     
    #process_pool.map(execute, all_processes)                                                         
        

