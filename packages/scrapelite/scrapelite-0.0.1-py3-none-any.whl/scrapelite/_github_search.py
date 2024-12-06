from html_content_extractor import extract_content
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
import re

from ._base_search import AutomateWebParser

class Topic(BaseModel):
    name: str


class Repository(BaseModel):
    owner: str
    name: str
    full_name: str
    description: str
    language: Optional[str]
    stars: int
    last_updated: str
    topics: List[Topic] = []
    url: str



class GithubExtractor(AutomateWebParser):
    def search_url(self, query: str) -> str:
        return f"https://github.com/search?q={query}&type=repositories"

    def get_wait_condition(self) -> Dict[str, str]:
        return {
            "selector": "div[data-testid='results-list']"  # GitHub's repository results container
        }

    def parse_github_repositories(self,text: str) -> List[Repository]:
        repositories = []

        # Split the text into repository sections using '###' as delimiter
        repo_sections = text.split('###')[1:]  # Skip the first empty section

        for section in repo_sections:
            try:
                # Extract repository full name
                full_name_match = re.search(r'\[(.*?)\]', section)
                if not full_name_match:
                    continue

                full_name = full_name_match.group(1)
                full_name = re.sub(r'[\*\\]', '', full_name)  # Remove asterisks and backslashes
                owner, name = full_name.split('/')

                # Extract URL
                url_match = re.search(r'\]\((.*?)\)', section)
                url = url_match.group(1) if url_match else ""

                # Extract description
                lines = section.split('\n')
                description = ""
                for line in lines[1:]:
                    if line.strip() and not line.startswith('[') and not line.startswith('*'):
                        description = line.strip()
                        break

                # Extract language
                language_match = re.search(r'\* (\w+)\n·', section)
                language = language_match.group(1) if language_match else None

                # Extract stars
                stars_match = re.search(r'·\* \[(\d+\.?\d*k?)\]', section)
                if stars_match:
                    stars_text = stars_match.group(1)
                    if 'k' in stars_text:
                        stars = int(float(stars_text.replace('k', '')) * 1000)
                    else:
                        stars = int(stars_text)
                else:
                    stars = 0

                # Extract last updated
                updated_match = re.search(r'Updated (.*?)(?:\n|$)', section)
                last_updated = updated_match.group(1) if updated_match else "Unknown"

                # Extract topics
                topics = []
                topic_matches = re.finditer(r'\[([^\]]+)\](/topics/[^\)]+)', section)
                for match in topic_matches:
                    topics.append(Topic(name=match.group(1)))

                repo = Repository(
                    owner=owner.strip(),
                    name=name.strip(),
                    full_name=f"{owner.strip()}/{name.strip()}",
                    description=description,
                    language=language,
                    stars=stars,
                    last_updated=last_updated,
                    topics=topics,
                    url=url
                )
                repositories.append(repo)

            except Exception as e:
                print(f"Error parsing repository section: {e}")
                continue

        return repositories

    def print_repo(self,repo):
        print("\n" + "=" * 50)
        print(f"Repository: {repo.full_name}")
        print(f"Owner: {repo.owner}")
        print(f"Name: {repo.name}")
        print(f"Description: {repo.description}")
        print(f"Language: {repo.language}")
        print(f"Stars: {repo.stars}")
        print(f"Last Updated: {repo.last_updated}")
        print(f"Topics: {[topic.name for topic in repo.topics]}")
        print(f"URL: {repo.url}")

    def extract_with_processing(self, query: str) -> dict:
        js_processor = """
            var results = [];
            var elements = document.querySelectorAll('div[data-testid="results-list"] > div');
            for (var i = 0; i < elements.length; i++) {
                var element = elements[i];
                var titleElement = element.querySelector('a[data-hydro-click]');
                var descElement = element.querySelector('p');
                var statsElement = element.querySelector('div[class*="color-fg-muted"]');

                if (titleElement) {
                    results.push({
                        title: titleElement.innerText.trim(),
                        url: titleElement.href,
                        description: descElement ? descElement.innerText.trim() : '',
                        stats: statsElement ? statsElement.innerText.trim() : ''
                    });
                }
            }
            return results;
        """
        return self.extract(query, process_js=js_processor)

    def extract(
        self,
        query: str,
        process_js: Optional[str] = None,
        min_wait_time:int=5,
        markdown = False
    ) -> List[Repository]:
        html = self._extract(query=query,
                      process_js=process_js,
                      min_wait_time=min_wait_time,
                      markdown=markdown)
        text = extract_content(html, format='markdown')
        repositories = self.parse_github_repositories(text)
        return repositories

