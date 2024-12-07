import typing
import urllib.parse
import requests
import urllib

from .environment import ClientEnvironment
from .auth.client import AuthClient
from .events.client import EventsClient
from .profile.client import ProfileClient

FileContent = typing.Union[typing.IO[bytes], bytes, str]
File = typing.Union[
    # file (or bytes)
    FileContent,
    # (filename, file (or bytes))
    typing.Tuple[typing.Optional[str], FileContent],
    # (filename, file (or bytes), content_type)
    typing.Tuple[typing.Optional[str], FileContent, typing.Optional[str]],
    # (filename, file (or bytes), content_type, headers)
    typing.Tuple[
        typing.Optional[str],
        FileContent,
        typing.Optional[str],
        typing.Mapping[str, str],
    ],
]

class Client:
    def __init__(
        self,
        email: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        base_url: typing.Optional[str] = None,
        environment: ClientEnvironment = ClientEnvironment.DEFAULT,
    ):
        self.base_url = _get_base_url(base_url, environment)
        self.email = email
        self.password = password
        self.cookies = None
        
        self.auth = AuthClient(self)
        self.events = EventsClient(self)
        self.profile = ProfileClient(self)


    def request(
        self,
        path: typing.Optional[str] = None,
        *,
        method: str,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        data: typing.Optional[typing.Any] = None,
        files: typing.Optional[typing.Dict[str, typing.Optional[typing.Union[File, typing.List[File]]]]] = None,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
        cookies: typing.Optional[typing.Dict[str, typing.Any]] = None
    ):
        if headers is None:
            headers = self._get_header()

        if cookies is None:
            cookies = self.cookies

        response = requests.request(
            method = method,
            url = urllib.parse.urljoin(self.base_url, path),
            params = params,
            data = data,
            cookies = cookies,
            files = files,
            headers = headers
        )

        return response


    def _get_header(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        
    

def _get_base_url(base_url: typing.Optional[str], environment: ClientEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception('Please provide a base_url or an environment to construct the client')