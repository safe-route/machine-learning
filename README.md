# Safe Route - Machine Learning

## Overview
* **[Clustering](#clustering)**
* **[Habit Tracker](#habit-tracker)**
* **[Known Issues](#known-issues)**
* **[Team](#team)**

## Clustering
### Model Description

Clustering model is produced using scikit-learn DBScan class. Centroid comes from the average of each cluster with the range is the maximum distance of centroid to one of cluster members.

### Model generation

- Model : Use create_model() method
- Statistic : Use generate_area_statistic(data) with data being the DataFrame of csv file

### Centroid
JSON File Format
```
{
    "centroids": [
        {
            "id": ... (int),
            "latitude": ... (float),
            "longitude": ... (float),
            "range": ... (float),
            "crime_info": {
                <crime_type>(string): ... (int),
                ...
            }
        },
        ...
    ]
}
```

### Statistic
JSON File Format
```
{
    "statistic": [
        "subdistrict": ... (string),
        "total_crime": ... (int),
        "crime_info": {
            <crime_type>(string): ... (int),
            ...
        }
        "coordinates": ... (list of* float)
    ]
}
```
Statistic JSON File Note:
- coordinates list order is latitude, longitude
- list may contain another list
- please take a look at area_statistic.json before use


## Habit Tracker

### Model Description

Habit tracker model is created for each user that use the application, it utilize LSTM mechanics to predict multivariate multilabel time series data. Model will be fed with multiple inputs which is date, time, and location. The model will give location (latitude and longitude) as output.

### Model Generation

User's model will be generated when the endpoint ```/create``` called with username as URL parameters*.

\* further endpoint detail will be given [below](#flask)

### Model
```
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 lstm (LSTM)                 (None, 15, 64)            18176     
                                                                 
 lstm_1 (LSTM)               (None, 15, 32)            12416     
                                                                 
 lstm_2 (LSTM)               (None, 16)                3136      
                                                                 
 flatten (Flatten)           (None, 16)                0         
                                                                 
 dense (Dense)               (None, 16)                272       
                                                                 
 dense_1 (Dense)             (None, 8)                 136       
                                                                 
 dense_2 (Dense)             (None, 2)                 18        
                                                                 
=================================================================
Total params: 34,154
Trainable params: 34,154
Non-trainable params: 0
_________________________________________________________________
```
* Model input shape=(15, 6)
* Model input data columns:
| column      | type    | range          | description              |
|-------------|---------|----------------|--------------------------|
| year        | integer |        *       | year timestamp           |
| month       | integer |     1 - 12     | month timestamp          |
| day_of_week | integer |      1 - 7     | day of week              |
| time        | integer |    0 - 1440    | cumulative minute of day |
| latitude    |  float  |  -90.0 - 90.0  | latitude                 |
| longitude   |  float  | -180.0 - 180.0 | longitude                |
* Model output:
| column    | type  | range          | description |
|-----------|-------|----------------|-------------|
| latitude  | float |  -90.0 - 90.0  | latitude    |
| longitude | float | -180.0 - 180.0 | longitude   |

### Flask
url: https://model-ck44nnq7hq-as.a.run.app

| endpoint  | url_param        | body           | method |
|-----------|------------------|----------------|--------|
| /create   | username(string) |        -       | GET    |
| /train    | username(string) | json-object-1* | POST   |
| /forecast | username(string) | json-object-2* | POST   |

\* refer to the format below

* json-object-1
```
{
	"username": ...,
	"data": [
	        {
	            "datetime": ...,
	            "latitude": ...,
	            "longitude": ...
	        },
	        ...
	        {
	            "datetime": ...,
	            "latitude": ...,
	            "longitude": ...
	        }
	    ]
}
```

* json-object-2
```
{
	"username": ...,
    "email": ...,
    "latitude": ...,
	"longitude": ...,
	"data": [
	        {
	            "datetime": ...,
	            "latitude": ...,
	            "longitude": ...
	        },
	        ...
	        {
	            "datetime": ...,
	            "latitude": ...,
	            "longitude": ...
	        }
	    ]
}
```
* json key-value description
| key       | value                | range                     |
|-----------|----------------------|---------------------------|
| username  |        string        |             -             |
| email     |        string        |             -             |
| latitude  |         float        |        -90.0 - 90.0       |
| longitude |         float        |       -180.0 - 180.0      |
| data      | json-array-of-object |             -             |
| datetime  |       timestamp      | %yyyy/%mm/%dd %hh:%MM:%ss |

## Known Issues

* Clustering - Require real data from local authorities
* Habit Tracker - Model architecture has not yet been optimized
* Habit Tracker - Costly data and model pipelining
* Habit Tracker - Require a lots of data to create optimum model

## Team
* M2002F0101 - Christopher Chandrasaputra
* M2006F0613 - Hanif Adam Al Abraar
* A2183F1771 - Fillah Akbar Firdausyah
* A2009J0968 - Ikhsan Cahya Mardika 
* C2009F0967 - I Putu Cahya Adi Ganesha
* C2306G2617 - Muhammad Anggi Wirahmat