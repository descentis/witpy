import pymongo
from pymongo import MongoClient
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()


def get_users(file):

    # returns a dict of users

    cluster = MongoClient()
    db = cluster["Revisions"]
    collection = db[f"{file}.xml"]

    users = dict()
    x = collection.find()
    for i in x:
        user = i['user']
        users[user] = users.get(user, 0) + 1

    return users


def max_user(file):

    users = get_users(file)

    max_user = max(users, key=users.get)

    return (max_user, users[max_user])


def min_user(file):

    users = get_users(file)

    min_user = min(users, key=users.get)

    return (min_user, users[min_user])


def user_comments(file):

    user_comments = dict()

    cluster = MongoClient()
    db = cluster["Revisions"]
    collection = db[f"{file}.xml"]

    x = collection.find()

    for i in x:

        user = i['user']
        for j in i['comments']:
            user_comments[user] = user_comments.get(user, [])
            user_comments[user].append(j['text'])

    return user_comments


def user_sentiment_analyzer(file, user=None):

    all_comments = user_comments(file)

    if(user != None):

        comments = all_comments[user]

        comment_added = str()

        i = 0

        compound_score = 0
        for comment in comments:

            score = analyzer.polarity_scores(comment)
            compound_score += score['compound']
            i += 1

        average_compound_score = compound_score/i

        star = '⭐'
        if(average_compound_score >= 0.32):
            star *= 5
        elif(average_compound_score < 0.32 and average_compound_score >= 0.05):
            star *= 4
        elif(average_compound_score < 0.05 and average_compound_score >= (-0.05)):
            star *= 3
        elif(average_compound_score < (-0.05) and average_compound_score >= (-0.25)):
            star *= 2
        else:
            star *= 1

        return (star, average_compound_score)

    else:

        user_scores = dict()
        for key in all_comments.keys():
            user_scores[key] = user_sentiment_analyzer(file, key)

        return user_scores


def document_sentiment_analyzer(file):

    user_scores = dict()

    cluster = MongoClient()
    db = cluster["Revisions"]

    collection = db[f"{file}.xml"]

    x = collection.find()
    counter = 0
    for i in x:
        # print(i['user'])
        compound_score = 0
        for j in i['comments']:

            comment = j['text']
            score = analyzer.polarity_scores(comment)
            compound_score += score['compound']
            counter += 1
    average_compound_score = compound_score/counter

    star = '⭐'
    if(average_compound_score >= 0.32):
        star *= 5
    elif(average_compound_score < 0.32 and average_compound_score >= 0.05):
        star *= 4
    elif(average_compound_score < 0.05 and average_compound_score >= (-0.05)):
        star *= 3
    elif(average_compound_score < (-0.05) and average_compound_score >= (-0.25)):
        star *= 2
    else:
        star *= 1

    return star, average_compound_score


if __name__ == "__main__":

    pass
