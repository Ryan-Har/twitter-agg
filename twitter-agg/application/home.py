from application import app
import requests
import json
import asyncio
import aiohttp

class DataOperations():
    def get_users():
        users = []
        with open('application/users.ini', 'r') as f:
            for line in f.readlines():
                users.append(line.strip())
        return users

    def get_tags():
        tags = []
        with open('application/tags.ini', 'r') as f:
            for line in f.readlines():
                tags.append(line.strip())
        return tags

    def check_duplicate(data, type):
        if type not in ('application/users', 'tags'):
            raise Exception("type not 'users' or 'tags'")
        to_check = eval(f"get_{type}()")
        if data in to_check:
            return True
        else:
            return False

    def add_users(users_to_add): #must be iterable(set, list, etc. Not a string)
        with open('application/users.ini', 'a') as f:
            for user in users_to_add:
                if not check_duplicate(user, 'users'):
                    f.write(f"{user}\n")

    def add_tags(tags_to_add): #must be iterable(set, list, etc. Not a string)
        with open('application/tags.ini', 'a') as f:
            for tag in tags_to_add:
                if not check_duplicate(tag, 'tags'):
                    f.write(f"{tag}\n")

    def del_users(users_to_del): #must be iterable(set, list, etc. Not a string)
        for user in users_to_del:
            with open('application/users.ini', 'r+') as f:
                data = f.readlines()
                f.seek(0)
                for item in data:
                    if item.strip() != user:
                        f.write(item)
                    f.truncate()

    def del_tags(tags_to_del): #must be iterable(set, list, etc. Not a string)
        for tag in tags_to_del:
            with open('application/tags.ini', 'r+') as f:
                data = f.readlines()
                f.seek(0)
                for item in data:
                    if item.strip() != tag:
                        f.write(item)
                    f.truncate()

class TwitterOperations():

    async def get_twitter_api_request(url):
        payload={}
        headers = {
            'Authorization': f"Bearer {app.config['BEARER']}",
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, data=payload) as resp:
                return await resp.json()
        

    async def get_single_user_info_by_id(user_id):
        url = f"https://api.twitter.com/2/users/{user_id}?user.fields=profile_image_url"
        response_request = asyncio.create_task(TwitterOperations.get_twitter_api_request(url))
        response = await response_request
        return response['data']

    #get user ID, handle, name and profile image
    async def get_users_info(users): 
        url = f"https://api.twitter.com/2/users/by?usernames={','.join(users)}&user.fields=profile_image_url"
        
        response_request = asyncio.create_task(TwitterOperations.get_twitter_api_request(url))
        response = await response_request
        #add objects into list
        twitter_users = []
        for i in response['data']:
            twitter_users.append(TwitterUser(i['id'], i['username'], i['name'], i['profile_image_url']))

        #convert list to a dict with the ID as the key    
        twitter_users_by_ID = {}
        for i in twitter_users:
            twitter_users_by_ID[i.user_ID] = i
        
        return twitter_users_by_ID

        #get tweets for specific user
    async def get_tweets(get_type, **kwargs):#get_type being tag or user lookup
        if get_type == 'user':
            formatted_users = " OR ".join([f"from:{user}" for user in DataOperations.get_users()]) # format for the api
            if 'next_token' in kwargs: #next token to retrieve older tweets if there are any
                url = f"https://api.twitter.com/2/tweets/search/recent?query=({formatted_users}) -is:reply&next_token={kwargs.get('next_token')}&tweet.fields=author_id,referenced_tweets,created_at"
            else:
                url = f"https://api.twitter.com/2/tweets/search/recent?query=({formatted_users}) -is:reply&tweet.fields=author_id,referenced_tweets,created_at"
  
            response_request = asyncio.create_task(TwitterOperations.get_twitter_api_request(url))
            response = await response_request
            
            #Retweets are truncated, this function resolves that - To add the expansion of short URL's for display
            fixed_data = TwitterOperations.fix_truncated_data(response)
            
            return await fixed_data

        if get_type == 'tag':
            formatted_tags = " OR ".join([f"%23{tag}" for tag in DataOperations.get_tags()])#%23 is the # symbol
            if 'next_token' in kwargs: #next token to retrieve older tweets if there are any
                url = f"https://api.twitter.com/2/tweets/search/recent?query=({formatted_tags}) -is:reply&next_token={kwargs.get('next_token')}&tweet.fields=author_id,referenced_tweets,created_at"
            else:
                url = f"https://api.twitter.com/2/tweets/search/recent?query=({formatted_tags}) -is:reply&tweet.fields=author_id,referenced_tweets,created_at"

            response_request = asyncio.create_task(TwitterOperations.get_twitter_api_request(url))
            response = await response_request
            #Retweets are truncated, this function resolves that - To add the expansion of short URL's for display
            fixed_data_task = asyncio.create_task(TwitterOperations.fix_truncated_data(response))
            fixed_data = await fixed_data_task
            return fixed_data
        
    async def fix_truncated_data(data):
        for x in data['data']:
            # un truncate retweets which truncate within the API
            if x['text'].startswith('RT'):
                try:
                    full_text_task = asyncio.create_task(TwitterOperations.get_single_tweet_text((x['referenced_tweets'][0]['id'])))
                    full_text = await full_text_task
                    x['text'] = f"RT: {full_text}"
                except:
                    print("text started with 'RT' but wasn't a retweet") 
            else:
                pass

        return data

    #returns only the text for a single tweet, by ID
    async def get_single_tweet_text(id):
        url = f"https://api.twitter.com/2/tweets/{id}"
        response_request = asyncio.create_task(TwitterOperations.get_twitter_api_request(url))
        response = await response_request

        return response['data']['text']


class TwitterUser(object):

    def __init__(self, user_ID, user_handle, friendly_name, profile_picture):
        self.user_ID = user_ID
        self.user_handle = user_handle
        self.friendly_name = friendly_name
        self.profile_picture = profile_picture
    


    
