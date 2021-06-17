# witpy

**witpy** is a Python library that contains functions to parse _Wikipedia XML_. The library mainly focuses on extracting data from Revision pages in _JSON_ format.


## USE:

Redirect to **witpy/dist** and run the following command to install the library
    ```cmd
    pip install witpy-0.1.0-py3-none-any.whl
    ```

### Setup A local Mongo Database 
**For More details on this read the Mongo DB Setup section below**
    
### Import the library by typing the command

#### For importing the database storing functions
```python 
from witpy.revision_parser import parser
```

#### For importing the information fetching functions
```python 
from witpy.fetch_details import *
```





## Retrieving Functions 

### get_users 
  The function take the xml file name as the input with the '.xml' part and return a dictonary containing all the users along with their number of comments 

### max_user 
    The function take the xml file name as the input with the '.xml' part and return a tuple containing the name of the user with the most comments and it's number of comments

### min_user

    The function take the xml file name as the input with the '.xml' part and return a tuple containing the name of the user with the least comments and it's number of comments

### user_comments

    The function take the xml file name as the input with the '.xml' part and return a dictonary with users as the keys and their comments stored in a list as the corresponding value

### user_sentiment_analyzer

    The function take the xml file name as the input with the '.xml' part as the first arguement. As the second arguement it you can provide a user's name if you want sentiment analysis only for that user otherwise it will return a dictonary containing all the users along with their rating score 

### document_sentiment_analyzer

    The function take the xml file name as the input with the '.xml' part and return the sentiment analysis score for the whole document


### For revision pages:

The Revision XML file contains revision sections. Each revision section has a contributor and a publishing date.
Further there are replies under that section commented by other users sorted according to their posting date.

The Revision History Parser takes the XML file and and seperates different sections using python's inbuilt xml module.
By detecting the user tag it easily finds the contributor for a particular section and the same is done for finding the publishing date, section-id and the parent-id. Further, the parser also takes care of replies under that section. It extracts the username, reply text and time of comment of each reply.

The replies sometimes have links referenced to some other content or resource over the internet. These links are are contained in a sequence of square and curly braces and some special characters. Here, the parser uses _mwparserfromhell_ to find out content written in between curly braces. Then, the parser extracts useful data present between brackets, arranges it accordingly and merges into final JSON.

For each full revision xml, there is dedicated database in the _Local cluster_. After parsing of each revision section, its JSON is stored in the database as a separate collection.



## MongoDB Setup

### Installer Download
To install the Community Edition of Mongo in your local machine, follow this link: [https://www.mongodb.com/try/download/community]

 - In the *Version* dropdown, choose the version of MongoDB to be downloaded.
   Recommended version is the current version.
    
 - In the *Platform* dropdown, selcet your *OS*.

 - In the *Package* dropdown, selcet **msi**.

 - Click on the **Download** button.

This will download the MongoDB installer in your machine. Once it is downloaded, run it.

### Installation
In the **Installation wizard**:

- Go through the *End User Licence Agreement*. To continue agree to the terms and press *Next*.

- For *Setup type*, if you are new to this, just proceed with **Complete**.

- In *Service Configuration*, procced with the default settings and keep a note of the *Data and Log Directory*.

- In *Install MongoDB* menu, there is a checkbox asking permission to download ***MongoDB Compass***. It is the UI of Mongo. Click that if you want to download it too and proceed.

It will install MongoDB in your machine.


- To run the interactive shell, open teminal and execute the follwing command:
    ```cmd
    "C:\Program Files\MongoDB\Server\4.4\bin\mongo.exe"
    ```