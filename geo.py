import requests
import math
 
def get_coordinates(city_name):
    try:
        # url, ïî êîòîðîìó äîñòóïíî API ßíäåêñ.Êàðò
        url = "https://geocode-maps.yandex.ru/1.x/"
        # ïàðàìåòðû çàïðîñà
        params = {
            # ãîðîä, êîîðäèíàòû êîòîðîãî ìû èùåì
            'geocode': city_name,
            # ôîðìàò îòâåòà îò ñåðâåðà, â äàííîì ñëó÷àå JSON
            'format': 'json'
        }
        # îòïðàâëÿåì çàïðîñ
        response = requests.get(url, params)
        # ïîëó÷àåì JSON îòâåòà
        json = response.json()
        # ïîëó÷àåì êîîðäèíàòû ãîðîäà (òàì íàïèñàíû äîëãîòà(longitude),
        # øèðîòà(latitude) ÷åðåç ïðîáåë).
        # Ïîñìîòðåòü ïîäðîáíîå îïèñàíèå JSON-îòâåòà ìîæíî
        # â äîêóìåíòàöèè ïî àäðåñó
        # https://tech.yandex.ru/maps/geocoder/
        coordinates_str = json['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        # Ïðåâðàùàåì string â ñïèñîê, òàê êàê òî÷êà - 
        # ýòî ïàðà äâóõ ÷èñåë - êîîðäèíàò
        long, lat = map(float, coordinates_str.split())
        # Âåðíåì îòâåò
        return long, lat
    except Exception as e:
        return e
    
    
def get_country(city_name):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            'geocode': city_name,
            'format': 'json'
        }
        data = requests.get(url, params).json()
        # âñå îòëè÷èå òóò, ìû ïîëó÷àåì èìÿ ñòðàíû
        return data['response']['GeoObjectCollection']['featureMember'][0][
            'GeoObject']['metaDataProperty']['GeocoderMetaData'][
            'AddressDetails']['Country']['CountryName']
    except Exception as e:
        return e   
     
def get_info(city_name, type_info):
    if type_info == city_name:
        try:
            url = "https://geocode-maps.yandex.ru/1.x/"
            params = {'geocode': city_name, 'format': 'json'}
            data = requests.get(url, params).json()
            return data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName']
        except Exception as e:
            return e  
        else:
            try:
                url = "https://geocode-maps.yandex.ru/1.x/"
                params = {'geocode': city_name, 'format': 'json'}
                response = requests.get(url, params)
                json = response.json()
                coordinates_str = json['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']['Point']['pos']
                long, lat = map(float, coordinates_str.split())
                return long, lat
            except Exception as e:
                return e
             
def get_distance(p1, p2):
    # p1 è p2 - ýòî êîðòåæè èç äâóõ ýëåìåíòîâ - êîîðäèíàòû òî÷åê
    radius = 6373.0
 
    lon1 = math.radians(p1[0])
    lat1 = math.radians(p1[1])
    lon2 = math.radians(p2[0])
    lat2 = math.radians(p2[1])
 
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
 
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)
 
    distance = radius * c
    return distance
