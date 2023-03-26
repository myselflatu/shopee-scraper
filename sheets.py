from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# create a new ChromeDriver service using the webdriver_manager package
service = Service(ChromeDriverManager().install())

# create a new Chrome webdriver instance
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

# define the URL of the Google Sheet containing the product URLs
url = "https://docs.google.com/spreadsheets/u/0/d/1QQj8gAD9jexgz2OoYEyQOIe7xVSG-0r0FyTDHSAYYg0/htmlview#gid=0"

# load the webpage using the URL
driver.get(url)

# wait for the page to load
driver.implicitly_wait(10)

try:
    with open('product_urls.txt', 'w') as f:
        for r in range(1, 121):
            # retrieve the link from the current row
            link = driver.find_element(By.XPATH, f'//*[@id="0"]/div/table/tbody/tr[{r}]/td/div/a')
            url = link.get_attribute('href')
            # write the link to the file
            f.write(url + '\n')

except Exception as e:
    print(e)

finally:
    driver.quit()