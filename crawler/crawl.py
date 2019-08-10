import asyncio
import aiohttp
import re

from typing import Set, Union
from itertools import chain


class Crawler:
    
    def __init__(self, loop=None, timeout=5, max_tasks=20):
        loop = loop or asyncio.get_event_loop()
        self._loop = loop
        self._urls = []

        self._timeout = aiohttp.ClientTimeout(total=timeout)

        # semaphore to limit max number of async tasks
        self._sem = asyncio.Semaphore(max_tasks)

    def add_url(self, url: str) -> None:
        self._urls.append(url)

    async def crawl(self) -> Union[Set[str], None]:
        tasks = []

        async with aiohttp.ClientSession() as session:
            for url in self._urls:
                tasks.append(self._loop.create_task(self._fetch(session, url)))
            return set(chain(*await asyncio.gather(*tasks)))

    async def _fetch(self, session, url: str) -> Set[str]:

        parsed = set()

        try:

            print(f'fetching and parsing: {url}')

            async with self._sem:
                async with session.get(url, timeout=self._timeout) as response:
                    resp = await response.text()
                    parsed = Crawler._parse(resp)

        except Exception as e:
            print(f'error fetching {url}: {e}')

        return parsed

    @staticmethod
    def _parse(resp: str) -> Set[str]:

        res = set()

        for phone in re.findall(r'\b[\+7|7|8]?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}\b|'
                                r'\b[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}\b',
                                resp):

            # remove spaces, dashes and parenths
            phone = re.sub(r'[\s\-\(\)]', '', phone)

            # normalize to 8KKKNNNNNNN
            if len(phone) == 7:  # XXXYYZZ
                phone = '8495' + phone

            elif len(phone) == 11:           # [8|7]916XXXYYZZ
                if phone.startswith('7'):    # 7916XXXYYZZ
                    phone = '8' + phone[1:]

            elif len(phone) == 10:  # 498XXXYYZZ
                phone = '8' + phone

            else:
                # invalid phone number
                continue

            res.add(phone)

        return res
