# Table of Contents
- [About](#about)
- [Examples](#examples)
- [Purpose](#purpose)
- [Inspiration](#inspiration)
- [Limitations](#limitations)
- [Set up](#set-up)
- [Versions](#versions)

# About
This program is meant to track and update a win-loss record in [Overwatch 2](https://overwatch.blizzard.com/en-us/) using Optical Character Recognition (OCR) with both OpenCV and Tesseract. Here is a high-level overview of the flow of the program:
* A 1920x1080 screenshot is taken using PyAutoGUI
* The screenshot is pre-processed with OpenCV before being passed to Tesseract
* Tesseract attempts to detect text in the image. If either the string "victory" or "defeat" is detected or if the output string is close enough to those words (we use a [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to determine this), the record will be updated appropriately by writing to a text file.
* We repeat the process continually

# Examples
![Alt Text](https://github.com/gcmaidana/Visionwatch/blob/master/images/ocr_win.gif)
![Alt Text](https://github.com/gcmaidana/Visionwatch/blob/master/images/ocr_defeat.gif)

<p align="center">
  <img src="https://github.com/gcmaidana/Visionwatch/blob/master/images/ocr_win_log.png"/>
</p>
<p align="center">
  <img src="https://github.com/gcmaidana/Visionwatch/blob/master/images/ocr_defeat_log.png"/>
</p>


# Purpose
Whether someone is a live streamer or simply just a player, one thing about tracking your wins and losses is that you may sometimes forget to update it when you're manually updating a win-loss record. This leads to asking yourself questions like "Did I already add a win from last game? Or the game before?". This program solves that issue for you by automating the updating aspect of your win-loss record.

# Why I Chose To Use Python Instead of C++
I initially started this project in C++. I was talking to a recruiter at Blizzard, from the Overwatch team specifically, and he told me that the Overwatch team primarily uses C++. I'll include the screenshot of that conversation below this paragraph (though I'll keep the recruiter anonymous for privacy reasons). The reason I ended up switching to Python is because when you work with Tesseract in C++, you have to download the entire OCR engine using a package manager like vcpkg, as well as link it to Visual Studio. I did end up doing that and worked on the project for a bit in C++, but it was really tedious finding resources for when I was stuck because most people who work with Tesseract tend to use Python. Additionally, detecting the text was difficult due to the font Overwatch uses. That led me down a rabbit hole that took a lot of my time as I tried training a custom font, but to no avail. The reality is, it's much less of a headache working with binary files provided by [UB Mannequin](https://github.com/UB-Mannheim/tesseract/wiki) because PyTesseract exists, which is a Python wrapper for Tesseract. This avoids having to download Tesseract in its entirety. Even beyond that, I had to think of my end user, and while making the project in C++ makes more sense since I would like to work on the Overwatch team or the games industry in general, I don't think making a user download the entirety of Tesseract through a package manager like vcpkg (which takes quite a bit of time to download!) was practical or user-friendly. I chose Python and PyTesseract for both ease-of-use for me, as well as the end user who wishes to use this program. In addition to the recruiter's comment about the Overwatch team using C++, I've included some other things he told me in case anyone finds it useful as I did.

<p align="center">
  <img src="https://github.com/gcmaidana/OverwatchVision/blob/main/recruitercomments.png"/>
</p>

<p align="center">
<img src="https://github.com/gcmaidana/OverwatchVision/blob/main/experience1.png"/>
</p>


<p align="center">
<img src="https://github.com/gcmaidana/OverwatchVision/blob/main/experience2.png"/>
</p>



# Inspiration

In this project, when I detect a win or a loss in a game and I update the record, that record will be reflected on screen through [OBS](https://obsproject.com/) while someone is livestreaming. I knew this was technically feasible because I saw this cool project of someone training an AI to fight an enemy in the game Elden Ring, the project is called [EldenRingAI](https://github.com/jameszampa/EldenRingAI). Whenever the AI was defeated, a counter on the screen would be updated to show how many times attempts the AI has made thus far. Because I came across this cool project, I knew there was a way I could mess with the numbers in my win-loss record in an automated way and get it to show up in OBS. Below is a screenshot of the EldenRingAI project I came across.

<p align="center">
  <img src="https://github.com/gcmaidana/OverwatchVision/blob/main/eldenringai.jpg"/>
</p>

<br>
Another project that I took inspiration from is this [Dark Souls death counter project that uses OCR](https://github.com/Jan-9C/deathcounter_ocr/). In Dark Souls, when a player dies, the text "YOU DIED" shows up on screen, and this project detects that text to add to the counter. Below is a screenshot of the project

<p align="center">
  <img src="https://github.com/gcmaidana/OverwatchVision/blob/main/readmeDeathcounter.png"/>
</p>

I took inspiration from the Dark Souls project by wanting to use OCR to figure out when an event happens (win or loss) and I took inspiration from the EldenRingAI project by wanting to automatically update the record through writing to the text file and having that be reflected on screen through OBS.
# How the Program Works

The steps of this program can be broken up into 4 basic steps:
* Image acquisition (Grab a screenshot)
* Image manipulation (Pre-process the screenshot using OpenCV)
* Obtaining relevant information (Use Tesseract to detect text from the pre-processed image)
* Decision making (If we detect a win or loss, update the record appropriately)

# Limitations

This program will have limitations that you should be aware of

* The text detection is not 100% accurate. That goes without saying since Tesseract isn't perfect. Additionally, Overwatch has an animation for the victory, and defeat screens, as well text at various points in the game depending on what you are doing, as well as different shades of lighting which can affect text detection.

* I am assuming the user is using 1920x1080 resolution. The screenshot and crop configurations are for 1920x1080, so if you use a different resolution, then you would have to change the crop configurations as well as the capture screenshot functionality.

* I use a dual monitor setup and I am testing on that, so if you use 2 or more monitors, you may have the wrong screen being screenshot depending on which monitor you are actually playing on. Maybe try swapping your screens in the Windows settings if this is actually an issue you encounter, I did not encounter this issue, personally.

* I play games in English. While Tesseract can detect text in different languages, you would need to configure this during the Tesseract installation and modify the program to detect the specific strings in your language of choice if your game is not in English.

* Part of what makes this project particularly tricky is we are detecting 2 different possible conditions rather than only one. Goes without saying that when we add more conditions, the program gets ever more complex and imperfect.

* When conditions are detected, the program will sleep for 5 minutes to avoid false positives, as it's unlikely you'll finish another game within that time frame. The problem with this, however, is if you have a false positive trigger to begin with, you won't have the program work for 5 minutes. So, you would need to stop and re-run the program. Additionally, the record will need to be manually reset in OBS.

* Night time maps in Overwatch can lead to less accurate detections

* This is not too serious of a limitation, but I initially included draws, but don't anymore. It's not "impossible" to get a draw, but it's very difficult as 2cp (or "Assault") is not really a standard game mode in Quick Play or Ranked Play. It is an arcade / custom game mode. I am not sure if the new Clash game mode (which is similar to 2cp) coming out in the future will lead to more frequent draws, but as it currently stands, draws are incredibly, incredibly difficult to achieve so I did not include draws as a possibility. As I said previously, the more conditions we add to the program to detect, the more complex and the harder it gets to accurately detect things, so I have decided to exclude draws as it made this program less accurate and less useful when I was also detecting draws.

# Set up
Install Tesseract-OCR from here, [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

```bash
pip install pytesseract 
```
```bash
pip install opencv-python
```
```bash
pip install python-Levenshtein
```
```bash
pip install PyAutoGUI
```

Make sure you have a TESSDATA_PREFIX system variable in your environment variables, and set the path to your tessdata folder. Mine is like this: F:\Tesseract-OCR\tessdata

You will also need to add a new path to your User Variables in your environment variables and add the Tesseract path, mine is: F:\Tesseract-OCR

To know everything is good, go to your command prompt and type "Tesseract --version" and if it works, then you should be good to go.

Run the main.py file in Visual Studio Code or whatever works for you.


# Versions
Python 3.11.3

pip 22.3.1

pytesseract 0.3.10

opencv-python 4.7.0.68

Tesseract (from UB-Mannheim) 5.4.0, 64 bit

PyAutoGUI 0.9.54

python-Levenshtein 0.25.1



