# TTS-
This repo is for my exp in generating audiobook using tts like edge tts

#audiobookmaker.py
-when used will turn everything in the (chapters)- folder into a audio files the generated audio file will look like 
chapter_0001.mp3
chapter_0002.mp3
etc.
the stuff inside the chapters folder will need to be in .txt format

the files that will be made will be put into a file called "LOTM Audiobook"
just rename it to whatever you want 

#check_files.py
-this will list out all the files in chapters folder it will also mean if this file works then the audiobookmaker.py will also work fine 

#missingchapterfinder.py
-this will find if there are any missing chapters in the( chapters ) folder if there are it will list it out it.

#missingchaptergenerator.py
-this script will generate the missing chapters that is found by the missingchaptersfinder.py this generates mp3 files 
