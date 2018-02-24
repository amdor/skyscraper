from flask import Flask, request, abort, Response
from flask_restful import Resource, Api
import re

from skyscraper.comparator_service import CarComparator
from skyscraper.scraper_service import ScraperService, ScraperServiceFactory

app = Flask(__name__)
api = Api(app)

URl_PATTERN = '^http[s]?:\/\/www.hasznaltauto.hu\/auto\/([a-zA-Z]|\d|\/|_|-|\.)+$'
URL_KEY = 'carUrls'
HTML_KEY = 'htmls'


class ScrapeByUrls(Resource):
	def post(self):
		valid_urls = []
		if request.is_json:
			request_data = request.get_json()
			if URL_KEY not in request_data:
				abort(Response('Provide car URL', status=400))
			for url in request_data[URL_KEY]:
				if re.match(URl_PATTERN, url):
					valid_urls.append(url)
			html_contents = request_data.get(HTML_KEY, {})
			if html_contents:
				scraper = ScraperServiceFactory.get_for_dict(html_contents)
			else:
				scraper = ScraperService(valid_urls)
			data = scraper.get_car_data()
			CarComparator.compare_cars(data)
			return data, 200, {'Access-Control-Allow-Origin': '*'}
		else:
			abort(Response('Body is not json', status=400))

	def options(self):
		return {'Allow': 'POST'}, 200, \
				{'Access-Control-Allow-Origin': '*',
					'Access-Control-Allow-Methods': 'POST,GET',
					'Access-Control-Allow-Headers': 'Content-Type'}


api.add_resource(ScrapeByUrls, '/')

if __name__ == '__main__':
	context = ('certificate.crt', 'privatekey.key')  # certificate and key files
	app.run(ssl_context=context)
