import sqlite3
import pandas as pd 
import glob 
import db_lib
import os  
import utils 
import re 
import time
from datetime import datetime
import subprocess
import sys

from db_lib import *


def current_time_stamp():

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    time_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return time_string 

def validate_file(file_data,ts_data,f):

    # file name match
    if not re.search(".*[.]SMRT$", f): 
        print("Incorrect file extension.") 
        return False

    # check dimensions are as expected 
    if file_data.shape[1] != 6: 
        print("Header not correct.") 
        return False 
    if file_data.shape[0] < 3: 
        print("No data to insert.") 
        return False
    if ts_data.shape[1] != 5: 
        print("Time series data not correct length.") 
        return False

    # check header exists 
    head_value = file_data.iloc[0][0]
    if head_value != 'HEADR': 
        print("Header not present.") 
        return False 
    
    # check tail exists 
    tail_value = file_data.tail(1).to_numpy()
    if tail_value[0][0] != 'TRAIL': 
        print("Trail not present.") 
        return False 

    # validate there is data to insert into the DB 
    if ts_data.iloc[0][0] != 'CONSU': 
        print("CONSU not present.") 
        return False 

    # validate file generation number
    file_generation_number = file_data.iloc[0][5]
    if not re.search("^(PN|DV)[0-9]{6}$", file_generation_number): 
        print("File generation number not correct.") 
        return False 

    # if passed return true 
    print("Data is valid.")
    return True 

def move_file(file_path_from,file_path_to,f):
    subprocess.call("mv "+ str(file_path_from) + str(f) + " " + str(file_path_to), shell=True)
    print("File " + str(f) + " has been moved.") 

def delete_old_records(conn,ts_data):
    # create where statement 
    where_clause = '' 
    for row in ts_data.iterrows():
        where_clause = where_clause + " OR ( meter_number = '"+str(row[1][1])+ "' AND measurement_date = '"+str(row[1][2])+"' AND measurement_time = '"+str(row[1][3])+"')"
    # remove initial OR 
    where_clause = where_clause[4:]

    # call delete to the DB
    db_lib.delete_records(conn,where_clause) 


