from application import app
from application.home import DataOperations, TwitterOperations, TwitterUser
from flask import render_template, render_template_string
import datetime

@app.route('/')
def main():
    users_info = TwitterOperations.get_users_info()
    #add objects into list
    users = []
    for i in users_info:
        users.append(TwitterUser(i['id'], i['username'], i['name'], i['profile_image_url']))
    #convert list to a dict with the handle as the key    
    users_by_ID = {}
    for i in users:
        users_by_ID[i.user_ID] = i

    #get 10 tweets for the users
    tweets = TwitterOperations.get_tweets([user.user_handle for user in users])

    #combine tweet and user data
    tweets_with_user = []
    for tweet in tweets['data']:
        tweet_dict = {}
        tweet_dict['handle'] = users_by_ID[tweet['author_id']].user_handle
        tweet_dict['name'] = users_by_ID[tweet['author_id']].friendly_name
        tweet_dict['profile_image'] = users_by_ID[tweet['author_id']].profile_picture
        tweet_dict['text'] = tweet['text']
        tweet_dict['created_at'] = tweet['created_at']
        tweets_with_user.append(tweet_dict)
    return render_template('home.html', tweets=tweets_with_user)
    

@app.route('/api/')
def api():
    return render_template('home.html')
