# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 12:37:28 2021

@author: dhamlk
"""

from flask import Flask,request
import pandas as pd
import numpy as np
import pickle
import flasgger
from flasgger import Swagger




app = Flask(__name__)
Swagger(app)

df_aero=pd.read_csv("removals_cox.csv")
with open('survival_cph_pkl' , 'rb') as f:
    lr = pickle.load(f)


@app.route('/')

def welcome():
    return "Welcome To Survival Analysis of Parts"

@app.route('/getprob')

def get_probability():

        
    """Type the part no and the time cycles.
    ---
    parameters:  
      - name: serialno
        in: query
        type: string
        required: true
      - name: timecycles
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
        
    """
    
    serialno=request.args.get('serialno')
    timecycles=int(request.args.get('timecycles'))
    if len(df_aero[df_aero['SERIAL_NUMBER']==serialno]==1):
        part_row_details = df_aero[df_aero['SERIAL_NUMBER']==serialno]
    else:
        part_row_details = df_aero[df_aero['SERIAL_NUMBER']==serialno].iloc[-1]
        
    probability= lr.predict_survival_function(part_row_details).iloc[timecycles].tolist()
    prob = ','.join(str(v) for v in probability)
    return "Probability of part "+str(serialno)+" being removed after "+str(timecycles)+" number of cycles is "+prob+""
    
if __name__=='__main__':
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)