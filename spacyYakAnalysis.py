import pandas
import matplotlib.pyplot as plt
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
#Mohamed Gadelrab, mag2sqv

#create pipeline and add spacytextblob to it
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob")

#convert csv to dataframe
colnames=['Date', 'Yak'] 
df = pandas.read_csv("database.csv", names=colnames, encoding='latin-1')

#compute the polarity score, from -1 to 1, for each yak
polarityDict = {}
for index, row in df.iterrows():
    body = row['Yak']
    docx = nlp(body)
    polarityDict[row['Yak']] = docx._.polarity

#Add polarity scores to dataframe
df['polarity'] = df['Yak'].map(polarityDict)

#Make a dataframe with two columns: Date and average polarity score
datePolarityDF = df.groupby('Date')['polarity'].mean().reset_index()

print(datePolarityDF)
#convert our test set to a dataframe for comparison
colN=['Date', 'polarity'] 
tdf = pandas.read_csv("humanSentiment.csv", names=colN, encoding='latin-1')
tdf['Polarity'] = tdf['polarity'].astype(float)

#Plot the dates from 11-19 to 12-09 against their averaged polarity.
plt.plot(datePolarityDF['Date'],datePolarityDF['polarity'], '-o', label = "Spacy-Determined Polarity")
plt.plot(tdf['Date'],tdf['polarity'], 'o', label = "Human-Determined Polarity")
plt.legend(loc="lower right")
plt.title('Daily Yikyak Average Polarity Score')
plt.xlabel('Date')
plt.ylabel('Polarity')
plt.xticks(rotation = 50)
plt.show()



