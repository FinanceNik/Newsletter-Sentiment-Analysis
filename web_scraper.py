import articles
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re


def clean_text(text):
    """Basic text cleaning - remove extra spaces, HTML tags, etc."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    return text


def fetch_html_to_dataframe(urls):
    data = {'url': [], 'title': [], 'author': [], 'publication_date': [], 'content': []}

    for url in urls:
        print(f"Fetching HTML for {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'N/A'

            author_element = soup.find(class_=lambda c: c and ('contributor' in c or
                                                               'author' in c or
                                                               'name' in c or
                                                               'TextContributorName' in c or
                                                               'authorText' in c))
            if author_element:
                author = author_element.get_text(strip=True)
                if author.lower().startswith('by'):
                    author = author[2:]  # Remove 'by' from the start
            else:
                author = 'N/A'

            # Extract publication date if available
            pub_date_element = soup.find(class_=lambda c: c and ('date' in c or
                                                                 'publication' in c or
                                                                 'metadata' in c or
                                                                 'timeStamp' in c))

            if pub_date_element:
                pub_date = pub_date_element.get_text(strip=True)
                if pub_date.lower().startswith('Published on'):
                    pub_date = pub_date[12:]
                if pub_date.lower().startswith('Posted: '):
                    pub_date = pub_date[8:]
            else:
                pub_date = 'N/A'

            # Extract content
            content = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
            content = ' '.join([clean_text(tag.get_text(strip=True)) for tag in content])

            data['url'].append(url)
            data['title'].append(title)
            data['author'].append(author)
            data['publication_date'].append(pub_date)
            data['content'].append(content)

            print(f"Successfully fetched HTML for {url}")

        except requests.RequestException as e:
            print(f"An error occurred while fetching {url}: {e}")

    # Convert the data dictionary to a DataFrame
    print("----------------------------------------")
    print("DONE FETCHING HTML FOR ALL WEBPAGES")
    print("----------------------------------------")
    df = pd.DataFrame(data)
    df.to_csv('data/webpages.csv', index=False)
    return df


fetch_html_to_dataframe(articles.articles)


def show_webpage():
    df = pd.read_csv('data/webpages.csv')
    for row in df.itertuples():
        print("URL:", row.url)
        print("Title:", row.title)
        print("Author:", row.author)
        print("Publication Date:", row.publication_date)
        print('Content:')
        print('----------------------------------------')
        print(row.content)
        print('========================================\n')


show_webpage()
