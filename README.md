# Machine Learning


## Generate

- Model : Use create_model() method
- Statistic : Use generate_area_statistic(data) with data being the DataFrame of csv file



## Model

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