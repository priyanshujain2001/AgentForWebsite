import logging
import requests
from bs4 import BeautifulSoup
import logging

class WebScraper:

    def __init__(self, urls):
        self.urls = urls
        self.results = []
        
        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def scrape(self):
        for url in self.urls:
            try:
                self.logger.info(f"Scraping URL: {url}")
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses
                soup = BeautifulSoup(response.text, 'html.parser')

                # Example scraping of the main content: This can be adjusted as needed
                content = ' '.join([p.get_text() for p in soup.find_all('p')])

                # Append result to the results list
                self.results.append({
                    "text": content,
                    "tags": {
                        "base_url": url
                    }
                })
                self.logger.info(f"Successfully scraped: {url}")

            except requests.exceptions.HTTPError as e:
                self.logger.error(f"HTTP error occurred while scraping {url}: {e}")
            except requests.exceptions.ConnectionError as e:
                self.logger.error(f"Connection error occurred while scraping {url}: {e}")
            except requests.exceptions.Timeout as e:
                self.logger.error(f"Timeout occurred while scraping {url}: {e}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request error occurred while scraping {url}: {e}")
            except Exception as e:
                self.logger.error(f"An unexpected error occurred while scraping {url}: {e}")

        return self.results
    
    def chunk_text(self, text, chunk_size=1000, overlap_size=100):
        """Chunks the text into pieces with specified sizes and overlap."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += (chunk_size - overlap_size)  # Move forward by (chunk_size - overlap_size)

        return chunks

    def scrape_and_chunk(self):
        """Scrapes the specified websites and chunks the text, returning a list of chunks."""
        final_chunks = []
        results = self.scrape()

        for result in results:
            text = result["text"]
            url = result["tags"]["base_url"]
            chunks = self.chunk_text(text)
            
            for chunk in chunks:
                final_chunks.append({
                    "text": chunk,
                    "tags": {
                        "url": url
                    }
                })

        return final_chunks