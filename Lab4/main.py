import threading
import requests
import time
import re
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template

class Crawler:
  main_url = 'https://www.olx.ro/d/piese-auto'
  titles = []
  ad_filters = {
    "Anvelope": {
      "Iarna": [],
      "Vara": [],
      "All-Season": [],
      "Altele": [],
    },
    "Jante": {
      "16 inch": [],
      "17 inch": [],
      "18 inch": [],
      "19 inch": [],
      "19 inch": [],
      "21 inch": [],
      "Altele": []
    },
    "Electronice" : {
      "Senzori": [],
      "Computer": [],
      "Altele": [],
    },
    "Interior": {
      "Audio": [],
      "Navigatie": [],
      "Scaune": [],
      "Elemente bord": [],
      "Mochete": [],
      "Altele": [],
      "Tapiterie": [],
    },
    "Exterior": {
      "Faruri/Stopuri/Alte beculete": [],
      "Portiere/Haioane": [],
      "Eleron": [],
      "Aripi": [],
      "Altele": [],
    },
    "Geamuri": {
      "Parbrizuri": [],
      "Lunete": [],
      "Geamuri laterale": [],
    },
    "Carlige remorcare": {
      "Dacia": [],
      "Audi": [],
      "BMW": [],
      "Altele": []
    },
    "Dezmembrari": {
      "Dacia": [],
      "Audi": [],
      "BMW": [],
      "Altele": []
    },
    "Motor": {
      "Ambreaj": [],
      "Trubina": [],
      "Injectoare": [],
      "Chiuloasa": [],
      "Volanta": [],
      "Altele": [],
    },
    "Transmisie": {
      "Cutii de viteze": [],
      "Diferentiale/Cutii de transfer": [],
    },
    "Marca Masina": {
      "Dacia": [],
      "Audi": [],
      "BMW": [],
      "Altele": []
    },
    "Altele": [], 
  }

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
  return render_template('index.html', titles = crawler.titles)

if __name__ == "__main__":
  app.run()