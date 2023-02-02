import pandas as pd
import re
file = 'WhatsApp Chat with Chain Reaction Peeps.txt'
def yearformatter(s):
  pattern = "\d{1,2}/\d{1,2}/"
# s = df.Date[0]
  re.split(pattern,s)
  return re.findall(pattern,s)[0] + '20' + re.split(pattern,s)[1]

def preprocessor(data):
    # f = open(file,'r',encoding='utf-8')
    # data = f.read()
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_messages': messages[1:], 'Date': dates})
    # Convert the message_date type to datetime
    df['Date'] = df['Date'].astype(str).apply(lambda x: yearformatter(x))
    df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y, %H:%M - ")
    users = []
    messages = []
    for i in df['user_messages']:
        if ':' in i:
            x = i.split(':')
            users.append(x[0])
            messages.append(x[1])
        else:
            messages.append(i)
            users.append('group_notification')

    df['Users'] = users
    df['user_messages'] = messages
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['date_name'] = df['Date'].dt.day_name()
    period = []
    for hour in df[['date_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
