from GetReplayJSON import GetJSON
from predict_live import get_prediction
from predict_live import encode_missing_variables
from predict_live import PredictLive
from CompileGamestates import CompileGamestatesToDataframe
import sys
import os
import time

GetJSON('Replays Folder', 'Quadruple Agent')

list_of_files = filter(lambda x: os.path.isfile(os.path.join('Quadruple Agent', x)),
                       os.listdir('Quadruple Agent'))
list_of_files = sorted( list_of_files,
                        key = lambda x: os.path.getmtime(os.path.join('Quadruple Agent', x))
                        )
for file in list_of_files:
    input()
    print(file)
    PredictLive(file)
    filepath = 'Quadruple Agent/' + file
    os.remove(filepath)
