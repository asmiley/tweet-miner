# tweet-mining

A command line tool built using Tweepy to mine Tweets that include a provided query. Has full Unicode support for mining tweets in all languages.

##  Arguments 
 
 	tweet-miner query file since_id max_id
	
	* query - Search term
	* file - The name of the file to create and/or write over
	* since_id - Optional. When retrieving tweets posted since a previous query was completed, insert the tweet_id from the top of the previous file after this flag.
	* max_id - If a search is interrupted, insert the tweet of the last tweet in the file after this flag to complete the search.
	