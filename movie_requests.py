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


movies = res_omdb_data()
print(movies)