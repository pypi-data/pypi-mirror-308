from typing import Dict
from ._base_search import AutomateWebParser

# Example implementation for Google
class GoogleExtractor(AutomateWebParser):
    def search_url(self, query: str) -> str:
        return f"https://www.google.com/search?q={query}"

    def get_wait_condition(self) -> Dict[str, str]:
        return {"selector": "div.g"}

    def extract_with_processing(self, query: str) -> dict:
        js_processor = """
            var results = [];
            var elements = document.querySelectorAll('div.g');
            for (var i = 0; i < elements.length; i++) {
                var element = elements[i];
                var titleElement = element.querySelector('h3');
                var linkElement = element.querySelector('a');
                if (titleElement && linkElement) {
                    results.push({
                        title: titleElement.innerText,
                        link: linkElement.href
                    });
                }
            }
            return results;
        """
        return self.extract(query, process_js=js_processor)