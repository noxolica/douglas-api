import urllib
import  requests
from bs4 import BeautifulSoup
import json
import csv

class CsisProgram:

    
    def __init__(self,csis_program_id =""):
        self.csis_program_id = csis_program_id

    def requestHeaders(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive'}
        return headers

    def CSIS_program(self):

        csisPrograms = []

        url = 'https://www.douglascollege.ca/programs-courses/catalogue/programs/results?semesterSelect=All+Semesters&credentialSelect=All+Credentials&deliverySelect=All+Delivery+Methods&campusSelect=All+Campuses'

        result = requests.get(url, headers = self.requestHeaders())

        soup = BeautifulSoup(result.text,'html.parser')

        programDeictionary = json.loads(str(soup.text))

        commerce_besiness_admin = programDeictionary["Faculty"][1]
        
        #print(commerce_besiness_admin["Programs"][0])

        cba_program = commerce_besiness_admin["Programs"]

        for i in range(len(cba_program)):
            if cba_program[i]["ProgramName"] == "Computing Studies  Information Systems":
                csisPrograms.append(cba_program[i]["Name"])

        return csisPrograms
    
    def convertCsv(self,csislist):
        with open('csis_programs_data.txt','w') as data_file:
            wr = csv.writer(data_file,quoting=csv.QUOTE_ALL)
            wr.writerow(csislist)


    @staticmethod
    def run():
        csis = CsisProgram()
        csislist = csis.CSIS_program()
        csis.convertCsv(csislist)
