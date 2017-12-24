import logging
import json

from flask import Flask, render_template
from flask_ask import Ask, statement, question
from six.moves.urllib.request import urlopen

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger('flask_ask').setLevel(logging.DEBUG)
OMDB_API_URL = 'http://www.omdbapi.com/?apikey=<YOUR_API_KEY_HERE>&i='

# IMDb IDs for the film series
FRIDAY_FILMS = {}
FRIDAY_FILMS['Part1'] = 'tt0080761'
FRIDAY_FILMS['Part2'] = 'tt0082418'
FRIDAY_FILMS['Part3'] = 'tt0083972'
FRIDAY_FILMS['Part4'] = 'tt0087298'
FRIDAY_FILMS['Part5'] = 'tt0089173'
FRIDAY_FILMS['Part6'] = 'tt0091080'
FRIDAY_FILMS['Part7'] = 'tt0095179'
FRIDAY_FILMS['Part8'] = 'tt0097388'

@ask.launch
def launch():
	welcome_text = render_template('welcome')
	reprompt_text = render_template('reprompt')
	return question(welcome_text).reprompt(reprompt_text)

@ask.intent('GetMovieMetadataIntent', convert={'sequel':int})
def get_movie_metadata(sequel):
	movie_url = OMDB_API_URL + FRIDAY_FILMS['Part'+str(sequel)]
	omdb_api = urlopen(movie_url).read().decode('utf-8')
	metadata = json.loads(omdb_api)
	title = metadata['Title']
	year = metadata['Year']
	plot = metadata['Plot']
	poster = metadata['Poster']
	rating = metadata['imdbRating']
	movie_info_text = render_template('movie_info', title=title, plot=plot, year=year, imdb_rating=rating)
	card_text = '{}\nIMDb rating: {}'.format(plot, rating)
	return statement(movie_info_text).standard_card(title=title, text=card_text, small_image_url=poster)

@ask.session_ended
def session_ended():
	return '{}', 200


if __name__ == '__main__':
	app.run(debug=True)