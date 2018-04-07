from flask import Flask, request, abort, Response
from flask_restful import Resource, Api
from skyscraper.auth_service import AuthService, authenticated_users

from skyscraper.comparator_service import CarComparator
from skyscraper.scraper_service import ScraperService, ScraperServiceFactory

app = Flask(__name__)
api = Api(app)

URl_PATTERN = '^http[s]?:\/\/www.hasznaltauto.hu\/auto\/([a-zA-Z]|\d|\/|_|-|\.)+$'
URL_KEY = 'carUrls'
HTML_KEY = 'htmls'
USER_ID_TOKEN_KEY = 'idToken'


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
			authorized = AuthService.validate_token(id_token)
			if not authorized[0]:
				abort(Response('Authorization failed', status=401))

			return [
					   {
						   "CarUri": "https://www.hasznaltauto.hu/auto/bmw/x4/bmw_x4_3.5_d_automata_m-packet.x-line.313le-11200623",
						   "prod_date": "2014/8",
						   "power": "230 kW, 313 LE",
						   "price": "13.300.000 Ft",
						   "speedometer": "73 000 km",
						   "worth": 25.18
					   },
					   {
						   "CarUri": "https://www.hasznaltauto.hu/szemelyauto/audi/a6/audi_a6_2_0_tdi_ultra_75_000_km_sz_konyv_s_mentes-12769076",
						   "power": "140 kW",
						   "price": "7 199 000 Ft",
						   "prod_date": "2014/12",
						   "speedometer": "75 000 km",
						   "worth": 22
					   }
				   ], 200, {'Access-Control-Allow-Origin': '*'}
		else:
			abort(Response('Body is not json', status=400, headers={'Access-Control-Allow-Origin': '*'}))

	def options(self):
		return {'Allow': 'POST'}, 200, \
				{'Access-Control-Allow-Origin': '*',
					'Access-Control-Allow-Methods': 'POST,GET',
					'Access-Control-Allow-Headers': 'Content-Type'}


api.add_resource(ScrapeByUrls, '/')
api.add_resource(LoadSavedCars, '/saved-cars')

if __name__ == '__main__':
	#context = ('certificate.crt', 'privatekey.key')  # certificate and key files
	app.run()
