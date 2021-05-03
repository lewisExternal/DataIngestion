DataIngestionExample
==================================

Data ingestion script to process file uploads from a user defined directory, then after validation write to a database.

Installation
============

The bash script will create a python environment and install the following dependencies from requirements.txt.
Has been tested with Python 3.8.5 (hardcoded in the script).

```console
numpy==1.20.2
pandas==1.2.4
Flask==1.1.2
```

Example usage for starting the ingestion script 
===============================

The bash script to run data ingestion takes two optional parameters, the directory for which files are read and where they are copied after being processed. 

Which can be seen below, respectively.

>1. (Optional) file_path_from i.e /home/pi/data_ingestion/ [default] 
>2. (Optional) file_path_to i.e /home/pi/data_processed/ [default]

An example command can be seen below. 

```console
./run_script.sh /home/pi/data_ingestion/ /home/pi/data_processed/
```

Script output can be seen here. 
```console
$ watch tail log.txt
```

The script will be ran in the background. To stop the script, run the following (Replacing the PID).
```console
$ ps aux | grep main.py
pi        1039 98.6  4.1  67556 39708 pts/0    R    09:35   4:06 python3.8 -u ./main.py /home/pi/data_ingestion/ /home/pi/data_processed/
$ kill -9 1039
```

Example usage for the endpoint 
===============================

Run the below to start the Flask app. 
```console
$ ./run_api.sh
```
There are three endpoints, which can be seen below. 

>1. Returns the last file uploaded to the DB and the time stamp for which it was uploaded. 
```console
$ curl http://127.0.0.1:5000/api/v1/lastfilereport
{"last_file":"PN000009","time_stamp":"02/05/2021 22:01:37"}
```

>2. Returns overall number of meters (num_meters) and the number of files (num_files).
```console
$ curl http://127.0.0.1:5000/api/v1/overviewreport
{"num_files":10,"num_meters":10}
```

>3. Takes an argument 'meter' from the query string as can be seen below. Returns all data for a particular meter.
```console
$ curl http://127.0.0.1:5000/api/v1/meterdata?meter=1
{"0":"(386, 'CONSU', '1', '20191016', '1600', '8.34', 'PN000002')","1":"(387, 'CONSU', '1', '20191016', '1700', '9.2', 'PN000002')","10":"(437, 'CONSU', '1', '20191016', '1200', '14.46', 'P '1300', '2.75', 'PN000003')","12":"(439, 'CONSU', '1', '20191016', '1400', '6.59', 'PN000003')","13":"(440, 'CONSU', '1', '20191016', '1500', '15.33', 'PN000003')","14":"(480, 'CONSU', '1'481, 'CONSU', '1', '20191014', '100', '7.38', 'PN000004')","16":"(482, 'CONSU', '1', '20191014', '200', '9.27', 'PN000004')","17":"(483, 'CONSU', '1', '20191014', '300', '2.36', 'PN000004')11.83', 'PN000004')","19":"(485, 'CONSU', '1', '20191014', '500', '19.6', 'PN000004')","2":"(388, 'CONSU', '1', '20191016', '1800', '17.55', 'PN000002')","20":"(486, 'CONSU', '1', '20191014U', '1', '20191014', '700', '18.97', 'PN000004')","22":"(488, 'CONSU', '1', '20191014', '800', '9.95', 'PN000004')","23":"(489, 'CONSU', '1', '20191014', '900', '10.91', 'PN000004')","24":"'PN000004')","25":"(491, 'CONSU', '1', '20191014', '1100', '0.67', 'PN000004')","26":"(492, 'CONSU', '1', '20191014', '1200', '3.53', 'PN000004')","27":"(493, 'CONSU', '1', '20191014', '1301', '20191014', '1400', '19.89', 'PN000004')","29":"(495, 'CONSU', '1', '20191014', '1500', '2.97', 'PN000004')","3":"(389, 'CONSU', '1', '20191016', '1900', '16.84', 'PN000002')","30":"(49000004')","31":"(497, 'CONSU', '1', '20191014', '1700', '4.87', 'PN000004')","32":"(498, 'CONSU', '1', '20191014', '1800', '6.69', 'PN000004')","33":"(499, 'CONSU', '1', '20191014', '1900', '20191014', '2000', '6.34', 'PN000004')","35":"(501, 'CONSU', '1', '20191014', '2100', '16.02', 'PN000004')","36":"(502, 'CONSU', '1', '20191014', '2200', '14.32', 'PN000004')","37":"(503,00004')","38":"(504, 'CONSU', '1', '20191015', '0', '19.38', 'PN000004')","39":"(505, 'CONSU', '1', '20191015', '100', '0.82', 'PN000004')","4":"(390, 'CONSU', '1', '20191016', '2000', '3.61015', '200', '9.51', 'PN000004')","41":"(507, 'CONSU', '1', '20191015', '300', '10.44', 'PN000004')","42":"(508, 'CONSU', '1', '20191015', '400', '1.82', 'PN000004')","43":"(509, 'CONSU', 4":"(510, 'CONSU', '1', '20191015', '600', '13.9', 'PN000004')","45":"(511, 'CONSU', '1', '20191015', '700', '10.4', 'PN000004')","46":"(512, 'CONSU', '1', '20191015', '800', '13.09', 'PN0000', '11.15', 'PN000004')","48":"(514, 'CONSU', '1', '20191015', '1000', '14.76', 'PN000004')","49":"(515, 'CONSU', '1', '20191015', '1100', '4.77', 'PN000004')","5":"(391, 'CONSU', '1', '276, 'CONSU', '1', '20191015', '1200', '12.55', 'PN000010')","51":"(877, 'CONSU', '1', '20191015', '1300', '5.83', 'PN000010')","52":"(878, 'CONSU', '1', '20191015', '1400', '18.75', 'PN00000', '9.8', 'PN000010')","54":"(880, 'CONSU', '1', '20191015', '1600', '1.22', 'PN000010')","55":"(881, 'CONSU', '1', '20191015', '1700', '17.47', 'PN000010')","56":"(882, 'CONSU', '1', '201, 'CONSU', '1', '20191015', '1900', '13.81', 'PN000010')","58":"(1370, 'CONSU', '1', '20191015', '2000', '7.13', 'PN000008')","59":"(1371, 'CONSU', '1', '20191015', '2100', '17.72', 'PN0000, '7.6', 'PN000003')","60":"(1372, 'CONSU', '1', '20191015', '2200', '15.7', 'PN000008')","61":"(1373, 'CONSU', '1', '20191015', '2300', '10.59', 'PN000008')","62":"(1374, 'CONSU', '1', '20 'CONSU', '1', '20191016', '100', '16.17', 'PN000008')","64":"(1376, 'CONSU', '1', '20191016', '200', '11.9', 'PN000008')","65":"(1377, 'CONSU', '1', '20191016', '300', '6.42', 'PN000008')"0.98', 'PN000008')","67":"(1379, 'CONSU', '1', '20191016', '500', '3.26', 'PN000008')","68":"(1380, 'CONSU', '1', '20191016', '600', '1.07', 'PN000008')","69":"(1381, 'CONSU', '1', '2019101U', '1', '20191016', '900', '10.37', 'PN000003')","8":"(435, 'CONSU', '1', '20191016', '1000', '12.67', 'PN000003')","9":"(436, 'CONSU', '1', '20191016', '1100', '11.51', 'PN000003')"}
```

Script output can be seen here. 
```console
$ watch tail api_log.txt
```
The script will be ran in the background. To stop the script, run the following (Replacing the PID).
```console
$ ps aux | grep api.py
pi        1121  9.3  4.7  73148 45024 pts/0    S    09:57   0:02 python3.8 -u ./api.py
$ kill -9 1121
```

Testing
===============================

N/A

Improvements 
===============================
N/A