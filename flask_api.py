# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask,request
import pandas as pd
import numpy as np
import pickle
import flasgger
from flasgger import Swagger




app = Flask(__name__)
Swagger(app)
with open('survival_pkl' , 'rb') as f:
    lr = pickle.load(f)


@app.route('/')

def welcome():
    return "Welcome To Survival Analysis of Parts"

@app.route('/getprob')

def get_probability():

        
    """Type the part no and the time cycles.
    ---
    parameters:  
      - name: partno
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
    
    partno=request.args.get('partno')
    timecycles=int(request.args.get('timecycles'))
    probability= lr.survival_function_at_times(timecycles).tolist()
    prob = ','.join(str(v) for v in probability)
    return "Probability of part "+str(partno)+" being removed after "+str(timecycles)+" number of cycles is "+prob+""
    
if __name__=='__main__':
    app.run()
