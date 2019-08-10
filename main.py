import asyncio
from crawler import Crawler


async def main():
    crawler = Crawler(asyncio.get_event_loop())

    crawler.add_url('http://hands.ru/company/about')
    crawler.add_url('https://repetitors.info')

    print(await crawler.crawl())


if __name__ == '__main__':
    asyncio.run(main())
