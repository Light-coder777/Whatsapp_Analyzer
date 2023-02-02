from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected,df1):
    # df1 = df
    if selected != 'Overall':
        df1 = df1[df1['Users']==selected]
    # no of messages
    total_messages = df1.shape[0]
    # no of words in the messages
    words = []
    for message in df1['user_messages']:
        words.extend(message.split())

    # no of links
    links = []
    extract = URLExtract()
    for i in df1['user_messages']:
        links.extend(extract.find_urls(i))
    total_links = len(links)

    # NO of media shared
    total_media = df1[df1['user_messages']==' <Media omitted>\n'].shape[0]
    return total_messages,len(words),total_media,total_links

def most_busy_user(df2):
    t = df2['Users'].value_counts()[:-1]
    percent = round(df2['Users'].value_counts() / df2.shape[0] * 100, 2).reset_index().rename(columns={'index': 'Users', 'Users': 'percent'})
    return t,percent

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users']==selected_user]

    f = open('stop_hinglish.txt')
    stopwords = f.read()
    temp = df[df['Users'] != 'group_notification']
    temp = temp[temp['user_messages'] != ' <Media omitted>\n']
    def remove_stopwords(df):
        # for i in df.user_messages:
        words = []
        for word in df:
            if word not in stopwords:
                if word[0] != '@':
                    words.append(word)
        return " ".join(words)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['user_messages'].apply(remove_stopwords)
    df_wc = wc.generate(temp['user_messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users']==selected_user]

    f = open('stop_hinglish.txt')
    stopwords = f.read()
    temp = df[df['Users'] != 'group_notification']
    temp = temp[temp['user_messages'] != ' <Media omitted>\n']
    # print(stopwords)
    words = []
    for i in temp.user_messages:
        for word in i.lower().split():
            if word not in stopwords:
                if word[0] != '@':
                    words.append(word)

    df_common = pd.DataFrame(Counter(words).most_common(30))
    return df_common

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users']==selected_user]

    emojis = []
    for message in df.user_messages:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users']==selected_user]
    df['month_num'] = df['Date'].dt.month
    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['user_messages'].reset_index()
    # timeline
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline.Month[i] + '-' + str(timeline.Year[i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users']==selected_user]

    df['only_date'] = df['Date'].dt.date
    # df.head()
    daily_timeline = df.groupby('only_date').count()['user_messages'].reset_index()
    # plt.plot(daily_timeline['only_date'], daily_timeline['user_messages'])
    return daily_timeline

# def week_timeline(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['Users']==selected_user]
#     df['date_name'] = df['Date'].dt.day_name()
#     return df['day_name'].value_counts()

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    return df['date_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    user_heatmap = df.pivot_table(index='date_name', columns='period', values='user_messages', aggfunc='count').fillna(0)
    return user_heatmap