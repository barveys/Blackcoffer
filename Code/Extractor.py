from asyncio.windows_events import NULL
from importlib.resources import path
from select import select
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

class ReadFile:
    def __init__(self, path,fileName, fileextension) -> None:
        self.fileName=fileName
        self.path= path
        self.fileExtension= fileextension
        
    def ReadFile(self, endcoding):
        try:
            lines=[]
            filepath= Path(f"{self.path}\\{self.fileName}{self.fileExtension}")
            with open(filepath,"r", encoding=endcoding) as f:
                line=f.readline()
                while line != "":
                    if line[-2:] == "\n":
                        lines.append(line[:-2])
                    else:
                        lines.append(line)
                    line =f.readline()
            return lines  
        except Exception as e:
            print(f"Exception occurenred while reading the path { self.path} ,file {self.fileName} , extension {self.fileExtension}, exception {e}")
    

def ExtractData():
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
def CleanData(current_path):
        
        print("current path ="+current_path)
        current_path=Path(current_path+"\\Code\\StopWords")
        files=os.listdir(current_path)
        stopWordList=[]
        for file in files:
            #print(file[len(file)-3:])
            print(file)
            filename= file[:-4]
            extension= file[len(file)-4:]
            if  extension== ".txt":
                readfile= ReadFile(current_path, filename, extension)
                data=readfile.ReadFile("unicode-escape")
                stopWordList.extend(data)
        #print(stopWordList)
        #print(cleanData(" ",stopWordList))
        cleanWords=[]
        for word in stopWordList:
            splited_words= word.split(" ")
            cleanWords.append(splited_words[0].strip())
        return cleanWords

def CleanTheArticleWithStopWord(current_path, stopWords):

    input_path= Path(current_path+"\Code\Data\insights.blackcoffer.com")
    output_path= Path(f"{current_path}\Code\Data\StopWordRemovedData")
    files=os.listdir(input_path)
    for file in files:
        print(file)
        filename= file[:-4]
        extension= file[len(file)-4:]
        if  extension== ".txt":
            readfile= ReadFile(input_path, filename, extension)
            lines=readfile.ReadFile("utf-8")
            newlines =[]
            if lines is not None:
                for line in lines:
                    newLine=""
                    splited_words=line.split(" ")
                    for word in splited_words:
                        if( word.lower() not in stopWords) or(word.upper() not in stopWords) or (word not in stopWords):
                            newLine=newLine+" "+word
                    newlines.append(newLine)
                output_file=Path(f"{output_path}\{filename}{extension}")
                print("-------------------------Writing the file-------------------")
                print(f"Path = {output_path}")
                with open(output_file,"w",encoding="utf-8") as f:
                    f.writelines(newlines)
                    print(f"Data Written in the files successfully")    
                            

if __name__=="__main__":
    current_path=os.getcwd()
    #ExtractData()

    print("\n------------------Reading Stop Words Started-----------------------\n")
    StopWords=CleanData(current_path)
    print("\n------------------Reading Stop Words Completed-----------------------\n")
    #print(StopWords)
    CleanTheArticleWithStopWord(current_path, StopWords)
