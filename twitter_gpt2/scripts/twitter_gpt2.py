# import statements:
import tweepy
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import time
import re
from random import randint
from datetime import datetime
import json
import os

#Twitter API credentials
consumer_key = 'NvmfyRI0y3lbskoDcFhNklWMX'
consumer_secret = 'fClojvv7531V4kZ59M24tVvOBnva6bRhRxwloGu8uAJMc3NMsj'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPKfOAEAAAAAy2HePVkdpqJi743j30qdSV%2BQBqw%3DPw9lZl6qCrPQZVzeYLyADdxFh0KvfCGwe2iwt4VrRdoWdRqZ5o'
access_key = ""
access_secret = ""

# Used to store tweet data: 
tweets_text = {}
cleaned_tweets_text = {}
generated_tweets = {}

# input parameters:
filepath = ''
username = ''


def save_file(out_dict, username, tweets):
    global filepath
    json_tweets = json.dumps(out_dict)
    now = re.sub(" ", "_", str(datetime.now()))
    now = re.sub("[:.]", "-", now)
    if tweets:
        content = "tweets"
        savepath = filepath + "/tweets/"
    else:
        content = "gen"
        savepath = filepath + "/generated/"
    f = open(savepath + f'{username}_{content}__{now}.txt', 'w')
    f.write(json_tweets)
    f.close()
    

def get_all_tweets(screen_name):
    global tweets_text
    global cleaned_tweets_text
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets 
    alltweets = []
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode='extended')
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, tweet_mode='extended')
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print(f"...{len(alltweets)} tweets downloaded so far")
    
    #transform the tweepy tweets into a dict that will populate the json text file: 
    # outtweets = {tweet.id_str: tweet._json for tweet in alltweets}
    tweets_text = {tweet.id_str:tweet.full_text for tweet in alltweets}
    
    removelist = ".,'!?\s"

    for tweet_id, tweet_text in tweets_text.items():
        cleaned_tweet = re.sub("(@[A-Za-z0-9]+)|(_[A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", tweet_text)
        cleaned_tweet = re.sub("\s+", " ", cleaned_tweet.strip())
        cleaned_tweet = re.sub("RT", "", cleaned_tweet)
        # cleaned_tweet = re.sub(r'[^\w'+removelist+']', '', cleaned_tweet)
        cleaned_tweet = re.sub(" : ", "", cleaned_tweet)
        cleaned_tweets_text[tweet_id] = cleaned_tweet
    
    save_file(tweets_text, screen_name, True)
    pass


def generate(t_id):
    global generated_tweets
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    t_list = list(cleaned_tweets_text.values())
    seed = " ".join([t_list[randint(0, len(t_list) - 1)] for i in range(3)]) + ". "
    seed_length = len(seed)
    
    print("Initialized...")
    
    inputs = tokenizer.encode(seed, return_tensors='pt')
    outputs = model.generate(inputs, max_length=200, do_sample=True)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    tweet = text[seed_length:].strip()

    generated_tweets[t_id] = tweet


def get_new_tweets(pull_new, filename, username, num_gen):
    global tweets_text
    global cleaned_tweets_text
    global generated_tweets
    global filepath
    generated_tweets = {}
    
    if pull_new:
        get_all_tweets(username)
        print("Got new tweets...")
    else:
        f = open(filepath + "/tweets/" + filename, "r")
        tweets_text = json.loads(f.read())
        
        for tweet_id, tweet_text in tweets_text.items():
            cleaned_tweet = re.sub("(@[A-Za-z0-9]+)|(_[A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", tweet_text)
            cleaned_tweet = re.sub("\s+", " ", cleaned_tweet.strip())
            cleaned_tweet = re.sub("RT", "", cleaned_tweet)
            # cleaned_tweet = re.sub(r'[^\w'+removelist+']', '', cleaned_tweet)
            cleaned_tweet = re.sub(" : ", "", cleaned_tweet)
            cleaned_tweets_text[tweet_id] = cleaned_tweet
        print("Read in old tweets")
            
    for i in range(num_gen):
        generate(i)
        print(f"Generated tweet {i}...")
    
    save_file(generated_tweets, username, False)
    
    for tweet in generated_tweets.values():
        print(tweet, "\n")
            
def main():
    global filepath
    global username
    pull_new_input = False
    userfile_exists = False
    filename_input = "" 
    num_input = ""
    
    username = input("Enter username: ")
    filepath = "../users/" + username
    
    if os.path.isdir(filepath):
        userfile_exists = True
        pull_fresh = input("Pull fresh from twitter? y/n: ")
        pull_new_input = (True if pull_fresh == "y" else False)
    else:
        pull_new_input = True
        userfile_exists = False
        os.mkdir(filepath)
        os.mkdir(filepath + "/tweets")
        os.mkdir(filepath + "/generated")
    
    if not pull_new_input:
        filename_input = input("Enter filename to retrieve: ")
    
    num_input = int(input("Enter number of tweets to generate: "))
    
    get_new_tweets(pull_new_input, filename_input, username, num_input)
    # get_new_tweets(False, 'rylandhunstad_tweets__2021-04-01_01-34-06-037050.txt', 'rylandhunstad', 2)


main()