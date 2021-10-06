from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from time import sleep
import sys, getopt
import os
import requests
from requests.exceptions import HTTPError
import builtwith

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
    file0 = open('output.html', 'w+')
    file0.write('''<!DOCTYPE html>
<html>
   <head>
       <title></title>
       <style>
            table{
                width: 100%;
            }
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            } 
       </style>
   </head>
   <body>
        <table>
            ''')
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
        URL = "https://" + line.rstrip()
        try:
            
            file0.write("<tr>\n")

            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            driver.get(URL)
            S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
            driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
            driver.find_element_by_tag_name('body').screenshot(line.rstrip() + '.png')
            driver.quit()
            file0.write("            <td> <img src=\"screens/" + line.rstrip() + ".png\" alt=\"" + URL + "\"></td>\n")
            response = requests.get(URL, timeout=5)
            print("\033[1;34;40m" + URL + "\033[0m")
            file0.write("            <td>"+ URL +"</td>\n")
            print(response.headers)
            file0.write("            <td>"+ str(response.headers) +"</td>\n")
            resp = builtwith.parse(URL)
            print(str(resp))
            file0.write("            <td>"+ str(resp) +"</td>\n")
            file0.write("            </tr>\n")
        except requests.exceptions.Timeout as e: 
            print("\033[1;31;40m" + URL + " TIMED OUT \033[0m")
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        except:
            print("failed " + line)
    file1.close()
    file0.write('''
        </table>
   </body>
</html>''')
    file0.close()

if __name__ == "__main__":
   main(sys.argv[1:])
