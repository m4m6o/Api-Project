from flask import Flask, request
import logging
import json
from geo import get_country, get_distance, get_coordinates
 
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
  
@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)
 
 
def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = \
            'Ïðèâåò! ß ìîãó ïîêàçàòü ãîðîä èëè ñêàçàòü ðàññòîÿíèå ìåæäó ãîðîäàìè!'
        return
    cities = get_cities(req)
    if not cities:
        res['response']['text'] = 'Òû íå íàïèñàë íàçâàíèå íå îäíîãî ãîðîäà!'
    elif len(cities) == 1:
        res['response']['text'] = 'Ýòîò ãîðîä â ñòðàíå - ' + \
            get_country(cities[0])
    elif len(cities) == 2:
        distance = get_distance(get_coordinates(
            cities[0]), get_coordinates(cities[1]))
        res['response']['text'] = 'Ðàññòîÿíèå ìåæäó ýòèìè ãîðîäàìè: ' + \
            str(round(distance)) + ' êì.'
    else:
        res['response']['text'] = 'Ñëèøêîì ìíîãî ãîðîäîâ!'
 
 
def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])
    return cities
 
 
if __name__ == '__main__':
    app.run()
