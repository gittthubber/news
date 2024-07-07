import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# URL del sito di notizie (Linkiesta)
URL = 'https://www.linkiesta.it/'

def fetch_news(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Errore: Impossibile accedere al sito web, status code {response.status_code}")
        return None
    return response.content

def parse_news(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('div', class_='article')
    
    news_data = []
    
    for article in articles:
        headline = article.find('h3', class_='article-title')
        summary = article.find('p', class_='article-summary')
        link = article.find('a', href=True)
        
        if headline and summary and link:
            headline_text = headline.get_text(strip=True)
            summary_text = summary.get_text(strip=True)
            link_url = link['href']
            if not link_url.startswith('http'):
                link_url = f'https://www.linkiesta.it{link_url}'
                
            news_data.append({
                'headline': headline_text,
                'summary': summary_text,
                'link': link_url,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return news_data

def save_to_csv(news_data, filename):
    df = pd.DataFrame(news_data)
    df.to_csv(filename, index=False)
    print(f"Notizie salvate in {filename}")

def main():
    print("Estrazione delle ultime notizie da Linkiesta...")
    html_content = fetch_news(URL)
    if html_content:
        news_data = parse_news(html_content)
        if news_data:
            save_to_csv(news_data, 'linkiesta_news.csv')
        else:
            print("Nessuna notizia trovata.")
    else:
        print("Impossibile ottenere il contenuto HTML da Linkiesta.")

if __name__ == "__main__":
    main()
