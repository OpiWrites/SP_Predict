import html
import json
import requests
import os


def GetJSON(directory, json_directory):
    url = 'https://www.spypartydebrief.com/quadruple_agent_json'
    list_of_files = filter(lambda x: os.path.isfile(os.path.join(directory, x)),
                           os.listdir(directory))
    list_of_files = sorted(list_of_files,
                           key=lambda x: os.path.getmtime(os.path.join(directory, x))
                           )
    for iteration, file in enumerate(list_of_files):
        filepath = directory / file
        print(file)
        upload_file = open(filepath, 'rb')
        response = requests.post(url, files={'file': upload_file})
        if response.ok:
            print("Success")
        else:
            print("Oops")
        response_json = response.json()
        venue = response_json['venue']
        spy = response_json['spy']
        timestamp = response_json
        if '/steam' in spy:
            spy = spy[:-6]
        dumpfile = json_directory / ("game" + str(iteration))
        with open(dumpfile, 'w') as outfile:
            json.dump(response_json, outfile)
