from application import app
from application.home import DataOperations, TwitterOperations, TwitterUser
from quart import render_template, request
import asyncio

@app.route('/')
async def main():
    tweet_calls = [
        asyncio.ensure_future(DataOperations.user_tweets()),
        asyncio.ensure_future(DataOperations.tag_tweets())
    ]
    tweets = await asyncio.gather(*tweet_calls)

    return await render_template('home.html', user_tweets=tweets[0], tag_tweets=tweets[1], zip=zip, enumerate=enumerate)

@app.route('/api/')
async def api():
    user_next_token = request.args.get('user_next_token')
    tag_next_token = request.args.get('tag_next_token')
    if not (user_next_token or tag_next_token):
        return None
    else:
        tweet_calls = [
        asyncio.ensure_future(DataOperations.user_tweets(user_next_token)),
        asyncio.ensure_future(DataOperations.tag_tweets(tag_next_token))
        ]
        tweets = await asyncio.gather(*tweet_calls)

        return await render_template('reload.html', user_tweets=tweets[0], tag_tweets=tweets[1], zip=zip, enumerate=enumerate)
