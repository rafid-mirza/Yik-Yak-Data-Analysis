import cohere
import pandas
from cohere.responses.classify import Example

import asyncio

async def wait_60_seconds():
    print("Waiting for 60 seconds...")
    await asyncio.sleep(60)
    print("60 seconds have passed. Now executing the code.")
    # Your code goes here

# co = cohere.Client('5H78yE5Mm7GM6S6IjsHNtLEDrIYP4pXFcJGuQGJy')
# classifications = co.classify(
#   model='embed-english-v2.0',
#   inputs=["This item was broken when it arrived", "This item broke after 3 weeks"],
#   examples=[Example("The order came 5 days early", "positive"), Example("The item exceeded my expectations", "positive"), Example("I ordered more for my friends", "positive"), Example("I would buy this again", "positive"), Example("I would recommend this to others", "positive"), Example("The package was damaged", "negative"), Example("The order is 5 days late", "negative"), Example("The order was incorrect", "negative"), Example("I want to return my item", "negative"), Example("The item\'s material feels low quality", "negative")])
# print('The confidence levels of the labels are: {}'.format(
#        classifications.classifications))
colnames=['Date', 'Yak'] 
df = pandas.read_csv("database.csv", names=colnames, encoding='latin-1')


print(df)

import cohere  
co = cohere.Client('AdejHg0jqr05TQpHWauZ6J4RbfKrkFXDaoTkMOSP')
responses = {}

# test = df.iloc[0]["Yak"]

# prompt = "Using only one of the following six words (sadness, happiness, fear, anger, surprise and disgust), rank this statement as one of the six basic emotions, outputting only one of those six words: " + test

# response = co.generate(  
#     model='command-nightly',  
#     prompt = prompt,  
#     max_tokens=200, # This parameter is optional. 
#     temperature=0.750)

# intro_paragraph = response.generations[0].text
# print(test)
# print(intro_paragraph)


count = 0
for index, row in df.iterrows():
  if count >= 5:
     asyncio.run(wait_60_seconds())
     count = 0

  prompt = "I will give you a statement. I need you to return only one word which expresses the sentiment of the statement using the following words: admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride, realization, relief, remorse, sadness, surprise, neutral. The statement is: " +  + row['Yak'] + "DO NOT EXPLAIN YOUR ANSWER OR GIVE ME MORE THAN ONE WORD."
  try:
    response = co.generate(  
          model='command-nightly',  
          prompt = prompt,  
          max_tokens=200, # This parameter is optional. 
          temperature=0.750)
    intro_paragraph = response.generations[0].text
  except cohere.CohereError as e:
      print(e.message)
      print(e.http_status)
      print(e.headers)
      intro_paragraph = e.message
  responses[row['Yak']] = intro_paragraph
  print(row['Yak'], intro_paragraph)
  count += 1

print(responses)
df['emotion'] = df['Yak'].map(responses)

print(df)
df.to_csv('file_name.csv', index=False)



