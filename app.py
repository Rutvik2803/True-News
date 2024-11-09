from flask import Flask, render_template, request,session,redirect,url_for
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import time

app = Flask(__name__)

app.secret_key = 'hii this is a secret key'

def scrape_bbc():
    search_url = "https://www.bbc.com/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    for attempt in range(5):
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            break
        except ConnectionError:
            print(f"Attempt {attempt + 1}: Connection failed, retrying...")
            time.sleep(2)
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    headlines = soup.find_all('h2', class_='sc-8ea7699c-3 kwWByH')
    for headline in headlines:
        title = headline.get_text().strip()
        link = headline.find_parent('a')['href'] if headline.find_parent('a') else ""
        full_url = f"https://www.bbc.com{link}" if link else "No URL available"
        paragraph = ""
        for sibling in headline.find_next_siblings():
            if sibling.name == 'p':
                paragraph += sibling.get_text().strip() + " "
            elif len(paragraph) > 200:
                break
        if not paragraph:
            paragraph = "No full summary available."
        articles.append({'title': title, 'paragraph': paragraph.strip(), 'url': full_url})

    card_headlines = soup.find_all('h2', class_='sc-8ea7699c-3 dhclWg')
    for card in card_headlines:
        title = card.get_text().strip()
        link = card.find_parent('a')['href'] if card.find_parent('a') else ""
        full_url = f"https://www.bbc.com{link}" if link else "No URL available"
        paragraph = ""
        for sibling in card.find_next_siblings():
            if sibling.name == 'p':
                paragraph += sibling.get_text().strip() + " "
            elif len(paragraph) > 200:
                break
        if not paragraph:
            paragraph = "No full summary available."
        articles.append({'title': title, 'paragraph': paragraph.strip(), 'url': full_url})

    return articles


def scrape_cnn():
    search_url = "https://www.cnn.com/world"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    for attempt in range(5):
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            break
        except ConnectionError:
            print(f"Attempt {attempt + 1}: Connection failed, retrying...")
            time.sleep(2)
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    headlines = soup.find_all('h2', class_='container__title_url-text container_lead-package__title_url-text')
    for headline in headlines:
        title = headline.get_text().strip()
        link = headline.find_parent('a')['href'] if headline.find_parent('a') else ""
        full_url = f"https://www.cnn.com{link}" if link else "No URL available"
        paragraph = ""
        for sibling in headline.find_next_siblings():
            if sibling.name == 'p':
                paragraph += sibling.get_text().strip() + " "
            elif len(paragraph) > 200:
                break
        if not paragraph:
            paragraph = "No full summary available."
        articles.append({'title': title, 'paragraph': paragraph.strip(), 'url': full_url})

    card_headlines = soup.find_all('div', class_='container__headline container_lead-plus-headlines__headline')
    for card in card_headlines:
        title = card.get_text().strip()
        link = card.find_parent('a')['href'] if card.find_parent('a') else ""
        full_url = f"https://www.cnn.com{link}" if link else "No URL available"
        paragraph = ""
        for sibling in card.find_next_siblings():
            if sibling.name == 'p':
                paragraph += sibling.get_text().strip() + " "
            elif len(paragraph) > 200:
                break
        if not paragraph:
            paragraph = "No full summary available."
        articles.append({'title': title, 'paragraph': paragraph.strip(), 'url': full_url})

    return articles


def verify_news(news_title):
    bbc_articles = scrape_bbc()
    cnn_articles = scrape_cnn()

    combined_articles = bbc_articles + cnn_articles

    if not combined_articles:
        return "No relevant news found on BBC or CNN."

    for article in combined_articles:
        title, paragraph, url = article['title'], article['paragraph'], article['url']
        print("Checking headline:", title)
        if news_title.lower() in title.lower():
            return f"The news is likely verified:\n\nTitle: {title}\nSummary: {paragraph}\nLink: {url}"

    return "The news is potentially fake or not verified by BBC or CNN."


@app.route('/')
def welcome():
    return render_template('firstpage.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    print("Home route accessed")
    if request.method == 'POST':
        user_input = request.form['news_title']
        result = verify_news(user_input)
        session['result'] = result
        return redirect(url_for('result'))
    return render_template('secondpage.html')

@app.route('/result')
def result():
    result_text = session.get('result', 'No result found')
    return render_template('thirdpage.html', result=result_text)


if __name__ == '__main__':
    app.run(debug=True)
