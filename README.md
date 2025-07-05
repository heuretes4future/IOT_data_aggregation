# IOT_data_aggregation

DESCRIPTION
This project simulates an IoT ETL system to demonstrate data ingestion, transformation, and storage workflows. Tools used for data aggregation is hadoop, flask for api calls between sensor and app and docker for containerization. Program run on ubuntu version Ubuntu 24.04 LTS


INSTALLATION SETUP 

dependencies 
  sudo apt update
  sudo apt install openjdk-8-jdk
  
  hadoop file is required to run batch processing correctly inside the hadoop folder
  - wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
  - tar -xvzf hadoop-3.3.6.tar.gz

important 
  -docker might have problem running on some specific OS

USAGE 

Running the application 
- docker-compose up --build

Closing the application
docker-compose down --volumes --remove-orphans

Running hadoop processing 
- ./hadoop-3.3.6/bin/hadoop jar ./hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -files ./mapper.py,./reducer.py \
  -input /tmp/input \
  -output /tmp/output \
  -mapper "python3 mapper.py var X var Y" \
  -reducer "python3 reducer.py"

Check result 1. terminal or 2. download hadoop processing 
1. - hdfs dfs -file /tmp/output/part-00000
2. - hdfs dfs -get /tmp/output /path/to/local_folder

Additional commands
    Get file of specific sensor units
  - http://localhost:8080/fetch?type=sensor
    Show values of sensor unit captured within timeframe 
  - http://localhost:8080/retrieve?sensor_id=1&start_time=2025-06-08T00:00:00&end_time=2025-06-09T00:00:00

FUTURE ADDITIONS
 -Sensors input can be swapped out with realtime meta-data in the sensor scripts.
 -SQL structure is prepared for ease of scaling, adjustment of sensor scripts is recommended. 

