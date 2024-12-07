from __future__ import annotations

import base64
import typing
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image

if typing.TYPE_CHECKING:
    from ..client import Client

from ..core import ApiError

class ProfileClient:
    def __init__(self, client_wrapper: Client):
        self._client_wrapper = client_wrapper


    def get(self):
        response = self._client_wrapper.request(
            'atleta/meus-dados',
            method = 'GET',
        )

        if 200 <= response.status_code < 300:
            soup = BeautifulSoup(response.text, features='html.parser')
            card = soup.find('div', {'class': 'card-body'})

            inputs = card.find_all('input')

            return {
                'profile_image': inputs[0].get('value'),
                'name': inputs[2].get('value'),
                'email': inputs[3].get('value'),
                'nif': inputs[4].get('value'),
                'priority': int(inputs[5].get('value').replace('Prioridade', '').strip()),
                'coach': inputs[6].get('value'),
            }
        else:
            raise ApiError(response.status_code, response.text)


    def update(
        self,
        name: str,
        email: str,
        nif: str
    ) -> None:
        response = self._client_wrapper.request(
            'atleta/updateMyData',
            method='POST',
            data = {
                # 'logoUpload': image,
                'name': name,
                'email': email,
                'nif': nif
            }
        )

        if 200 <= response.status_code < 300:
            return
        else:
            raise ApiError(response.status_code, response.text)
        

    def add_picture(
        self,
        image: str
    ):
        img = image_to_base64(create_square_image(image))

        response = self._client_wrapper.request(
            'addPhoto',
            method = 'POST',
            data = {
                'logo': img
            }
        )

        if 200 <= response.status_code < 300:
            return
        else:
            raise ApiError(response.status_code, response.text)


def create_square_image(image_path: str) -> Image:
    with Image.open(image_path) as img:
        width, height = img.size
        square_size = min(width, height)
        square_image = Image.new('RGB', (square_size, square_size))
        square_image.paste(img, ((square_size - width) // 2, (square_size - height) // 2))
        return square_image
    

def image_to_base64(img: Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    base64_string = base64.b64encode(buffer.read()).decode('utf-8')
    return base64_string