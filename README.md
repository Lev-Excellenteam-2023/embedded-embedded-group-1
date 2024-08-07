
# BIRDS DETECTION

# This project is a part of the Embedded Systems project at scale-up bootcamp
the project is a birds detectors system that uses a camera to detect birds and send notifications to the user

the project is divided into 3 parts:
1 - the detection system
2 - the server
3 - the client application


## 1 - the detection system 
the detection system is a python module that uses the camera to capture picture and detect birds in it
using a pre-trained model from roboflow
the script is using a camera module
the script is using the following libraries:
- opencv
- roboflow
- flask
- requests
- dotenv
this module can be used on small devices like raspberry pi
the module requires an .env file with the following variables:
```
API_KEY=your_api_key
CAMERA_ID=your_camera_id
```
you can get your api key from https://universe.roboflow.com/jess-minaya/birds-detector-tis9s/model/1

## 2 - the server
the server is a flask server that receives alerts from the detection system and send them to the client application
the server also saves the alerts in a database (a json file for now)
it also has functionality to send reports to the client application with different statistics about the birds detected
such as the most frequent hour of the day for birds detection
the server is using the following libraries:
- flask
- requests



## 3 - the client application
the client application is a flask application that receives alerts from the server and displays them to the user
it has also a web page that displays the reports sent from the server and the alerts in real time
the client application is using the following libraries:
- flask
- requests



## installation
download the project
add .env file in the detector with the following variables:
```
API_KEY=your_api_key 
CAMERA_ID=your_camera_id
SERVER_URL=your_server_url
```


# TODO LIST
- add a real database to the server
- add predictions to the reports, such as the number of birds that will be detected in the next hour based on the previous data
- create a nicer UI for the client application


# that's it! you are ready to go
thank you for visiting our project
we hope you enjoy it







