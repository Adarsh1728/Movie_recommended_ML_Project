import streamlit as st
import pandas as pd
import pickle
import requests
import platform

# Fetch poster from TMDB
def fetch_poster(movie_id): 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c4f96c6c39991eee118d7189d35d7e74&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return "https://via.placeholder.com/500x750?text=No+Image"
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation logic
def recommend(movie):
    try:
        movie_index = Movies[Movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_posters = []

        for i in movie_list:
            movie_id = Movies.iloc[i[0]]['id']
            recommended_movies.append(Movies.iloc[i[0]]['title'])
            recommended_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_posters
    except IndexError:
        return ["Movie not found."] * 5, ["https://via.placeholder.com/500x750?text=No+Image"] * 5

# Load data
Movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
Movies = pd.DataFrame(Movies_dict)

# Streamlit UI
st.title('🎬 Movie Recommendation System')

selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", Movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
            