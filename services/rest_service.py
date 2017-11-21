from flask import Flask, request, abort, Response
from flask_restful import Resource, Api
import re

from services.comparator_service import CarComparator
from services.scraper_service import ScraperService

app = Flask(__name__)
api = Api(app)

URl_PATTERN = '^http[s]?:\/\/www.hasznaltauto.hu\/auto\/([a-zA-Z]|\d|\/|_|-|\.)+$'
URL_KEY = 'carUrls'


class ScraperApi(Resource):
	def post(self):
		valid_urls = []
		if request.is_json:
			request_data = request.get_json()
			if URL_KEY not in request_data:
				abort(Response('Provide car URLS', status=400))
				# abort(400, message="Provide car URLS")
			for url in request_data[URL_KEY]:
				if re.match(URl_PATTERN, url):
					valid_urls.append(url)
		scraper = ScraperService(valid_urls)
		data = scraper.get_car_data()
		CarComparator.compare_cars(data)
		return data, 200, {'Access-Control-Allow-Origin': '*'}

	def options(self):
		return {'Allow': 'POST'}, 200, \
				{'Access-Control-Allow-Origin': '*',
					'Access-Control-Allow-Methods': 'POST,GET',
					'Access-Control-Allow-Headers': 'Content-Type'}


api.add_resource(ScraperApi, '/')

if __name__ == '__main__':
	context = ('certificate.crt', 'privatekey.key')  # certificate and key files
	app.run(ssl_context=context)
