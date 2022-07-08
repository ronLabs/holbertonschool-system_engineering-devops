#!/usr/bin/python3
"""This module makes a request to reddit api"""
import requests as rq

url = 'https://www.reddit.com/r/{}/hot/.json'


def append_posts(hot_list=[], posts=[], ind=0):
    """Add a post to the list"""
    if ind >= len(posts):
        return
    post = posts[ind].get('data', {})
    title = post.get('title', '')
    hot_list.append(title)
    append_posts(hot_list, posts, ind + 1)


def recurse(subreddit, hot_list=[], params={}):
    """This function fetches a reddit and returns a list with post
    titles for a reddit account"""
    headers = {'User-Agent': 'New agent 1.0'}

    res = rq.get(url.format(subreddit), headers=headers, params=params,
                 allow_redirects=False)

    if res.status_code != 200:
        return None

    try:
        body = res.json().get('data', None)
        if body is None:
            return None
    except ValueError:
        return None

    updated_params = {
        'after': body.get('after', None),
        'count': body.get('dist', 0) + params.get('count', 0),
        'limit': 100
    }

    append_posts(hot_list, body.get('children', []), 0)

    if updated_params.get('after') is None:
        return hot_list

    return recurse(subreddit, hot_list, params=updated_params)
