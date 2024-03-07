#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 2024 Robert P. Spang

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import pandas as pd
import random
import os

LOG_FILE_NAME_performance = "log/performance_log.csv"
LOG_FILE_NAME_mission = "log/session_data.csv"
###############################################################################
# Flask app
###############################################################################

app = Flask(__name__)
CORS(app)

def log_performance(data):
    print('log_performance')
    file_exists = os.path.exists(LOG_FILE_NAME_performance)
    if not file_exists:
            print('create file')
            with open(LOG_FILE_NAME_performance, mode='a', newline='', encoding='utf-8') as file:
                file.write('session_id,taskID,first_number,second_number,operation,result,difficulty,tries,taskComplete,responseTime,choiceTime,timestamp,game_type,nth_mission,skipped,aborted,time_up\n')
    
    with open(LOG_FILE_NAME_performance, mode='a', newline='', encoding='utf-8') as file:
        print('write to file')
        file.write(f"{data['session_id']},{data['taskID']},{data['first_number']},{data['second_number']},{data['operation']},{data['result']},{data['difficulty']},{data['tries']},{data['taskComplete']},{data['responseTime']},{data['choiceTime']},{data['timestamp']},{data['game_type']},{data['nth_mission']},{data['skipped']},{data['aborted']},{data['time_up']}\n")

def log_mission_data(data):
    print('log_mission_data')
    file_exists = os.path.exists(LOG_FILE_NAME_mission)
    if not file_exists:
            print('create file')
            with open(LOG_FILE_NAME_mission, mode='a', newline='', encoding='utf-8') as file:
                file.write('session_id,nth_mission,mission_time,mission_points,success,points_achieved,response_time,rank_now,successes_in_a_row_now,skips,aborted,timestamp,game_type\n')
    
    with open(LOG_FILE_NAME_mission, mode='a', newline='', encoding='utf-8') as file:
        print('write to file')
        file.write(f"{data['session_id']},{data['nth_mission']},{data['mission_time']},{data['mission_points']},{data['success']},{data['points_achieved']},{data['response_time']},{data['rank_now']},{data['successes_in_a_row_now']},{data['skips']},{data['aborted']},{data['timestamp']},{data['game_type']}\n")


all_ops_data = pd.read_csv('./tasks/all_ops_rated.csv', dtype={
    'first_number': 'int64',
    'second_number': 'int64',
    'result': 'int64',
    'difficulty': 'int64',
    'operation': 'string'
})

# performance_log_data = pd.read_csv('./log/performance_log.csv', index_col=False, header=0)
performance_log_data_file = './log/performance_log.csv'
if os.path.isfile(performance_log_data_file):
    performance_log_data = pd.read_csv(performance_log_data_file, index_col=None, header=0)
    print('performance_log_data')
    print(performance_log_data.shape)
    print(performance_log_data.head())
else:
    print('performance_log_data file does not exist')
    # performance_log_data = pd.DataFrame(columns=['session_id', 
    #                                                 'taskID', 
    #                                                 'first_number', 
    #                                                 'second_number', 
    #                                                 'operation', 
    #                                                 'result', 
    #                                                 'difficulty', 
    #                                                 'tries', 
    #                                                 'taskComplete', 
    #                                                 'responseTime', 
    #                                                 'choiceTime' ]) 
    performance_log_data = pd.DataFrame(columns=['session_id', 
                                                    'taskID', 
                                                    'first_number', 
                                                    'second_number', 
                                                    'operation', 
                                                    'result', 
                                                    'difficulty', 
                                                    'tries', 
                                                    'taskComplete', 
                                                    'responseTime', 
                                                    'choiceTime',
                                                    'timestamp',
                                                    'game_type',
                                                    'nth_mission',
                                                    'skipped',
                                                    'aborted',
                                                    'time_up'] ) 



# session_data.to_csv('./log/session_data.csv', index_label=None, index=False)
session_data_file = './log/session_data.csv'
if os.path.isfile(session_data_file):
    session_data = pd.read_csv(session_data_file, index_col=None, header=0)
    print('session_time_data')
    # print(session_data.shape)
    print(session_data.head())
else:
    print('session_data file does not exist')
    # session_data = pd.DataFrame(columns=['session_id', 
    #                                     'nth_mission',
    #                                     'mission_time', 
    #                                     'mission_points',
    #                                     'success', 
    #                                     'points_achieved', 
    #                                     'response_time', 
    #                                     'rank_now', 
    #                                     'successes_in_a_row_now', 
    #                                     'skips', 
    #                                     'saved_points_now']) 
    session_data = pd.DataFrame(columns=['session_id', 
                                            'nth_mission',
                                            'mission_time', 
                                            'mission_points',
                                            'success', 
                                            'points_achieved', 
                                            'response_time', #response_time
                                            'rank_now', # rank_now
                                            'successes_in_a_row_now', 
                                            'skips', 
                                            'aborted',
                                            'timestamp',
                                            'game_type'], dtype='int64') 



print('performance_log_data')
print(performance_log_data.shape)
print(performance_log_data)
print('session_data')
print(session_data.shape)
print(session_data)

@app.route('/next_task', methods=['POST'])
def next_task():
    global performance_log_data
    global session_data
   
    try:
        # parse request data
        print("request", request)
        data = request.get_json()

        print('data keys length')
        print(data.keys())

        #initial set up when first entering session name, return last row in session data for that session-id
        if 'get_session_data' in data :
            print('get_session_data')  
            if session_data['session_id'].eq(data['session_id']).any():
                print('session_id in session_data')
                session_data_id_subset = session_data[session_data['session_id'] == data['session_id']]
                past_missions = session_data_id_subset['mission_points'].values.tolist()
                past_successes = session_data_id_subset['success'].values.tolist()
                past_achieved_points = session_data_id_subset['points_achieved'].values.tolist()
                past_response_times = session_data_id_subset['response_time'].values.tolist()


                print('session_data_id_subset session_id')
                # print(session_data_id_subset.shape)
                last_row = session_data_id_subset.tail(1)
                print(type(last_row['skips'].values[0]))
                print(type(last_row['nth_mission'].values[0]))
                print(type(last_row['rank_now'].values[0]))
                print(type(last_row['successes_in_a_row_now'].values[0]))    
                last_row_data = {
                    'session_id': last_row['session_id'].values[0],
                    # 'nth_mission': last_row['nth_mission'].values[0].item(),
                    # 'mission_time': last_row['mission_time'].values[0].item(),
                    # 'mission_points': last_row['mission_points'].values[0].item(),
                    # 'success': last_row['success'].values[0].item(),
                    # 'points_achieved': last_row['points_achieved'].values[0].item(),
                    # 'response_time': last_row['response_time'].values[0].item(),
                    'rank_now': last_row['rank_now'].values[0].item(),
                    'successes_in_a_row_now': last_row['successes_in_a_row_now'].values[0].item(),
                    'past_successes': past_successes,
                    'past_missions': past_missions,
                    'past_achieved_points': past_achieved_points,
                    'past_response_times': past_response_times,
                    'skips': last_row['skips'].values[0].item(),
                    'nth_mission': last_row['nth_mission'].values[0].item(),
                    # 'saved_points_now': last_row['saved_points_now'].values[0].item()
                }            
            else:
                last_row_data = {
                    'session_id': data['session_id'],
                    # 'nth_mission': 0,
                    # 'mission_time': 120,
                    # 'mission_points': 60,
                    # 'success': 0,
                    # 'points_achieved': 0,
                    # 'response_time': 0,
                    'rank_now': int(1),
                    'successes_in_a_row_now': int(0),
                    'past_successes': int(-1),
                    'past_missions': int(-1),
                    'past_achieved_points': int(-1),
                    'past_response_times': int(-1),
                    'skips': int(2),
                    'nth_mission': int(0),
                    # 'successes_overall': 0,
                    # 'saved_points_now': 0
                }
            print('last_row_data')
            print(last_row_data)
            return create_json_response_from(last_row_data, 200)
        
        if 'log_performance' in data:
            print('log_performance')
            # relevant_fields_no_rate = ['session_id', 'taskID', 'first_number', 'second_number', 'operation', 'result',  'difficulty', 'tries', 'taskComplete', 'responseTime', 'choiceTime' ]
            relevant_fields = ['session_id', 'taskID', 'first_number', 'second_number', 'operation', 'result', 'difficulty','tries', 'taskComplete','responseTime', 'choiceTime','timestamp','game_type','nth_mission','skipped','aborted', 'time_up']
            if all([field in data for field in relevant_fields]):
                print('relevent fields to log performance there')
                performance_row = pd.DataFrame([[data['session_id'], data['taskID'],  data['first_number'], data['second_number'], data['operation'], data['result'], data['difficulty'], data['tries'], data['taskComplete'], data['responseTime'], data['choiceTime'], data['timestamp'],data['game_type'],data['nth_mission'],data['skipped'],data['aborted'],data['time_up']]], columns=relevant_fields)
                print('performance_row')
                print(performance_row.shape)
                print('performance_log_data')
                print(performance_log_data.shape)
                print(performance_log_data.head())
                performance_log_data = pd.concat([performance_log_data, performance_row], ignore_index=True)

                log_performance(data)
                return create_json_response_from({'success': 'logged performance'}, 200)
            else:
                print('not all relevant fields there')
                print(data)
                print([field + ' ' + str(field in data) for field in relevant_fields])
        if 'log_mission_data' in data:
            print('log_mission_data')
            # relevant_fields = ['session_id', 'nth_mission', 'mission_time', 'mission_points', 'success', 'points_achieved', 'response_time', 'rank_now', 'successes_in_a_row_now', 'skips', 'saved_points_now' ]
            relevant_fields = ['session_id', 'nth_mission','mission_time', 'mission_points', 'success', 'points_achieved', 'response_time', 'rank_now','successes_in_a_row_now', 'skips', 'aborted', 'timestamp', 'game_type']
            if all([field in data for field in relevant_fields]):
                print('relevent fields to log mission data there')
                session_data_row = pd.DataFrame([[data['session_id'], data['nth_mission'], data['mission_time'], data['mission_points'], data['success'], data['points_achieved'], data['response_time'], data['rank_now'], data['successes_in_a_row_now'], data['skips'], data['aborted'],data['timestamp'], data['game_type']]], columns=relevant_fields) 
                print('session_data_row')
                print(session_data_row.shape)
                print('session_data')
                print(session_data.shape)
                print(session_data.head())
                session_data = pd.concat([session_data, session_data_row], ignore_index=True)
                log_mission_data(data)
                return create_json_response_from({'success': 'logged mission data'}, 200)
        
        if 'get_task' in data: 
            print('get_task')
            if 'difficulty' not in data:
                return create_json_response_from({'error': 'difficulty not in data'}, 400)
            else:
                all_ops_data_difficulty = all_ops_data.copy()

                if data['session_id'] in performance_log_data['session_id'].values:
                    # Session ID exists in performance_log_data
                    session_id_used_tasks = performance_log_data[performance_log_data['session_id'] == data['session_id']]
                    all_ops_data_difficulty = all_ops_data.drop(session_id_used_tasks['taskID'].values, errors='ignore')
                
                all_ops_data_difficulty = all_ops_data_difficulty[all_ops_data_difficulty.iloc[:, 3] == data['difficulty']]
                random_task = all_ops_data_difficulty.sample(n=1)
                next_task = {
                    'session_id': data['session_id'],
                    'first_number': int(all_ops_data.iloc[random_task.index[0], 0]),
                    'second_number': int(all_ops_data.iloc[random_task.index[0], 1]),
                    'operation': all_ops_data.iloc[random_task.index[0], 4],
                    'result': int(all_ops_data.iloc[random_task.index[0], 2]),
                    'taskID': int(random_task.index[0])
                }
                return create_json_response_from(next_task, 200)

    except Exception as e:
        print('error:', e)
        return create_json_response_from({
            'error': str(e),
            'description': 'malformed response values',
        }, 400)



###############################################################################
# helper
###############################################################################

def create_json_response_from(hash, code):
    response = jsonify(hash)
    response.status_code = code

    print('respond with:', response)
    sys.stdout.flush()
    return response



# entry point as a stand alone script
if __name__ == '__main__':
    # start flask http server
    app.run(debug=True, port = 5051)
    # app.run(host = '0.0.0.0')
