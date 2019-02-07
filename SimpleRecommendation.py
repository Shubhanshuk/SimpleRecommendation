# Import pandas
import pandas as pd

#Copy the data in a dataframe
file = pd.read_csv("movies_metadata.csv", low_memory=False, encoding="latin1")

print(file.head(5))

#calculate the mean
votemean = file['vote_average'].mean()
print(votemean)

# Calculate the minimum number of votes required to be in the chart, m
m = file['vote_count'].quantile(0.90)
print(m)

# Filter out all qualified movies into a new DataFrame
q_movies = file.copy().loc[file['vote_count'] >= m]
q_movies.shape

# Function that computes the weighted rating of each movie
def weighted_rating(x, m=m, C=votemean):
    v = x['vote_count']
    R = x['vote_average']

# Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)

# Define a new feature 'score' and calculate its value with `weighted_rating()`
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)


#Sort movies based on score calculated above
q_movies = q_movies.sort_values('score', ascending=False)

#Print the top 15 movies
print(q_movies[['title', 'vote_count', 'vote_average', 'score']].head(15))