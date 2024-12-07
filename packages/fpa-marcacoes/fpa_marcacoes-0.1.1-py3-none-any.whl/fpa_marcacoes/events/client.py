from __future__ import annotations

import re
import typing
from datetime import datetime
from bs4 import BeautifulSoup

if typing.TYPE_CHECKING:
    from ..client import Client

from ..core import ApiError
from ..errors.payment_needed_error import PaymentNeededError

class EventsClient:
    def __init__(self, client_wrapper: Client):
        self._client_wrapper = client_wrapper

    def get_my_events(
        self,
        start_date: datetime,
        end_date: datetime,
        view: typing.Literal['semanal, diario'] = 'diario'
    ):
        response = self._client_wrapper.request(
            'eventos/loadUserEvent',
            method = 'POST',
            data = {
                'start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end': end_date.strftime('%Y-%m-%d %H:%M:%S'),
                'view': view
            }
        )

        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise ApiError(response.status_code, response.text)
        
    
    def duplicate(
        self,
        start_date: datetime,
        end_date: datetime,
        weeks_difference: int
    ):
        response = self._client_wrapper.request(
            'event/duplicateWeek',
            method = 'POST',
            data = {
                'start': start_date.strftime('%d-%m-%Y'),
                'end': end_date.strftime('%d-%m-%Y'),
                'current': start_date.isocalendar()[1],
                'plus': weeks_difference
            }
        )

        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise ApiError(response.status_code, response.text)
        

    def delete(
        self,
        event_id: int
    ) -> None:
        response = self._client_wrapper.request(
            f'event/removeData/{event_id}',
            method = 'GET'
        )

        if 200 <= response.status_code < 300:
            return
        else:
            raise ApiError(response.status_code, response.text)
        

    def delete_multiple(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        response = self._client_wrapper.request(
            'desmarcar-multiplos-eventos/removeData',
            method = 'POST',
            data = {
                'startDate': start_date.strftime('%d/%m/%Y'),
                'endDate': end_date.strftime('%d/%m/%Y')
            }
        )

        if 200 <= response.status_code < 300:
            return
        else:
            raise ApiError(response.status_code, response.text)
        

    def get_places(
        self
    ):
        response = self._client_wrapper.request(
            'criar-evento',
            method = 'GET'
        )

        if 200 <= response.status_code < 300:
            page = BeautifulSoup(response.text, features='html.parser')
            cards = page.find_all('div', {'class': 'p-2'})

            places = []

            for card in cards:
                link = card.find('a', {'class': 'btn'})
                name = link.text.replace('Selecionar', '').strip()
                places.append({
                    'id': int(re.findall(r'\d+', link.get('href'))[0]),
                    'name': name,
                    'slug': re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
                })
            
            return places
        else:
            raise ApiError(response.status_code, response.text)
        

    def get_areas(
        self,
        place_id: int,
    ):
        response = self._client_wrapper.request(
            f'criar-evento/{place_id}/_',
            method = 'GET'
        )

        if 200 <= response.status_code < 300:
            page = BeautifulSoup(response.text, features='html.parser')
            cards = page.find_all('div', {'class': 'card'})

            areas = []

            for card in cards:
                areas.append({
                    'id': int(re.findall(r'\d+', card.find('a').get('href'))[-1]),
                    'name': card.find('h5', {'class': 'text-primary'}).text,
                })
            
            return areas
        else:
            raise ApiError(response.status_code, response.text)
        

    def get_rooms(
        self,
        place_id: int,
        area_id: int,
    ):
        response = self._client_wrapper.request(
            f'criar-evento/{place_id}/_/{area_id}/_',
            method = 'GET'
        )

        if 200 <= response.status_code < 300:
            page = BeautifulSoup(response.text, features='html.parser')
            cards = page.find_all('div', {'class': 'card'})

            rooms = []

            for card in cards:
                rooms.append({
                    'id': int(re.findall(r'\d+', card.find('a').get('href'))[-1]),
                    'name': card.find('h5', {'class': 'text-primary'}).text,
                })
            
            return rooms
        else:
            raise ApiError(response.status_code, response.text)
        
    
    def get_room_events(
        self,
        start_date: datetime,
        end_date: datetime,
        room: int,
        view: typing.Literal['semanal', 'diario'] = 'semanal'
    ):
        response = self._client_wrapper.request(
            'eventos/loadEventFromCalendar',
            method = 'POST',
            data = {
                'calendar': room,
                'start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end': end_date.strftime('%Y-%m-%d %H:%M:%S'),
                'view': view
            }
        )

        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise ApiError(response.status_code, response.text)

    
    def book_room(
        self,
        room: int,
        date: datetime,
        athlete: int,
    ):
        response = self._client_wrapper.request(
            'evento/addData',
            method = 'POST',
            data = {
                'room': room,
                'start': date.strftime('%d-%m-%Y %H:%M'),
                'athlete': athlete
            }
        )

        if 200 <= response.status_code < 300:
            return
        elif response.status_code == 402:
            raise PaymentNeededError(response.text)
        else:
            raise ApiError(response.status_code, response.text)