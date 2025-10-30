import pandas as pd
import numpy as np
import ast
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
class MovieRec:
    def __init__(self):
        self.movies=None
        self.credits=None
        self.data=None
        self.similarity_matrix=None
        self.indices=None
    def load(self):
        import os
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            movies_path = os.path.join(current_dir, 'tmdb_5000_movies.csv')
            credits_path = os.path.join(current_dir, 'tmdb_5000_credits.csv')
            
            print(f"Looking for movies file at: {movies_path}")
            print(f"Looking for credits file at: {credits_path}")
            
            self.movies=pd.read_csv(movies_path)
            self.credits=pd.read_csv(credits_path)
            print("CSV files loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading CSV files: {e}")
            return False
        
    def clean(self):
        self.data=self.movies.merge(self.credits, left_on='id', right_on='movie_id')
        self.data['overview'].fillna('', inplace=True)
        self.data['genres'].fillna('[]', inplace=True)
        self.data['keywords'].fillna('[]', inplace=True)
        self.data['cast'].fillna('[]', inplace=True)
        self.data['crew'].fillna('[]', inplace=True)
        
    def parse(self, json_str):
        try:
            parsed=ast.literal_eval(json_str)
            names=[]
            for item in parsed:
                if 'name' in item:
                    names.append(item['name'])
            return names
        except:
            return []
    def director(self, crew):
        try:
            crew_list=ast.literal_eval(crew)
            for person in crew_list:
                if person['job']=='Director':
                    return person['name']
        except:
            pass
        return ''
    def features(self):
        self.data['genres_list']=self.data['genres'].apply(self.parse)
        self.data['keywords_list']=self.data['keywords'].apply(self.parse)
        self.data['cast']=self.data['cast'].apply(lambda x: self.parse(x)[:3])
        self.data['director']=self.data['crew'].apply(self.director)
        self.data['combined']=''
        for index, row in self.data.iterrows():
            genres_str=' '.join(row['genres_list']).lower()
            keywords_str=' '.join(row['keywords_list']).lower()
            cast_str=' '.join(row['cast']).lower()
            director_str=row['director'].lower()
            overview_str=row['overview'].lower()
            features=genres_str+' '+keywords_str+' '+cast_str+' '+director_str+' '+overview_str
            self.data.at[index, 'combined']=features
        self.indices=pd.Series(self.data.index, index=self.data['title_x'])

    def simularities(self):
        vectorizer=TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix=vectorizer.fit_transform(self.data['combined'])
        self.similarity_matrix=cosine_similarity(tfidf_matrix, tfidf_matrix)

    def recommend(self, title, count=5):
        if title not in self.indices:
            return []
        movie_index=self.indices[title]
        scores=list(enumerate(self.similarity_matrix[movie_index]))
        scores=sorted(scores, key=lambda x: x[1], reverse=True)
        movie_indices=[score[0] for score in scores[1:count+1]]
        recommendations=[]
        for position, movie_idx in enumerate(movie_indices):
            movie=self.data.iloc[movie_idx]
            similarity=scores[position+1][1]*100
            try:
                genre_data=ast.literal_eval(movie['genres'])
                genre_str=', '.join([genre['name'] for genre in genre_data])
            except:
                genre_str='Unknown'
            try:
                year=movie['release_date'][:4]
            except:
                year='N/A'
            recommendation={
                'title': movie['title_x'],
                'year': year,
                'genres': genre_str,
                'rating': movie['vote_average'],
                'similarity': round(similarity, 2),
                'overview': movie['overview'][:150]+'...' if len(movie['overview'])>150 else movie['overview']
            }
            recommendations.append(recommendation)
        return recommendations
    def setup(self):
        if not self.load():
            return False
        self.clean()
        self.features()
        self.simularities()
        return True
    def search(self, query):
        if self.data is None:
            return []
        matches=self.data[self.data['title_x'].str.contains(query, case=False, na=False)]
        return matches['title_x'].tolist()[:10]
def test():
    recommender=MovieRec()
    if not recommender.setup():
        print("Failed")
        return
    movies=['The Dark Knight', 'Avatar', 'Spider-Man', 'Inception']
    for movie in movies:
        print(f"For: {movie}")
        recommendations=recommender.recommend(movie)
        if recommendations:
            for index, recommendation in enumerate(recommendations, 1):
                print(f"{index}. {recommendation['title']} ({recommendation['year']}) - {recommendation['similarity']}%")
        else:
            print("None found")
if __name__=="__main__":
    test()