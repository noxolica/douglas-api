from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import numpy as np
import pandas as pd


class Professors:

    def __init__ (self, csis_professor_id = ""):
        self.csis_professor_id = csis_professor_id

    ## HEADER LIST
    def requestHeaders(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive'}

        return headers
    
    ## SCRAPER FOR CSIS DATA
    def CSIS_professor(self):

        csisProfessors = []
        full_info = []
        subject = []
        session = []
    
        url = 'https://banserv2.douglas.bc.ca/prod/bwysched.p_course_search?wsea_code=CRED&term_code=202030&session_id=6784192&sel_subj=dummy&sel_camp=dummy&sel_sess=dummy&sel_attr=dummy&sel_levl=dummy&sel_schd=dummy&sel_ptrm=dummy&sel_insm=dummy&sel_link=dummy&sel_wait=dummy&sel_day=dummy&sel_begin_hh=dummy&sel_begin_mi=dummy&sel_begin_am_pm=dummy&sel_end_hh=dummy&sel_end_mi=dummy&sel_end_am_pm=dummy&sel_instruct=dummy&sel_open=dummy&sel_resd=dummy&sel_resd=R&sel_subj=CSIS&sel_number=&sel_camp=&sel_sess=&sel_day=m&sel_day=t&sel_day=w&sel_day=r&sel_day=f&sel_day=s&sel_day=u&sel_instruct='

        driver = webdriver.Chrome(executable_path='./drivers/chromedriver')
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,'html.parser')

        # Access the table structure to get the proper data
        for a in soup.select('table')[3].select('tr')[1:]:
            # Get the 3rd td where the `course` name and `sesseion` is saved.  
            rows = a.select('td:nth-child(3)')
            for row in rows:
                # Filtering unnecessary strings in the rows
                if("CSIS" in row.text[:15] and len(row.text[:15]) == 13):
                    # Save `Course Name` + `Section` into fill_info list
                    full_info.append(row.text[:15])

            # Get the 13th td where the course `professors` are saved
            rows = a. select('td:nth-child(13)')
            for row in rows:
                # Save the all `Instructor(professors)` name into csisProfessors list 
                csisProfessors.append(row.get_text())
        
        # Divide full_info string into `subject` and `session` to save it properly in a Dictionary later
        for value in full_info:
            subject.append(value[:9])
            session.append(value[10:])
        

        return subject, session, csisProfessors

        driver.quit()

    ## Function for professor data into CSV file.
    def convertCsv(self, dict_list):
        toCSV = dict_list
        keys = toCSV[0].keys()
        # THis time we need to use 'w' to ignore error 
        with open('semester_info.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)

   
    ## Create a `Dictionary` which consist of course, section, and instructor name 
    def creat_dictionary(self, course, section, instructor):        
        # Dictionary Key and Value
        sub_dic = {
            "course" : course,
            "section" : section,
            "instructor" : instructor
        }
        return sub_dic

    ## Create List for saving dictionaries
    def dict_list(self):
        dict_list = []
        return dict_list

    ## Search `course name` and `section` by Instructor
    def search_by_instroctor(self,dict_list):
        for i in range(len(dict_list)):
            ## You can edit instructor who you want to search
            if(dict_list[i]['instructor'] == 'Noman Saleem'):
                print(dict_list[i]['course'] + " " +dict_list[i]['section'])

    ## Search 'Instructor' by 'course name'
    def search_by_course(self, dict_list):
        instructor = []
        for i in range(len(dict_list)):
            ## You can edit course name what you want to search
            if(dict_list[i]['course'] == 'CSIS 2270'):
                instructor.append(dict_list[i]['instructor'])
        print(np.unique(instructor))
                

    ## STATIC METHOD FOR EXECUTING THIS CLASS         
    @staticmethod
    def run():

        professors = Professors()
        subject_data, session_data, csisProf_data = professors.CSIS_professor()
        

        # Call the dictionary list 
        dict_list = professors.dict_list()


        # Iterating list to save each of list element in the dictionary
        for i in range(len(subject_data)):
            data = professors.creat_dictionary(subject_data[i],session_data[i],csisProf_data[i])
            dict_list.append(data)
        
        # Save the dict_list info into CSV File
        professors.convertCsv(dict_list)

        """ # Check the list elements which is a dictionary format 
        for value in dict_list:
            print(value)

        # SEARCH FUNCTION(1)
        professors.search_by_instroctor(dict_list)

        # SEARCH FUNCTION(2)
        professors.search_by_course(dict_list)
        """

        