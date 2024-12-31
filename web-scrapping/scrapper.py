
#Names: Leen Abhari, Simrah Shabandri

from bs4 import BeautifulSoup as bs
from selenium import webdriver as se
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = se.Chrome()

driver.get("https://www.rit.edu/dubai/directory")

#for loop to click 'load more' 5 times
for i in range(5):
        button = driver.find_element(By.CLASS_NAME,"see-more") #selecting the element from its class
        driver.execute_script("arguments[0].scrollIntoView(true);", button) #scrolls to element so that it can be clickable (doesnt work without this for sum reason)
        button.click()
        print('Load More Button Clicked: ' , i+1)
        time.sleep(3) #waits for 3 seconds to give the page time to load

#using soup from the loaded page
soup = bs(driver.page_source, "html.parser") #to extract html code of the webpage
driver.quit()

employee_blocks = soup.select('div.col-xs-12.col-sm-5.person--info')  # selecting the div that includes the information of employees
employees = [] #empty list for employees

count=0  
for block in employee_blocks:
        # extract name
        name = block.select_one('div.pb-2 a').get_text(strip=True) if block.select_one('div.pb-2 a') else " "
        
        # extract title
        title = block.select_one('div.pb-2.directory-text-small').get_text(strip=True) if block.select_one('div.pb-2.directory-text-small') else " "
        
        # extract email
        email_block = block.find_next_sibling('div', class_='col-xs-12 col-sm-4 person--extra-text')
        email = email_block.select_one('a[href^="mailto:"]').get_text(strip=True) if email_block and email_block.select_one('a[href^="mailto:"]') else " "
        
        # append to the list
        employees.append({'Name': name, 'Title': title, 'Email': email})
        count+=1

print("Entries Fetched!")

df = pd.DataFrame(employees, columns=["Name", "Title", "Email"])

# save to CSV
df.to_csv("directory.csv", index=False)
print("No of Entries: ",count)
print("CSV File 'directory' Created!")