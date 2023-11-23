"""
Module: scraper.py
Description: Script for scraping real estate data using Scrapy and configured logging settings.
"""

import argparse
import logging
import psycopg

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from config_manager import Config, ConfigManager
from scrapers import SCRAPERS
from scrapers.types import ScraperType
from logging_config import configure_logging


configure_logging()

logger = logging.getLogger(__name__)

cfg: Config = ConfigManager.initialize_from_env().config


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape real estate data')
    parser.add_argument('--spider', choices=[e.value for e in ScraperType], help='Choose the spider type')
    parser.add_argument('--base-url', type=str, help='Base URL for the sreality website')
    parser.add_argument('--path', type=str, help='Path parameter for the sreality website')
    parser.add_argument('--pages', type=int, default=1, help='Number of pages to scrape')
    args = parser.parse_args()

    # Initialize Scrapy CrawlerProcess
    process = CrawlerProcess(get_project_settings())

    # Get the selected scraper
    scraper = SCRAPERS.get(args.spider)

    # Run the Scrapy crawler with the specified parameters
    process.crawl(
        scraper,
        base_url=args.base_url,
        path=args.path,
        pages=args.pages,
        config=cfg,
    )
    process.start()
