import logging
import os

from contextlib import suppress
from datetime import datetime
from typing import TypedDict, cast

import httpx


class UserData(TypedDict):
    id: int                             # User ID
    name: str                           # Name
    name_trans: str | None              # Transliterated name for search
    info: str | None                    # Self description
    info_parsed: list[dict] | None      # Parsed description (with post parser)
    unique_name: str                    # Unique name (@uname)
    deleted: bool                       # Flag for deleted accounts
    active: bool                        # Flag for actiovation state
    time_updated: datetime              # Last data updation
    time_created: datetime              # Registarion datetime
    is_bot: bool                        # Flag for bots
    owner_id: int | None                # If bot, his owner id (user id)
    organizations: list[int] | None     # User member of this teams
    timezone_offset_minutes: int | None  # Timezone, offset in minutes


class TeamData(TypedDict):
    id: int
    slug: str | None
    title: str
    description: str | None
    email_domain: str | None
    time_created: datetime
    time_updated: datetime
    two_step_required: bool
    is_member: bool
    is_admin: bool
    state: str
    inviter_id: int
    guests: list[int]
    users: list[int]
    admins: list[int]
    groups: list[int]
    description_parsed: str | None
    default_chat_id: int | None


class ClientError(Exception):
    pass


class UnauthorizedError(ClientError):
    pass


class NoAccessError(ClientError):
    pass


class InputDataError(ClientError):
    pass


class MethodError(ClientError):
    pass


class TooManyRequestsError(ClientError):
    pass


class ServerError(ClientError):
    pass


class RedirectError(ClientError):
    pass


class Client:
    __secret__: str = ''
    host: str = ''
    log = logging.getLogger('client')

    def __init__(self, secret: str = '', host: str = '') -> None:
        secret = secret or os.environ.get('SECRET', '')[20:]
        assert secret, 'Set SECRET env'
        self.__secret__ = secret

        host = host or os.environ.get('API_HOST', 'api.pararam.io')
        self.host = f'https://{host}'

    def __repr__(self) -> str:
        return f'Client [{self.host}]' + (' with ' if self.__secret__ else ' no ') + 'secret'

    async def api_call(self, uri: str, method: str = 'GET', data: dict | None = None) -> dict:
        async with httpx.AsyncClient(headers={'X-APIToken': self.__secret__}) as client:
            result = {}
            resp = await client.request(method, f'{self.host}{uri}', json=data or {})
            self.log.info('API %s %s: %s', method, uri, resp.status_code)

            with suppress(Exception):
                result = resp.json()

            match resp.status_code:
                case 400:
                    raise InputDataError(f'{method} {uri} \n<- {data} \n-> {result}')
                case 401:
                    raise UnauthorizedError(f'{method} {uri} \n-> {result}')
                case 403:
                    raise NoAccessError(f'{method} {uri} \n<- {data} \n-> {result}')
                case 429:
                    raise TooManyRequestsError(f'{method} {uri}\n-> {result}')
                case 301 | 302:
                    raise RedirectError(f'{method} {uri}')
                case 500 | 502 | 503 | 504:
                    raise ServerError(f'{method} {uri} > HTTP{resp.status_code}')

            return result

    async def send_post(self, chat_id: int, text: str) -> None:
        data = {'chat_id': chat_id, 'text': text}
        await self.api_call('/bot/message', 'POST', data)

    async def send_private_post(self, user_id: int, text: str) -> None:
        data = {'user_id': user_id, 'text': text}
        await self.api_call('/msg/post/private', 'POST', data)

    async def get_user_data(self, ids: list[int]) -> list[UserData]:
        data = await self.api_call(f'/user/list?ids={",".join(map(str, ids))}', 'GET')
        return cast(list[UserData], data['users'])

    async def get_team_data(self, ids: list[int]) -> list[TeamData]:
        data = await self.api_call(f'/core/org?ids={",".join(map(str, ids))}', 'GET')
        return cast(list[TeamData], data['orgs'])

    async def get_chat_data(self, ids: list[int]) -> list[dict]:
        data = await self.api_call(f'/core/chat?ids={",".join(map(str, ids))}', 'GET')
        return cast(list[dict], data['chats'])
