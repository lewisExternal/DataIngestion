import sqlite3
import pandas as pd 
import glob 
import db_lib
import os  
import re 
import time
from datetime import datetime
import subprocess
import sys

# imports from script 
import utils
import db_lib  

def main():

    # database name 
    database = r"pythonsqlite.db"

    # create the db if it doesn't already exist 
    conn = db_lib.main(database) 
    
    # check connection exists 
    if conn is None: 
        print("Connection to the DB couldn't be established, exiting.")
        exit()

    print("DB called. Connection to the DB established.")

    # take parameters from the command line 
    arguments = len(sys.argv) - 1
    print ("The script is called with %i argument(s)" % (arguments))
    
    # first command line argument read from file path 
    if arguments >= 1: 
        file_path_from = sys.argv[1]
    else: 
        print("Default file_path_from selected: /home/pi/data_ingestion/ ")
        file_path_from = '/home/pi/data_ingestion/'

    # second command line argument move to file path 
    if arguments == 2: 
        file_path_to = sys.argv[2]
    else: 
        print("Default file_path_to selected: /home/pi/data_processed/" )
        file_path_to = '/home/pi/data_processed/'   

    # read from the file path 
    while True: 
        
        # find files in current directory  
        files = [ f for f in os.listdir(file_path_from) if os.path.isfile(os.path.join(file_path_from,f)) ]

        # lookup files processed in the DB
        db_files = db_lib.select_all_files(conn) 

        for f in files:

            print("Processing file "+ str(f))
            
            try: 
                
                # if duplicate move file and continue
                if f in db_files: 
                    print("File already uploaded.")
                    move_file(file_path_from,file_path_to,f)
                    continue
                
                # data to df 
                file_data = pd.read_csv(file_path_from + f,header=None)
                ts_data = pd.read_csv(file_path_from + f ,skiprows = 1, skipfooter=1 ,engine='python',header=None) 

                # verify the dataset 
                valid = utils.validate_file(file_data,ts_data,f)

                if not valid: 
                    utils.move_file(file_path_from,file_path_to,f)
                    continue

                # get time stamp 
                time_string = utils.current_time_stamp()

                # add the time stamp and file name to the time series data  
                file_data['time_stamp'] = time_string
                ts_data['file_name'] = file_data.iloc[0][5]

                # delete duplciate meter readings
                db_lib.delete_old_records(conn,ts_data)

                # set df columns names 
                file_data.columns = ['record_identifier','file_type_identifier','company_id','file_creation_date','file_creation_time','file_generation_number','time_stamp']
                ts_data.columns = ['record_identifier','meter_number','measurement_date','measurement_time','consumption','file_name']                                        
                           
                # if valid then upload the data to DB 
                ts_data.to_sql('timeseries', conn, if_exists='append', index=False)
                print("Meter data uploaded.")
                file_data.iloc[0].to_frame().transpose().to_sql('files', conn, if_exists='append', index=False)
                print("File info uploaded.")
                # move the file 
                db_lib.move_file(file_path_from,file_path_to,f)
                print("File processed to the db and uploaded")


            except Exception as e:
                print("File cannot be processed: " + str(e))
                # move file 
                utils.move_file(file_path_from,file_path_to,f)


if __name__ == '__main__':
    main()