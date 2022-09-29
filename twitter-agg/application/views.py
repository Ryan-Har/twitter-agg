from application import app
from application.home import DataOperations, TwitterOperations, TwitterUser
from flask import render_template

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

    tweets = TwitterOperations.get_tweets([user.user_handle for user in users])
    

    return render_template('home.html', tweets=tweets['data'])
    

@app.route('/api/')
def api():
    return render_template('home.html')
