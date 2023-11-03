<h1 align="center">TranslateThis</h2>
<p align="center">
<a href="https://github.com/Search-BGU/PolyPlan/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# Info

Note: This project is in progress, translation is not optimal.

The project aims to help you play video games in another language without a game transcript and still understand enough.

# Usage

Note: Default translation is from Japanese to English and the active button is "`".

1. Copy the project and pip install all the requirements:
> pip install -r requirements.txt
2. Edit the config.py file to the wanted language and active button
3. Start the main.py file
4. Wait until you see "Script is ready"
5. Press the active button to start OCR, press again will close it
6. You can click on the overlay to toggle between original and translated text


# Pipeline

I am using:
1. [EasyOCR](https://github.com/JaidedAI/EasyOCR) library to read the screen
2. [googletrans](https://github.com/ssut/py-googletrans) library to translate each text
3. tkinter library to display the translation
