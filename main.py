import sys
import os
import csv
import tweepy
from textblob import TextBlob as TextBlob

'''
main file in stock0.2
'''

stockname = input("input stockname: ")
start_date = input("startdatum, (YYYY-DD-MM): ")
end_date = input("einddatum, (YYY-DD-MM): ")


#maak een tweedimensionale array van de irritante csv file
'''
1 = date
2 = opening price
3 = high
4 = low
5 = close
6 = volume
'''
with open('005935.csv', newline='') as csvfile:
    stocks = csv.reader(csvfile, delimiter=' ', quotechar='|')
    stockdata = []
    for row in stocks:
        stockdata.append(row)
    for i in range (0, len(stockdata)):
        stockdata[i] = stockdata[i][0].split(',')
        stockdata[i].append('null')

    with open('result_file.txt', 'w') as result_file:
        print(result_file.name)
        result_file.write("test")

# credentials voor twitter api johnashuben
consumer_key = 's8ZEi8uunyCGs4uU2NXmDtOOv'
consumer_key_secret = '1H6KhHyirN317jS7eDsfHA29rvJG7MQVjeSBQtgJnmrseKnQyW'
access_token = '859333296425246722-ZY40UIcrn7HQrm4rlagha8QlQBT5n86'
access_token_secret = 'alV6tlVJShpfpu11W3OYLZFI8C8zJjcHjTG3wm4CnXsYA'

# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

# get api
api = tweepy.API(auth)

temp_sentiment_sum = 0
temp_counter = 0

temp_current_date_in_format = str(2017) + '-' + str('Apr') + '-' + str('03')


for tweet in tweepy.Cursor(api.search, q=stockname, \
                           lang="en", \
                           since=start_date, \
                           until=end_date, \
                           wait_on_rate_limit=True, \
                           wait_on_rate_limit_notify=True).items():

    # sentiment analysis
    tweet_year = tweet.created_at.year
    tweet_month = tweet.created_at.month
    tweet_day = tweet.created_at.day
    print(tweet.created_at.hour)

    # date in right format
    switcher = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "jun",
        7: "Jul",
        8: "aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    tweet_date_in_format = str(tweet_day) + '-' + str(switcher.get(tweet_month)) + '-' + str(tweet_year)


    tweet_text = str(tweet.text)
    tweet_textblob_item = TextBlob(tweet_text)
    tweet_sentiment = tweet_textblob_item.sentiment.polarity

    print(tweet_date_in_format)
    print(temp_current_date_in_format)

    if tweet_date_in_format == temp_current_date_in_format:
        temp_counter += 1
        temp_sentiment_sum += tweet_sentiment
    else:
        print('new day')
        print('amount of tweets: ', temp_counter)
        temp_counter = 0
        day_avg_sentiment = temp_sentiment_sum  #dit is nog niet gemiddelde, misschien nog slimmer over nadenken
        temp_sentiment_sum = tweet_sentiment
        for k in range (0, len(stockdata)):
            print(str(stockdata[k][0]))
            print(str(temp_current_date_in_format))
            if str(stockdata[k][0]) == str(temp_current_date_in_format):
                print("matching date found")
                temp_current_date_in_format = tweet_date_in_format
                stockdata[k][7] = day_avg_sentiment
                print(str(stockdata[k][0]) + '::' + str(stockdata[k][3] - stockdata[k][4]) + str(stockdata[k][7]))
                with open('result_file.txt', 'w') as result_file:
                    result_file.write('date:: ', str(stockdata[k][0]), 'difference:: ',str(stockdata[k][3] - stockdata[k][4]), 'day_avg_sentiment:: ', str(stockdata[k][7]))
                break
        temp_current_date_in_format = tweet_date_in_format
        print('no matching date found, die luie zakken op wallstreet werken zeker niet in het weekend')