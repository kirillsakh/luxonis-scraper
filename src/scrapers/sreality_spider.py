"""
Module: sreality_spider.py
Description: Contains the SrealitySpider class for scraping real estate data from www.sreality.cz.
"""

import logging
import scrapy
from scrapy.http import Response, Request
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Iterable

from config_manager import Config
from database.adapter import create_database_session
from database.models import Ad, Base
from database.types import EstateType
from webdrivers.chrome import create_webdriver


logger = logging.getLogger(__name__)


class SrealitySpider(scrapy.Spider):
    """
    Spider for scraping real estate data from www.sreality.cz.

    Attributes:
        name (str): Spider name.
        allowed_domains (list): List of allowed domains.
        type (str): Type of real estate.

    Methods:
        __init__: Initialize the SrealitySpider instance.
        create_start_urls: Generate start URLs based on provided parameters.
        start_requests: Start the scraping process.
        parse: Parse the scraped data and store it in the database.
    """

    name = 'sreality'
    allowed_domains = ['www.sreality.cz']
    type = EstateType.APARTMENT

    def __init__(self, *args, config: Config = None, **kwargs):
        """
        Initialize the SrealitySpider instance.

        Args:
            config (Config): Configuration object.

        Usage:
            spider = SrealitySpider(config=my_config)
        """
        super(SrealitySpider, self).__init__(*args, **kwargs)
        self.driver: Remote = None
        self.wait: WebDriverWait = None
        self.start_urls = self.create_start_urls(**kwargs)
        self.config = config

    def create_start_urls(self, **kwargs) -> list[str]:
        """
        Generate start URLs based on provided parameters.

        Args:
            **kwargs: Keyword arguments for base_url, path, and pages.

        Returns:
            list: List of start URLs.
        """
        base_url: str = kwargs['base_url']
        path: str = kwargs['path']
        pages: int = int(kwargs['pages'])
        return [base_url + path + f'?page={i}' for i in range(1, pages + 1)]

    def start_requests(self) -> Iterable[Request]:
        """
        Start the scraping process.

        Yields:
            scrapy.Request: Request object for each start URL.
        """
        webdriver_kwargs = dict(
            host=self.config.webdriver_host,
            port=self.config.webdriver_port
        )

        psql_kwargs = dict(
            user=self.config.psql_user,
            password=self.config.psql_password,
            host=self.config.psql_host,
            port=self.config.psql_port,
            database=self.config.psql_database
        )

        with create_webdriver(**webdriver_kwargs) as self.driver:
            self.wait = WebDriverWait(self.driver, 10)
            with create_database_session(**psql_kwargs) as self.session:
                for url in self.start_urls:
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response):
        """
        Parse the scraped data and store it in the database.

        Args:
            response (scrapy.http.Response): Scrapy response object.

        Usage:
            self.parse(response)
        """
        try:
            self.driver.get(response.url)
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'text-wrap')))

            text_wrap_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.text-wrap')

            for text_wrap in text_wrap_divs:
                title = text_wrap.find_element(By.CSS_SELECTOR, 'span.name').get_attribute('textContent')
                address = text_wrap.find_element(By.CSS_SELECTOR, 'span.locality').get_attribute('textContent')
                price = text_wrap.find_element(By.CSS_SELECTOR, 'span.norm-price').get_attribute('textContent')
                ng_href = text_wrap.find_element(By.CSS_SELECTOR, 'h2 a').get_attribute('ng-href')

                img_wraps = self.driver.find_elements(By.XPATH, f'//a[@href="{ng_href}"]')
                for img_wrap in img_wraps:
                    image_url = img_wrap.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    break

                ad = Ad(title=title, address=address, price=price, image_url=image_url, type=self.type)
                try:
                    self.session.add(ad)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    logger.error('Error: {e}, , exc_info=True')
            self.log(f'Scraped {len(text_wrap_divs)} ads from {response.url}')
        except Exception as e:
            logger.error(f'Error adding ad to the database: {e}', exc_info=True)
