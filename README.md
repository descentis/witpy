# witpy

**witpy** is a Python library that contains functions to parse _Wikipedia XML_. The library mainly focuses on extracting data from Revision pages in _JSON_ format.

### For revision pages:

The Revision XML file contains revision sections. Each revision section has a contributor and a publishing date.
Further there are replies under that section commented by other users sorted according to their posting date.

The Revision History Parser takes the XML file and and seperates different sections using python's inbuilt xml module.
By detecting the user tag it easily finds the contributor for a particular section and the same is done for finding the publishing date, section-id and the parent-id. Further, the parser also takes care of replies under that section. It extracts the username, reply text and time of comment of each reply.

The replies sometimes have links referenced to some other content or resource over the internet. These links are are contained in a sequence of square and curly braces and some special characters. Here, the parser uses _mwparserfromhell_ to find out content written in between curly braces. Then, the parser extracts useful data present between brackets, arranges it accordingly and merges into final JSON.

For each full revision xml, there is dedicated database in the _Local cluster_. After parsing of each revision section, its JSON is stored in the database as a separate collection.

## USE:

Redirect to ** witpy/dist ** and run the following command to install the library
pip install witpy-0.1.0-py3-none-any.whl
