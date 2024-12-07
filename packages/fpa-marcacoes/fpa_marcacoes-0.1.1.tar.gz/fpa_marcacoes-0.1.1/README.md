# FPA Marcações Library

[![Upload Package](https://github.com/andrefpoliveira/fpa-marcacoes/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/andrefpoliveira/fpa-marcacoes/actions/workflows/release.yml)
![PyPI - Version](https://img.shields.io/pypi/v/fpa-marcacoes)

An API Wrapper for the FPA's website of trainings and massage scheduler

## Installation
```
pip install fpa-marcacoes
```

## Reference
A full reference for this library is available [here](./reference.md).

## Usage
Instantiate and use the client with the following:
```py
from fpa_marcacoes import Client

client = Client('your_email', 'your_password')
client.auth.login()

profile = client.profile.get()
```

## Exception Handling
When the API returns a non-success status code (4xx or 5xx respose), a subclass of the following error will be thrown.
```py
from fpa_marcacoes.core.api_error import ApiError

try:
    client.events.book_room(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```