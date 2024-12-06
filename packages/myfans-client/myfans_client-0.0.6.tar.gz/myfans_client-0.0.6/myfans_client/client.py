from __future__ import annotations

import time
from typing import Generator

import httpx

from myfans_client.exceptions import MyFansException
from myfans_client.models.follow import FollowUser
from myfans_client.models.user import UserProfile

# https://api.myfans.jp/api/v2/users/f6257cde-61cc-428f-834b-c95d138d21fb/followers?page=1
# https://api.myfans.jp/api/v2/users/show_by_username?username=XXXX


class MyFansClient:
    def __init__(self, email: str, password: str, base_url: str = 'https://api.myfans.jp', debug: bool = False):
        self._email = email
        self._password = password
        self._base_url = base_url
        self._session = httpx.Client()
        self.debug = debug
        self._xsrf_token = None
        if self.debug:
            import logging
            logging.basicConfig(
                format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                level=logging.DEBUG
            )

        self.logged_in = self.login()

    @property
    def base_url(self):
        return self._base_url

    @property
    def header(self):
        base = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': 'https://myfans.jp',
            'Referer': 'https://myfans.jp/',
            'google-ga-data': 'event328',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        if self._xsrf_token:
            base['Authorization'] = f'Token token={self._xsrf_token}'

        return base

    def login(self) -> bool:
        try:
            res = self._post(
                'api/v1/sign_in',
                json={
                    'email': self._email,
                    'password': self._password,
                    'locale': 'ja',
                },
                headers=self.header,
            )
            self._xsrf_token = res['token']

            return True
        except MyFansException as e:
            raise e

    def get_follows(self, user_id: str, start_page: int = 1, max_page: int = 10) -> Generator[FollowUser, None, None]:
        """
        url:
        https://api.myfans.jp/api/v2/users/USER_ID/following?page=1
        response:
        {
            "data": [
                {
                    "about": null,
                    "avatar_url": "https://p1.cdn.myfans.jp/static/XXXX.png",
                    "banner_url": "https://p1.cdn.myfans.jp/static/XXXX.png",
                    "id": "XXXXXX",
                    "likes_count": 0,
                    "name": "hoge",
                    "username": "hoge",
                    "active": true,
                    "cant_receive_message": false,
                    "is_following": false
                },
                :
            ],
            "pagination": {
                "current": 2,
                "previous": 1,
                "next": 3 -- Optional[int]
            }
        }
        """
        page = start_page
        while True:
            try:
                res_json = self._get(
                    f'api/v2/users/{user_id}/following?page={page}',
                    headers=self.header
                )
            except MyFansException as e:
                raise MyFansException(
                    f'failed get follows of {user_id} page {page} [{e}]'
                )

            for f in res_json['data']:
                yield FollowUser(**f)

            pagination = res_json['pagination']
            if pagination['next'] is None or pagination['current'] == max_page:
                break
            page += 1
            time.sleep(0.5)

    def get_followed(self, user_id: str, start_page: int = 1, max_page: int = 10) -> Generator[FollowUser, None, None]:

        page = start_page
        while True:
            try:
                res_json = self._get(
                    f'api/v2/users/{user_id}/followers?page={page}',
                    headers=self.header
                )
            except MyFansException as e:
                raise MyFansException(
                    f'failed get follows of {user_id} page {page} [{e}]'
                )

            for f in res_json['data']:
                yield FollowUser(**f)

            pagination = res_json['pagination']
            if pagination['next'] is None or pagination['current'] == max_page:
                break
            page += 1
            time.sleep(0.5)

    def follow(self, user_id: str) -> bool:
        """
        POST https://api.myfans.jp/api/v1/users/USER_ID/follow
        true or false
        """

        is_followed = self._post(
            f'api/v1/users/{user_id}/follow',
            headers=self.header,
        )
        return is_followed

    def unfollow(self, user_id: str) -> bool:
        """
        POST https://api.myfans.jp/api/v1/users/USER_ID/unfollow
        true or false
        """

        is_followed = self._post(
            f'api/v1/users/{user_id}/unfollow',
            headers=self.header,
        )
        return is_followed

    def show_by_username(self, username: str) -> UserProfile:
        """
        GET https://api.myfans.jp/api/v2/users/show_by_username?username=USERNAME
        """
        res = self._get(
            f'api/v2/users/show_by_username?username={username}',
            headers=self.header,
        )
        return UserProfile(**res)

    def get_users(self, user_code: str) -> UserProfile:
        """
        GET https://api.myfans.jp/api/v1/users/USER_CODE
        """
        res = self._get(
            f'api/v1/users/{user_code}',
            headers=self.header,
        )
        return UserProfile(**res)

    def _post(self, path: str, *arg, **kwargs):
        return self._request('POST', path, *arg, **kwargs)

    def _get(self, path: str, *arg, **kwargs):
        return self._request('GET', path, *arg, **kwargs)

    def _put(self, path: str, *arg, **kwargs):
        return self._request('PUT', path, *arg, **kwargs)

    def _request(self, method: str, path: str, *arg, **kwargs):
        url = f'{self.base_url}/{path}'
        response = self._session.request(method, url, *arg, **kwargs)
        response_json = response.json()

        if isinstance(response_json, dict) and 'error' in response_json:
            raise MyFansException(response_json['error'])

        return response_json
