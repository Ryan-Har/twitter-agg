from application import app
from application.home import DataOperations, TwitterOperations, TwitterUser
from quart import render_template
import asyncio

@app.route('/')
async def main():  
    user_tweets_task = asyncio.create_task(user_tweets())
    tag_tweets_task = asyncio.create_task(tag_tweets())
    user_tweets_result = await user_tweets_task
    tag_tweets_result = await tag_tweets_task

    return await render_template('home.html', user_tweets=user_tweets_result, tag_tweets=tag_tweets_result, zip=zip)

    
async def user_tweets():
    #get 10 tweets for the users
    monitored_user_tweets_task = asyncio.create_task((TwitterOperations.get_tweets('user')))
    # dictionary of the monitored users handle, name, username and image
    monitored_users_info_task = asyncio.create_task((TwitterOperations.get_users_info(DataOperations.get_users())))

    monitored_user_tweets = await monitored_user_tweets_task
    monitored_users_info = await monitored_users_info_task
    
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

async def tag_tweets():
    #get 10 tweets for the tags
    monitored_tag_tweets_task =  asyncio.create_task(TwitterOperations.get_tweets('tag'))
    monitored_tag_tweets = await monitored_tag_tweets_task

    tag_tweets_with_user = []
    for tweet in monitored_tag_tweets['data']:
        tweet_dict = {}
        user_task = asyncio.create_task(TwitterOperations.get_single_user_info_by_id(tweet['author_id']))
        user = await user_task
        tweet_dict['handle'] = user['username']
        tweet_dict['name'] = user['name']
        tweet_dict['profile_image'] = user['profile_image_url']
        tweet_dict['text'] = tweet['text']
        tweet_dict['created_at'] = tweet['created_at']
        tag_tweets_with_user.append(tweet_dict)
    
    return tag_tweets_with_user


# @app.route('/api/')
# def api():
#     return render_template('home.html')
