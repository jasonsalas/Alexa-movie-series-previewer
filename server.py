import logging
import json
import movie_series
from flask import Flask, render_template
from flask_ask import Ask, statement, question
from six.moves.urllib.request import urlopen

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger('flask_ask').setLevel(logging.DEBUG)
OMDB_API_URL = 'http://www.omdbapi.com/?apikey=<YOUR_API_KEY_HERE>&i='

@app.route('/')
def homepage():
	return render_template('greeting')

@ask.launch
def launch():
	welcome_text = render_template('welcome')
	reprompt_text = render_template('reprompt')
	return question(welcome_text).reprompt(reprompt_text)

@ask.intent('GetMovieMetadataIntent', convert={'sequel':int})
def get_movie_metadata(sequel):
	movie_url = OMDB_API_URL + movie_series.FILMS['Part'+str(sequel)]
	omdb_api = urlopen(movie_url).read().decode('utf-8')
	metadata = json.loads(omdb_api)
	title = metadata['Title']
	year = metadata['Year']
	plot = metadata['Plot']
	poster = metadata['Poster']
	rating = metadata['imdbRating']
	rotten_tomatoes_score = metadata['Ratings'][1]['Value']	
	movie_info_text = render_template('movie_info', title=title, plot=plot, year=year, imdb_rating=rating, rt_score=rotten_tomatoes_score)
	card_text = render_template('card_text', plot=plot, rating=rating, rt_score=rotten_tomatoes_score)
	return statement(movie_info_text).standard_card(title=title, text=card_text, small_image_url=poster)

@ask.intent('FilmsInSeriesIntent')
def films_in_series():
	movies = ', '.join(sorted(movie_series.TITLES.values()))
	available_movies = render_template('available_movies', movies=movies)
	return question(available_movies).reprompt(reprompt_text)

@ask.intent('AMAZON.HelpIntent')
def help():
	help_text = render_template('help')
	reprompt_text = render_template('reprompt')
	return question(help_text).reprompt(reprompt_text)

@ask.intent('AMAZON.StopIntent')
def stop():
	bye = render_template('goodbye')
	return statement(bye)

@ask.intent('AMAZON.CancelIntent')
def cancel():
	bye = render_template('goodbye')
	return statement(bye)

@ask.session_ended
def session_ended():
	return '{}', 200


if __name__ == '__main__':
	if 'ASK_VERIFY_REQUESTS' in os.environ:
		verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
		if verify == 'false':
			app.config['ASK_VERIFY_REQUESTS'] = False
	app.run(debug=True)