#Importing all neccessary libraries
from selenium import webdriver  #Automate browser activities
from bs4 import BeautifulSoup #Parsing HTML Page
import pandas as pd #to store and extract data

#Configuring webdriver to use Chrome browser and Seeting path of the driver
driver = webdriver.Chrome("C:\\Users\\mishr\\Downloads\\chromedriver_win32\\chromedriver.exe")

#Providing Data URL to the driver
driver.get("https://www.gkseries.com/general-knowledge/geography/geo-tectonics/geography-mcqs")

#Creating the base URL it will be used for getting data from multiple pages
baseurl = "https://www.gkseries.com/general-knowledge/geography/geo-tectonics/"

#creating dataframe
df = pd.DataFrame(columns=['Question','Options','Answer'])

#extracting data and storing data as per requirement
content = driver.page_source
soup = BeautifulSoup(content,features= "html.parser")
for i in soup.findAll('li',attrs={'itemprop':'position'}):
    link = i.a.attrs['href'] #getting links of multiple pages
    url = baseurl+link
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content,features= "html.parser")
    #Retrieving data by using the attritutes of html element
    for a in soup.findAll(attrs={'class':'mcq'}):
        temp_question = a.find('div', attrs={'class':'question-content clearfix'}).text
        temp_options = a.find('div', attrs={'class':'options'}).text
        temp_answer = a.find('div', attrs={'class':'card card-block'}).text
        #Replacing \n \t 
        question = temp_question.replace('\t', '')
        final_question = question.replace('\n', '')
        options = temp_options.replace('\t', '.')
        final_options = options.replace('\n', '')
        final_answer = temp_answer.replace('\n','')
        #Appending the data extracted
        df = df.append({'Question': final_question, 'Options':final_options, 'Answer':final_answer}, ignore_index=True)
#Importing data to csv file
df.to_csv('GKSeries_Scrapping.csv', index=False, encoding='utf-8')
#print(df)
