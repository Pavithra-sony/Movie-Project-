import pickle
import streamlit as st
import requests
import urllib.parse

# Fetch movie poster by title from TMDb API
def fetch_poster_by_title(title):
    api_key = "2aba13ae941aec21405c2cbcf7fcd721"  # Your actual TMDb API key
    query = urllib.parse.quote(title)  # Safely encode the title
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"

    response = requests.get(url)
    data = response.json()

    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    
    return "https://via.placeholder.com/300x450.png?text=No+Image"


# Recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title  # Get movie title
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster_by_title(movie_title))  # Fetch poster by title

    return recommended_movie_names, recommended_movie_posters


# Streamlit UI
st.header('Movie Recommender System')

# Load movie data and similarity data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
