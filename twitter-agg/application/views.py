from application import app
from application.home import DataOperations, TwitterOperations, TwitterUser
from quart import render_template
import asyncio

@app.route('/')
async def main():
    tweet_calls = [
        asyncio.ensure_future(user_tweets()),
        asyncio.ensure_future(tag_tweets())
    ]
    tweets = await asyncio.gather(*tweet_calls)

    return await render_template('home.html', user_tweets=tweets[0], tag_tweets=tweets[1], zip=zip)

    
async def user_tweets():


    calls = [
        asyncio.ensure_future(TwitterOperations.get_tweets('user')),
        asyncio.ensure_future(TwitterOperations.get_users_info(DataOperations.get_users()))
    ]

    monitored_user_tweets, monitored_users_info = await asyncio.gather(*calls)
        
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
    
    tag_tweet_users_task = []
    for tweet in monitored_tag_tweets['data']:
        tag_tweet_users_task.append(asyncio.create_task(TwitterOperations.get_single_user_info_by_id(tweet['author_id'])))
    tag_tweet_users = await asyncio.gather(*tag_tweet_users_task)

    #combine tweet and user data
    tag_tweets_with_user = []    
    for tweet, user in zip(monitored_tag_tweets['data'], tag_tweet_users):
        tweet_dict = {}
        tweet_dict['handle'] = user['username']
        tweet_dict['name'] = user['name']
        tweet_dict['profile_image'] = user['profile_image_url']
        tweet_dict['text'] = tweet['text']
        tweet_dict['created_at'] = tweet['created_at']
        tag_tweets_with_user.append(tweet_dict)

    return tag_tweets_with_user


@app.route('/api/')
def api():
    return render_template('home.html')
