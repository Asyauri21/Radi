import requests as req
from bs4 import BeautifulSoup as bs
import csv


hades = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_kbs_headlines(hal):
    articles_list = []
    
    for page in range(1, hal + 1):
        try:
            url = f'https://world.kbs.co.kr/service/news_list.htm?page={page}&lang=e&id='
            ge = req.get(url, headers=hades)
            ge.raise_for_status() 
            sop = bs(ge.text, 'lxml')

            li = sop.find('div', class_='contents')
            if not li:
                print(f"No articles found on page {page}")
                continue
            
            articles = li.find_all('article')
            for article in articles:
                headline_tag = article.find('h2')  
                date_tag = article.find('p', class_='date')  
                content_tag = article.find('p', class_='sum')
                 
                if headline_tag:
                    headline = headline_tag.text.strip()
                else:
                    print("No headline found.")
                    continue

                date = date_tag.text.strip() if date_tag else "Date not found"
                
                
                if content_tag:
                    content = content_tag.text.strip()
                else:
                    content = "Content not found"
                
                articles_list.append({
                    'Headline': headline ,
                    'Date': date ,
                    'Content': content
                })
                print(f'Found article: {headline}, Date: {date} , Content: {content}')
        
        except Exception as e:
            print(f"An error occurred: {e}")

    with open('articles.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Date', 'Headline', 'Content']
        wr = csv.DictWriter(file, fieldnames=fieldnames)
        wr.writeheader()  
        for article in articles_list:
            wr.writerow(article)


try:
    hal = int(input("Enter the number of pages to scrape: "))
    scrape_kbs_headlines(hal=hal)
except ValueError:
    print("Please enter a valid integer.")
