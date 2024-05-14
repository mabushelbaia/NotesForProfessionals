# **NotesForProfessionals Downloader**
 A simple script to download all the programming notebooks from [GoalKicker](https://goalkicker.com) website. It uses the `requests` and `beautifulsoup4` libraries to scrape the website and download the notes and uses multithreading to speed up the process.
## **Usage**
install the required packages using the following command:
```bash
pip install -r requirements.txt
```
run the script:
```bash
python scraper.py
```
All the notes will be downloaded under `NotesForProfessionals` directory.
