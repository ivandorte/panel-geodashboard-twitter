# :bird: Twitter dashboard

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A Panel-based dashboard visualizing geotagged tweets with hvplot, Datashader and Echarts.

![img](https://raw.githubusercontent.com/ivandorte/panel-geodashboard-twitter/main/assets/images/dashboard.png)

The dashboard includes:

- An heatmap showing the number of tweets;

- A bar plot showing the 5 most common languages within the current map extent;

- A [wordcloud](https://amueller.github.io/word_cloud/) SVG showing the 10 most popular hashtags within the current map extent;

- A pie chart showing the overall sentiment (positive/negative) within the current map extent;

- Two line charts showing the number of tweets and unique users on a daily basis within the current map extent;

### Deployed on

Hugging Face: https://huggingface.co/spaces/ivn888/Twitter-dashboard

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
| tweet_sentiment | Sentiment Analysis (Multilingual model)|
| tweet_topic | Topic Classification (English, single-label model) |
| x | x-coordinate of the tweet |
| y | y-coordinate of the tweet |

### How to run this app on your local system

1. Git clone this repository:

`git clone git@github.com:ivandorte/panel-geodashboard-twitter.git`

`cd panel-geodashboard-twitter`

2. Install the required Python packages:

`python -m pip install -r requirements.txt`

3. Run the app

`panel serve app.py --show`

The dashboard will be available in your default web browser!!!

### References

- [HoloViz](https://holoviz.org/)

- [hvplot](https://hvplot.holoviz.org)

- [PyViz Topics Examples](https://examples.pyviz.org/index.html)

- [Awesome Panel](https://awesome-panel.org/)

- [TweetNLP](https://github.com/cardiffnlp/tweetnlp)

- [Echarts](https://echarts.apache.org/examples/en/index.html)

- [Markdown Badges](https://github.com/Ileriayo/markdown-badges)

### Authors

- Ivan D'Ortenzio

[![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/ivanziogeo)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ivan-d-ortenzio/)
