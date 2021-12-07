# ALI

### Adaptive Learning Intelligence (A.L.I):

Adaptive Learning Intelligence( A. L. I) is a security software that works as a continous user authenticator. It works as the second phase for laptop/desktop authentication, the 
first being the passcode authentication phase. A.L.I authenticates users based on soft biometrics (behaviourial metrics) such as keystroke dynamics, mouse dynamics, and desktop
application usage. The learning algorithms (AutoEncoder(s)) are trained on the preprocessed data generated and then put together to detect anomalies when users are interacting with the device.


### Simple User Interface
##### Welcome Screen
![Welcome screen](images/first_screen.png)


##### Collection Screen
![Collection screen](images/collection_screen.png)


##### Train&Protect Screen
![train and protect screen](images/train_n_protect_screen.png)


### Requirements to Run Desktop Application:
1) Use a system running on Windows.
2) To run the application make sure to have the python 3.6.x version.


### How to run application:
1) Clone the repository
2) On the local repository create and activate a virtual enviroment
3) Install the required libraries from the requirements.txt   --> pip install -r requirements.txt 
4) On the cli run: python main.py

### Tools
- Python Programming Language
- PyQT5 & QT designer
- Keras


### Repositority Breakdown:

##### Folders:

- continuous_collection_scripts: This folder contains the scripts that run hourly collecting data.
- data_storage: This folder contains the temporary data collected.
- initial_collection_scripts: This folder contains the scripts that collect data for the specified number of days.
- models :  This folder contains the saved the models after training has been done.
- UI : This folder contains the designs built with QT designer.

##### Scripts:
- main.py: This python file runs the whole application when run from the cli
- learning_script.py: This python file runs the code that processes the data and trains the model.
- protection_script.py: This scripts runs the code that performs period authentication.
- run_script.py : This script runs the scripts that collects the initial data in parallel.
- run_script2.py : This script runs the scripts that continuously collect data in parallel.



### Future Plan:
More updates will be made in other to fix current issues and optimize application flow.





