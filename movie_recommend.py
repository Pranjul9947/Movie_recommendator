import streamlit as st
import pickle
import pandas as pd

# Load pre-trained models
data = pickle.load(open('models.pkl', 'rb'))
movies = data['movies']
content_sim = data['content_sim']
collab_sim = data['collab_sim']
user_item_matrix = data['user_item_matrix']
svd = data['svd']

# App title
st.title('Movie Recommender System')

# Recommendation type selection
rec_type = st.radio(
    "Select recommendation type:",
    ('Content-Based (Genres)', 'Collaborative (User Ratings)')
)

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Select a movie you like:",
    movie_list
)

# Number of recommendations
num_rec = st.slider('Number of recommendations:', 1, 20, 5)

def get_content_rec(movie_title, n=5):
    idx = movies[movies['title'] == movie_title].index[0]
    sim_scores = list(enumerate(content_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]

def get_collab_rec(movie_title, n=5):
    try:
        movie_id = movies[movies['title'] == movie_title]['movieId'].values[0]
        idx = user_item_matrix.columns.get_loc(movie_id)
        sim_scores = list(enumerate(collab_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        movie_indices = [i[0] for i in sim_scores]
        movie_ids = [user_item_matrix.columns[i] for i in movie_indices]
        return movies[movies['movieId'].isin(movie_ids)]['title']
    except:
        return pd.Series(["Not enough data for collaborative filtering"])

if st.button('Get Recommendations'):
    if rec_type == 'Content-Based (Genres)':
        recommendations = get_content_rec(selected_movie, num_rec)
    else:
        recommendations = get_collab_rec(selected_movie, num_rec)
    
    st.subheader(f"Recommended Movies based on {selected_movie}:")
    for i, movie in enumerate(recommendations, 1):
        st.write(f"{i}. {movie}")