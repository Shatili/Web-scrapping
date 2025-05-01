import requests
from bs4 import BeautifulSoup
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
BASE_URL = "https://habr.com/ru/articles/page{}/"  
NUM_PAGES_TO_PARSE = 30  

def parse_habr_page(url, keywords):
    articles = []
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) # Добавил User-Agent
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for article_element in soup.find_all('article', class_='tm-articles-list__item'):
            try:
                title_element = article_element.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2')
                if not title_element:
                    continue
                title = title_element.text.strip()
                link = "https://habr.com" + title_element.find('a')['href']
                date_element = article_element.find('time')
                date_str = date_element.get('datetime') if date_element else None  
                date = None
                if date_str:
                    try:
                        date = datetime.fromisoformat(date_str[:-1])
                    except ValueError:
                        print(f"Не удалось преобразовать дату: {date_str}")
                        date = None
                preview_text = article_element.get_text(separator=" ").lower()
                for keyword in keywords:
                    if keyword.lower() in preview_text:
                        date_str_formatted = date.strftime("%Y-%m-%d") if date else "Дата неизвестна"
                        articles.append({
                            'date': date_str_formatted,
                            'title': title,
                            'link': link
                        })
                        break  
            except Exception as article_error:
                print(f"Ошибка при обработке статьи: {article_error}") 
    except requests.exceptions.RequestException as request_error:
        print(f"Ошибка при запросе к {url}: {request_error}")
    except Exception as e:
        print(f"Произошла ошибка при парсинге страницы {url}: {e}")
    return articles


def main():
    all_articles = []
    for page_number in range(1, NUM_PAGES_TO_PARSE + 1):
        url = BASE_URL.format(page_number)
        print(f"Парсинг страницы: {url}")
        articles = parse_habr_page(url, KEYWORDS)
        all_articles.extend(articles)

    
    if all_articles:
        print("\nНайденные статьи:")
        for article in all_articles:
            print(f"{article['date']} – {article['title']} – {article['link']}")
    else:
        print("Статьи с указанными ключевыми словами не найдены.")


if __name__ == "__main__":
    main()
        