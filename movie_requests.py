import requests
from keys import api_key
import csv


res = requests.get(f"http://www.omdbapi.com/?apikey={api_key}")


def res_omdb_data():
    all_movies = []
    with open('data/oscar_winners.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            ombd_res = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&i={row[1]}").json()
            all_movies.append(ombd_res)
        return all_movies


def save_to_csv(data):
    header = ['Movie Title', 'Runtime', 'Genre', 'Award Wins', 'Award Nominations', 'Box Office']
    with open('data/movies.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for movie in data:
            title = movie['Title']
            runtime = int(movie['Runtime'].replace(' min', ''))
            genre = movie['Genre']
            awards_data = [int(word) for word in movie['Awards'].split() if word.isdigit()]
            award_wins = int(awards_data[1])
            award_nominations = int(awards_data[2])
            box_office = int(movie['BoxOffice'].replace('$', '').replace(',', ''))
            info = [title, runtime, genre, award_wins, award_nominations, box_office]
            writer.writerow(info)


movies = res_omdb_data()
save_to_csv(movies)
