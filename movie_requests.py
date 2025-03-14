import requests
from keys import api_key
import csv


res = requests.get(f"http://www.omdbapi.com/?apikey={api_key}")


def res_omdb_data(user_csv):
    all_movies = []
    with open(f'data/{user_csv}', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            try:
                ombd_res = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&i={row[1]}")
                ombd_res.raise_for_status()
                all_movies.append(ombd_res.json())
            except requests.exceptions.RequestException as err:
                print(f"Error for movie ID {row[1]}: {err}")
    return all_movies


def save_to_csv(user_csv, user_movies):
    header = ['Movie Title', 'Runtime', 'Genre', 'Award Wins', 'Award Nominations', 'Box Office']
    with open(f'data/{user_csv}', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for movie in user_movies:
            try:
                title = movie['Title']
                runtime = int(movie['Runtime'].replace(' min', ''))
                genre = movie['Genre']
                awards_data = [int(word) for word in movie['Awards'].split() if word.isdigit()]
                award_wins = int(awards_data[1])
                award_nominations = int(awards_data[2])
                box_office = int(movie['BoxOffice'].replace('$', '').replace(',', ''))
                info = [title, runtime, genre, award_wins, award_nominations, box_office]
                writer.writerow(info)
            except (KeyError, ValueError, IndexError) as err:
                print(f"There was an error saving the movie '{movie['Title']}': {err}")



