import pickle
import json
import numpy as np
import os

#__data_columns = None
__model = None

def predict_sign(video_input):
    
    #df = pd.DataFrame([data],columns = __data_columns)
    #cat_columns = df.select_dtypes(include='object').columns.tolist()
    
    #for c in cat_columns:
    #    df[c] = df[c].astype('category')
    
    #pred = __model.predict(df)
    
    #if pred >= 0.5:
    #    return 'Loan Approved!'
    #else:
    #    return 'Loan Rejected!' 


def load_saved_artifacts():
    print("loading saved artifacts...start")
    #global __data_columns

    path = os.path.dirname(__file__) 
    artifacts = os.path.join(path, "artifacts"),

    #with open(artifacts[0]+"/columns.json", "r") as f:
    #    __data_columns = json.load(f)['data_columns']

    global __model
    if __model is None:
        with open(artifacts[0]+"/loanPickleFileGBM.pkl", 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

#def get_data_columns():
#    return __data_columns

load_saved_artifacts()
