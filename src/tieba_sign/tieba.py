import json
import re
from typing import Any
import asyncio

import httpx

from tieba_sign.config import Config

__all__ = ["Tieba", "Forum"]

_config = Config(
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Host": "tieba.baidu.com",
    }
)
_headers = _config.config["headers"] | {"Cookie": _config.config["cookie"]}
_client = httpx.AsyncClient(headers=_headers)


class Tieba:
    _TIEBA_URL = "https://tieba.baidu.com"
    _FORUM_LIST_PATTERN = re.compile(r"""['"]forums['"]\s*:\s*(\[[^\]]*\])""")
    _TBS_PATTERN = re.compile(r"""['"]tbs['"]\s*:\s*['"]([^'"]+)['"]""")

    def __init__(self):
        self._html = asyncio.create_task(self._get_home_page())

    @classmethod
    async def _get_home_page(cls):
        resp = await _client.get(cls._TIEBA_URL)
        resp.raise_for_status()

        return resp.text

    @classmethod
    def _get_forums(cls, html: str):
        forum_list_match = cls._FORUM_LIST_PATTERN.search(html)
        if not forum_list_match:
            raise NotImplementedError(
                "Failed to get forum list. Need to update the pattern"
            )

        forum_list = json.loads(forum_list_match.group(1))
        return list(map(lambda forum: Forum(forum), forum_list))

    async def get_forums(self):
        return self._get_forums(await self._html)


class Forum:
    _FORUM_URL = Tieba._TIEBA_URL + "/f"
    _SIGN_URL = Tieba._TIEBA_URL + "/sign/add"
    _TBS_PATTERN = re.compile(r"""['"]tbs['"]\s*:\s*['"]([^'"]+)['"]""")

    def __init__(self, forum_json: dict[str, Any]):
        self._forum_json = forum_json
        self._tbs = asyncio.create_task(self._get_tbs())

    @property
    def name(self) -> str:
        return self._forum_json["forum_name"]

    @property
    def is_sign(self) -> bool:
        return self._forum_json["is_sign"] != 0

    async def _get_tbs(self) -> str:
        resp = await _client.get(self._FORUM_URL, params={"kw": self.name})
        resp.raise_for_status()

        matches = self._TBS_PATTERN.search(resp.text)
        if not matches:
            raise NotImplementedError("Failed to get tbs. Need to update the pattern")

        return matches.group(1)

    async def sign(self):
        data = {"ie": "utf-8", "kw": self.name, "tbs": await self._tbs}
        resp = await _client.post(self._SIGN_URL, data=data)
        resp.raise_for_status()
