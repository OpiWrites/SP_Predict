from pathlib import Path
import os

from GetReplayJSON import GetJSON
from predict_live import PredictLive

CODE_FOLDER = Path(__file__).parent

REPLAYS_FOLDER = CODE_FOLDER / 'Replays Folder'
QUADRUPLE_AGENT_FOLDER = CODE_FOLDER / 'Quadruple Agent'

if not REPLAYS_FOLDER.exists():
    REPLAYS_FOLDER.mkdir()

if not QUADRUPLE_AGENT_FOLDER.exists():
    QUADRUPLE_AGENT_FOLDER.mkdir()

GetJSON(REPLAYS_FOLDER, QUADRUPLE_AGENT_FOLDER)

list_of_files = filter(lambda x: os.path.isfile(QUADRUPLE_AGENT_FOLDER / x),
                       QUADRUPLE_AGENT_FOLDER.iterdir())
list_of_files = sorted(list_of_files,
                       key=lambda x: os.path.getmtime(QUADRUPLE_AGENT_FOLDER / x)
                       )
for file in list_of_files:
    input()
    print(file)
    PredictLive(file)
    filepath = 'Quadruple Agent/' + file
    os.remove(filepath)
