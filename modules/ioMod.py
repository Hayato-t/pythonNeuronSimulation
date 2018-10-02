import os.path
import numpy as np
import pickle
from datetime import datetime
import shutil

def pickleData(**dict):
    if os.path.isdir('./result/') is False:
        os.mkdir('./result/')
    if int(dict["host_info"][1]) == 0:
        if os.path.isdir('./result/' + dict["datetime"]) is False:
            os.mkdir('./result/' + dict["datetime"])
            shutil.copy(dict['paths']['setting_file_path'],'./result/' + dict['datetime'] + '/')
    dict["pc"].barrier()
    filename = './result/' + dict["datetime"] + "/" + str(int(dict["host_info"][1])) + "_" + str(int(dict["host_info"][0])) +  '.pickle'
    with open(filename, 'wb') as f:
        dict.pop("pc")
        pickle.dump(dict, f)

def validator():
    return 0

def readExternalFiles(paths):
    f = open(paths['dynamics_def_path'], 'r')
    str_dynamics = f.read()
    f.close()
    dynamics_list = str_dynamics.split('\n')
    dynamics_list.pop()
    print(dynamics_list)
    num = len(dynamics_list)

    f = open(paths['connection_def_path'], 'r')
    str_connection = f.read()
    f.close()
    str_list = str_connection.split('\n')
    str_list.pop()
    print(str_list)
    connection_list = []
    for str in str_list:
        if str == '':
            continue
        split_str = str.rstrip().split(',')
        connection_list.append(con_decorator(split_str))
    print(connection_list)

    f = open(paths['stim_setting_path'], 'r')
    str_stim = f.read()
    f.close()
    str_list = str_stim.split('\n')
    str_list.pop()
    stim_settings_precast = [str.split(',') for str in str_list]
    stim_settings = [[int(str[0]), float(str[1]), float(str[2]), float(str[3])] for str in stim_settings_precast]

    f = open(paths['record_setting_path'], 'r')
    str_record = f.read()
    f.close()
    str_list = str_record.split('\n')
    str_list.pop()
    rec_index_list = []
    for str in str_list:
        if str == "":
            continue
        split_str = str.split(",")
        rec_index_list.append(rec_decorator(split_str))
    return num, dynamics_list, connection_list, stim_settings, rec_index_list

def con_decorator(split_str):
    if len(split_str) == 2:
        return [int(split_str[0]),int(split_str[1]),"soma",0.5,"soma",0.5,"E"]
    elif len(split_str) == 3:
        return [int(split_str[0]),int(split_str[1]),"soma",0.5,"soma",0.5,split_str[2]]
    elif len(split_str) == 7:
        return [int(split_str[0]),int(split_str[1]),split_str[2],float(split_str[3]),split_str[4],float(split_str[5]),split_str[6]]
    else:
        print("Error: " + "connection_def_path " + "contains invalid data. Each row must be INT INT STR or INT INT\n")
        exit()

def rec_decorator(split_str):
    if len(split_str) == 1:
        return [int(split_str[0]), "soma", 0.5]
    elif len(split_str) == 3:
        return [int(split_str[0]), split_str[1], float(split_str[2])]
    else:
        print("Error: " + "rec_def_path " + "contains invalid data. Each row must be INT or INT STR FLOAT\n")
        exit()
