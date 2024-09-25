from textblob import TextBlob

def analyze_sentiment(mood_text):
    blob = TextBlob(mood_text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        return 'positive'
    elif sentiment_score < 0:
        return 'negative'
    else:
        return 'neutral'
