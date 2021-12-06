### PyQt5 imports ########################################################
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication,QWidget,QStackedWidget
from PyQt5.QtCore import QTimer

### Other Imports ########################################################
import os
from os import listdir
import psutil
from datetime import datetime
import datetime as dt
import time
import pickle
from subprocess import call
import threading
import multiprocessing
import sys
import signal
##########################################################################

class UserInterface(QDialog):
    def __init__(self):
        super(UserInterface,self).__init__()
        loadUi("UI/user_interface.ui",self)

        # Get user name
        name = psutil.Process().username()
        if "\\" in name:
            name = name.split('\\')[1]
        self.nameLabel.setText(f"{name}")
        self.next.clicked.connect(self.gotodatacollection)

    def gotodatacollection(self):
        dc = DataCollection()
        widget.addWidget(dc)
        widget.setCurrentIndex(widget.currentIndex()+1)


class DataCollection(QDialog):

    def  __init__(self):
        super(DataCollection, self).__init__()
        loadUi("UI/data_collection.ui",self)
        self.back1.clicked.connect(self.backtouser)
        self.next1.clicked.connect(self.learnNtrain)
        self.run.clicked.connect(self.run_script)

    def backtouser(self):
        interface = UserInterface()
        widget.addWidget(interface)
        widget.setCurrentIndex(widget.currentIndex()-1)

    def learnNtrain(self):
        lt = LearnNTrain()
        widget.addWidget(lt)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.stoptime.setText(f"")
        self.instructionOne.setText("")
        self.instructionTwo.setText("")


    def run_script(self):
        days = self.daysInput.text()
        if days == '':
            self.retry.setText("Please type in a value.")
        else:
            self.daysInput.setText("")
            self.retry.setText("")

            start_date = datetime.now()
            date = datetime.now().strftime("%Y-%m-%d")
            date_1 = datetime.strptime(date, "%Y-%m-%d") # "%Y-%m-%d  %H:%M:%S.%f"
            end_date = date_1 + dt.timedelta(days=int(days))


            self.stoptime.setText(f"This program will stop running on {end_date.strftime('%Y-%m-%d')} midnight.")
            self.instructionOne.setText("When system is not in use do not shut down, only hibernate.")
            self.instructionTwo.setText("When the program is done, wait 2 hours for proper storage.")


            ### disable run button 
            self.run.setStyleSheet("background-color : #e9cdff;border-radius:20px;")
            self.run.setEnabled(False)
            difference = (end_date - start_date).total_seconds() * 1000
            QTimer.singleShot(difference, lambda: self.run.setEnabled(False))

            ### run data collection scripts
            threading.Thread(target=call, args=(f"python run_script.py {int(days)}" ,), ).start()

class LearnNTrain(QDialog):

    def __init__(self):
        super(LearnNTrain, self).__init__()
        loadUi("UI/learn_train.ui",self)
        self.back2.clicked.connect(self.backtodc)
        self.learn.clicked.connect(self.learnpattern)
        self.activate.clicked.connect(self.activatesystem)
        self.deactivate.clicked.connect(self.deactivatesystem)


    def activatesystem(self):
        self.learningprogress1.setText("")  
        state =  True
        threading.Thread(target=call, args=(f"python run_protect.py {state}" ,), ).start()
        time.sleep(6)
        self.label_4.setText("Activated")
        

    def deactivatesystem(self):

        #os.system(f"python terminate_all_script.py")
        #threading.Thread(target=call, args=(f"python terminate_all_script.py" ,), ).start()
        #os._exit(0)
        #os._exit(1)
        open_file_1 = open('protect.pkl', "rb")
        protect_list = pickle.load(open_file_1)
        open_file_1.close()

        #for pid in protect_list:
        #    print(pid)
            #p = psutil.Process(pid)
            #p.terminate() 
        #    os.kill(pid, signal.SIGTERM)
        #   print(f'Terminated {pid}.')

        self.label_4.setText("Deactivated")

        name = os.path.abspath("protection_script.py")
        mypid = protect_list[0]

        for process in psutil.process_iter():
            if process.pid != mypid:
                for path in process.cmdline():
                    if name in path:
                        print("process found")
                        process.terminate()
                        exit()
        #os.remove('protect.pkl')


        
        #pass
        
        
        

    def backtodc(self):
        dc = DataCollection()
        widget.addWidget(dc)
        widget.setCurrentIndex(widget.currentIndex()-1)

    def learnpattern(self):
        num_scripts = len(listdir('data_storage'))

        if num_scripts == 0:
            self.condition.setText("No data generated, it is either this program is still collecting data \n or it has not started collecting data.")

        elif num_scripts < 3:
            self.condition.setText("Please wait, this program is in the process of storing your data.")

        else:

            #self.learningprogress2.setText("Learning ...") 

            os.system("python learning_script.py")  

            self.learningprogress1.setText("Completed. ")






    
# main
app = QApplication(sys.argv)
interface = UserInterface()
widget = QStackedWidget()
widget.setWindowIcon(QtGui.QIcon('ali.ico'))
widget.setWindowTitle('A.L.I')
widget.addWidget(interface)
widget.setFixedHeight(580)
widget.setFixedWidth(826)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print('Exiting ...')