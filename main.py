from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import os

product_details = []

# create a new ChromeDriver service using the webdriver_manager package
service = Service(ChromeDriverManager().install())

# create a new Chrome webdriver instance
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

# define the path of the txt file containing the product URLs
url_file = os.path.join(os.getcwd(), "product_urls.txt")

try:
    # open the txt file containing the product URLs
    with open(url_file, "r") as file:
        urls = [url.strip() for url in file.readlines()]

    # iterate over the URLs and retrieve the delivery information for each product
    for url in urls:
        # load the webpage using the URL
        driver.get(url)

        # wait for the page to load
        driver.implicitly_wait(10)

        try:
            # find the "Down arrow" option for delivery information using the appropriate selectors
            down_arrow = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, 'IwHyBY')))

            # hover over the "Down arrow" option to make the delivery information visible
            ActionChains(driver).move_to_element(down_arrow).perform()

            # find all the elements that contain the delivery options using the appropriate XPath
            delivery_options_elements = WebDriverWait(driver, 20).until(ec.presence_of_all_elements_located(
                (By.XPATH,
                 '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[4]/div/div[3]/div/div[3]/div[3]/div[2]/div[2]/div/div[2]/div/div')))

            # extract the delivery options from each element and concatenate them into a single string
            delivery_options = ", ".join([product.text for product in delivery_options_elements])

            # print the delivery options for the current product
            print(delivery_options)

        except Exception as e:
            print(f"Error retrieving delivery information for URL: {url}. Error message: {str(e)}")

except Exception as e:
    print(f"Error retrieving URLs from the file {url_file}. Error message: {str(e)}")

finally:
    driver.close()
