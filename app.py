import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    respons= requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    #data = requests.get(url)
    data = respons.json()
    print(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies =[]
    recommended_movies_poster =[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
         # fetch poster from API 
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

similarity = movies_dict = pickle.load(open('similarity.pkl','rb'))
movies =pd.DataFrame(movies_dict)


movies_dict = pickle.load(open('moviesdict.pkl','rb'))
movies =pd.DataFrame(movies_dict)

st.title('Movie Recommender System')
selected_movie_name= st.selectbox(
    'How would like to be contacted',
    movies['title'].values
 )


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    
    for col, movie_name, movie_poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        col.text(movie_name)
        col.image(movie_poster, use_column_width=True)




