import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
spotify_data = pd.read_csv('df US_spotify.csv')

# Dropdown menu for visualization selection
chart_option = st.selectbox(
    'Choose a Visualization',
    [
        'Choose a Visualization',
        'Artist Popularity Trends',
        'Top 5 Songs (2017-2021)',
        'Top 10 Artists (2017-2021)',
        'Artist Streams Over Time',
    ]
)

# Set a style for all charts
sns.set_style("darkgrid")

# Visualization logic
if chart_option == 'Top 10 Artists (2017-2021)':
    data_subset = spotify_data[spotify_data['year'].between(2017, 2021)]
    top_10_artists = data_subset['artist'].value_counts().head(10)
    top_10_df = pd.DataFrame(top_10_artists).reset_index()
    top_10_df.columns = ['artist', 'count']

    # Horizontal bar chart with a custom color palette
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='artist', data=top_10_df, palette='Blues_r')
    plt.title('Top 10 Artists (2017-2021)')
    st.pyplot(plt)

elif chart_option == 'Artist Streams Over Time':
    data_subset = spotify_data[spotify_data['year'].between(2017, 2021)]
    top_10_artists = data_subset['artist'].value_counts().head(10).index
    artist_data_filtered = data_subset[data_subset['artist'].isin(top_10_artists)]

    artist_choice = st.selectbox('Choose an Artist', top_10_artists)
    artist_info = artist_data_filtered[artist_data_filtered['artist'] == artist_choice]

    # Change to a scatter plot instead of an area plot
    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=artist_info, x='year', y='streams', color='green', s=100)
    plt.title(f'{artist_choice} - Streams Over Time (2017-2021)')
    plt.grid(True)
    st.pyplot(plt)

elif chart_option == 'Top 5 Songs (2017-2021)':
    top_songs = spotify_data['title'].value_counts().head(5).index
    top_songs_data = spotify_data[spotify_data['title'].isin(top_songs)]
    song_streams = top_songs_data.groupby('title')['streams'].sum().reset_index()
    song_streams_sorted = song_streams.sort_values(by='streams', ascending=False)

    # Horizontal bar chart instead of a pie chart
    plt.figure(figsize=(8, 5))
    sns.barplot(x='streams', y='title', data=song_streams_sorted, palette='Spectral')
    plt.title('Top 5 Songs by Total Streams (2017-2021)')
    st.pyplot(plt)

elif chart_option == 'Artist Popularity Trends':
    selected_artist = st.selectbox('Choose an Artist', spotify_data['artist'].unique())
    artist_trend_data = spotify_data[spotify_data['artist'] == selected_artist].groupby('year')['streams'].sum().reset_index()

    # Change to a bar chart for artist popularity trends
    plt.figure(figsize=(10, 6))
    sns.barplot(data=artist_trend_data, x='year', y='streams', color='blue')
    plt.title(f'{selected_artist} Popularity Trend (2017-2021)')
    plt.grid(True)
    st.pyplot(plt)
