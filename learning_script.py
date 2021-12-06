print(' TRAINING ...')

import os
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer, MinMaxScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import FeatureUnion
import tensorflow as tf
import pickle
import joblib
from keras.models import load_model



########################### IMPORT DATASETS ###################################################################
mouse = pd.read_csv('data_storage/mouse_data.csv')
all_keys = pd.read_csv('data_storage/all_keys_data.csv')
apps = pd.read_csv('data_storage/application_usage_data.csv')
###############################################################################################################


############################################### PIPELINES & FUNCTIONS ##################################################
# handle null values
def handle_na(data):
    cols = data.columns
    for col in cols:
        if data[col].isnull().sum() == data.shape[0]:
            data.drop(col,axis=1, inplace=True)
            
        else:
            data[col] = data[col].fillna(data[col].mode()[0])
            
    return data


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
    
    year = []
    month = []
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


enc = OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1)

pipeline1 = Pipeline([('normalizer', Normalizer()), ('scaler', MinMaxScaler())])
pipeline2 = Pipeline([('normalizer', Normalizer()), ('scaler', MinMaxScaler())])
pipeline3 = Pipeline([('normalizer', Normalizer()), ('scaler', MinMaxScaler())])

# The last arg ([0]) is the list of columns you want to transform in this step
ct1 = ColumnTransformer([("enc", enc,[0])], remainder="drop")   
ct2 = ColumnTransformer([('scale_pipe', pipeline2, slice(1, apps.shape[1]+1))], remainder="drop")

columnTranfomers = FeatureUnion([
    ('ct1', ct1),
    ('ct2', ct2)
])
#################################################################################################################
   

################################################## CALLING THE FUNCTIONS #########################################

all_keys = handle_na(all_keys)
apps = correct_datatype(apps)
day, hour, minute = extract_time(apps)

apps['activation_day'] =  day
apps['activation_hour'] = hour
apps['activation_minute'] = minute
apps.drop('Activation_time', axis=1, inplace=True)
#################################################################################################################



########################################### KEY STROKE TRAINING ####################################################
# configure our pipeline


pca = PCA(10)

#with open("models/keys_pca", "wb") as f: 
#    pickle.dump(pca, f)

#joblib.dump(pca , 'models/keys_pca.pkl')


all_keys = pca.fit_transform(all_keys) #.iloc[:,:300]
#pickle.dump(pca, open("models/keys_pca.pkl","wb"))

columns = [f'V{i}' for i in range(1,all_keys.shape[1] + 1)]
all_keys = pd.DataFrame(all_keys,columns = columns)
all_keys = pipeline1.fit_transform(all_keys)
all_keys = pd.DataFrame(all_keys, columns=columns)

#save pipeline
joblib.dump(pipeline1, 'models/keys_pipeline.pkl', compress = 1)


class AutoEncoder():
    def __init__(self):
        pass
    
    def create_model(input_dim):
        autoencoder = tf.keras.models.Sequential([
    
        # deconstruct / encode
        tf.keras.layers.Dense(input_dim, activation='elu', input_shape=(input_dim, )), 
        tf.keras.layers.Dense(16, activation='elu'),
        tf.keras.layers.Dense(8, activation='elu'),
        tf.keras.layers.Dense(4, activation='elu'),
        tf.keras.layers.Dense(2, activation='elu'),

        # reconstruction / decode
        tf.keras.layers.Dense(2, activation='elu'),
        tf.keras.layers.Dense(4, activation='elu'),
        tf.keras.layers.Dense(8, activation='elu'),
        tf.keras.layers.Dense(16, activation='elu'),
        tf.keras.layers.Dense(input_dim, activation='elu')

        ])
        
        #self.autoencoder.compile(optimizer="adam", loss="mse",metrics=["acc"])
        
        return autoencoder
                    
# data dimensions // hyperparameters 
input_dim1 = all_keys.shape[1]
BATCH_SIZE = 64
EPOCHS = 60


autoencoder1 = None

if os.path.exists('models/autoencoder1_best_weights.h5'):
    autoencoder1 = load_model('models/autoencoder1_best_weights.h5')
else:
    autoencoder1 = AutoEncoder.create_model(input_dim1)


# https://keras.io/api/models/model_training_apis/
autoencoder1.compile(optimizer="adam", 
                    loss="mse",
                    metrics=["acc"])


save_model = tf.keras.callbacks.ModelCheckpoint(
    filepath='models/autoencoder1_best_weights.h5',
    save_best_only=True,
    monitor='val_loss',
    verbose=0,
    mode='min'
)

log_subdir = 'anomaly1_logs'
tensorboard = tf.keras.callbacks.TensorBoard(
    f'models/logs/{log_subdir}',
    batch_size=BATCH_SIZE,
    update_freq='batch'
)

# callbacks argument only takes a list
cb = [save_model, tensorboard]



autoencoder1.fit(
    all_keys, all_keys,
    shuffle=True,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.1,
    callbacks=cb
);


############################################################### Application Data ###################################################
scale = Pipeline([
    ('ct',columnTranfomers)
    ])
    

train_apps_scaled = scale.fit_transform(apps)
columns2 = [f'V{i}' for i in range(1,train_apps_scaled.shape[1] + 1)]
train_apps_scaled = pd.DataFrame(train_apps_scaled, columns=columns2)


joblib.dump(scale, 'models/apps_pipeline.pkl', compress = 1)


# data dimensions // hyperparameters 
input_dim2 = train_apps_scaled.shape[1]
BATCH_SIZE = 64
EPOCHS = 120

autoencoder2 = None

if os.path.exists('models/autoencoder2_best_weights.h5'):
    autoencoder2 = load_model('models/autoencoder2_best_weights.h5')
else:
    autoencoder2 = AutoEncoder.create_model(input_dim2)

autoencoder2.compile(optimizer="adam", 
                    loss="mse",
                    metrics=["acc"])


save_model2 = tf.keras.callbacks.ModelCheckpoint(
    filepath='models/autoencoder2_best_weights.h5',
    save_best_only=True,
    monitor='val_loss',
    verbose=0,
    mode='min'
)

log_subdir2 = 'anomaly2_logs'

tensorboard2 = tf.keras.callbacks.TensorBoard(
    f'models/logs/{log_subdir2}',
    batch_size=BATCH_SIZE,
    update_freq='batch'
)

# callbacks argument only takes a list
cb2 = [save_model2, tensorboard2]


autoencoder2.fit(
    train_apps_scaled,train_apps_scaled,
    shuffle=True,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.1,
    callbacks=cb2
);


########################################################## Mouse Data ################################################################

train_mouse_scaled = pipeline3.fit_transform(mouse)
columns3 = [f'V{i}' for i in range(1,train_mouse_scaled.shape[1] + 1)]
train_mouse_scaled = pd.DataFrame(train_mouse_scaled, columns=columns3)

joblib.dump(pipeline3, 'models/mouse_pipeline.pkl', compress = 1)

input_dim3 = train_mouse_scaled.shape[1]
BATCH_SIZE = 64
EPOCHS = 90

autoencoder3 = None

if os.path.exists('models/autoencoder3_best_weights.h5'):
    autoencoder3 = load_model('models/autoencoder3_best_weights.h5')
else:
    autoencoder3 = AutoEncoder.create_model(input_dim3)

autoencoder3.compile(optimizer="adam", 
                    loss="mse",
                    metrics=["acc"])


save_model3 = tf.keras.callbacks.ModelCheckpoint(
    filepath='models/autoencoder3_best_weights.h5',
    save_best_only=True,
    monitor='val_loss',
    verbose=0,
    mode='min'
)

log_subdir3 = 'anomaly3_logs'
tensorboard3 = tf.keras.callbacks.TensorBoard(
    f'models/logs/{log_subdir3}',
    batch_size=BATCH_SIZE,
    update_freq='batch'
)

# callbacks argument only takes a list
cb3 = [save_model3, tensorboard3]

autoencoder3.fit(
    train_mouse_scaled,train_mouse_scaled,
    shuffle=True,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.1,
    callbacks=cb3
);

#autoencoder1.save('models/autoencoder1_weights.h5')
#autoencoder2.save('models/autoencoder2_weights.h5')
#autoencoder3.save('models/autoencoder3_weights.h5')



os.remove('data_storage/mouse_data.csv')
os.remove('data_storage/all_keys_data.csv')
os.remove('data_storage/application_usage_data.csv')

print(' DONE. ')