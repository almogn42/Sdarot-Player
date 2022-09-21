#SLENIUM import's
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import selenium.common.exceptions
#rest of the module import
from re import compile as RegCompile
#type ignore comments is for my[py] so he wont scream at me just becouse i dident written a scrub file for this library
from bs4 import BeautifulSoup # type: ignore
from sys import exc_info,argv,exit
from os import getcwd,popen
#type ignore comments is for my[py] so he wont scream at me just becouse i dident written a scrub file for this library
import requests # type: ignore
import time
import asyncio

#Function Declaration Part
def Argument_Parser(arguments):
    """Function for Argument parsing all the parsing is made inside the function pass only the argument list \n\t Usage: Argument_Parser(Arguments)"""

    #sdarot Default wesite link variable
    Sdarot_Default_Link = r"https://sdarot.tw"

    if len(arguments) > 1:

        #argument is config
        if arguments[1].lower() == "--config":

            #configuring if mpv is wanted
            print("This is importenet Follow the instruction because if not the program wont work ")
            Use_MPV =  input("please enter if you want to Use MPV [True | False] : ")
            Driver_Path = input("\nPlease Enter Selenium Driver Folder FULL PATH (Exemple: C:\\Users\\Moshe\\Downloads\\mpv) \n\tif the Driver is in PATH (Windows: enviromental variables path) Than Press Enter :\n")
            #checking for Driver
            if Driver_Path.strip() == "":
                Driver_Path = "False"

            #further confugartions if mpv is wanted
            if Use_MPV.lower() == "true":
                Use_MPV = "True"
                MPV_Path = input(r"Please enter MPV Folder FULL PATH (Exemple: C:\Users\Moshe\Downloads\mpv) : ")
                Cookies_File_Location = input(r"Please enter Wanted Cookies Folder FULL PATH (Exemple: C:\Users\Moshe\Downloads\mpv\Cookies) if you want in the script folder Press Enter ")


                if Cookies_File_Location == "":
                    Cookies_File_Location = getcwd()



                Linux_Windows = input("Please enter your os [Win | Lin] (Mac is Linux for this script) : ")

                if Linux_Windows.lower() == "win":
                    MPV_Path = MPV_Path + "\\"
                    Cookies_File_Location = Cookies_File_Location + "\\"
                    if Driver_Path != "False":
                        Driver_Path = Driver_Path + "\\" + "geckodriver.exe"

                elif Linux_Windows.lower() == "lin":
                    MPV_Path = MPV_Path + r"/"
                    Cookies_File_Location = Cookies_File_Location + r"/"
                    if Driver_Path != "False":
                        Driver_Path = Driver_Path + r"/" + "geckodriver"

                print("Creating Config File" )

                #Writing all the configurations decided erlier
                Conf_File = open("Sdarot-Player.conf", "w")
                Conf_File.write(f"Use MPV = {Use_MPV}\n")
                Conf_File.write(f"MPV Path = '{MPV_Path}mpv'\n")
                Conf_File.write(f"Cookies Path = '{Cookies_File_Location}Sdarot-Player.cookie'\n")
                Conf_File.write(f"Driver Path = '{Driver_Path}'\n")
                Conf_File.write(f"OS Type = {Linux_Windows.upper()}\n")
                Conf_File.write(f"Sdarot Website Link = '{Sdarot_Default_Link}'\n")
                Conf_File.close()
                print("Config File Created Have a good day")
                exit()

            elif Use_MPV.lower() != "true":
                #setting MPV state
                Use_MPV = "False"
                MPV_Path = "False"
                Cookies_File_Location = "False"
                Linux_Windows = input("Please enter your os [Win | Lin] (Mac is Linux for this script) : ")
                #Getting Path right Depend on OS
                if (Linux_Windows.lower() == "win") and (Driver_Path != "False"):
                    Driver_Path = Driver_Path + "\\" + "geckodriver.exe"

                elif Linux_Windows.lower() == "lin" and (Driver_Path != "False"):
                    Driver_Path = Driver_Path + r"/" + "geckodriver"

                #Writing configurations
                Conf_File = open("Sdarot-Player.conf", "w")
                Conf_File.write(f"Use MPV = {Use_MPV}\n")
                Conf_File.write(f"MPV Path = '{MPV_Path}'\n")
                Conf_File.write(f"Cookies Path = '{Cookies_File_Location}'\n")
                Conf_File.write(f"Driver Path = '{Driver_Path}'\n")
                Conf_File.write(f"OS Type = {Linux_Windows.upper()}\n")
                Conf_File.write(f"Sdarot Website Link = '{Sdarot_Default_Link}'\n")
                Conf_File.close()
                print("Config File Created Have a good day")
                exit()


def ShowSearch(search_string):
    """Search logic for searching shows usage ShowSearch("<Show Name>") return's only the Show ID(int)"""
#Getting parsable page object
    #getting Url page and if he gets a show page return show ID
    try:
        r = requests.get(rf"{Sdarot_Link}/search?term={search_string}")
    except requests.exceptions.SSLError:
        #print("enterd requests.exceptions.SSLError")
        if "search" not in str(exc_info()):
            return str(exc_info()[1]).split("/")[2].split("-")[0]
        else:
            print("There are Not Result Found")
            print("Have A GOOD DAY SIR!! \n\n")
            print("I Said GOOD DAY!!!!!")
    except requests.exceptions.ConnectionError:
        input("There was an error please check if your connected to the internet or if the site is up and try again \n press enter to close the program")
        exit()



    #Parsing into Soup object
    soup = BeautifulSoup(r.text, "html.parser")

    #Getting search Divs
    Search_Results = soup.findAll(class_= "sInfo")

#extraction of information part and validation
    Show_ID_List = []
    Show_Name_List = []
    Optinon_Num = 0
    if len(Search_Results) != 0:
        print("Please enter the number of the show you want to watch")
        for Show in Search_Results:
            Optinon_Num += 1
            #explantion for the horror below: first () for slicing to the start of ShowID by index secound () for slicing the excess from ShowID by split methood and than selecting from lthe list ShowID
            Show_ID_List.append(((f"https://www.sdarot.tw{Show.a['href']}")[28:].split("-"))[0])
            Show_Name_List.append(fr"{Show.h4.string} - {Show.h5.string}")
            print(f"    {Optinon_Num}.  {Show.h5.string} - {Show.h4.string}")

            #Visual new line for beuty
            if Show == Search_Results[-1]:
                print("")


#Show selection loop
        while True:
            try:
                Show_Select = int(input())
                if 1 <= Show_Select <= len(Search_Results):
                    return Show_ID_List[Show_Select - 1], Show_Name_List[Show_Select - 1]

            except ValueError:
                print("please enter only a valid number")
    #for in case the the certificate is fine and theres only one option so he goes diractly to show page
    elif "watch" in r.url:
        #getting show name from page (findall fuction) the replace is for replacing the / to - for uniform show naming
        Show_String1 = ((soup.findAll("h1")[1].strong.contents[0].text).replace("/", "")).strip()
        Show_String2 =  soup.findAll("h1")[1].span.contents[0].text
        Show_Name = f"{Show_String1} - {Show_String2}"


        #the horror is to slice just the ID from Url by / and by - (.../watch/<ID>-<Show Name>)
        print("stright in")
        return r.url.split("/")[4].split("-")[0], Show_Name


    else:
        print("There are Not Result Found")
        print(r.url)
        exit()


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

#selecring Season \ Episode
    #managing selection and variables depending on mode
    if Mode == "se":
        r = requests.get(rf"{Sdarot_Link}/watch/{ShowID}")
        List_Type = "Season"
        Data_Attribute_Type = "data-season"

    elif Mode == "ep":
        r = requests.get(rf"{Sdarot_Link}/watch/{ShowID}/season/{Season}")
        List_Type = "Episode"
        Data_Attribute_Type = "data-episode"

    #Parsing into Soup object
    soup = BeautifulSoup(r.text, "html.parser")

    #Getting search Divs
    Search_Results = soup.findAll("li",attrs={Data_Attribute_Type : RegCompile(".")})


    while True:
        try:
            Season_Episode_Select = input(f"Select {List_Type} [1 - {len(Search_Results)}] \n")

            if Mode == "ep":
                #cleaning and validating the input Data
                if "-" in Season_Episode_Select:
                    #splitiing to list
                    Season_Episode_Select = Season_Episode_Select.split("-")
                    #range input validator
                    if len(Season_Episode_Select) > 2:
                        print("Enter only 1 Range (Only 1 '-')")
                        continue

                    for Num in range(len(Season_Episode_Select)):
                        #validating type and converting\ cleanig the list object to int (for Clean output)
                        int(Season_Episode_Select[Num])
                        Season_Episode_Select[Num] = int(Season_Episode_Select[Num])

                else:
                    #validating type and converting\ cleanig the list object to int (for Clean output)
                    Temp_Season_Episode_Select = int(Season_Episode_Select.strip())
                    Season_Episode_Select = [Temp_Season_Episode_Select]
                    #clearing temp variable from memory
                    del Temp_Season_Episode_Select

            elif Mode == "se":
                int(Season_Episode_Select)
                Season_Episode_Select = int(Season_Episode_Select)

            break
        except ValueError:
            print("Enter Numbers Only !!!")
    return Season_Episode_Select


async def MPV_Player_Play(Configuration_File, url ):
    """Function For Playing the video via mpv player Usage: \nMPV_Player_Play(<configuration file as list>, <Video Url> ) \nreturn's void"""
    #cleaning Path's
    Cookies_Path = Configuration_File[2].split(r"'")[1]
    MPV_Player = Configuration_File[1].split(r"'")[1]
    #Reading cookies from site for video authontication
    Cookies = driver.get_cookie("Sdarot")
    #Filling blanks and Formating for writing
    Cookies_at_date = 0
    Cookies_Contain_SubDomains = "True"
    Cookies_Netscape_Format = f"{Cookies['domain']}\t{Cookies_Contain_SubDomains}\t{Cookies['path']}\t{Cookies['secure']}\t{Cookies_at_date}\t{Cookies['name']}\t{Cookies['value']}"
    #Writing to cookie file
    Cookies_File = open(f"{Cookies_Path}", "w")
    Cookies_File.write(Cookies_Netscape_Format)
    Cookies_File.close()
    #Creating the Player Command
    Player_Command = fr'"{MPV_Player}" --cookies --cookies-file="{Cookies_Path}" "{url}"'
    #Running the Commend in the CLI
    Player_Runner = popen(Player_Command)
    # await asyncio.sleep(0)

    print(Player_Runner.read())


def After_Played_Options(episode, show_ID, season):
    """Function for desplaying and adding\selecting episode after the video played \n\t Usage: After_Played_Options(Episode <int>, Show <int>, Season <int>) """
#While loop for repeting if input is not correct
    while True:
            print("Please Enter Selection \n\n\n")
            print("[n] Next Episode")
            print("[p] Previos Episode")
            print("[s] Select Episode From Season")
            print("[r] Replay Episode")
            print("[h] Select from history")
            print("[q] Quit")

            After_Play_Selector = input()

            if (After_Play_Selector.lower() == "s") or (After_Play_Selector.lower() == "p") or (After_Play_Selector.lower() == "n") or (After_Play_Selector.lower() == "r") or (After_Play_Selector.lower() == "h") or (After_Play_Selector.lower() == "q"):

                #statment returns \ episode number attribution

                #next episode adding one and returning episode
                if After_Play_Selector.lower() == "n":
                    episode += 1
                    print(episode)
                    return [episode]


                #previous episode adding one and returning episode
                elif After_Play_Selector.lower() == "p":
                    if episode > 1 :
                        episode -= 1
                        return [episode]
                    else:
                        print("current Episode is 1 there is no Episode prior to it")
                        print("Belive me!!")
                        continue


                #Selecting episode using function & than returning episode
                elif After_Play_Selector.lower() == "s":
                    episode =  EpSe_Selector(show_ID,"Ep",season)
                    return episode


                #replaying episode and runnig video layin logic locally for not doing uneccery teps and wait time
                elif After_Play_Selector.lower() == "r":
                    print(episode)

                    #chacking if play methood configured is MPV
                    if Lines[0].strip() == "Use MPV = True":
                        MPV_Player_Play(Lines,Url)

                    elif Lines[0].strip() != "Use MPV = True":
                        driver.get(Url)

                    continue

                #Selecting episode From History
                elif After_Play_Selector.lower() == "h":
                    global Show_ID, Show_Name, Season
                    #Wierd coup out because when runnig the fuction the program expect an episode (list) setting evrithing but thr episode globally
                    Show_ID, Show_Name, Season, episode = History_Keep("Read")
                    return episode

                #quiting from program
                elif After_Play_Selector.lower() == "q":
                    print("\t\t Have a nice day :-)")
                    driver.quit()
                    exit()

            else:
                continue


def Timer_Bar(Time = 30, Bar_Leangh = 50):
    """A function to desplay bar by percent of time left \nUsage: Timer_Bar({int}<Time>,{int}<Bar Lengh> )"""
    for Secound in range(Time + 1):

        #calculating percentage and spaces
        Progress_Percent = (Secound * 100 // Time)
        Progress_Leangh = Progress_Percent * Bar_Leangh // 100
        Progress_Left = Bar_Leangh - Progress_Leangh
        #displayng

        print(f"\r[{Progress_Leangh * '#'}{Progress_Left * ' '}]{Progress_Percent}%", end="")
        time.sleep(1)
    print("")


def History_Keep(Mode ,Show_ID = 1, Show_Name = "", Season = 1, Episode = 1):
    """ Function For Writing the history to the file  \n Usage(Mode = <Write|Read> , Show_ID, Show_Name, Season, Episode)"""


    if Mode.lower() == "write":

        #checking if history file exists
        try:
            History_File = open("Sdarot-Player.hist","r+", encoding="utf-8")
        except:
            History_File = open("Sdarot-Player.hist","w+", encoding="utf-8")

        Lines_History = History_File.readlines()

        #finding if show is there and if so get index
        for Line in Lines_History:
            if Show_ID == (Line.split(","))[0]:
                print((Line.split(","))[0])
                Show_Line = Lines_History.index(Line)
                Show_Found = True
                break
            else:
                Show_Found = False
        if len(Lines_History) == 0:
            Show_Found = False

        #Writing the current episode & Season based if exist in file or not
        if Show_Found == True:
            Lines_History[Show_Line] = f"{Show_ID}, {Show_Name}, {Season}, {Episode[0]}\n"
            History_File.seek(0)
            History_File.writelines(Lines_History)
        else:
            text = f"{Show_ID}, {Show_Name}, {Season}, {Episode[0]}\n"
            History_File.write(text)
        History_File.close()


    elif Mode.lower() == "read":
        #Trying to open History File
        try:
            History_File = open("Sdarot-Player.hist","r", encoding="utf-8")

        except:
            Print("There is no History File Yet Go Watch some shows and try again :-)")
            input("Press Enter to exit the program")
            exit()


        Lines_History = History_File.readlines()
        History_File.close()

        #Printing list of history and selecting
        History_Show_ID = []
        Option_Counter = 0
        for Line in Lines_History:
            if (Line != None) and (Line != "\n"):

                Option_Counter += 1
                Show_ID, Show_Name, Season, Episode = Line.split(",")
                print(f"[{Option_Counter}]. {Show_Name.strip()} Se:{int(Season)} Ep{int(Episode)}")

            #History Show selection loop
                while True:
                    try:

                        History_Show_Select = int(input())

                        if 1 <= History_Show_Select <= Option_Counter:

                            Show_ID, Show_Name, Season, Episode = Lines_History[History_Show_Select - 1].split(",")
                            return Show_ID.strip(), Show_Name.strip(), int(Season), [int(Episode)]

                    except ValueError:
                        print("please enter only a valid number")


def LogIn_Post():

    Login_Body_Request = {"location":"/", "username":"kvothe42", "password":"f2Di77jRkaaGwqA", "submit_login":""}

    #getting cookies: for getting cookies wsing a session and readin cookies from theres
    with requests.Session() as Login_Session:
        Login_Session.post("https://sdarot.tw/login",data = Login_Body_Request)

        Login_Cookie = Login_Session.cookies
        return Login_Cookie.get_dict()


def Login_Func(Driver, UserName, Password):

    # Set correct user agent
    selenium_user_agent = Driver.execute_script("return navigator.userAgent;")

    Login_Body_Request = {"location":"/", "username":UserName, "password":Password, "submit_login":""}

    #getting cookies: for getting cookies wsing a session and readin cookies from theres
    with requests.Session() as Login_Session:

        Login_Session.headers.update({"user-agent": selenium_user_agent})
        for cookie in Driver.get_cookies():
            Login_Session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

            Login_Session.post("https://sdarot.tw/login",data = Login_Body_Request)

    Login_Cookie = Login_Session.cookies
    print(Login_Cookie.get_dict())


async def Async_Play_Prepare(driver,url):

    #Creating\Opening New Tab
    driver.switch_to.new_window("tab")
    driver.switch_to.new_window("tab")

    #getting a list of tabsID
    driver.window_handles

    #setting Var Name for Tabs for easy Acces
    Original_Tab = driver.window_handles[0]
    Next_Ep_Tab = driver.window_handles[1]
    Pervios_Ep_Tab = driver.window_handles[2]
    Next_Video_Url = ""
    Previous_Video_Url = ""

    #Making Url's for function
    #splitting by /
    #Base_Url = "/".join(url.split("/")[:-1]) #not Used Because of bad readability
    temp_Url = url.split("/")

    #Getting ep num
    Current_Ep_Num = int(temp_Url[-1])
    #REmoving ep num and converting to string
    temp_Url.pop()
    Base_Url = "/".join(temp_Url)
    #making astring out of it
    Next_Url = f"{Base_Url[:-1]}/{Current_Ep_Num + 1}"
    #switching to original tab
    driver.switch_to.window(Next_Ep_Tab)

    #Opening
    while True:
        try:
            driver.get(url)
            # await asyncio.sleep(30)
            # await asyncio.sleep(30)
            WebDriverWait(driver,40).until(EC.presence_of_element_located((By.ID, "videojs_html5_api")))
            element = driver.find_element(By.ID,"videojs_html5_api")
            Next_Video_Url = element.get_attribute("src")
            driver.close()
            break
        except selenium.common.exceptions.TimeoutException:
            continue

        except:

            Next_Video_Url = ""
            driver.close()
            break

    if Current_Ep_Num > 1:
        #making astring out of it
        Previous_Url = f"{Base_Url[:-1]}/{Current_Ep_Num + 1}"
        driver.switch_to.window(Pervios_Ep_Tab)
        while True:
            try:
                driver.get(url)
                # await asyncio.sleep(30)
                WebDriverWait(driver,40).until(EC.presence_of_element_located((By.ID, "videojs_html5_api")))
                element = driver.find_element(By.ID,"videojs_html5_api")
                Previous_Video_Url = element.get_attribute("src")
                driver.close()
                driver.switch_to.window(Original_Tab)
                break

            except selenium.common.exceptions.TimeoutException:
                continue

    else:
        driver.switch_to.window(Pervios_Ep_Tab)
        driver.close()
        driver.switch_to.window(Original_Tab)

    return Previous_Video_Url, Next_Video_Url

async def MPV():
    Player_Command = fr'"C:\Users\almogn\Downloads\mpv-x86_64-20220807-git-9add44b\mpv" "C:\Users\almogn\Videos\Captures\Windows PowerShell 2022-09-06 08-36-57.mp4"'
    player = popen(Player_Command)
    await asyncio.sleep(0)
    print(player.read())


async def runner(driver):

    #logging in and opening ep
    driver.get("https://sdarot.tw")
    Login_Func(driver, "kvothe42", "f2Di77jRkaaGwqA")
    Url = r"https://www.sdarot.tw/watch/203/season/1/episode/2"

    while True:
        try:
            driver.get(Url)

            WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "videojs_html5_api")))
            element = driver.find_element(By.ID, "videojs_html5_api")
            Next_Video_Url = element.get_attribute("src")
            break
        except selenium.common.exceptions.TimeoutException:
            continue


    # MPV_Player_Play(Lines, Url)
    task1 = asyncio.create_task(MPV_Player_Play(Lines,Url))
    task2 = asyncio.create_task(Async_Play_Prepare(driver, Url))

    print(task2)

async def Test_Runner(Lines,Url):
    await MPV_Player_Play(Lines,Url)



try:
    #reading Conf File For Path's
    File = open("Sdarot-Player.conf","r")
    Lines = File.readlines()
    File.close()
except:
    print("\t it Seemed there is not a configuration file in this folder \n\t Please run the Program again with --config For the Configuration setup")
    input("\t Press any key to exit program \n")
    exit()



driver = webdriver.Firefox()
driver.get("https://sdarot.tw")
Login_Func(driver, "kvothe42", "f2Di77jRkaaGwqA")
Url = r"https://www.sdarot.tw/watch/203/season/1/episode/2"
asyncio.run(Test_Runner(Lines, Url))
# MPV_Player_Play(Lines,Url)
driver.quit()
