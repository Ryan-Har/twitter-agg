from application import app
import tweepy
import requests
import json

class DataOperations():
    def get_users():
        users = []
        with open('application/users.txt', 'r') as f:
            for line in f.readlines():
                users.append(line.strip())
        return users

    def get_tags():
        tags = []
        with open('tags.txt', 'r') as f:
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
        with open('users.txt', 'a') as f:
            for user in users_to_add:
                if not check_duplicate(user, 'users'):
                    f.write(f"{user}\n")

    def add_tags(tags_to_add): #must be iterable(set, list, etc. Not a string)
        with open('tags.txt', 'a') as f:
            for tag in tags_to_add:
                if not check_duplicate(tag, 'tags'):
                    f.write(f"{tag}\n")

    def del_users(users_to_del): #must be iterable(set, list, etc. Not a string)
        for user in users_to_del:
            with open('users.txt', 'r+') as f:
                data = f.readlines()
                f.seek(0)
                for item in data:
                    if item.strip() != user:
                        f.write(item)
                    f.truncate()

    def del_tags(tags_to_del): #must be iterable(set, list, etc. Not a string)
        for tag in tags_to_del:
            with open('tags.txt', 'r+') as f:
                data = f.readlines()
                f.seek(0)
                for item in data:
                    if item.strip() != tag:
                        f.write(item)
                    f.truncate()

class TwitterOperations():
    
    def get_users_info():
        url = f"https://api.twitter.com/2/users/by?usernames={','.join(DataOperations.get_users())}&user.fields=profile_image_url"

        payload={}
        headers = {
            'Authorization': f"Bearer {app.config['BEARER']}",
            }
        response = requests.request("GET", url, headers=headers, data=payload).json()
        return response['data']

    def get_tweets(users_to_get_tweets, **kwargs):
        formatted_users = " OR ".join([f"from:{user}" for user in users_to_get_tweets])
        
        if 'next_token' in kwargs:
            url = f"https://api.twitter.com/2/tweets/search/recent?query=({formatted_users})&next_token={kwargs.get('next_token')}&tweet.fields=author_id"
        else:
            url = f"https://api.twitter.com/2/tweets/search/recent?query=({formatted_users})&tweet.fields=author_id"
        payload={}
        headers = {
            'Authorization': f"Bearer {app.config['BEARER']}",
            }
        response = requests.request("GET", url, headers=headers, data=payload).json()

        return response

class TwitterUser(object):

    def __init__(self, user_ID, user_handle, friendly_name, profile_picture):
        self.user_ID = user_ID
        self.user_handle = user_handle
        self.friendly_name = friendly_name
        self.profile_picture = profile_picture
    


    
