import requests
import os
import bs4
import multiprocessing
def download_book(url):
    book_page = requests.request("GET", url)
    soup = bs4.BeautifulSoup(book_page.text, 'lxml')
    download_button = soup.find('button', {'class': 'download'})
    download_url = download_button.get('onclick').split("'")[1]
    print("Downloading: " + download_url)
    notebook = requests.request("GET", url + download_url)
    # make a dir called books and save the books there
    os.makedirs('NotesForProfessionals', exist_ok=True)
    with open ('NotesForProfessionals/' + download_url, 'wb') as f:
        f.write(notebook.content)
if __name__ == '__main__':
    goal_kicker="https://goalkicker.com/"
    response = requests.request("GET", goal_kicker)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    notebooks = soup.find_all('div', {'class': 'bookContainer grow'})
    notebooks_url = [goal_kicker + book.find('a')['href'] for book in notebooks]
    with multiprocessing.Pool() as p:
        p.map(download_book, notebooks_url)