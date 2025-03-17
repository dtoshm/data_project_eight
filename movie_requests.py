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
    """Saves movie data to a CSV file with specified fields.
    
    Args:
        user_csv (str): Name of the output CSV file
        user_movies (list): List of movie data dictionaries
    
    Returns:
        None
    """
    header = ['Movie Title', 'Runtime', 'Genre', 'Award Wins', 'Award Nominations', 
              'Box Office', 'Director', 'Language', 'Plot']
    
    with open(f'data/{user_csv}', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for movie in user_movies:
            try:
                row = [
                    movie['Title'],
                    int(movie['Runtime'].replace(' min', '')),
                    movie['Genre'],
                    sum(int(num) for num in re.findall(r'(\d+)\s*win', movie['Awards'])),
                    sum(int(num) for num in re.findall(r'(\d+)\s*nomination', movie['Awards'])),
                    int(movie['BoxOffice'].replace('$', '').replace(',', '')),
                    movie['Director'],
                    movie['Language'],
                    movie['Plot']
                ]
                writer.writerow(row)
            except (KeyError, ValueError) as err:
                print(f"Error saving '{movie['Title']}': {err}")
