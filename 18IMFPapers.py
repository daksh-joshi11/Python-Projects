#########################################
## Program to fetch IMF Working Papers ##
## And write summary in a created file ##
#########################################

###### Part I: Fetching Papers

### Importing relevant libraries

#Time and date
from datetime import date
from datetime import time

#Sleep functionality
import time

#Requests
import requests

#BeautifulSoup
from bs4 import BeautifulSoup

###Selenium Libraries

#Webdriver
from selenium import webdriver

#Keys
from selenium.webdriver.common.keys import Keys

###
###
today = date.today()

### Intro: opening safari, opening website

driver = webdriver.Safari()
driver.maximize_window()
driver.implicitly_wait(15)

try:
    print("\n Loading... \n")
    driver.get('https://www.imf.org/en/publications/search?when=After&series=IMF+Working+Papers')
    print("\n IMF Paper Search loaded. \n")
except:
    print("\n IMF Paper Search currently unavailable. Please try again later.\n")
    driver.quit()
    quit()

### Welcome
print("\n Welcome to the IMF Paper Search Program!\n")
print("Kindly enter your search queries below! \n")

### Fetch Search queries from user
#Paper info
ptitle = input("\n Enter Paper Title | Press Enter to move forward or skip. \n")
pauthor = input("\n Enter Paper Author | Press Enter to move forward or skip. \n")
pkeyword = input("\n Enter Subject/Keyword | Press Enter to move forward or skip. \n")

### Multipage search functionality in future
#Search pages number
#try:
#    pages = int(input("\n Enter number of pages to load. Recommended: 1.\n Please enter numbers only: \n"))
#except:
#    print("\n Error in input. Please re-run the program.\n")

### Detecting respective search boxes
try:
    stitle = driver.find_element_by_id('TitleInput')
    sauthor = driver.find_element_by_id('AuthorEditorInput')
    skeyword = driver.find_element_by_id('SubjectKeywordInput')
except:
    print("\n Failed to detect search box. Please troubleshoot \n")
    driver.quit()
    quit()

### Input search queries
try:
    stitle.send_keys(ptitle)
    sauthor.send_keys(pauthor)
    try:
        skeyword.send_keys(pkeyword, Keys.ENTER)
        print("\n Search queries input successfully. \n")
    except:
        print("\n Unable to load search results. Please troubleshoot. \n")
        driver.quit()
        quit()

except:
    print("\n Failed to input queries. Please troubleshoot.\n")
    driver.quit()
    quit()

###Selecting Working Paper
#try:
    #wp = driver.find_element_by_css_selector('option[value = "IMF Working Papers"]')
    #wp.click()
#except:
    #print("\n Working Paper Selection not working. Please troubleshoot. \n")


#
#
#

#### Archive Start ####
### Click and iterate through every paper box
#DJ: a way to click on every paper link without commonness

#all_links = driver.find_elements_by_tag_name('a')
#for link in all_links:
#    if "/en/Publications/WP/Issues" in link.get_attribute('outerHTML'):
#        link.click()
#        time.sleep(1)
#### Archive End ####

##### Fetching url of every paper on page, then will run soup on each

### Problem: need html of new page which has search results
###can do either by getting updated source or
###getting updated url and then reopening driver with new url
###anything assoc with driver doesnt work and
###bs4 needs url in the first place
###getting url from the sourcecode using find_element somehow is the only option

#Possible Solution
time.sleep(3)

#Fetch page source
source_code = driver.page_source

#Souping
soup = BeautifulSoup(source_code, 'html.parser')

#Paper box
pbox = soup.find_all("div", class_ = "result-row pub-row")

##### Opening file
#### Fetching link of every paper
with open("IMF Papers and Summary.txt", "w+") as IMFfile:

    IMFfile.write("\n")
    IMFfile.write("*****************************************\n")
    IMFfile.write("** IMF Papers Search and Fetch Program **\n")
    IMFfile.write("*****************************************\n")
    IMFfile.write("\n\n")
    IMFfile.write(f"IMF Paper Search and Fetch on: {today}\n\n")
    IMFfile.write(f"You searched for:\n\n")
    IMFfile.write(f"Title: {ptitle}\n\n")
    IMFfile.write(f"Author: {pauthor}\n\n")
    IMFfile.write(f"Keyword: {pkeyword}\n\n")
    IMFfile.write("Today's papers are:\n \n")

    for counter, paper in enumerate(pbox):
        partial_link = paper.find('a')['href']   #['attribute'] fetches the equal to value of att
        full_paper_link = "https://www.imf.org" + partial_link
        ###
        paper_web = requests.get(full_paper_link).text
        soup = BeautifulSoup(paper_web, 'html.parser')

        ### Paper Info
        title = soup.find('h2').text
        #
        divtag = soup.find('div', class_ = "column-padding")
        author = divtag.section.p.next_sibling.next_sibling.a.text
        date = divtag.section.contents[9].text  ##### .contents is a MUCH better...
        # ...way to navigate html tree
        stripped_date = date.strip()
        summary = divtag.section.contents[19].text

        print("\n Paper No.", counter + 1, ":", title, "\n| ** HTML fetched ** | \n")
        print("Feeding in file...\n")

        ### File writinhg
        IMFfile.write(f"{counter + 1}.) {title}\n\n")
        IMFfile.write(f"Written by: {author}\n")
        IMFfile.write(f"Date: {stripped_date}\n\n")
        IMFfile.write("Paper Summary:\n\n")
        IMFfile.write(f"{summary}\n\n")
        IMFfile.write(f"Like it? Find the paper at: {full_paper_link}\n\n")
        IMFfile.write("********************\n\n")

        if counter == 9:
            IMFfile.write("******** End of Program ********")
            print("File feed successful.\n\n")

### Future: Multi page functionality ###



### End Browser selenium session
time.sleep(10)
try:
    driver.quit()
    print("\n Browser session closed successfully. \n \n")
except:
    print("\n Browser failed to close. Please troubleshoot.\n \n")
