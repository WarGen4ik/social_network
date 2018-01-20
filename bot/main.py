from bot.config import *
from requests import get, post, Session
from random import randint


def register_users():
    available_emails = ['bot', 'test']
    email_number = 0
    users = list()
    i = 0
    while i < number_of_users:
        body = {'email': '{}{}@gmail.com'.format(available_emails[email_number], i + 1),
                'password': 'botbotbot'}
        response = post(SITE_NAME + 'register/', json=body)
        if response.status_code == 400:
            email_number += 1
            continue
        users.append(body)
        i += 1
    return users


def create_posts(user: dict):
    response = post(SITE_NAME + 'auth/', json=user)
    headers = {'Authorization': 'JWT {}'.format(response.json()['token']),
               'Content-Type': 'application/json'}

    count_posts = randint(0, max_posts_per_user)

    for i in range(count_posts):
        body = {'title': '{} {} post'.format(user['email'], i + 1),
                'text': 'Some text from {}'.format(user['email'])}
        post(SITE_NAME + 'create/post/', json=body, headers=headers)


def like_posts(user):
    response = post(SITE_NAME + 'auth/', json=user)
    headers = {'Authorization': 'JWT {}'.format(response.json()['token'])}

    posts = get(SITE_NAME + 'view/posts/', headers=headers).json()

    for i in range(max_likes_per_user):
        post_to_like = posts[randint(0, len(posts) - 1)]
        body = {'post': post_to_like['id']}
        post(SITE_NAME + 'like/', json=body, headers=headers)


if __name__ == '__main__':
    users = register_users()
    for user in users:
        create_posts(user)

    for user in users:
        like_posts(user)
