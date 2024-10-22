# News Generator
Generates a pdf file of healines and url links to the news article online. It generates top headlines or searches through thousands of articles from multiples sources depending on the flag it is given.
### Desccription
#### Project.py

```bash
    usage: project.py [-h] (-t | -e) -f FILE

    options:
    -h, --help            show this help message and exit
    -t, --headlines       headlines: provides live top and breaking headlines for a country, specific category in a    
                          country, single source, or multiple sources. You can also search with keywords. Articles
                          are  sorted by the earliest date published first
    e, --everything      Search through millions of articles from over 150,000 large and small news sources and blogs
    -f FILE, --file FILE  name of output pdf file for news to be sourced.
```

Contains global variable like country list and category list for helper functions to validate input and helper functions.

#### Functions

##### main: 
The main part of the program, where all functions are utilised to achieve the overall aim of the program.

##### get_source_table: 
gets the source table to help users input correct values in proceeding prompts access return a dictionary with sources , country, and name keys

##### cli: 
handles the commandline arguments and flag options given. It validates command line arguments and returns a list of two values, the news type(healines or everything) and the file path to which the pdf is saved

##### inp_params:
checks for the news type (everything or headlines) and proceed to prompt the users for params and validates the input. All aided by helper functions like check_q e.t.c returns a dictionary of with the appropriate parameters as keys and user input for corresponding parameters as values

##### check_q:
accepts a string check if its a single letter then exits the program, if it is an empty string it return None or if its a not empty or a single character, it returns the string.

##### check_date:
takes a string and checks if it is a valid ISO 8601 date or datetime and the returns the string. It exits the program if it is invalid or return none if it is empty.

##### check_page:
accepts a string then checks if it can be converted to an integer then returns the integer otherwise exits the program

##### check_country:
checks if the string it is passed is in the list of valid countries otherwise exits the program. If it is passed an emptry string returns None.

##### check category:
checks if the string it is passed is in the list of valid categories otherwise exits the program. If it is passed an emptry string returns None.

##### everything:
uses the dictionary object it is passed to request for a data from the everything endpoint of the newsapi API via an http request and returns the JSON formatted data

##### headlines:
uses the dictionary object it is passed to request for a data from the top-healines endpoint of the newsapi API via an http request and returns the JSON formatted data

##### check_source:
checks if the string it is passed is in the list of valid sources otherwise exits the program. If it is passed an emptry string returns None

##### check_path:
checks if the string it is passed is a valid file path or if it can be converted to a file path, exits if otherwise. Returns the file path

##### pdfify:
responsible for generating the pdf. It adds each new healines to a pdf file and outputs the pdf file

## test_project.py
contains test functions to test various function from the project.py file

##### test_check_q:
tests the check_q function

##### test_check_date:
tests the check_date function

##### test_check_num:
tests the check_page function

##### test_check_country:
test the check_country function

##### test_check_category:
test the check_category function

#### requirements.txt
a text file containing external packages and module relevant to the project
