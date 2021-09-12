from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from time import sleep
import sys, getopt
import os


def main(argv):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print ('Input file is "', inputfile)
    
    try: 
        os.mkdir("screens") 
    except OSError as error: 
        print(error) 
    
    file1 = open(inputfile, 'r')
    count = 0
    os.chdir("screens")
    while True:
        count += 1
 
        # Get next line from file
        line = file1.readline()
        # if line is empty
        # end of file is reached
        if not line:
            break
        print("trying: " + line)
        URL = "https://" + line
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(URL)
    
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
        driver.find_element_by_tag_name('body').screenshot(line + '.png')

        driver.quit()
    file1.close()

if __name__ == "__main__":
   main(sys.argv[1:])

