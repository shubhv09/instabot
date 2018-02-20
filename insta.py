import requests,urllib
# Used for working with the url's
from textblob import TextBlob
#Python (2 and 3) library for processing textual data.
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = '6b48cf0bb798497d80904d55f89c930d'
BASE_URL = 'https://api.instagram.com/v1/'

#self imformation function

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        print 'Username: %s' %(user_info['data']['username'])
        print'Bio: %s' %(user_info['data']['bio'])
        print 'No. of people you follow: %s' %(user_info['data']['counts']['follows'])
        print 'No. of followers: %s' %(user_info['data']['counts']['followed_by'])
        print 'Your website : %s' %(user_info['data']['website'])
        print 'Your id: %s' %(user_info['data']['id'])
        print 'Your full name : %s'%(user_info['data']['full_name'])
        print 'Your Profle picture is %s'%(user_info['data']['profile_picture'])
    else:
        print 'Status code other than 200 received!'

#user id details

def get_user_id(insta_username):

    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

#user info followers, people and post

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if 'data' in user_info:
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

#own post details

def get_own_post():

    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

#check post and download

def get_user_post(insta_username):

    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
    else:
        print 'Post does not exist!'

#like a post

def like_a_post(insta_username):
	media_id = get_user_post(insta_username)

	request_url = (BASE_URL + 'media/%s/likes') % (media_id)
	payload = {"access_token": APP_ACCESS_TOKEN}
	print 'POST request url : %s' % (request_url)
	post_a_like = requests.post(request_url, payload).json()

	if post_a_like['meta']['code'] == 200:
		print 'Like was successful!'
	else:
		print 'Your like was unsuccessful. Try again!'

#del negative comments
def delete_negative_comment(insta_username):

    media_id = get_user_post(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:

        if len(comment_info['data']) > 0:

            for comment in comment_info['data']:
                comment_text = comment['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                if blob.sentiment.p_neg > blob.sentiment.p_pos:

                    comment_id = comment['id']

                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                        media_id, comment_id, APP_ACCESS_TOKEN)

                    print 'DELETE request url : %s' % (delete_url)

                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!'
                    else:
                        print 'Could not delete the comment'

        else:
            print 'No comments found'
    else:
        print 'Status code other than 200 received!'

#start bot

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "j.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "j":
            exit()
        else:
            print "wrong choice"

start_bot()