from application import app
from application.home import DataOperations, TwitterOperations, TwitterUser
from flask import render_template, render_template_string
import datetime

@app.route('/')
def main():
    
    def user_tweets():
        #get 10 tweets for the users
        monitored_user_tweets = TwitterOperations.get_tweets('user')
        # dictionary of the monitored users handle, name, username and image
        monitored_users_info = TwitterOperations.get_users_info(DataOperations.get_users())
        
        #combine tweet and user data
        user_tweets_with_user = []
        for tweet in monitored_user_tweets['data']:
            tweet_dict = {}
            tweet_dict['handle'] = monitored_users_info[tweet['author_id']].user_handle
            tweet_dict['name'] = monitored_users_info[tweet['author_id']].friendly_name
            tweet_dict['profile_image'] = monitored_users_info[tweet['author_id']].profile_picture
            tweet_dict['text'] = tweet['text']
            tweet_dict['created_at'] = tweet['created_at']
            user_tweets_with_user.append(tweet_dict)
        
        return user_tweets_with_user

    def tag_tweets():
        #get 10 tweets for the tags
        monitored_tag_tweets = TwitterOperations.get_tweets('tag')

        tag_tweets_with_user = []
        for tweet in monitored_tag_tweets['data']:
            tweet_dict = {}
            user = TwitterOperations.get_single_user_info_by_id(tweet['author_id'])
            tweet_dict['handle'] = user['username']
            tweet_dict['name'] = user['name']
            tweet_dict['profile_image'] = user['profile_image_url']
            tweet_dict['text'] = tweet['text']
            tweet_dict['created_at'] = tweet['created_at']
            tag_tweets_with_user.append(tweet_dict)
        
        return tag_tweets_with_user      

    return render_template('home.html', user_tweets=user_tweets(), tag_tweets=tag_tweets(), zip=zip)


    

@app.route('/api/')
def api():
    return render_template('home.html')
