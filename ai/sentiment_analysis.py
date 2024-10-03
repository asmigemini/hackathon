from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return 'positive', 1 
    elif polarity < 0:
        return 'negative', -1  
    else:
        return 'neutral', 0 
