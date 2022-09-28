import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '518c3b8cc5a9ba53eda3c96664c8cfa2'
tmdb.language = 'ko-KR'

def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]  # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기  
    sim_scores = list(enumerate(cosine_sim[idx]))  # 코사인 유사도 매트릭스 (cosine_sim)에서 idx에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sim_scores[1:11]  # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
    movie_indices = [i[0] for i in sim_scores]  # 추천 영화 목록 10개의 인덱스 정보 추출
    # 인덱스 정보를 통해 영화 제목 추출
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details =  movie.details(id)

        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'

        images.append(image_path)
        titles.append(details['title'])

    return images, titles

movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide')  # 화면을 넓게 생성
st.header('Subeenflix')  # 제목 생성

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)
if st.button('Recommend'):  # 버튼 생성
    with st.spinner('Please wait...'):  # 로딩 표시
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):  # 0, 1 두번 동작
            cols = st.columns(5)  # 5개의 컬럼 생성
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1
