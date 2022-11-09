import json
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from math import sqrt
import os
from os import listdir
import re
import bisect
import random
from anytree import Node, RenderTree,NodeMixin
import pickle
# from surprise import NMF, Dataset, Reader, accuracy, SVD,dump
from sklearn.metrics import mean_squared_error
import heapq
import matplotlib.pyplot as plt

def get_lowest_content(Prediction_score_dict, time):
    # return the lowest score content and the content itself.
    farthest_time = datetime(2000, 6, 30, 0, 20, second=0)
    content_with_score = set()
    farthest_content = None  # initial
    content_lowest_score = 10000000
    lowest_content = None  # initial
    content_score = 0
    for content in list(Prediction_score_dict):
        record = Prediction_score_dict[content]
        if len(record) == 0:
            return content,datetime(9999, 12, 30, 0, 0, second=0)

        for i in range(len(record)):
            if time >= record[i][0] and time <= record[i][1]:  # have score at this time
                content_with_score.add(content)
                content_score += record[i][2]  # sum up all contributors' score
            # if content has impulse score, then no else will not be exed
            elif farthest_time < record[i][0] and time < record[i][0]:  # time<record[0][0] means it should be after current time
                farthest_time = record[i][0]  # same content has same len, so [0] should be the earliset time comparing with [1]...
                farthest_content = content
        if content_score < content_lowest_score:
            content_lowest_score = content_score
            lowest_content = content
        content_score = 0

    if farthest_content is None:
        #all have socre
        return lowest_content,content_lowest_score
    else:
        return farthest_content,farthest_time

def get_lowest_content2(Prediction_score_dict,your_cache, time):
    # return the lowest score content and the content itself.
    farthest_time = datetime(2000, 6, 30, 0, 20, second=0)
    content_with_score = set()
    farthest_content = None  # initial
    content_lowest_score = 10000000
    lowest_content = None  # initial
    content_score = 0
    for content in list(your_cache):
        record = Prediction_score_dict[content]
        if len(record) == 0:
            return content,datetime(9999, 12, 30, 0, 0, second=0)

        for i in range(len(record)):
            if time >= record[i][0] and time <= record[i][1]:  # have score at this time
                content_with_score.add(content)
                content_score += record[i][2]  # sum up all contributors' score
            # if content has impulse score, then no else will not be exed
            elif farthest_time < record[i][0] and time < record[i][0]:  # time<record[0][0] means it should be after current time
                farthest_time = record[i][0]  # same content has same len, so [0] should be the earliset time comparing with [1]...
                farthest_content = content
        if content_score < content_lowest_score:
            content_lowest_score = content_score
            lowest_content = content
        content_score = 0

    if farthest_content is None:
        #all have socre
        return lowest_content,content_lowest_score
    else:
        return farthest_content,farthest_time

def get_highest_content(Prediction_score_dict, time):
    # find if from content who has score
    earliest_time = datetime(9999, 12, 30, 0, 0, second=0)
    content_with_score = set()

    earliest_content = None #in case of empty Prediction_score
    for idx,content in enumerate(Prediction_score_dict):
        earliest_content = content  # initial(avoid none)
        break
    content_highest_score = 0
    highest_content = None
    content_score = 0
    for content in list(Prediction_score_dict):
        record = Prediction_score_dict[content]
        for i in range(len(record)):
            if time >= record[i][0] and time <= record[i][1]:  # have score at this time
                content_score += record[i][2]  # sum up all contributors' score
            elif earliest_time > record[i][0] and time < record[i][0]:
                earliest_time = record[i][0]  # same content has same len, so [0] should be the earliset time comparing with [1]...
                earliest_content = content
        if content_highest_score < content_score:
            content_highest_score = content_score
            highest_content = content
        content_score = 0

    if highest_content is not None:
        return highest_content,content_highest_score
    else:
        return earliest_content,earliest_time

def get_highest_content2(Prediction_score_dict,outcache_item, time):
    # find if from content who has score
    earliest_time = datetime(9999, 12, 30, 0, 0, second=0)
    content_with_score = set()

    earliest_content = None #in case of empty Prediction_score
    for idx,content in enumerate(outcache_item):
        earliest_content = content  # initial(avoid none)
        break
    content_highest_score = 0
    highest_content = None
    content_score = 0
    for content in list(outcache_item):
        record = Prediction_score_dict[content]
        for i in range(len(record)):
            if time >= record[i][0] and time <= record[i][1]:  # have score at this time
                content_score += record[i][2]  # sum up all contributors' score
            elif earliest_time > record[i][0] and time < record[i][0]:
                earliest_time = record[i][0]  # same content has same len, so [0] should be the earliset time comparing with [1]...
                earliest_content = content
        if content_highest_score < content_score:
            content_highest_score = content_score
            highest_content = content
        content_score = 0

    if highest_content is not None:
        return highest_content,content_highest_score
    else:
        return earliest_content,earliest_time

def compare_score(score1,score2):
    #score1>score2->True
    if (type(score1) is float or type(score1) is int) and type(score2) is datetime:
        return True
    if type(score1) is datetime and (type(score2) is float or type(score2) is int):
        return False
    if (type(score1) is float or type(score1) is int) and (type(score2) is float or type(score2) is int):
        return True if score1 >= score2 else False
    if type(score1) is datetime and type(score2) is datetime:
        return True if score1 <= score2 else False
    else:
        print(score1,type(score1))
        print(score2,type(score2))
        print('compare error')
        w
        
    return False

def update_predition_from_time(Prediction_score_dict, time,user_contribution2item):
    k = 0.5
    for item in list(Prediction_score_dict.keys()):
        record = Prediction_score_dict[item].copy()
        for i in range(len(record)):
#             if time > record[i][0] and time < record[i][1] - timedelta(
#                     seconds=(record[i][1] - record[i][0]).total_seconds() * k):
            if time > record[i][0] and time < record[i][1] - (record[i][1] - record[i][0])* k:
                record[i][0] = time
#                 record[i][2] *= ((record[i][1] - record[i][0]).total_seconds())/((record[i][1] - time).total_seconds())
                record[i][2] *= ((record[i][1] - record[i][0]))/((record[i][1] - time))
                record[i][3] = True# this score has been increased
                # record[i][2] = SCORE_Norm / ((record[i][1] - time).total_seconds() / 60)
#             elif time > record[i][1] - timedelta(seconds=(record[i][1] - record[i][0]).total_seconds() * k) and time < \
#                     record[i][1]:
            elif time > record[i][1] - (record[i][1] - record[i][0]) * k and time < \
                    record[i][1]:                
                record[i][0] = time
                if record[i][3] is False:# this score has never been increased
                    record[i][2] /= (1-k)
                    record[i][3] = True#his score has been increased
            elif time > record[i][1]:
                delete_item = record[i]
                Prediction_score_dict[item].remove(delete_item)
                #delete user_contribution2item record
                delete_item_name = item
                delete_item_correspond_user = record[i][4]
#                 print(delete_item_correspond_user,delete_item_name)
                try:
                    user_contribution2item[delete_item_correspond_user].remove(delete_item_name)                
                except:
                    pass
            else:
                pass

    return


def strip_the_served_score(Cache_score,time,content_name,user):
    hit_score = Cache_score[content_name].copy()
    
    if len(hit_score)==0:
        return
    for i in range(len(hit_score)):
        if user == hit_score[i][4]:
            # Cache_score[content_name][i][1] = time + timedelta(minutes=0.5)
            Cache_score[content_name].pop(i)#each user has at most 1 contribution for each item.
            break
    return


def get_series_len_average_name(req_name):
    series_indicator = True
    if re.search('集', req_name) and re.search('第', req_name):  # series data
        try:
            episode_num = re.findall(r"\d+\.?\d*", req_name)[-2]  # get the num-th of series
            if episode_num == '4.':  # mp4.mp4 file
                episode_num = re.findall(r"\d+\.?\d*", req_name)[-3]
            if episode_num == '600.':
                episode_num = re.findall(r"\d+\.?\d*", req_name)[-4]
            episode_num = int(episode_num)
            series_name = req_name.split('(')[0]
            series_indicator = True
        except:
            # print(req_name)
            series_name = req_name
            series_indicator = False
    else:  # other data
        # tree
        series_name = req_name
        series_indicator = False
    return series_name,series_indicator

def check_score(Prediction_score_dict, content_name, time):
    # get the current content score
    record = Prediction_score_dict[content_name]
    if len(record)==0:
        return datetime(9999, 12, 30, 0, 0, second=0)

    current_content_score = 0
    earliest_time = time + timedelta(minutes=1000)
    for i in range(len(record)):
        if time >= record[i][0] and time <= record[i][1]:  # have score at this time
            current_content_score += record[i][2]

        if record[i][0] > time and  earliest_time > record[i][0]:  # find the earliest time after current time
            earliest_time = record[i][0]

    if current_content_score>0:
        return current_content_score
    else:
        return earliest_time
    # return current_content_score, earliest_time
def get_lruK_action_rank(K, cache_list,past_timestamps,timenow):
    pasttimeforrank = {}
    min_lruK_score = datetime(2021, 6, 26, 0, 0, second=0)
    min_lru1_score = datetime(2021, 6, 26, 0, 0, second=0)
    lruK_action = None
    pos = 0
    feature_pos = -K
    for content in cache_list:
        if len(past_timestamps[content]) < K:
            min_lruK_score = datetime(2010, 6, 25, 0, 0, second=0)#-1 then will never go to elif
            pasttimeforrank[content] = timenow - past_timestamps[content][-1]  # record lruk score(actually it is lru1 score
            if past_timestamps[content][-1] < min_lru1_score:
                min_lru1_score = past_timestamps[content][-1]
                # if content not in pasttimeforrank:

                kick_name = content
                lruK_action = pos
        elif past_timestamps[content][feature_pos] < min_lruK_score:
            min_lruK_score = past_timestamps[content][feature_pos]#record last arrivel time of the kick_name
            pasttimeforrank[content] = (timenow - past_timestamps[content][feature_pos])/K
            lruK_action = pos
            kick_name = content
        else:
            pasttimeforrank[content] = (timenow - past_timestamps[content][feature_pos])/K
            pass  # never happen
        pos += 1
    return lruK_action,kick_name,pasttimeforrank