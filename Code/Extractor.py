from asyncio.windows_events import NULL
from pandas import notnull
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from pathlib import Path

from InputReader import InputReader
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
    cwd = os.getcwd()
    print(f"Path = {cwd}")
    input=InputReader("Code\Input.xlsx")
    print(f"input read succfully with size{input.data.shape}")
    urlsList=input.data["URL"]
    extractor_obj=DataExtractor()
    for url in urlsList:
        print(f"Reading URl {url}")
        if url != NULL and url !="":
            extractor_obj.openUrl(url)
            data= extractor_obj.findElementByClassName("td-post-content")
            print(f"Data Extracted for Urls {url}\n")
            output_file = Path(cwd+f"\\Code\\Data\\{url[8:-2]}.txt")
            output_file.parent.mkdir(exist_ok=True, parents=True)
            with open(output_file,"w",encoding="utf-8") as f:
                f.writelines(data.text)
                print(f"Data Written in the files successfully")
