from application import app
import tweepy
import requests
import json

class DataOperations():
    def get_users():
        users = []
        with open('application/users.ini', 'r') as f:
            for line in f.readlines():
                users.append(line.strip())
        return users

    def get_tags():
        tags = []
        with open('tags.ini', 'r') as f:
            for line in f.readlines():
                tags.append(line.strip())
        return tags

    def check_duplicate(data, type):
        if type not in ('users', 'tags'):
            raise Exception("type not 'users' or 'tags'")
        to_check = eval(f"get_{type}()")
        if data in to_check:
            return True
        else:
            return False

    def add_users(users_to_add): #must be iterable(set, list, etc. Not a string)
        with open('users.ini', 'a') as f:
            for user in users_to_add:
                if not check_duplicate(user, 'users'):
                    f.write(f"{user}\n")

    def add_tags(tags_to_add): #must be iterable(set, list, etc. Not a string)
        with open('tags.ini', 'a') as f:
            for tag in tags_to_add:
                if not check_duplicate(tag, 'tags'):
                    f.write(f"{tag}\n")

    def del_users(users_to_del): #must be iterable(set, list, etc. Not a string)
        for user in users_to_del:
            with open('users.ini', 'r+') as f:
                data = f.readlines()
                f.seek(0)
                for item in data:
                    if item.strip() != user:
                        f.write(item)
                    f.truncate()

    def del_tags(tags_to_del): #must be iterable(set, list, etc. Not a string)
        for tag in tags_to_del:
            with open('tags.ini', 'r+') as f:
                data = f.readlines()
                f.seek(0)
                for item in data:
                    if item.strip() != tag:
                        f.write(item)
                    f.truncate()

class TwitterOperations():
    #get user ID, handle, name and profile image
    def get_users_info(): 
        url = f"https://api.twitter.com/2/users/by?usernames={','.join(DataOperations.get_users())}&user.fields=profile_image_url"
        
        payload={}
        headers = {
            'Authorization': f"Bearer {app.config['BEARER']}",
            }
        response = requests.request("GET", url, headers=headers, data=payload).json()
        return response['data']

        #get tweets for specific user
    def get_tweets(users_to_get_tweets, **kwargs):
        formatted_users = " OR ".join([f"from:{user}" for user in users_to_get_tweets]) # format for the api
        
        if 'next_token' in kwargs: #next token to retrieve older tweets if there are any
            url = f"https://api.twitter.com/2/tweets/search/recent?query=({formatted_users}) -is:reply&next_token={kwargs.get('next_token')}&tweet.fields=author_id,referenced_tweets,created_at"
        else:
            url = f"https://api.twitter.com/2/tweets/search/recent?query=({formatted_users}) -is:reply&tweet.fields=author_id,referenced_tweets,created_at"
        payload={}
        headers = {
            'Authorization': f"Bearer {app.config['BEARER']}",
            }
        response = requests.request("GET", url, headers=headers, data=payload).json()
        #Retweets are truncated, this function resolves that - To add the expansion of short URL's for display
        fixed_data = TwitterOperations.fix_truncated_data(response)

        return fixed_data

    def fix_truncated_data(data):
        for x in data['data']:
            # un truncate retweets which truncate within the API
            if x['text'].startswith('RT'):
                try:
                    full_text = TwitterOperations.get_single_tweet_text((x['referenced_tweets'][0]['id']))
                    x['text'] = f"RT: {full_text}"
                except:
                    print("text started with 'RT' but wasn't a retweet") 
            else:
                pass

        return data

    #returns only the text for a single tweet, by ID
    def get_single_tweet_text(id):
        url = f"https://api.twitter.com/2/tweets/{id}"
        payload={}
        headers = {
            'Authorization': f"Bearer {app.config['BEARER']}",
            }
        response = requests.request("GET", url, headers=headers, data=payload).json()

        return response['data']['text']

class TwitterUser(object):

    def __init__(self, user_ID, user_handle, friendly_name, profile_picture):
        self.user_ID = user_ID
        self.user_handle = user_handle
        self.friendly_name = friendly_name
        self.profile_picture = profile_picture
    


    
