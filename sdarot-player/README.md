# Sdarot-Player
client for Sdarot Website

## Install Option's
you can "install" the script either by  

1.  downloading the .exe \ bin file or running as a script so you could play with it
2.  running as a script so you could play with it

## Dowloding executable
**Requirements**
  - MPV (if you want to play with local player and not web player)
  - Selenium Driver

*the instruction to install requerments are at the end 

### Links
Linux - https://gitlab.com/kvothe42-public/sdarot-player/-/jobs/2978579305/artifacts/file/dist/sdarot-player

Windows - https://gitlab.com/kvothe42-public/sdarot-player/-/jobs/2978579303/artifacts/file/dist/windows/sdarot-player.exe

## Runnig Script

**Requirements**
  - Python3
  - MPV (if you want to play with local player and not web player)
  - Selenium
  - BeautifulSoup4
  - requests (Requests: HTTP for Humans™)
  - Selenium Driver

## Module's Install Commands \ Instructions

***Remember the Script is written in python3 hence python  = python3 with how its saved at your computer**

*Requests*
```
python -m pip install requests
```

*Beautifulsoup4*
```
python -m pip install beautifulsoup4
```

**Selenium**
```
python -m pip install selenium
```
#### Selenium Driver install
Driver link: https://github.com/mozilla/geckodriver/releases
1.  Go To the link and download depending on your os
2. Extract and than Either
  - Add to your Computer PATH (in linux $PATH | in Windows Enviromental Variable)
  - Or Place where you want and Specify in the Configuration Setup

## MPV Installation Guide

### Windows

Download Link https://mpv.io/installation/
 1. download and extract
 2. run updater.bat \  updater.ps1

 ### Linux (Debian \ Ubuntu {apt})

 adding Repository
 ```
 sudo add-apt-repository ppa:mc3man/mpv-tests
 ```
updating repository's
 ```
 sudo apt-get update
 ```
Installing
 ```
 sudo apt-get install mpv
 ```

## Program Instructions

at First Run add --config for creating the Software configuration (there a setup don't worry :-))

after that Enjoy there is instructions in the program
