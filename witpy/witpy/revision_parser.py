from xml.etree import ElementTree as ET

import time
import mwparserfromhell as hell
import os

from pymongo import MongoClient


def _unique_comment_code(user, date):
    return user+date


def rev_parser(file, delete=False):

    local_cluster = MongoClient()
    mydb = local_cluster["Revisions"]

    unique_ids = list()

    file_name = file

    collection = mydb[file_name]

    if(delete):
        collection.drop()
    dir = os.getcwd()
    tree = ET.parse(f'{dir}/{file_name}')
    root = tree.getroot()
    page_id = root.find('id').text

    revisions = root.findall('revision')
    section = 1
    data = dict()
    data['data'] = list()
    start_time = time.time()

    for revision in revisions:
        rev = dict()
        rev['comments'] = list()
        rev['id'] = revision.find('id').text
        rev['timestamp'] = revision.find('timestamp').text

        if(revision.find('parentid') != None):
            rev['parent_id'] = revision.find('parentid').text
        else:
            rev['parent_id'] = "null"

        if(revision.find('contributor').find('username') != None):
            rev['user'] = revision.find('contributor').find('username').text

        else:
            rev['user'] = revision.find('contributor').find('ip').text

        if(revision.find('comment') != None):
            rev_main_comment = ""
            if(revision.find('comment').text != None):
                rev_main_comment = revision.find('comment').text

            new_main_comment = str()
            if "[[" in rev_main_comment:

                brac_start = list()
                brac_end = list()

                for i in range(len(rev_main_comment)):
                    if rev_main_comment[i:i+2] == "[[":
                        brac_start.append(i)
                    if rev_main_comment[i:i+2] == "]]":
                        brac_end.append(i)

                len_brac_array = len(brac_start)

                new_main_comment = rev_main_comment[:brac_start[0]]
                for j in range(len_brac_array):
                    try:
                        if j == len_brac_array-1:
                            if '|' in rev_main_comment[brac_start[j]+2:brac_end[j]]:
                                ind = rev_main_comment[brac_start[j] +
                                                       2:brac_end[j]].index('|') + brac_start[j] + 2
                                new_main_comment += rev_main_comment[ind +
                                                                     1:brac_end[j]]
                                new_main_comment += rev_main_comment[brac_end[j]+2:]

                        else:
                            if '|' in rev_main_comment[brac_start[j]+2:brac_end[j]]:
                                ind = rev_main_comment[brac_start[j] +
                                                       2:brac_end[j]].index('|') + brac_start[j] + 2
                                new_main_comment += rev_main_comment[ind +
                                                                     1:brac_end[j]]
                                new_main_comment += rev_main_comment[brac_end[j] +
                                                                     2:brac_start[j]]
                    except Exception as e:
                        pass
            else:
                new_main_comment = rev_main_comment

            rev['parent_comment'] = new_main_comment
        rev_text = ''
        if (revision.find('text') != None and revision.find('text').text != None):
            rev_text += revision.find('text').text

        #  removing curly braces
        wikihell = hell.parse(rev_text)
        templates = wikihell.filter_templates()

        for template in templates:
            rev_text = rev_text.replace(str(template), "")

        start_index = 0
        sqr_start = list()
        sqr_end = list()
        heading = False
        parent_sec = ""
        for t in range(len(rev_text)-4):
            if (rev_text[t:t+2] == "[["):
                sqr_start.append(t)

            if(rev_text[t:t+2] == "]]"):
                sqr_end.append(t)

            if (rev_text[t:t+5] == "(UTC)"):
                if ':' in rev_text[t-26:t]:
                    mini_str = rev_text[t-26:t+5]
                    colon_index = mini_str[::-1].index(':')
                    colon_index = len(mini_str) - colon_index - 1
                    final_date = mini_str[colon_index-3:t+5]

                    if sqr_start != []:
                        sqr_array_len = len(sqr_start)
                        text = rev_text[start_index:sqr_start[0]]
                        child_user = str()
                        for j in range(sqr_array_len):
                            # if j != sqr_start(sqr_array_len-1):

                            if ((rev_text[sqr_start[j]+2:sqr_start[j]+7]).lower() == 'user:'):
                                danda_cnt = rev_text[sqr_start[j] +
                                                     2:sqr_end[j]].count('|')
                                if danda_cnt == 1:
                                    danda_index = rev_text[sqr_start[j] +
                                                           2:sqr_end[j]].index('|')
                                    child_user = rev_text[sqr_start[j] +
                                                          7:danda_index+sqr_start[j]+2]
                                    # print(danda_index)
                                    break
                                else:
                                    child_user = rev_text[sqr_start[j] +
                                                          7:sqr_end[j]]
                                    break

                            elif((rev_text[sqr_start[j] + 2: sqr_start[j] + 11]).lower() == 'user talk'):
                                index = rev_text[sqr_start[j] +
                                                 2: sqr_end[j]].index("|")
                                child_user = rev_text[sqr_start[j] +
                                                      12:index+sqr_start[j]+2]
                                break
                            elif((rev_text[sqr_start[j] + 2: sqr_start[j] + 11]).lower() == 'user_talk'):
                                index = rev_text[sqr_start[j] +
                                                 2: sqr_end[j]].index("|")
                                child_user = rev_text[sqr_start[j] +
                                                      12:index+sqr_start[j]+2]
                                break

                            else:
                                danda_cnt = rev_text[sqr_start[j] +
                                                     2:sqr_end[j]].count('|')

                                if danda_cnt == 1:

                                    index = rev_text[sqr_start[j] +
                                                     2:sqr_end[j]].index('|')
                                    text += rev_text[sqr_start[j] +
                                                     3 + index: sqr_end[j]]
                                    text += rev_text[sqr_end[j] +
                                                     2:sqr_start[j+1]]

                                elif danda_cnt == 0:
                                    text += rev_text[sqr_start[j]+2:sqr_end[j]]
                                    text += rev_text[sqr_end[j] +
                                                     2:sqr_start[j+1]]

                                else:
                                    text += rev_text[sqr_end[j] +
                                                     2:sqr_start[j+1]]

                        sqr_start = []
                        sqr_end = []

                        start_index = t+5

                    # obtaing section head name if any
                    text = text.replace('\n', '')
                    try:
                        while text[0] == ":":
                            text = text.replace(text[0], '')

                    except:
                        pass

                    if ('==' in text):

                        head_start = text.index('==')

                        head_end = text[::-1].index('==')
                        head_end = len(text) - head_end - 2
                        sec_head = text[head_start+2:head_end]
                        parent_sec = parent_sec.replace(parent_sec, sec_head)
                        text = text.replace(text[head_start:head_end+2], '')
                        heading = True

                    # removing angular brackets

                    ang_start = list()
                    ang_end = list()
                    final_text = ''
                    for num in range(len(text)):
                        if text[num] == '<':
                            ang_start.append(num)

                        elif text[num] == '>':
                            ang_end.append(num)

                    if ang_start != []:
                        final_text += text[:ang_start[0]]

                        ang_num = len(ang_start)
                        for r in range(ang_num-1):
                            final_text += text[ang_end[r]+1:ang_start[r+1]]

                        final_text += text[ang_end[ang_num-1]+1:]

                    else:
                        final_text += text

                    uid = _unique_comment_code(child_user, final_date)
                    if uid not in unique_ids:

                        unique_ids.append(uid)
                    # adding to json
                        if heading == False:
                            obj = {
                                "text": final_text,
                                "user": child_user,
                                "date": final_date
                            }
                        else:
                            obj = {
                                "text": final_text,
                                "user": child_user,
                                "date": final_date,
                                "section_name": parent_sec
                            }
                        rev['comments'].append(obj)

        if rev['comments'] != []:
            collection.insert_one(rev)
        print("Inserted Section:", section)
        section += 1

    end_time = time.time()
    print(end_time-start_time)


def parser(file):
    ''' Provide the full file name or the relative path to your current working directory to store it in you mongo databse 
     Make sure your local mogo db connectin is active '''
    local_cluster = MongoClient()
    mydb = local_cluster["Revisions"]

    collections = mydb.list_collection_names()

    if(file in collections):
        print("Data for this file has already been stored\n\nDo you want to delete and restore it?\n")
        choice = input("Type Y or N : ")

        if(choice == "Y" or choice == "y"):
            rev_parser(file, delete=True)

        else:
            return
    else:
        rev_parser(file)


if __name__ == '__main__':
    pass
