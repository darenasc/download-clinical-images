# download-clinical-images

This project downloads images from [https://openi.nlm.nih.gov/](https://openi.nlm.nih.gov/faq?it=xg) excluding graphics.

## Set up
* Install [pipenv](https://pipenv.pypa.io/en/latest/)
* run `pipenv install`
* Download the [chromedriver](https://chromedriver.chromium.org/downloads)
* There are 1.5M images in total. Edit the START_NUMBER and END_NUMBER in [`download_images.py`](src/download_images.py) to download that range of images.
* run the [`download_images.py`](src/download_images.py) files

The project will create a `data` folder where it will store the images and data about the images.