import trafilatura
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
from typing import Optional, Dict, Any


class AutomateWebParser:
    def __init__(self, chromedriver_path: str = "/usr/local/bin/chromedriver",
                 animation:bool = False):
        self.chromedriver_path = chromedriver_path
        self.animation = animation
        # Performance-optimized chrome options
        self.chrome_options = Options()
        if not self.animation:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-images")
        self.chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        self.chrome_options.page_load_strategy = 'none'  # Don't wait for all resources

    def search_url(self, query: str) -> str:
        """Override this method to define your URL pattern"""
        raise NotImplementedError("Define your URL pattern")

    def get_wait_condition(self) -> Dict[str, str]:
        """Override this to define what element to wait for"""
        # raise NotImplementedError("Define wait condition")
        return {"selector": "div.g"}

    def _extract(self, query: str, process_js: Optional[str] = None,
                min_wait_time:int=5,
                markdown = True) -> Any:
        """
        Fast extraction with dynamic waiting and optional JS processing

        Args:
            query: Search query
            process_js: Optional JavaScript to process the page
        """
        service = Service(self.chromedriver_path)
        driver = webdriver.Chrome(service=service, options=self.chrome_options)

        try:
            # Get page
            url = self.search_url(quote_plus(query))
            driver.get(url)

            # Dynamic waiting for specific element
            wait_condition = self.get_wait_condition()
            try:
                WebDriverWait(driver, min_wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_condition["selector"]))
                )
            except Exception as e:
                print(f"Exception: {e}")

            # If JavaScript processing is provided, run it
            if markdown:
                return trafilatura.extract(driver.page_source, include_formatting=True)

            if process_js:
                result = driver.execute_script(process_js)
                return result

            return driver.page_source

        finally:
            driver.quit()

    def extract(self, query: str, process_js: Optional[str] = None,
                min_wait_time: int = 5,
                markdown=True) -> Any:
        return self._extract(query=query,
                             process_js=process_js,
                             min_wait_time=min_wait_time,
                             markdown=markdown)



