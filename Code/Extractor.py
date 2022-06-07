from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
class DataExtractor:
    
    #Constructor 
    def __init__(self) -> None:
        try:
            #installs the chrome driver
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        except Exception as e:
            print(f"Exception occured at DataExtractor Constructor {e}")
    
    def openUrl(self, url):
        try:
            if self.driver:
                self.driver.get(url)
        except Exception as e:
            print(f"Exception at opening URL {e}")
    
    def findElementByClassName(self, atical_path):
        #element= self.driver.find
        element= self.driver.find_element_by_class_name(atical_path)
        return element

if __name__=="__main__":
    extractor_obj=DataExtractor()
    extractor_obj.openUrl("https://insights.blackcoffer.com/impacts-of-covid-19-on-vegetable-vendors-and-food-stalls/")
    data= extractor_obj.findElementByClassName("td-post-content")
