# Google Books Preview Extractor

**_This project is for educational purposes_**

This project Helps you download maximum images from pages of a particular payed bookfrom Google Books

## How to run it

```
pip install -r requirements.txt
docker compose up -d
python script.py
```

## How it works

It downloads maximum images from a particular book from Google Books.
It uses Tor Proxy and Selenium Webdriver to download the images as images selected to preview change from one user to another and also from one Ip address to another .
It downloads the maximum of images and it handles the errors and retries in a reasonable way and time
