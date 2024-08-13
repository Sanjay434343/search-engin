from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def bing_search(query, num_pages=20):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    results = []
    
    for page in range(num_pages):
        start = page * 10
        url = f'https://www.bing.com/search?q={query}&first={start + 1}'
        response = requests.get(url, headers=headers)
        
        # Check if the response was successful
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from Bing")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if we have reached the end of the results
        if not soup.select('.b_algo'):
            break

        for item in soup.select('.b_algo'):
            title = item.select_one('h2').text
            link = item.select_one('a')['href']
            snippet = item.select_one('.b_caption p').text if item.select_one('.b_caption p') else ''
            results.append({'title': title, 'link': link, 'snippet': snippet})

        # Optional: Add a delay between requests to avoid hitting rate limits
        # import time
        # time.sleep(1)

    return results

@app.route('/', methods=['GET', 'POST'])
def home():
    query = ''
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = bing_search(query, num_pages=5)  # Adjust num_pages as needed
    return render_template('search.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
