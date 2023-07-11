
# Third-party Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from wordcloud import WordCloud, STOPWORDS

# set characters
APP_TITLE = 'Sentiment Analysis'
APP_HEADER = 'This application is using the Streamlit to analyze the sentiment of tweets'
APP_SUBHEADER = 'made by Jie'
SIDEBAR_TITLE = 'Navigation'
SENTIMENT_TEXT_INPUT_MSG = 'Insert your choice here: positive, neutral or negative'
SENTIMENT_BUTTON_MSG = 'Make sentiment analysis'
SENTIMENT_ELSE_MSG = "Please enter your choice"

HOME_MSG = 'Try to create the interactive dashboards with streamlit'

MENU_MSG = 'Choose your next action'
MENU_CHOICES = [
    'Home',
    'Show Random Tweet',
    'Data Analysis',
    'Map',
    'Wordcloud']


@st.cache()
# set load_data function
def load_data():
    # read csv data
    df = pd.read_csv(
        '//Users/syq/Desktop/M2_AI&BA/unit3/Advanced Python/streamlit-sentiment-dashboard/Tweets.csv')
    # collate the data time
    df['tweet_created'] = pd.to_datetime(df['tweet_created'])
    return df

# set home information function


def home_msg():
    st.write(HOME_MSG)

# set show_random_tweet function


def show_random_tweet(data):
    # use sidebar selection to choose different types of sentiment
    random_tweet = st.sidebar.radio(
        'Sentiment', ('positive', 'neutral', 'negative'))
    # use function data.query to get specific data
    st.write(data.query('airline_sentiment == @random_tweet')[['text']].
             sample(n=1).iat[0, 0])

# set fucntion


def data_analysis(data):

    # collate data
    sentiment_count = data["airline_sentiment"].value_counts()
    sentiment_count = pd.DataFrame({"Sentiment": sentiment_count.index,
                                    "Tweets": sentiment_count.values})

    # If "Hide" is net selected, the chart is displayed
    select = st.sidebar.radio("Visualization type", ('Hide', "Histogram"))
    if not select == 'Hide':
        # write arguments to the app
        st.write('Numbers of tweets by sentiment')
        # show a bar chart
        plt.xticks(rotation=45)
        st.bar_chart(data=sentiment_count, x="Sentiment", y="Tweets")
# set function


def interactive_map(data):
    st.write("When and where are users tweeting from?")
    # use a slider widget to collate the hour
    hour = st.slider('Hour of day', 0, 23)
    # collate the hours of data time
    hour_data = data[data["tweet_created"].dt.hour == hour]

    # display the map if close is not selected
    if not st.checkbox('Close', True, key='1'):
        st.write('Tweets location based on the time of day')
        # set specific arguments
        st.write('%i tweets between %i:00 and %i:00' %
                 (len(hour_data), hour, (hour + 1) % 24))
        # a map chart
        st.map(hour_data)
        # display a checkbox widget
        if st.sidebar.checkbox("Show raw data", False):
            st.write(hour_data)

# set function


def wordcould():
    st.write('Display word cloud for what sentiment?')
    # dsplay a single-line text input widget
    tweet = st.radio(
        'Sentiment', ('positive', 'neutral', 'negative'))
    run_analysis = st.button(SENTIMENT_BUTTON_MSG)

    if run_analysis:
        wordcloud1(tweet)
    else:
        st.write(SENTIMENT_ELSE_MSG)


def wordcloud1(text):
    data = pd.read_csv(
        '//Tweets.csv')
    # Send the GET request to the specified URL
    r = requests.get(f"http://127.0.0.1:5000/predict?text={text}")
    # when r.status_code =200, the request is successful
    if r.status_code == 200:
        # return values from URL
        polarity = r.json()['polarity']
        if polarity > 0.0:
            df = data[data['airline_sentiment'] == 'positive']
            # get a new string by concatenating the element ' text'
            words = ' '.join(df['text'])
            # get a new string by concatenating the element,and by separating
            # sentences and filtering words
            processed_words = ' '.join([word for word in words.split(
            ) if 'http' not in word and not word.startswith('@') and word != 'RT'])
            # set wordcould
            wordcloud = WordCloud(
                # set block words
                stopwords=STOPWORDS,
                # set background color
                background_color='white',
                # set the output chart width
                width=800,
                # set the output chart height,and generate the wordcloud
                height=640).generate(processed_words)
            # set a figure and its size as 12*8
            fig, ax = plt.subplots(figsize=(12, 8))
            # set a heat map
            ax.imshow(wordcloud)
            # show plot
            st.pyplot(fig)
        elif polarity < 0:
            df = data[data['airline_sentiment'] == 'negative']
            words = ' '.join(df['text'])
            processed_words = ' '.join([word for word in words.split(
            ) if 'http' not in word and not word.startswith('@') and word != 'RT'])
            wordcloud = WordCloud(
                stopwords=STOPWORDS,
                background_color='white',
                width=800,
                height=640).generate(processed_words)
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.imshow(wordcloud)
            st.pyplot(fig)
        else:
            df = data[data['airline_sentiment'] == 'neutral']
            words = ' '.join(df['text'])
            processed_words = ' '.join([word for word in words.split(
            ) if 'http' not in word and not word.startswith('@') and word != 'RT'])
            wordcloud = WordCloud(
                stopwords=STOPWORDS,
                background_color='white',
                width=800,
                height=640).generate(processed_words)
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.imshow(wordcloud)
            st.pyplot(fig)


def main():
    # load data
    df = load_data()
    # set app title
    st.title(APP_TITLE)
    # set app header
    st.header(APP_HEADER)
    # set app sidebar title
    st.sidebar.title(SIDEBAR_TITLE)
    # set app sidebar selection box
    menu_action = st.sidebar.selectbox(MENU_MSG, MENU_CHOICES)

    if menu_action == 'Home':
        st.subheader(APP_SUBHEADER)
        home_msg()

    elif menu_action == 'Show Random Tweet':
        show_random_tweet(df)

    elif menu_action == 'Data Analysis':
        data_analysis(df)

    elif menu_action == 'Map':
        interactive_map(df)

    else:
        wordcould()


if __name__ == '__main__':
    main()

