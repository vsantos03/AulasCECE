import pandas as pd

# Load the datasets
world_population_data = pd.read_csv('../../../Downloads/world-population-2022.csv')
imdb_movie_data = pd.read_csv('../../../Downloads/IMDB-Movie-Data.csv')

# Exercise 2 - Explore data using pandas

# Analyse the dataset and select a subset of the data
# 1. How many lines and columns?
lines, columns = world_population_data.shape
print(f"World Population Data: {lines} lines, {columns} columns")

lines, columns = imdb_movie_data.shape
print(f"IMDB Movie Data: {lines} lines, {columns} columns")

# 2. List all the columns
print("World Population Data Columns:", world_population_data.columns.tolist())
print("IMDB Movie Data Columns:", imdb_movie_data.columns.tolist())

# 3. Create a subset of the data, containing the columns `pop2022`, `area`, `Density`, `GrowthRate`
wp1 = world_population_data[['name', 'pop2022', 'area', 'GrowthRate', 'rank']].copy()

# Explore the data
# 1. Show the data for the first 5 countries
print("First 5 countries in World Population Data:")
print(wp1.head())

# 2. Show the data for the last 10 countries
print("Last 10 countries in World Population Data:")
print(wp1.tail(10))

# 3. Show the data from countries ranked between 90 and 100
print("Countries ranked between 90 and 100 in World Population Data:")
print(wp1[(wp1['rank'] >= 90) & (wp1['rank'] <= 100)])

# 4. Check if `Portugal` is in the list
is_portugal_in_list = 'Portugal' in wp1['name'].values
print(f"Is Portugal in the list? {'Yes' if is_portugal_in_list else 'No'}")

# 5. Show the statistics for `Portugal`
if is_portugal_in_list:
    print("Statistics for Portugal:")
    print(wp1[wp1['name'] == 'Portugal'])

# Operate on data
# 2. Add a new country named `Tamriel` with a population of 3500000 and an area of 10000000 square meters
tamriel = pd.DataFrame([['Tamriel', 3500000, 10000000, None, None]], columns=['name', 'pop2022', 'area', 'GrowthRate', 'rank'])
wp1 = pd.concat([wp1, tamriel], ignore_index=True)

# 3. Change the area of `Tamriel` to 9000000
wp1.loc[wp1['name'] == 'Tamriel', 'area'] = 9000000

# 4. Create a new column `density`, based on the `area` and `pop2022`, which corresponds to the number of people per square meters.
wp1['density'] = wp1['pop2022'] / wp1['area']

# Note that the population count is in thousands.
wp1['density'] = wp1['density'] * 1000

# 5. Check that this column has similar values to the column `Density` in the original data
similar_density_check = wp1[['name', 'density']].merge(world_population_data[['name', 'Density']], on='name')
similar_density_check['similar_density'] = similar_density_check.apply(lambda row: abs(row['density'] - row['Density']) < 0.01, axis=1)
print("Density similarity check:")
print(similar_density_check)

# 6. Create a new dataframe `wp2`, where the country name is the dataframe index
wp2 = wp1.set_index('name')

# Perform calculations
# 1. Calculate the `mean` of the area of the 10 most populated countries
mean_area_top_10_populated_countries = wp2.nlargest(10, 'pop2022')['area'].mean()
print(f"Mean area of the top 10 most populated countries: {mean_area_top_10_populated_countries}")

# 2. How many countries have a GrowthRate above 1.03?
countries_with_high_growth_rate = wp2[wp2['GrowthRate'] > 1.03].shape[0]
print(f"Number of countries with GrowthRate above 1.03: {countries_with_high_growth_rate}")

# 3. How many countries have an area above 1 million square meters?
countries_with_large_area = wp2[wp2['area'] > 1000000].shape[0]
print(f"Number of countries with area above 1 million square meters: {countries_with_large_area}")

# Exercise 3 - Aggregate and group data using IMDB dataset

# Group the movies by 'Genre' and calculate the average IMDb rating for each genre
average_rating_by_genre = imdb_movie_data.groupby('Genre')['Rating'].mean()
print("Average IMDb rating by genre:")
print(average_rating_by_genre)

# Group the movies by 'Year' and count how many movies were released in each year.
movies_count_by_year = imdb_movie_data.groupby('Year')['Title'].count()
print("Number of movies released each year:")
print(movies_count_by_year)

# Create a pivot table showing the average rating of movies for each genre per year.
pivot_table_genre_year_rating = imdb_movie_data.pivot_table(values='Rating', index='Year', columns='Genre', aggfunc='mean')
print("Pivot table showing average rating of movies for each genre per year:")
print(pivot_table_genre_year_rating)

# Use vectorized string operations to extract the first letter of each director's name
imdb_movie_data['Director_First_Letter'] = imdb_movie_data['Director'].str[0]
print("First letter of each director's name:")
print(imdb_movie_data[['Director', 'Director_First_Letter']])

# Find all movies whose title starts with the word 'The'
movies_starting_with_the = imdb_movie_data[imdb_movie_data['Title'].str.startswith('The')]
print("Movies whose title starts with 'The':")
print(movies_starting_with_the[['Title', 'Year', 'Genre', 'Rating']])

# Convert all movie titles to uppercase
imdb_movie_data['Title_Uppercase'] = imdb_movie_data['Title'].str.upper()
print("Movie titles converted to uppercase:")
print(imdb_movie_data[['Title', 'Title_Uppercase']])