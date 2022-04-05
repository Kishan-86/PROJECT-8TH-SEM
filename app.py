
import streamlit as st
import tweepy as tweepy

import wordcloud as wordcloud
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns



consumerKey = "dESc2np7NEyIR4OyQff5EKqDv"
consumerSecret = "7YzJC6ylSHcLMrXLantZxPEwm0zGa3xOuSFuEvRe42giL7vmK0"
accessToken = "714414466373394433-4df0quDG5QsnyonmwmtAzpfqGOpa6Oh"
accessTokenSecret = "sNXDoqS5Pt959Eme9Emg26lIF8Y9HJi6pyytO615dKnnC"


#Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)



# A function to clean the tweets
def cleanTxt(text):
	text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
	text = re.sub('#', '', text)  # Removing '#' hash tag
	text = re.sub('RT[\s]+', '', text)  # Removing RT
	text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink

	return text


# A Function To get the score
def getAnalysis(score):
	if score < 0:
		return 'Negative'
	elif score == 0:
		return 'Neutral'
	else:
		return 'Positive'


# Create a function to get the Subjectivity
def getSubjectivity(text):
	return TextBlob(text).sentiment.subjectivity


# Create a function to get the polarity
def getPolarity(text):
	return TextBlob(text).sentiment.polarity


# A function to show Polarity Graph.
def Plot_Analysis(user_name):

	posts = api.user_timeline(screen_name=user_name, count=100, lang="en", tweet_mode="extended")

	df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


	# Clean the tweets
	df['Tweets'] = df['Tweets'].apply(cleanTxt)

	# Create two new columns 'Subjectivity' & 'Polarity'
	df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
	df['Polarity'] = df['Tweets'].apply(getPolarity)


	df['Analysis'] = df['Polarity'].apply(getAnalysis)

	return df

def get_tweets(posts):
	l = []
	i = 1
	for tweet in posts[:10]:
		l.append(tweet.full_text)
		i = i + 1
	return l

# A function to show recent tweets
def Show_Recent_Tweets(user_name):
	# Extract 100 tweets from the twitter user
	posts = api.user_timeline(screen_name=user_name, count=100, lang="en", tweet_mode="extended")

	recent_tweets = get_tweets(posts)
	return recent_tweets


def gen_wordcloud(user_name):
	posts = api.user_timeline(screen_name=user_name, count=100, lang="en", tweet_mode="extended")

	# Create a dataframe with a column called Tweets
	df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
	# word cloud visualization
	allWords = ' '.join([twts for twts in df['Tweets']])
	wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
	plt.imshow(wordCloud, interpolation="bilinear")
	plt.axis('off')
	plt.savefig('WC.jpg')
	img = Image.open("WC.jpg")
	return img


def get_data(user_name):
	posts = api.user_timeline(screen_name=user_name, count=100, lang="en", tweet_mode="extended")

	df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

	# Clean the tweets
	df['Tweets'] = df['Tweets'].apply(cleanTxt)

	# Create two new columns 'Subjectivity' & 'Polarity'
	df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
	df['Polarity'] = df['Tweets'].apply(getPolarity)

	df['Analysis'] = df['Polarity'].apply(getAnalysis)
	return df


def app():


	st.title("Tweet Sentiment Analyzer ")


	activities=["Tweet Analyzer","Generate Twitter Data"]

	choice = st.sidebar.selectbox("Select Your Activity", activities)



	if choice == "Tweet Analyzer":

		st.subheader("Analyze the tweets of your favourite Personalities")

		st.subheader("This tool performs the following tasks :")

		st.write("1. Fetches the 10 most recent tweets from the given twitter handel")
		st.write("2. Generates a Word Cloud")
		st.write("3. Performs Sentiment Analysis a displays it in form of a Bar Graph")


		user_name = st.text_area("Enter the exact twitter handle of the Personality (without @)")


		Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])


		if st.button("Analyze"):


			if Analyzer_choice == "Show Recent Tweets":

				st.success("Fetching last 10 Tweets")

				recent_tweets= Show_Recent_Tweets(user_name)

				st.write(recent_tweets)

			elif Analyzer_choice=="Generate WordCloud":

				st.success("Generating Word Cloud")

				img=gen_wordcloud(user_name)

				st.image(img)

			else:

				st.success("Generating Visualisation for Sentiment Analysis")

				df= Plot_Analysis(user_name)

				st.write(sns.countplot(x=df["Analysis"],data=df))

				st.pyplot(use_container_width=True)


	else:

		st.subheader("This tool fetches the last 100 tweets from the twitter handel & Performs the following tasks")

		st.write("1. Converts it into a DataFrame")
		st.write("2. Cleans the text")
		st.write("3. Analyzes Subjectivity of tweets and adds an additional column for it")
		st.write("4. Analyzes Polarity of tweets and adds an additional column for it")
		st.write("5. Analyzes Sentiments of tweets and adds an additional column for it")


		user_name = st.text_area("*Enter the exact twitter handle of the Personality (without @)*")

		if st.button("Show Data"):

			st.success("Fetching Last 100 Tweets")

			df=get_data(user_name)

			st.write(df)

if __name__ == "__main__":
	app()