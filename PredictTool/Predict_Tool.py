from GetReplayJSON import GetJSON
from predict_live import PredictLive
import os

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
