from flask import Flask, request, abort, Response
from flask_restful import Resource, Api

from skyscraper.auth_service import AuthService

from skyscraper.comparator_service import CarComparator
from skyscraper.database_service import DatabaseService
from skyscraper.scraper_service import ScraperService, ScraperServiceFactory
from skyscraper.utils.constants import URL_KEY, HTML_KEY, USER_ID_TOKEN_KEY, CAR_DATA_KEY

app = Flask(__name__)
api = Api(app)


class ScrapeByUrls(Resource):
	def post(self):
		if request.is_json:
			request_data = request.get_json()

			# get the urls one way or another
			if URL_KEY not in request_data:
				if HTML_KEY not in request_data:
					abort(Response('Provide car URL or html dict with url keys', status=400))
				else:
					urls = [*request_data.get(HTML_KEY)]
			else:
				urls = request_data.get(URL_KEY)

			valid_urls = [url for url in urls if url]

			# validate html contents
			html_contents = request_data.get(HTML_KEY, {})
			if html_contents:
				valid_html_contents = {url: html_contents[url] for url in valid_urls if url in html_contents}
			else:
				valid_html_contents = {}

			# scraping
			if valid_html_contents:
				scraper = ScraperServiceFactory.get_for_list_and_dict(valid_urls, valid_html_contents)
			else:
				scraper = ScraperService(valid_urls)
			data = scraper.get_car_data()
			CarComparator.compare_cars(data)
			return data, 200, {'Access-Control-Allow-Origin': '*'}
		else:
			abort(Response('Body is not json', status=400, headers={'Access-Control-Allow-Origin': '*'}))

	def options(self):
		return {'Allow': 'POST'}, 200, \
			   {'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods': 'POST,GET',
				'Access-Control-Allow-Headers': 'Content-Type'}


class LoadSavedCars(Resource):
	def post(self):
		if request.is_json:
			request_data = request.get_json()

			id_token = request_data.get(USER_ID_TOKEN_KEY, '')
			(authorized, auth_id) = AuthService.validate_token(id_token)
			if not authorized:
				abort(Response('Authorization failed', status=401))

			car_data = DatabaseService.get_car_data(auth_id)
			return car_data[auth_id], 200, {'Access-Control-Allow-Origin': '*'}

	def put(self):
		if request.is_json:
			request_data = request.get_json()

			id_token = request_data.get(USER_ID_TOKEN_KEY, '')
			car_data = request_data.get(CAR_DATA_KEY, [])
			(authorized, auth_id) = AuthService.validate_token(id_token)
			if not authorized or not car_data:
				abort(Response('Authorization failed', status=401))

			DatabaseService.save_car_data(auth_id, car_data)
			return 'Success', 200, {'Access-Control-Allow-Origin': '*'}
		else:
			abort(Response('Body is not json', status=400, headers={'Access-Control-Allow-Origin': '*'}))

	def options(self):
		return {'Allow': 'POST'}, 200, \
			   {'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods': 'POST,PUT',
				'Access-Control-Allow-Headers': 'Content-Type'}


api.add_resource(ScrapeByUrls, '/')
api.add_resource(LoadSavedCars, '/saved-cars')

if __name__ == '__main__':
	# context = ('certificate.crt', 'privatekey.key')  # certificate and key files
	app.run()
