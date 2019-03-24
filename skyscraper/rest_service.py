from flask import Flask, request, abort, Response
from flask_restful import Resource, Api

from skyscraper.comparator_service import CarComparator
from skyscraper.scraper_service import ScraperService, ScraperServiceFactory
from skyscraper.utils.constants import URL_KEY, HTML_KEY

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


api.add_resource(ScrapeByUrls, '/')

if __name__ == '__main__':
	# context = ('certificate.crt', 'privatekey.key')  # certificate and key files
	app.run()
