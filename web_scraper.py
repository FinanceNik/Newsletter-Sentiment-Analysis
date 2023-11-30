import articles
from bs4 import BeautifulSoup
import pandas as pd
import requests


def fetch_html_to_dataframe(urls):
    data = {'url': [], 'html_content': []}

    for url in urls:
        print(f"Fetching HTML for {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            headers_and_paragraphs = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
            text_content = ' '.join([tag.get_text(strip=True) for tag in headers_and_paragraphs])

            data['url'].append(url)
            data['html_content'].append(text_content)
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
        print(row.url)
        print('----------------------------------------')
        print(row.html_content)


show_webpage()