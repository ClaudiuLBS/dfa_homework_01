import threading
import requests
import time
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template

class Crawler:
  main_url = 'https://www.olx.ro/d/piese-auto'
  titles = []
  def getPage(self, index: int):
    page = requests.get(f'{self.main_url}/?page={index}')
    soup = bs(page.text, 'html.parser')
    page_titles = soup.find_all("h6")
    for item in page_titles:
      self.titles.append(item.text)
  def fetchAllTitles(self):
    index = 1
    while index <= 25:
      t = threading.Thread(target=lambda: self.getPage(index))
      t.start()
      index += 1
    print("Waiting...")
    time.sleep(15)
    print(f"Found {len(self.titles)} ads")

crawler = Crawler()
crawler.fetchAllTitles()

app = Flask(__name__)
@app.route("/")
def home():
  return render_template('index.html')

if __name__ == "__main__":
  app.run()