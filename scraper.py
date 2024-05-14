import requests
import os
import bs4
import threading

from tqdm import tqdm


def sizeof_fmt(num, suffix="B"):
    num = int(num)
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def download_book(notebook_url, cover_url):
    # Get the download link for the notebook
    book_page = requests.request("GET", notebook_url)
    soup = bs4.BeautifulSoup(book_page.text, 'lxml')
    download_button = soup.find('button', {'class': 'download'})
    download_url = download_button.get('onclick').split("'")[1]

    # Request the notebook and cover
    notebook = requests.request("GET", notebook_url + download_url, stream=True)
    cover = requests.request("GET", cover_url, stream=True)

    # Get the total size of the download
    total_size = int(notebook.headers.get('content-length', 0)) + int(
        cover.headers.get('content-length', 0))
    block_size = 1024  # 1 KB

    # Create a progress bar
    progress_bar = tqdm(total=total_size,
                        unit='B',
                        unit_scale=True,
                        desc=download_url,
                        ncols=100,
                        leave=False,)
    
    # Create a directory to store the downloaded files
    os.makedirs('NotesForProfessionals', exist_ok=True)

    with open('NotesForProfessionals/' + download_url, 'wb') as f:
        for data in notebook.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    with open('NotesForProfessionals/' + download_url.replace('.pdf', '.png'),
              'wb') as f:
        for data in cover.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)

    progress_bar.close()
    overall_progress_bar.update(1)


if __name__ == '__main__':
    goal_kicker = "https://goalkicker.com/"
    print("Fetching Webpage...")
    response = requests.request("GET", goal_kicker)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    notebooks = soup.find_all('div', {'class': 'bookContainer grow'})
    notebooks_url = [
        goal_kicker + book.find('a')['href']for book in notebooks
    ]
    covers_url = [
        goal_kicker + book.find('img')['src'] for book in notebooks
    ]

    print("Found", len(notebooks_url), "notebooks")
    threads = []
    # create a progress bar for the whole download 
    overall_progress_bar = tqdm(total=len(notebooks_url), desc="Downloading", ncols=100, position=0)

    for notebook, cover in zip(notebooks_url, covers_url):
        t = threading.Thread(target=download_book, args=(notebook,cover, ))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

