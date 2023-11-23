from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_webdriver(host: str, port: str) -> webdriver.Remote:
    """
    Create a headless Selenium WebDriver with specified connection details.

    Args:
        host (str): The hostname or IP address where the Selenium WebDriver is hosted.
        port (str): The port on which the Selenium WebDriver is running.

    Returns:
        webdriver.Remote: The configured Selenium WebDriver instance.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    remote_url = f'http://{host}:{port}/wd/hub'
    
    return webdriver.Remote(
        command_executor=remote_url,
        options=chrome_options
    )
