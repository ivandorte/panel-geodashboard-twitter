# :bird: Twitter dashboard

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A simple Panel-based dashboard visualizing geotagged tweets with hvplot and Datashader.

The dashboard includes:

- An heatmap showing the number of tweets;

- A bar plot showing the 5 most common languages within the current map extent;

- A [wordcloud](https://amueller.github.io/word_cloud/) image showing the 10 most popular hashtags within the current map extent;

- Two numeric indicators showing the number of tweets and unique users on a daily basis within the current map extent;

- Two line charts showing the number of tweets and unique users on a daily basis within the current map extent;

### The dashboard in action!!! :tv:

https://user-images.githubusercontent.com/1726395/186170258-b7643044-cf66-41df-b6ef-8a5c4519eee5.mp4

### Twitter data ([link](https://github.com/ivandorte/panel-geodashboard-twitter/blob/main/data/rome_tweets.parquet))

This dataset contains over 200k geotagged tweets in parquet format:

- Coverage: Historic Centre of Rome, Italy;

- [EPSG: 3857](https://epsg.io/3857);

- Year: 2018;

- Language: Multi;

- Source: This dataset was scraped by myself with snscrape; 

| Column | Description |
| ------------- | ------------- |
| tweet_date (index) | Tweet creation date |
| user_id | Unique identifier of the tweet author |
| user_location | User location information |
| tweet_id | Unique identifier of the tweet |
| tweet_text | Tweet content |
| tweet_hashtags | Comma separated list of the tweet hashtags |
| tweet_lang | Tweet language |
| x | x-coordinate of the tweet |
| y | y-coordinate of the tweet |

### Set up
To run this dashboard you will need to do the following steps:

1. Git clone this repository:

`git clone https://github.com/ivandorte/panel-geodashboard-twitter.git`

`cd panel-geodashboard-twitter`

2. Install the required Python packages:

`python -m pip install -r requirements.txt`

3. Run the app

`python -m panel serve app.py --show`

The dashboard will be available in your web browser!!!

### Deployment

This dashboard has not been deployed yet.

### References

- https://holoviz.org/

- https://hvplot.holoviz.org

- https://examples.pyviz.org/index.html

- https://awesome-panel.org/

- https://github.com/Ileriayo/markdown-badges

### Authors

- Ivan D'Ortenzio

[![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/ivanziogeo)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ivan-d-ortenzio/)
