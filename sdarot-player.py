#SLENIUM import's
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
#rest of the module import
from re import compile as RegCompile
#type ignore comments is for mt[py] so he wont scream at me just becouse i dident written a scrub file for this library
from bs4 import BeautifulSoup # type: ignore
from sys import exc_info,argv
from os import getcwd,popen
#type ignore comments is for mt[py] so he wont scream at me just becouse i dident written a scrub file for this library
import requests # type: ignore
import time

#Function Declaration Part

def ShowSearch(search_string):
    """Search logic for searching shows usage ShowSearch("<Show Name>") return's only the Show ID(int)"""
#Getting parsable page object
    #getting Url page and if he gets a show page return show ID
    try:
        r = requests.get(rf"https://sdarot.tv/search?term={search_string}")
    except requests.exceptions.SSLError:
        print("enterd requests.exceptions.SSLError")
        if "search" not in str(exc_info()):
            return str(exc_info()[1]).split("/")[2].split("-")[0]
        else:
            print("There are Not Result Found")
            print("Have A GOOD DAY SIR!! \n\n")
            print("I Said GOOD DAY!!!!!")
    except requests.exceptions.ConnectionError:
        input("There was an error please check if your connected to the internet or if the site is up and try again \n press enter to close the program")
        quit()



    #Parsing into Soup object
    soup = BeautifulSoup(r.text, "html.parser")

    #Getting search Divs
    Search_Results = soup.findAll(class_= "sInfo")

#extraction of information part and validation
    Show_ID_List = []
    Optinon_Num = 0
    if len(Search_Results) != 0:
        print("Please enter the number of the show you want to watch")
        for Show in Search_Results:
            Optinon_Num += 1
            #explantion for the horror below: first () for slicing to the start of ShowID by index secound () for slicing the excess from ShowID by split methood and than selecting from lthe list ShowID
            Show_ID_List.append(((f"https://www.sdarot.tv{Show.a['href']}")[28:].split("-"))[0])
            print(f"    {Optinon_Num}.  {Show.h5.string} - {Show.h4.string}")

            #Visual new line for beuty
            if Show == Search_Results[-1]:
                print("")


#Show selection loop
        while True:
            try:
                Show_Select = int(input())
                if 1 <= Show_Select <= len(Search_Results):
                    return Show_ID_List[Show_Select - 1]

            except ValueError:
                print("please enter only a valid number")
    #for in case the the certificate is fine and theres only one option so he goes diractly to show page
    elif "watch" in r.url:
        #the horror is to slice just the ID from Url by / and by - (.../watch/<ID>-<Show Name>)
        return r.url.split("/")[4].split("-")[0]

    else:
        print("There are Not Result Found")
        print(r.url)
        quit()








def EpSe_Selector (ShowID,Mode,Season = None):
    """Search logic for selecting dinamecly Episode / Season usage EpSe_Selector(<ShowID>,<Mode [Se | Ep], Season (Neede Only with Episode Selection (Mode = Ep) Default = None)> return's only the Number"""
#managing argumet selection Mode and Argument value and Raising an error if not correct
    Mode = Mode.lower()
    if (Mode != "se") and (Mode != "ep"):
        Mode_Error= ValueError(f" {Mode} is an Incorrect option Select [Se | Ep]")
        raise Mode_Error

    elif (Mode == "ep") and (Season == None):
        Season_Mode_Error = ValueError(f" if Mode = {Mode}, Season HAVE to be PASSED !!!")
        raise Season_Mode_Error

    elif (Mode == "ep") and (Season != None):
        try:
            Season = int(Season)
        except:
            Season_Type_Error = ValueError(f" if Mode = {Mode}, Season HAVE to be a NUMBER !!!")
            raise Season_Type_Error

#selecring Season
    #managing selection and variables depending on mode
    if Mode == "se":
        r = requests.get(rf"https://sdarot.tv/watch/{ShowID}")
        List_Type = "Season"
        Data_Attribute_Type = "data-season"

    elif Mode == "ep":
        r = requests.get(rf"https://sdarot.tv/watch/{ShowID}/season/{Season}")
        List_Type = "Episode"
        Data_Attribute_Type = "data-episode"

    #Parsing into Soup object
    soup = BeautifulSoup(r.text, "html.parser")

    #Getting search Divs
    Search_Results = soup.findAll("li",attrs={Data_Attribute_Type : RegCompile(".")})


    while True:
        try:
            Season_Episode_Select = int(input(f"Select {List_Type} [0 - {len(Search_Results)}] \n"))
            break
        except ValueError:
            print("Enter Numbers Only !!!")
    return Season_Episode_Select


#Configuration Setup & Creating needed Files

Arguments = argv

if len(Arguments) > 1:
    if Arguments[1].lower() == "--config":
        print("This is importenet Follow the instruction because if not the program wont work ")
        Use_MPV =  input("please enter if you want to Use MPV [True | False] : ")
        if Use_MPV.lower() == "true":
            Use_MPV = "True"
            MPV_Path = input(r"Please enter MPV Folder FULL PATH (Exemple: C:\Users\Moshe\Downloads\mpv) : ")
            Cookies_File_Location = input(r"Please enter Wanted Cookies Folder FULL PATH (Exemple: C:\Users\Moshe\Downloads\mpv\Cookies) if you want in the script folder klick Enter ")
            if Cookies_File_Location == "":
                Cookies_File_Location = getcwd()
            Linux_Windows = input("Please enter your os [Win | Lin] (Mac is Linux for this script) : ")

            if Linux_Windows.lower() == "win":
                MPV_Path = MPV_Path + "\\"
                Cookies_File_Location = Cookies_File_Location + "\\"
            elif Linux_Windows.lower() == "lin":
                MPV_Path = MPV_Path + r"/"
                Cookies_File_Location = Cookies_File_Location + r"/"

            print("Creating Config File" )

            Conf_File = open("Sdarot-Player.conf", "w")
            Conf_File.write(f"Use MPV = {Use_MPV}\n")
            Conf_File.write(f"MPV Path = '{MPV_Path}mpv'\n")
            Conf_File.write(f"Cookies Path = '{Cookies_File_Location}Sdarot-Player.cookie'\n")
            Conf_File.close()
            print("Config File Created Have a good day")
            quit()
        elif Use_MPV.lower() != "true":
            print("there is nothing to configer than \n      ---exiting---")
            quit()



#Getting the Show Season Episode Details
Search_String = input(" Please Enter Show's Name \n")
Show = ShowSearch(Search_String)
Season = EpSe_Selector(Show,"Se")
Episode =EpSe_Selector(Show,"Ep",Season)
print("Opening Episode")

#Making the Complete Url
Url = f"https://sdarot.tv/watch/{Show}/season/{Season}/episode/{Episode}"

#Running selenium driver to open timer for Episode
driver = webdriver.Firefox()
driver.get(Url)

#Making sure Were in the right page and opened
assert "Sdarot.TV" in driver.title
if True:
    #Getting Episode content
    try:
        element = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.ID, "videojs_html5_api"))
        )
        element = driver.find_element(By.ID,"videojs_html5_api")
        Url = element.get_attribute("src")
        print(Url)

        #reading Conf File For Path's
        File = open("Sdarot-Player.conf","r")
        Lines = File.readlines()
        File.close()
        #cleaning Path's
        Cookies_Path = Lines[2].split(r"'")[1]
        MPV_Player = Lines[1].split(r"'")[1]

        #chacking if play methood configured is MPV
        if Lines[0].strip() == "Use MPV = True":

            #Reading cookies from site for video authontication
            Cookies = driver.get_cookie("Sdarot")
            # Closing Driver seesson
            driver.quit()
            #Filling blanks and Formating for writing
            Cookies_at_date = 0
            Cookies_Contain_SubDomains = "True"
            Cookies_Netscape_Format = f"{Cookies['domain']}\t{Cookies_Contain_SubDomains}\t{Cookies['path']}\t{Cookies['secure']}\t{Cookies_at_date}\t{Cookies['name']}\t{Cookies['value']}"
            #Writing to cookie file
            Cookies_File = open(f"{Cookies_Path}", "w")
            Cookies_File.write(Cookies_Netscape_Format)
            Cookies_File.close()
            #Creating the Player Command
            Player_Command = fr'"{MPV_Player}" --cookies --cookies-file="{Cookies_Path}" "{Url}"'
            #Running the Commend in the CLI
            Player_Runner = popen(Player_Command)
            print(Player_Runner.read())
            input("click when ended")

        elif Lines[0].strip() != "Use MPV = True":
            driver.get(Url)
            input("click when ended")
            driver.quit()

    except:
        driver.quit()
