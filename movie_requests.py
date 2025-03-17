from keys import api_key
import requests
import csv
import re


# API Key
res = requests.get(f"http://www.omdbapi.com/?apikey={api_key}")


def res_omdb_data(user_csv):
    """Fetches movie data from OMDB API using IMDb IDs from a CSV file.
    
    Args:
        user_csv (str): Name of the CSV file containing movie IDs
        
    Returns:
        list: List of movie data dictionaries from OMDB API
    """
    movies = []
    with open(f'data/{user_csv}', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            try:
                ombd_res = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&i={row[1]}").json()
                movies.append(ombd_res)
            except requests.exceptions.RequestException as err:
                print(f"Error for movie ID {row[1]}: {err}")
    return movies


def save_to_csv(user_csv, user_movies):
    header = ['Movie Title', 'Runtime', 'Genre', 'Award Wins', 'Award Nominations', 'Box Office', 'Director', 'Language', 'Plot']
    with open(f'data/{user_csv}', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for movie in user_movies:
            try:
                title = movie['Title']
                runtime = int(movie['Runtime'].replace(' min', ''))
                genre = movie['Genre']
                awards_str = movie['Awards']
                wins = sum(int(num) for num in re.findall(r'(\d+)\s*win', awards_str))
                nominations = sum(int(num) for num in re.findall(r'(\d+)\s*nomination', awards_str))
                box_office = int(movie['BoxOffice'].replace('$', '').replace(',', ''))
                director = movie['Director']
                language = movie['Language']
                plot = movie['Plot']
                info = [title, runtime, genre, wins, nominations, box_office, director, language, plot]
                writer.writerow(info)
            except (KeyError, ValueError, IndexError) as err:
                print(f"There was an error saving the movie '{movie['Title']}': {err}")

res_omdb_data('python_winners.csv')