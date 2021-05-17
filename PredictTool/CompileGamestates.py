import csv
import json
import pandas as pd
import numpy as np
import os
validvenues = ["Aquarium", "Balcony", "Ballroom", "Courtyard", "Gallery", "High-Rise", "Library", "Moderne",
          "Pub", "Redwoods", "Teien", "Terrace", "Veranda"]
cast_list = ['Ambassador', 'SuspectedDoubleAgent', 'Toby', 'Damon', 'Double Agent']
balc_cast_list = ['Ambassador', 'SuspectedDoubleAgent', 'Toby', 'Damon']
def GetTimeline(file):
    timelineJSON = {'guest_count': None}
    try:
        game = open(file, 'r')
    except:
        print('failed to open file')
        print(file)
    valid = False
    try:
        timelineJSON = json.load(game)
    except:
        print('failed to load game')
        print(file)
    timelineList = []
    if timelineJSON["guest_count"] != None:
        valid = True
        for event in timelineJSON['timeline']:
            timelineList.append(event)
    return valid, timelineList, timelineJSON

def CompileGamestates(directory):
    count = 0
    data_file = open('sparse_data_file.csv', 'a')
    csv_writer = csv.writer(data_file)
    for file in os.listdir(directory):
        filepath = directory + "/" + file
        valid, timelineList, timelineJSON = GetTimeline(filepath)
        if valid == True:
            guest_list = {}
            hl_count = 0
            ll_count = 0
            spy_light = 1
            gamestateCurrent = {'uuid': 0, 'sniper': 0, 'spy': 0, 'result': 0,'venue': 0, 'reqmissions': 0, 'guest_count': 0, 'bug_avail':0,
                                'bug_selected': 0, 'da_avail': 0, 'da_selected': 0, 'swap_avail': 0, 'swap_selected': 0, 'inspect_avail': 0,
                                'inspect_selected': 0, 'seduce_avail': 0, 'seduce_selected': 0, 'purloin_avail': 0, 'purloin_selected': 0,
                                'fp_avail': 0, 'fp_selected': 0, 'micro_avail': 0, 'micro_selected': 0, 'elapsed': 0, 'spytime': 0, 'light': 'neutral', 'lowlights': 0,
                                'highlights': 0, 'flirt': 0, 'flirt_cd': 0, 'bb_count': 0, 'print_count': 0, 'difficult_attempts': 0, 'difficults_succeeded': 0, 'bugs_attempted': 0,
                                'case_prints': 0, 'book_prints':0, 'drink_prints':0, 'statue_prints':0, 'green_bbs':0, 'coughs':0, 'red_timeadds':0, 'green_timeadds':0,
                                'inspects': 0, 'micro_progress': 0, 'green_purloin':0, 'delegate_purloin' :0, 'green_swap':0, 'missions_bug': 0,'since_bug':0, 'missions_da': 0, 'since_da':0,
                                'missions_swap': 0,'since_swap':0, 'missions_inspect': 0, 'since_inspect': 0, 'since_seduce': 0, 'since_purloin': 0, 'since_fp': 0, 'since_micro': 0,
                                'missions_seduce': 0, 'missions_purloin': 0, 'missions_fp': 0, 'missions_micro': 0, 'purloin_pend': 0, 'delegate_avail': 0, 'has_book': 0,
                                'has_drink': 0, 'sips_count':0, 'has_case': 0, 'timeadd_count': 0, 'swap_pend': 0, 'spy_loc': 'elsewhere', 'countdown' : 0, 'countdown_elapsed': 0,
                                'since_bb' : 0, 'since_light': 0, 'since_statue':0, 'since_MFanim':0, 'since_delegate': 0, 'since_print':0, 'since_bugattempt':0, 'since_timeadd':0}
            gamestateCurrent['uuid'] = timelineJSON['uuid']
            gamestateCurrent['venue'] = timelineJSON['venue']
            gamestateCurrent['sniper'] = timelineJSON['sniper']
            gamestateCurrent['spy'] = timelineJSON['spy']
            gamestateCurrent['guest_count'] = timelineJSON['guest_count']                    
            gamestateCurrent['reqmissions'] = timelineJSON['game_type'][1]
            if timelineJSON['win_type'][1] == "SpyWin":
                gamestateCurrent['result'] = 1
            elif timelineJSON['win_type'][1] == 'SniperWin':
                gamestateCurrent['result'] = 0 
            countdown_start = -1
            bug_time = -1
            da_time = -1
            swap_time = -1
            purloin_time = -1 ###Initializes all the "time since" trackers; these variables will be updated to the timestamp a mission is completed at, or when countdown is triggered.
            fp_time = -1
            inspect_time = -1
            micro_time = -1
            seduce_time = -1
            spy_light_change = 0
            light_time = -1
            bb_time = -1
            statue_time = -1
            MFanim_time = -1
            delegate_time = -1
            print_time = -1
            bugattempt_time = -1
            timeadd_time = -1
            red_bb = -1

            
            gamestateList = []
            for event in timelineList:
                gamestateStart = gamestateCurrent
                change_made = 0
                category = 0
                mission = event['mission']
                try:
                    category = event['category'][0]
                except:
                    pass
                if category == 'Cast':
                    Cast(event, guest_list)
                
 
            for event in timelineList:
                gamestateStart = gamestateCurrent
                current_elapsed = event["elapsed_time"]
                current_spytime = event["time"]
                eventstring = event['event']
                time_since_dict = {'countdown':[countdown_start, 'countdown_elapsed'], 'missions_bug':[bug_time,'since_bug'], 'missions_da':[da_time,'since_da'], 'missions_swap':[swap_time,'since_swap'],
                                   'missions_purloin':[purloin_time,'since_purloin'], 'missions_fp':[fp_time, 'since_fp'], 'missions_inspect':[inspect_time, 'since_inspect'],
                                   'missions_seduce':[seduce_time, 'since_seduce'], 'missions_micro': [micro_time, 'since_micro'], 'bb_count':[bb_time, 'since_bb'], spy_light_change: [light_time, 'since_light'],
                                   'inspects': [statue_time, 'since_statue'], 'micro_progress': [MFanim_time, 'since_MFanim'], 'delegate_avail': [delegate_time, 'since_delegate'],
                                   'print_count':[print_time, 'since_print'], 'bugs_attempted' : [bugattempt_time, 'since_bugattempt'], 'timeadd_count': [timeadd_time, 'since_timeadd']}
                for x in time_since_dict:
                    try:
                        if gamestateCurrent[x] > 0:
                            gamestateCurrent[time_since_dict[x][1]] = (event['elapsed_time'] - time_since_dict[x][0])
                    except:
                        pass
                    try:
                        if x > 0:
                            gamestateCurrent[time_since_dict[x][1]] = (event['elapsed_time'] - time_since_dict[x][0])
                    except:
                        pass
                try:
                    prev_elapsed == 0
                except:
                    prev_elapsed = current_elapsed
                try:
                    prev_spytime == 0
                except:
                    prev_spytime = current_spytime
                category = 0
                category2 = 0
                category3 = 0
                mission = event['mission']
                try:
                    category = event['category'][0]
                except:
                    pass
                try:
                    category2 = event['category'][1]
                except:
                    pass
                try:
                    category3 = event['category'][2]
                except:
                    pass
                if category == 'MissionSelected' or category == 'MissionEnabled':
                    gamestateCurrent = MissionInitialize(event, gamestateCurrent, category)
##                for x in range(int(prev_elapsed+1), int(current_elapsed), 5):
##                    gamestateCurrent['elapsed'] = x
##                    gamestateCurrent['spytime'] = int(prev_spytime + 1) - (x - int(prev_elapsed))
##                    if gamestateCurrent['countdown'] == 1:
##                        gamestateCurrent['countdown_elapsed'] = x - countdown_start
##                    gamestateList.append(gamestateCurrent.copy())
                if mission == 'Fingerprint':
                    gamestateCurrent, change_made, fp_time, print_time = FingerprintHandler(event, gamestateCurrent, fp_time, print_time)
                elif mission == 'Bug':
                    gamestateCurrent, change_made, bug_time, bugattempt_time = BugHandler(event, gamestateCurrent, bug_time, bugattempt_time)
                elif mission == 'Inspect':
                    gamestateCurrent, change_made, inspect_time, statue_time = InspectHandler(event, gamestateCurrent, inspect_time, statue_time)
                elif mission == 'Transfer':
                    gamestateCurrent, change_made, micro_time, MFanim_time = TransferHandler(event, gamestateCurrent, micro_time, MFanim_time)
                elif mission == 'Purloin':
                    gamestateCurrent, change_made, purloin_time, delegate_time = PurloinHandler(event, gamestateCurrent, purloin_time, delegate_time)
                elif mission == 'Swap':
                    gamestateCurrent, change_made, swap_time = SwapHandler(event, gamestateCurrent, swap_time)
                elif mission == 'Seduce':
                    gamestateCurrent, change_made, seduce_time = SeduceHandler(event, gamestateCurrent, seduce_time)
                elif mission == 'Contact':
                    gamestateCurrent, change_made, da_time, bb_time, red_bb = ContactHandler(event, gamestateCurrent, da_time, bb_time, red_bb)
                elif category == 'SniperLights':
                    guest_list, gamestateCurrent, change_made, spy_light_change, light_time = SniperLights(event, guest_list, gamestateCurrent, light_time, spy_light_change)
                elif category == 'Conversation' or category == 'Statues':
                    gamestateCurrent, change_made = LocationHandler(event, gamestateCurrent)
                elif category == 'TimeAdd' or category2 == "TimeAdd" or category3 == "TimeAdd":
                    gamestateCurrent, change_made, timeadd_time = TimeaddHandler(event, gamestateCurrent, timeadd_time)
                elif eventstring == 'missions completed. 10 second countdown.':
                    gamestateCurrent['countdown'] = 1
                    countdown_start = event['elapsed_time']
                else:
                    gamestateCurrent, change_made, gamestateList = HoldingHandler(event, gamestateCurrent, gamestateList)
                if change_made == 1:
                    gamestateCurrent['elapsed'] = event['elapsed_time']
                    gamestateCurrent['spytime'] = event['time']
                    
                    gamestateList.append(gamestateCurrent.copy())
                category = []
                prev_elapsed = current_elapsed
                prev_spytime = current_spytime
            for x in gamestateList:
                if count == 0:
                    header = gamestateCurrent.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(x.values())
                
            
                
                
    return


def CompileGamestatesToDataframe(file):
    gamestateList = []

    valid, timelineList, timelineJSON = GetTimeline(file)
    if valid == True:
        guest_list = {}
        hl_count = 0
        ll_count = 0
        spy_light = 1
        gamestateCurrent = {'uuid': 0, 'sniper': 0, 'spy': 0, 'result': 0,'venue': 0, 'reqmissions': 0, 'guest_count': 0, 'bug_avail':0,
                            'bug_selected': 0, 'da_avail': 0, 'da_selected': 0, 'swap_avail': 0, 'swap_selected': 0, 'inspect_avail': 0,
                            'inspect_selected': 0, 'seduce_avail': 0, 'seduce_selected': 0, 'purloin_avail': 0, 'purloin_selected': 0,
                            'fp_avail': 0, 'fp_selected': 0, 'micro_avail': 0, 'micro_selected': 0, 'elapsed': 0, 'spytime': 0, 'light': 'neutral', 'lowlights': 0,
                            'highlights': 0, 'flirt': 0, 'flirt_cd': 0, 'bb_count': 0, 'print_count': 0, 'difficult_attempts': 0, 'difficults_succeeded': 0, 'bugs_attempted': 0,
                            'case_prints': 0, 'book_prints':0, 'drink_prints':0, 'statue_prints':0, 'green_bbs':0, 'coughs':0, 'red_timeadds':0, 'green_timeadds':0,
                            'inspects': 0, 'micro_progress': 0, 'green_purloin':0, 'delegate_purloin' :0, 'green_swap':0, 'missions_bug': 0,'since_bug':0, 'missions_da': 0, 'since_da':0,
                            'missions_swap': 0,'since_swap':0, 'missions_inspect': 0, 'since_inspect': 0, 'since_seduce': 0, 'since_purloin': 0, 'since_fp': 0, 'since_micro': 0,
                            'missions_seduce': 0, 'missions_purloin': 0, 'missions_fp': 0, 'missions_micro': 0, 'purloin_pend': 0, 'delegate_avail': 0, 'has_book': 0,
                            'has_drink': 0, 'sips_count':0, 'has_case': 0, 'timeadd_count': 0, 'swap_pend': 0, 'spy_loc': 'elsewhere', 'countdown' : 0, 'countdown_elapsed': 0,
                            'since_bb' : 0, 'since_light': 0, 'since_statue':0, 'since_MFanim':0, 'since_delegate': 0, 'since_print':0, 'since_bugattempt':0, 'since_timeadd':0}
        gamestateCurrent['uuid'] = timelineJSON['uuid']
        gamestateCurrent['venue'] = timelineJSON['venue']
        gamestateCurrent['sniper'] = timelineJSON['sniper']
        gamestateCurrent['spy'] = timelineJSON['spy']
        gamestateCurrent['guest_count'] = timelineJSON['guest_count']           ###Initialize a base gamestate for the game
        gamestateCurrent['reqmissions'] = timelineJSON['game_type'][1]
        if timelineJSON['win_type'][1] == "SpyWin":
            gamestateCurrent['result'] = 1
        elif timelineJSON['win_type'][1] == 'SniperWin':
            gamestateCurrent['result'] = 0
        countdown_start = -1
        bug_time = -1
        da_time = -1
        swap_time = -1
        purloin_time = -1 ###Initializes all the "time since" trackers; these variables will be updated to the timestamp a mission is completed at, or when countdown is triggered.
        fp_time = -1
        inspect_time = -1
        micro_time = -1
        seduce_time = -1
        spy_light_change = 0
        light_time = -1
        bb_time = -1
        statue_time = -1
        MFanim_time = -1
        delegate_time = -1
        print_time = -1
        bugattempt_time = -1
        timeadd_time = -1
        red_bb = -1

        
        for event in timelineList:
            change_made = 0
            category = 0
            category2 = 0
            category3 = 0
            mission = event['mission']
            try:
                category = event['category'][0]   ###Create a guest list before running through other events; 
            except:                               ###done because sniper lights can sometimes occur before cast initializes  
                pass
            if category == 'Cast':
                Cast(event, guest_list)
            try:
                category2 = event['category'][1]
            except:
                pass
            try:
                category3 = event['category'][2]
            except:
                pass
        for event in timelineList: ###Iterate through the timeline, updating gamestate on each event that requires it; if it requires it, save the updated gamestate to a list
            current_elapsed = event["elapsed_time"]
            current_spytime = event["time"]
            eventstring = event['event']
            time_since_dict = {'countdown':[countdown_start, 'countdown_elapsed'], 'missions_bug':[bug_time,'since_bug'], 'missions_da':[da_time,'since_da'], 'missions_swap':[swap_time,'since_swap'],
                               'missions_purloin':[purloin_time,'since_purloin'], 'missions_fp':[fp_time, 'since_fp'], 'missions_inspect':[inspect_time, 'since_inspect'],
                               'missions_seduce':[seduce_time, 'since_seduce'], 'missions_micro': [micro_time, 'since_micro'], 'bb_count':[bb_time, 'since_bb'], spy_light_change: [light_time, 'since_light'],
                               'inspects': [statue_time, 'since_statue'], 'micro_progress': [MFanim_time, 'since_MFanim'], 'delegate_avail': [delegate_time, 'since_delegate'],
                               'print_count':[print_time, 'since_print'], 'bugs_attempted' : [bugattempt_time, 'since_bugattempt'], 'timeadd_count': [timeadd_time, 'since_timeadd']}
            for x in time_since_dict:
                try:
                    if gamestateCurrent[x] > 0:
                        gamestateCurrent[time_since_dict[x][1]] = (event['elapsed_time'] - time_since_dict[x][0])
                except:
                    pass
                try:
                    if x > 0:
                        gamestateCurrent[time_since_dict[x][1]] = (event['elapsed_time'] - time_since_dict[x][0])
                except:
                    pass
            try:
                prev_elapsed == 0
            except:
                prev_elapsed = current_elapsed ##Funky weirdness to make interval gamestates possible. See below.
            try:
                prev_spytime == 0
            except:
                prev_spytime = current_spytime
            category = 0
            mission = event['mission']
            try:
                category = event['category'][0]
            except:
                pass
            if category == 'MissionSelected' or category == 'MissionEnabled':
                gamestateCurrent = MissionInitialize(event, gamestateCurrent, category)
            try:
                category2 = event['category'][1]
            except:
                pass
            try:
                category3 = event['category'][2]
            except:
                pass
            for x in range(int(prev_elapsed+1), int(current_elapsed), 1): 
                gamestateCurrent['elapsed'] = x
                gamestateCurrent['spytime'] = int(prev_spytime + 1) - (x - int(prev_elapsed)) ###Creates extra gamestate copies at set intervals between events for smoother gamestate structure over 1 game.
                for y in time_since_dict:                                                       ###Usually used for smoothing casting prediction values, using it for training causes overfitting
                    try:
                        if gamestateCurrent[y] > 0:
                            gamestateCurrent[time_since_dict[y][1]] = (x - time_since_dict[y][0])
                    except:
                        pass
                    try:
                        if y > 0:
                            gamestateCurrent[time_since_dict[y][1]] = (x - time_since_dict[y][0])
                    except:
                        pass
                gamestateList.append(gamestateCurrent.copy())

            if mission == 'Fingerprint':
                gamestateCurrent, change_made, fp_time, print_time = FingerprintHandler(event, gamestateCurrent, fp_time, print_time)
            elif mission == 'Bug':
                gamestateCurrent, change_made, bug_time, bugattempt_time = BugHandler(event, gamestateCurrent, bug_time, bugattempt_time)
            elif mission == 'Inspect':
                gamestateCurrent, change_made, inspect_time, statue_time = InspectHandler(event, gamestateCurrent, inspect_time, statue_time)
            elif mission == 'Transfer':
                gamestateCurrent, change_made, micro_time, MFanim_time = TransferHandler(event, gamestateCurrent, micro_time, MFanim_time)
            elif mission == 'Purloin':
                gamestateCurrent, change_made, purloin_time, delegate_time = PurloinHandler(event, gamestateCurrent, purloin_time, delegate_time)
            elif mission == 'Swap':
                gamestateCurrent, change_made, swap_time = SwapHandler(event, gamestateCurrent, swap_time)
            elif mission == 'Seduce':
                gamestateCurrent, change_made, seduce_time = SeduceHandler(event, gamestateCurrent, seduce_time)
            elif mission == 'Contact':
                gamestateCurrent, change_made, da_time, bb_time, red_bb = ContactHandler(event, gamestateCurrent, da_time, bb_time, red_bb)
            elif category == 'SniperLights':
                guest_list, gamestateCurrent, change_made, spy_light_change, light_time = SniperLights(event, guest_list, gamestateCurrent, light_time, spy_light_change)
            elif category == 'Conversation' or category == 'Statues':
                gamestateCurrent, change_made = LocationHandler(event, gamestateCurrent)
            elif category == 'TimeAdd' or category2 == 'TimeAdd' or category3 == 'TimeAdd':
                gamestateCurrent, change_made, timeadd_time = TimeaddHandler(event, gamestateCurrent, timeadd_time)
            elif eventstring == 'missions completed. 10 second countdown.':
                gamestateCurrent['countdown'] = 1
                countdown_start = event['elapsed_time']
            else:
                gamestateCurrent, change_made, gamestateList = HoldingHandler(event, gamestateCurrent, gamestateList)
                
            if change_made == 1:
                gamestateCurrent['elapsed'] = event['elapsed_time']
                gamestateCurrent['spytime'] = event['time']       ###This is where we add a gamestate to the list if there's been a copy.
                gamestateList.append(gamestateCurrent.copy())
            category = []
            prev_elapsed = current_elapsed
            prev_spytime = current_spytime
        gamestateList.append(gamestateCurrent.copy())
    gamestates = pd.DataFrame(gamestateList) ###When compiling gamestates, this will append the list to a file. For casting purposes, this sends it straight to a dataframe.
    return gamestates



def CompileFinalGamestates(directory):
    gamestateList = []
    for file in os.listdir(directory):
        filepath = directory + "/" + file
        valid, timelineList, timelineJSON = GetTimeline(filepath)
        if valid == True:
            guest_list = {}
            hl_count = 0
            ll_count = 0
            spy_light = 1
            gamestateCurrent = {'uuid': 0, 'sniper': 0, 'spy': 0, 'result': 0,'venue': 0, 'reqmissions': 0, 'guest_count': 0, 'bug_avail':0,
                                'bug_selected': 0, 'da_avail': 0, 'da_selected': 0, 'swap_avail': 0, 'swap_selected': 0, 'inspect_avail': 0,
                                'inspect_selected': 0, 'seduce_avail': 0, 'seduce_selected': 0, 'purloin_avail': 0, 'purloin_selected': 0,
                                'fp_avail': 0, 'fp_selected': 0, 'micro_avail': 0, 'micro_selected': 0, 'elapsed': 0, 'spytime': 0, 'light': 'neutral', 'lowlights': 0,
                                'highlights': 0, 'flirt': 0, 'flirt_cd': 0, 'bb_count': 0, 'print_count': 0, 'difficult_attempts': 0, 'difficults_succeeded': 0, 'bugs_attempted': 0,
                                'case_prints': 0, 'book_prints':0, 'drink_prints':0, 'statue_prints':0, 'green_bbs':0, 'coughs':0, 'red_timeadds':0, 'green_timeadds':0,
                                'inspects': 0, 'micro_progress': 0, 'green_purloin':0, 'delegate_purloin' :0, 'green_swap':0, 'missions_bug': 0,'since_bug':0, 'missions_da': 0, 'since_da':0,
                                'missions_swap': 0,'since_swap':0, 'missions_inspect': 0, 'since_inspect': 0, 'since_seduce': 0, 'since_purloin': 0, 'since_fp': 0, 'since_micro': 0,
                                'missions_seduce': 0, 'missions_purloin': 0, 'missions_fp': 0, 'missions_micro': 0, 'purloin_pend': 0, 'delegate_avail': 0, 'has_book': 0,
                                'has_drink': 0, 'sips_count':0, 'has_case': 0, 'timeadd_count': 0, 'swap_pend': 0, 'spy_loc': 'elsewhere', 'countdown' : 0, 'countdown_elapsed': 0,
                                'since_bb' : 0, 'since_light': 0, 'since_statue':0, 'since_MFanim':0, 'since_delegate': 0, 'since_print':0, 'since_bugattempt':0, 'since_timeadd':0}
            gamestateCurrent['uuid'] = timelineJSON['uuid']
            gamestateCurrent['venue'] = timelineJSON['venue']
            gamestateCurrent['sniper'] = timelineJSON['sniper']
            gamestateCurrent['spy'] = timelineJSON['spy']
            gamestateCurrent['guest_count'] = timelineJSON['guest_count']           ###Initialize a base gamestate for the game
            gamestateCurrent['reqmissions'] = timelineJSON['game_type'][1]
            if timelineJSON['win_type'][1] == "SpyWin":
                gamestateCurrent['result'] = 1
            elif timelineJSON['win_type'][1] == 'SniperWin':
                gamestateCurrent['result'] = 0
            countdown_start = -1
            bug_time = -1
            da_time = -1
            swap_time = -1
            purloin_time = -1 ###Initializes all the "time since" trackers; these variables will be updated to the timestamp a mission is completed at, or when countdown is triggered.
            fp_time = -1
            inspect_time = -1
            micro_time = -1
            seduce_time = -1
            spy_light_change = 0
            light_time = -1
            bb_time = -1
            statue_time = -1
            MFanim_time = -1
            delegate_time = -1
            print_time = -1
            bugattempt_time = -1
            timeadd_time = -1
            red_bb = -1

            
            for event in timelineList:
                change_made = 0
                category = 0
                category2 = 0
                category3 = 0
                mission = event['mission']
                try:
                    category = event['category'][0]   ###Create a guest list before running through other events; 
                except:                               ###done because sniper lights can sometimes occur before cast initializes  
                    pass
                if category == 'Cast':
                    Cast(event, guest_list)
                try:
                    category2 = event['category'][1]
                except:
                    pass
                try:
                    category3 = event['category'][2]
                except:
                    pass
            for event in timelineList: ###Iterate through the timeline, updating gamestate on each event that requires it; if it requires it, save the updated gamestate to a list
                current_elapsed = event["elapsed_time"]
                current_spytime = event["time"]
                eventstring = event['event']
                time_since_dict = {'countdown':[countdown_start, 'countdown_elapsed'], 'missions_bug':[bug_time,'since_bug'], 'missions_da':[da_time,'since_da'], 'missions_swap':[swap_time,'since_swap'],
                                   'missions_purloin':[purloin_time,'since_purloin'], 'missions_fp':[fp_time, 'since_fp'], 'missions_inspect':[inspect_time, 'since_inspect'],
                                   'missions_seduce':[seduce_time, 'since_seduce'], 'missions_micro': [micro_time, 'since_micro'], 'bb_count':[bb_time, 'since_bb'], spy_light_change: [light_time, 'since_light'],
                                   'inspects': [statue_time, 'since_statue'], 'micro_progress': [MFanim_time, 'since_MFanim'], 'delegate_avail': [delegate_time, 'since_delegate'],
                                   'print_count':[print_time, 'since_print'], 'bugs_attempted' : [bugattempt_time, 'since_bugattempt'], 'timeadd_count': [timeadd_time, 'since_timeadd']}
                for x in time_since_dict:
                    try:
                        if gamestateCurrent[x] > 0:
                            gamestateCurrent[time_since_dict[x][1]] = (event['elapsed_time'] - time_since_dict[x][0])
                    except:
                        pass
                    try:
                        if x > 0:
                            gamestateCurrent[time_since_dict[x][1]] = (event['elapsed_time'] - time_since_dict[x][0])
                    except:
                        pass
                try:
                    prev_elapsed == 0
                except:
                    prev_elapsed = current_elapsed ##Funky weirdness to make interval gamestates possible. See below.
                try:
                    prev_spytime == 0
                except:
                    prev_spytime = current_spytime
                category = 0
                mission = event['mission']
                try:
                    category = event['category'][0]
                except:
                    pass
                if category == 'MissionSelected' or category == 'MissionEnabled':
                    gamestateCurrent = MissionInitialize(event, gamestateCurrent, category)
                try:
                    category2 = event['category'][1]
                except:
                    pass
                try:
                    category3 = event['category'][2]
                except:
                    pass
                for x in range(int(prev_elapsed+1), int(current_elapsed), 1): 
                    gamestateCurrent['elapsed'] = x
                    gamestateCurrent['spytime'] = int(prev_spytime + 1) - (x - int(prev_elapsed)) ###Creates extra gamestate copies at set intervals between events for smoother gamestate structure over 1 game.
                    for y in time_since_dict:                                                       ###Usually used for smoothing casting prediction values, using it for training causes overfitting
                        try:
                            if gamestateCurrent[y] > 0:
                                gamestateCurrent[time_since_dict[y][1]] = (x - time_since_dict[y][0])
                        except:
                            pass
                        try:
                            if y > 0:
                                gamestateCurrent[time_since_dict[y][1]] = (x - time_since_dict[y][0])
                        except:
                            pass
                    #gamestateList.append(gamestateCurrent.copy())

                if mission == 'Fingerprint':
                    gamestateCurrent, change_made, fp_time, print_time = FingerprintHandler(event, gamestateCurrent, fp_time, print_time)
                elif mission == 'Bug':
                    gamestateCurrent, change_made, bug_time, bugattempt_time = BugHandler(event, gamestateCurrent, bug_time, bugattempt_time)
                elif mission == 'Inspect':
                    gamestateCurrent, change_made, inspect_time, statue_time = InspectHandler(event, gamestateCurrent, inspect_time, statue_time)
                elif mission == 'Transfer':
                    gamestateCurrent, change_made, micro_time, MFanim_time = TransferHandler(event, gamestateCurrent, micro_time, MFanim_time)
                elif mission == 'Purloin':
                    gamestateCurrent, change_made, purloin_time, delegate_time = PurloinHandler(event, gamestateCurrent, purloin_time, delegate_time)
                elif mission == 'Swap':
                    gamestateCurrent, change_made, swap_time = SwapHandler(event, gamestateCurrent, swap_time)
                elif mission == 'Seduce':
                    gamestateCurrent, change_made, seduce_time = SeduceHandler(event, gamestateCurrent, seduce_time)
                elif mission == 'Contact':
                    gamestateCurrent, change_made, da_time, bb_time, red_bb = ContactHandler(event, gamestateCurrent, da_time, bb_time, red_bb)
                elif category == 'SniperLights':
                    guest_list, gamestateCurrent, change_made, spy_light_change, light_time = SniperLights(event, guest_list, gamestateCurrent, light_time, spy_light_change)
                elif category == 'Conversation' or category == 'Statues':
                    gamestateCurrent, change_made = LocationHandler(event, gamestateCurrent)
                elif category == 'TimeAdd' or category2 == 'TimeAdd' or category3 == 'TimeAdd':
                    gamestateCurrent, change_made, timeadd_time = TimeaddHandler(event, gamestateCurrent, timeadd_time)
                elif eventstring == 'missions completed. 10 second countdown.':
                    gamestateCurrent['countdown'] = 1
                    countdown_start = event['elapsed_time']
                else:
                    gamestateCurrent, change_made, gamestateList = HoldingHandler(event, gamestateCurrent, gamestateList)
                    
                #if change_made == 1:
                    #gamestateCurrent['elapsed'] = event['elapsed_time']
                    #gamestateCurrent['spytime'] = event['time']       ###This is where we add a gamestate to the list if there's been a copy.
                    #gamestateList.append(gamestateCurrent.copy())
                category = []
                prev_elapsed = current_elapsed
                prev_spytime = current_spytime
            gamestateList.append(gamestateCurrent.copy())
    gamestates = pd.DataFrame(gamestateList) ###When compiling gamestates, this will append the list to a file. For casting purposes, this sends it straight to a dataframe.
    return gamestates

def TimeaddHandler(event, gamestate, timeadd_time):
    eventstring = event['event']
    change_made = 1
    timeadd_count = gamestate['timeadd_count']
    green_timeadds = gamestate['green_timeadds']
    red_timeadds = gamestate['red_timeadds']
    if eventstring == "45 seconds added to match.":
        timeadd_count += 1
    elif eventstring == "action test green: check watch":
        green_timeadds += 1
    elif eventstring == "action test red: check watch":
        red_timeadds += 1
    else:
        change_made = 0
    gamestate['timeadd_count'] = timeadd_count
    gamestate['green_timeadds'] = green_timeadds
    gamestate['red_timeadds'] = red_timeadds 
    return gamestate, change_made, timeadd_time

def HoldingHandler(event, gamestate, gamestateList):
    eventstring = event['event']
    change_made = 1
    has_case = gamestate['has_case']
    has_book = gamestate['has_book']
    has_drink = gamestate['has_drink']
    sips = gamestate['sips_count']
    got_drink = ["got cupcake from waiter.", "got drink from waiter.", "got drink from bartender.", "got cupcake from bartender."]
    finished_drink = ["took last sip of drink.", "gulped drink.", "chomped cupcake.","took last bite of cupcake."]
    sipped_drink = ["sipped drink.", "bit cupcake."]
    BCpickup = ["spy picks up briefcase.", "picked up fingerprintable briefcase.", "picked up fingerprintable briefcase (difficult)."]
    BCputdown = ["spy puts down briefcase.", "spy returns briefcase."]
    if eventstring in finished_drink:
        if has_drink == 0:
            for x in gamestateList:
                x['has_drink'] = 1
                x['sips_count'] = 1
        elif has_drink == 1:
            has_drink = 0
            sips = 0
    elif eventstring in got_drink:
        has_drink = 1
        sips = 3
    elif eventstring in sipped_drink:
        sips -= 1
    elif eventstring == "get book from bookcase.":
        has_book = 1
    elif eventstring == "put book in bookcase.":
        has_book = 0
    elif eventstring in BCpickup:
        has_case = 1
    elif eventstring in BCputdown:
        has_case = 0
    else:
        change_made = 0
    gamestate['has_drink'] = has_drink
    gamestate['has_book'] = has_book
    gamestate['has_case'] = has_case
    gamestate['sips_count'] = sips
    return gamestate, change_made, gamestateList
def LocationHandler(event, gamestate):
    eventstring = event['event']
    change_made = 1
    spy_loc = gamestate['spy_loc']
    spyjoin = ["spy enters conversation.", "spy joined conversation with double agent."]
    spyleave = ["spy leaves conversation.", "spy left conversation with double agent."]
    spystatue = ["picked up statue.","picked up fingerprintable statue (difficult).", "picked up fingerprintable statue."]
    spy_putdown = ["put back statue.", "dropped statue."]
    if eventstring in spyjoin:
        spy_loc = 'conversation'
    elif eventstring in spyleave:
        spy_loc = 'elsewhere'
    elif eventstring in spystatue:
        spy_loc = 'statue'
    elif eventstring in spy_putdown:
        spy_loc = 'elsewhere'
    else:
        change_made = 0
    gamestate['spy_loc'] = spy_loc
    return gamestate, change_made
def ContactHandler(event, gamestate, da_time, bb_time, red_bb):
    eventstring = event['event']
    change_made = 1
    bb_count = gamestate['bb_count']
    green_bbs = gamestate['green_bbs']
    coughs = gamestate['coughs']
    contact_bool = gamestate['missions_da']
    countlist = ["banana bread uttered.", "fake banana bread uttered."]
    if eventstring in countlist:
        bb_count += 1
        bb_time = event['elapsed_time']
        if red_bb == 1:
            coughs += 1
            red_bb = 0
    elif eventstring == "double agent contacted.":
        contact_bool = 1
        da_time = event['elapsed_time']
    elif eventstring == "action test green: contact double agent":
        green_bbs += 1
    elif eventstring == "banana bread aborted.":
        coughs += 1
    elif eventstring == "action test red: contact double agent":
        red_bb = 1
    else:
        change_made = 0
    gamestate['bb_count'] = bb_count
    gamestate['missions_da'] = contact_bool
    gamestate['green_bbs'] = green_bbs 
    gamestate['coughs'] = coughs
    return gamestate, change_made, da_time, bb_time, red_bb

def SwapHandler(event, gamestate, swap_time):
    eventstring = event['event']
    change_made = 1
    swap_pend = gamestate['swap_pend']
    swap_bool = gamestate['missions_swap']
    green_swap = gamestate['green_swap']
    if eventstring == "statue swap pending.":
        swap_pend = 1
    elif eventstring == "statue swapped.":
        if swap_pend == 1:
            green_swap = 1
            swap_pend = 0
        swap_bool = 1
        swap_time = event['elapsed_time']
    else:
        change_made = 0
    gamestate['swap_pend'] = swap_pend
    gamestate['missions_swap'] = swap_bool
    gamestate['green_swap'] = green_swap
    return gamestate, change_made, swap_time
def PurloinHandler(event, gamestate, purloin_time, delegate_time):
    eventstring = event['event']
    change_made = 1
    purloin_pend = gamestate['purloin_pend']
    delegate_avail = gamestate['delegate_avail']
    purloin_bool = gamestate['missions_purloin']
    green_purloin = gamestate['green_purloin']
    delegate_purloin = gamestate['delegate_purloin']
    delegate_venues = ["Aquarium", "Moderne", "Pub", "Redwoods", "Terrace"]

    if 'delegated purloin to' in eventstring or eventstring == "guest list purloin pending.":
        purloin_pend = 1
        delegate_avail = 0
    elif eventstring == "guest list purloined.":
        if purloin_pend == 1:
            if gamestate['venue'] in delegate_venues:
                delegate_purloin = 1
            else:
                green_purloin = 1
            purloin_pend = 0
        purloin_bool = 1
        purloin_time = event['elapsed_time']
    elif eventstring == "delegating purloin guest list.":
        delegate_avail = 1
        delegate_time = event['elapsed_time']
    elif eventstring == "delegated purloin timer expired.":
        delegate_avail = 0
        purloin_pend = 0
    else:
        change_made = 0
    gamestate['purloin_pend'] = purloin_pend
    gamestate['delegate_avail'] = delegate_avail
    gamestate['missions_purloin'] = purloin_bool
    gamestate['green_purloin'] = green_purloin
    gamestate['delegate_purloin'] = delegate_purloin
    return gamestate, change_made, purloin_time, delegate_time

def SeduceHandler(event, gamestate, seduce_time):
    eventstring = event['event']
    change_made = 1
    seduce_progress = gamestate['flirt']
    seduce_cd = gamestate['flirt_cd']
    seduce_bool = gamestate['missions_seduce']
    if "flirt with seduction target:" in eventstring:
        flirtvalue = str(eventstring[-3:-1])
        if flirtvalue != '00':
            seduce_progress = int(flirtvalue)
            seduce_cd = 1
        else:
            change_made = 0
    elif eventstring == "flirtation cooldown expired.":
        seduce_cd = 0
    elif eventstring == "target seduced.":
        seduce_bool = 1
        seduce_progress = 100
        seduce_time = event['elapsed_time']
    else:
        change_made = 0
    gamestate['flirt'] = seduce_progress
    gamestate['flirt_cd'] = seduce_cd
    gamestate['missions_seduce'] = seduce_bool
    return gamestate, change_made, seduce_time
def TransferHandler(event, gamestate, micro_time, MFanim_time):
    eventstring = event['event']
    change_made = 1
    micro_progress = gamestate['micro_progress']
    micro_bool = gamestate['missions_micro']
    prog_strings = ["hide microfilm in book.", "remove microfilm from book."]
    if eventstring in prog_strings:
        if micro_progress <= 3:
            micro_progress += 1
        else:
            change_made = 0
        MFanim_time = event['elapsed_time']
    elif eventstring == "transferred microfilm.":
        micro_bool = 1
        micro_time = event["elapsed_time"]
    else:
        change_made = 0
    gamestate['micro_progress'] = micro_progress
    gamestate['missions_micro'] = micro_bool
    return gamestate, change_made, micro_time, MFanim_time
def InspectHandler(event, gamestate, inspect_time, statue_time):
    eventstring = event['event']
    change_made = 1
    inspect_count = gamestate['inspects']
    inspect_bool = gamestate['missions_inspect']
    inspect_complete_strings = ["held statue inspected.", "left statue inspected.", "right statue inspected."]
    if eventstring in inspect_complete_strings:
        inspect_count += 1
        statue_time = event['elapsed_time']
    elif eventstring == "all statues inspected.":
        inspect_bool = 1
        inspect_time = event['elapsed_time']
    else:
        change_made = 0
    gamestate['inspects'] = inspect_count
    gamestate['missions_inspect'] = inspect_bool
    return gamestate, change_made, inspect_time, statue_time
def BugHandler(event, gamestate, bug_time, bugattempt_time):
    eventstring = event['event']
    change_made = 1
    bug_attempts = gamestate['bugs_attempted']
    bug_bool = gamestate['missions_bug']
    bug_complete_strings = ["bugged ambassador while standing.", "bugged ambassador while walking."]
    if eventstring == "action triggered: bug ambassador":
        bug_attempts += 1
        bugattempt_time = event['elapsed_time']
    elif eventstring in bug_complete_strings:
        bug_bool = 1
        bug_time = event['elapsed_time']
    else:
        change_made = 0
    gamestate['bugs_attempted'] = bug_attempts
    gamestate['missions_bug'] = bug_bool
    return gamestate, change_made, bug_time, bugattempt_time
        

def FingerprintHandler(event, gamestate, fp_time, print_time):
    eventstring = event['event']
    change_made = 1
    print_count = gamestate['print_count']
    print_bool = gamestate['missions_fp']
    diff_attempts = gamestate['difficult_attempts']
    diffs_succeeded = gamestate['difficults_succeeded']
    book_prints = gamestate['book_prints']
    case_prints = gamestate['case_prints']
    drink_prints = gamestate['drink_prints']
    statue_prints = gamestate['statue_prints']
    print_success_strings = ["fingerprinted book.", "fingerprinted briefcase.", "fingerprinted drink.", "fingerprinted cupcake.", "fingerprinted statue."]
    if eventstring == 'action test green: fingerprint ambassador':
        diff_attempts += 1
        diffs_succeeded += 1
    elif eventstring == 'action test ignored: fingerprint ambassador' or eventstring == 'action test red: fingerprint ambassador':
        diff_attempts += 1
    elif eventstring in print_success_strings:
        print_count += 1
        print_time = event['elapsed_time']
        if eventstring == "fingerprinted book.":
            book_prints += 1
        elif eventstring == "fingerprinted briefcase.":
            case_prints += 1
        elif eventstring == "fingerprinted drink." or eventstring == "fingerprinted cupcake.":
            drink_prints += 1
        elif eventstring == "fingerprinted statue.":
            statue_prints += 1
    elif eventstring == "fingerprinted ambassador.":
        print_bool = 1
        fp_time = event['elapsed_time']
    else:
        change_made = 0
    gamestate['print_count'] = print_count
    gamestate['missions_fp'] = print_bool
    gamestate['difficult_attempts'] = diff_attempts
    gamestate['difficults_succeeded'] = diffs_succeeded
    gamestate['book_prints'] = book_prints
    gamestate['case_prints'] = case_prints 
    gamestate['drink_prints'] = drink_prints
    gamestate['statue_prints'] = statue_prints
    return gamestate, change_made, fp_time, print_time
def MissionInitialize(event, gamestate, category):
    missions_dict = {'Bug':['bug_avail', 'bug_selected'], 'Contact': ['da_avail', 'da_selected'], 'Swap': ['swap_avail', 'swap_selected'],
                     'Inspect':['inspect_avail', 'inspect_selected'], 'Seduce':['seduce_avail', 'seduce_selected'], 'Purloin':['purloin_avail', 'purloin_selected'],
                     'Fingerprint':['fp_avail','fp_selected'], 'Transfer':['micro_avail', 'micro_selected']}
    mission = event['mission']
    if category == 'MissionSelected':
        gamestateindex = missions_dict[mission][1]
        gamestate[gamestateindex] = 1
    elif category == 'MissionEnabled':
        gamestateindex = missions_dict[mission][0]
        gamestate[gamestateindex] = 1
    return gamestate

def SniperLights(event, guest_list, gamestate, light_time, spy_light_change):
    cast_name = event['cast_name'][0]
    eventstring = event['event']
    hl_count = gamestate['highlights']
    ll_count = gamestate['lowlights']
    spy_light = gamestate['light']
    venue = gamestate['venue']
    change_made = 1
    if venue != 'Balcony':
        if event['role'][0] not in cast_list and cast_name not in cast_list:
            prev_light = guest_list[cast_name][1]
            if eventstring == 'marked suspicious.':
                if prev_light == 1:
                    hl_count += 1
                elif prev_light == 0:
                    ll_count -= 1
                    hl_count += 1
                guest_list[cast_name][1] = 2
            elif eventstring == 'marked spy suspicious.':
                if prev_light == 1:
                    hl_count += 1
                elif prev_light == 0:
                    ll_count -= 1
                    hl_count += 1
                guest_list[cast_name][1] = 2
                spy_light = 'highlight'
                spy_light_change = 1
                light_time = event['elapsed_time']
            elif eventstring == 'marked neutral suspicion.':
                if prev_light == 2:
                    hl_count -= 1
                elif prev_light == 0:
                    ll_count -= 1
                guest_list[cast_name][1] = 1
            elif eventstring == 'marked spy neutral suspicion.':
                if prev_light == 2:
                    hl_count -= 1
                elif prev_light == 0:
                   ll_count -= 1
                guest_list[cast_name][1] = 1
                spy_light = 'neutral'
                spy_light_change = 1
                light_time = event['elapsed_time']
            elif eventstring == 'marked less suspicious.':
                if prev_light == 2:
                    hl_count -= 1
                    ll_count += 1
                elif prev_light == 1:
                    ll_count += 1
                guest_list[cast_name][1] = 0
            elif eventstring == 'marked spy less suspicious.':
                if prev_light == 2:
                    hl_count -= 1
                    ll_count += 1
                elif prev_light == 1:
                    ll_count += 1
                guest_list[cast_name][1] = 0
                spy_light = 'lowlight'
                spy_light_change = 1
                light_time = event['elapsed_time']
            else:
                change_made = 0
        elif venue == 'Balcony':
            if event['role'][0] not in balc_cast_list and cast_name not in cast_list:
                prev_light = guest_list[cast_name][1]
                if eventstring == 'marked suspicious.':
                    if prev_light == 1:
                        hl_count += 1
                    elif prev_light == 0:
                        ll_count -= 1
                        hl_count += 1
                    guest_list[cast_name][1] = 2
                elif eventstring == 'marked spy suspicious.':
                    if prev_light == 1:
                        hl_count += 1
                    elif prev_light == 0:
                        ll_count -= 1
                        hl_count += 1
                    guest_list[cast_name][1] = 2
                    spy_light = 'highlight'
                    spy_light_change = 1
                    light_time = event['elapsed_time']
                elif eventstring == 'marked neutral suspicion.':
                    if prev_light == 2:
                        hl_count -= 1
                    elif prev_light == 0:
                        ll_count -= 1
                    guest_list[cast_name][1] = 1
                elif eventstring == 'marked spy neutral suspicion.':
                    if prev_light == 2:
                        hl_count -= 1
                    elif prev_light == 0:
                       ll_count -= 1
                    guest_list[cast_name][1] = 1
                    spy_light = 'neutral'
                    spy_light_change = 1
                    light_time = event['elapsed_time']
                elif eventstring == 'marked less suspicious.':
                    if prev_light == 2:
                        hl_count -= 1
                        ll_count += 1
                    elif prev_light == 1:
                        ll_count += 1
                    guest_list[cast_name][1] = 0
                elif eventstring == 'marked spy less suspicious.':
                    if prev_light == 2:
                        hl_count -= 1
                        ll_count += 1
                    elif prev_light == 1:
                        ll_count += 1
                    guest_list[cast_name][1] = 0
                    spy_light = 'lowlight'
                    spy_light_change = 1
                    light_time = event['elapsed_time']
                else:
                    change_made = 0
    gamestate['highlights'] = hl_count
    gamestate['lowlights'] = ll_count
    gamestate['light'] = spy_light
    return guest_list, gamestate, change_made, spy_light_change, light_time


def Cast(event, guest_list):
    if event["cast_name"][0] not in guest_list.keys():
        guest_data = [event['role'][0], 1]
        guest_list[event['cast_name'][0]] = guest_data
        
        
    

#CompileFinalGamestates('C:/Users/Aidan/Desktop/SpyPartyPredict/PAX_test_data/test_data')
