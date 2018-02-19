

import twitter
import json

CONSUMER_KEY = 'VBNzEdcD7FfU2SGKdZVoZ09LY'
CONSUMER_SECRET = 'QQy27eW0fWfMrUkMzN7a0HjgAwIqvbLomEExTUhTgANTEkOifT'
OAUTH_TOKEN = '910402876228345856-cF3ZuyT1IGQ61ClYiDoIRdADgzXhBj1'
OAUTH_TOKEN_SECRET = 'XBrW3On8y1vGPc7iwECQ3sHwah2eauztJNDkwezjivhM9'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

#round counter
round = 0;

#while loop for 2 rounds
while (round < 2):
    q = input('Enter a search term: ')


    count = 1000
    search_results = twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses']

    print("Searching...")
    print()

    for _ in range(5):

        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError as e:  # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']



    status_texts = [status['text']
                    for status in statuses]

    words = [w
             for t in status_texts
             for w in t.split()]





    #open file for scores
    sent_file = open('AFINN-111.txt')

    scores = {}  # initialize an empty dictionary
    for line in sent_file:

        term, score = line.split("\t")

        # The file is tab-delimited.
        # "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
        #print(scores)

    score = 0
    for word in words:
        if word in list(scores.keys()):

            score = score + scores[word]

    #set scores and terms from each round
    if (round == 0):
        term1 = q
        score1 = (float(score))
    if (round ==1):
        term2 = q
        score2 = (float(score))


    #increase round
    round = round + 1;


#output
print("Term 1:")
print(term1)
print("Sentiment Score:")
print(score1)
print()
print("Term 2:")
print(term2)
print("Sentiment Score:")
print(score2)

print()

#test to see which is higher
if (score1 > score2):
    print(term1 + " has a higher sentiment score than " + term2)
elif (score1 == score2):
    print("The terms have equal sentiment scores")
else:
    print(term2 + " has a higher sentiment score than " + term1)
