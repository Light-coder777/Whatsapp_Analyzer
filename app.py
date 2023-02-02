import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)
    data = bytes_data.decode('utf-8')
    # st.text(data)
    df = preprocess.preprocessor(data)
    # st.dataframe(df)
    # fetch unique users
    user_list = df['Users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)


    if st.sidebar.button("Show Analysis"):
        total_messages,total_words,total_media,total_links = helper.fetch_stats(selected_user,df)
        st.title("Data Statistics")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total_messages)
        with col2:
            st.header("Total words")
            st.title(total_words)
        with col3:
            st.header("Total media")
            st.title(total_media)
        with col4:
            st.header("Total links")
            st.title(total_links)
        # Monthly timeline
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        plt.plot(timeline['time'], timeline['user_messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['user_messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Weekly timeline
        # week_timeline = helper.week_timeline(selected_user,df)
        # fig, ax = plt.subplots()
        # plt.plot(week_timeline['day_name'], week_timeline['day_name'])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Heat Map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,percent_df = helper.most_busy_user(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(percent_df)

            # col1 = st.columns(1)
            # with col1 :
            # Pie Chart
            fig,ax = plt.subplots()
            ax.pie(percent_df['percent'],labels=percent_df['Users'],autopct='%0.2f')
            st.pyplot(fig)

        # WordCloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        st.title("Most Common Words")
        df_common = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(df_common[0],df_common[1]) #horizontal barchart
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("emoji analysis")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            try:
                st.header('Pie chart')
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(8),labels=emoji_df[0].head(8),autopct='%0.2f')
                # ax.barh(emoji_df[0].head(8),emoji_df[1].head(8))
                st.pyplot(fig)
            except:
                st.write('Not enough different types emojis used')

