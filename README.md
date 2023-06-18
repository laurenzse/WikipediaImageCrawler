# Wikipedia Image Crawler

This crawler gets all images on Wikipedia provided from the given article names  complete **with license information**. 

## Setup

Install the requirements [wptool](https://pypi.org/project/wptools/) and [tqdm](https://tqdm.github.io).

```
pip3 install -r requirements.txt
```

## How to use

You might need to update the endpoints defined in `wikipedia_image_crawler.py` to your country version of Wikipedia.

1) Put the names of the articles from which you would like to parse the images in .csv file named `articles.csv`
2) Run `wikipedia_image_crawler.py`
3) The images will be in the downloaded folder and the licenses in the `licenses.csv` file