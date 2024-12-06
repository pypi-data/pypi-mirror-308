# test_rezka_scraper.py

import aiohttp
from bs4 import BeautifulSoup

class RezkaScraper:
    def __init__(self) -> None:
        self.base_url: str = "https://rezka.ag"
        self.headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }

    async def search_rezka(self, name: str) -> tuple[str, str] | None:
        search_url = f"{self.base_url}/search/?do=search&subaction=search&q={name}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=self.headers) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, "html.parser")
                        results = soup.find_all("div", class_="b-content__inline_item")
                        for result in results:
                            title_element = result.find("div", class_="b-content__inline_item-link").find("a")
                            if title_element:
                                title = title_element.text.strip()
                                link = title_element["href"]
                                if name.lower() in title.lower():
                                    return title, link
                    else:
                        print(f"Ошибка: получен статус {response.status} для URL поиска {search_url}")
        except aiohttp.ClientError as e:
            print(f"Сетевая ошибка при поиске на Rezka: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при поиске на Rezka: {e}")
        return None

    async def search_anime(self, page: int = 1) -> list[tuple[str, str]] | None:
        return await self._search_category("animation", page)

    async def search_movies(self, page: int = 1) -> list[tuple[str, str]] | None:
        return await self._search_category("films", page)

    async def search_series(self, page: int = 1) -> list[tuple[str, str]] | None:
        return await self._search_category("series", page)

    async def search_cartoons(self, page: int = 1) -> list[tuple[str, str]] | None:
        return await self._search_category("cartoons", page)

    async def _search_category(self, category: str, page: int) -> list[tuple[str, str]] | None:
        url = f"{self.base_url}/{category}/page/{page}/"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        results = soup.find_all("div", class_="b-content__inline_item")
                        matches: list[tuple[str, str]] = []
                        for result in results:
                            title_element = result.find("div", class_="b-content__inline_item-link").find("a")
                            if title_element:
                                title = title_element.text.strip()
                                link = title_element["href"]
                                matches.append((title, link))
                        return matches
                    else:
                        print(f"Ошибка: получен статус {response.status} для URL категории {url}")
        except aiohttp.ClientError as e:
            print(f"Сетевая ошибка при доступе к категории {category}: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при доступе к категории {category}: {e}")
        return None
