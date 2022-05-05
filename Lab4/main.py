import threading
from jmespath import search
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
      "All-Seasons": [],
      "Altele": [],
    },
    "Jante": {
      "R15": [],
      "R16": [],
      "R17": [],
      "R18": [],
      "R19": [],
      "R20": [],
      "R21": [],
      "Altele": []
    },
    "Electronice" : {
      "Senzori": [],
      "Computer": [],
      "Audio": [],
      "Navigatie": [],
    },
    "Interior": {
      "Scaune": [],
      "Volane": [],
      "Mochete": [],
      "Tapiterie": [],
      "Altele": [],
    },
    "Exterior": {
      "Faruri/Stopuri/Alte beculete": [],
      "Portiere/Haioane": [],
      "Eleron/Bare": [],
      "Aripi": [],
      "Altele": [],
    },
    "Geamuri": {
      "Parbrize": [],
      "Lunete": [],
      "Altele": [],
    },
    "Motor": {
      "Ambreiaje": [],
      "Turbine": [],
      "Injectoare": [],
      "Chiuloase": [],
      "Volante": [],
      "Altele": [],
    },
    "Transmisie": {
      "Cutii de viteze": [],
      "Diferentiale/Cutii de transfer": [],
      "Altele": [],
    },
    "Dezmembrari": {
      "Dacia": [],
      "Audi": [],
      "BMW": [],
      "Altele": []
    },
    "Marca Masina": {
      "Dacia": [],
      "Audi": [],
      "BMW": [],
      "Altele": []
    },
    "Altele": [], 
  }

  def pickFilters(self, title:str):
    lower_title = title.lower()
    found_category = False
    if re.search("anvelop(a|e)|cauciuc", lower_title) and not re.search("cov(o|oa)r|pre(s|ș) ", lower_title):
      if re.search("var(a|ă)", lower_title):
        self.ad_filters["Anvelope"]["Vara"].append(title)
      elif re.search("iarn(a|ă)", lower_title):
        self.ad_filters["Anvelope"]["Iarna"].append(title)
      elif re.search("all seasons", lower_title):
        self.ad_filters["Anvelope"]["All-Seasons"].append(title)
      else:
        self.ad_filters["Anvelope"]["Altele"].append(title)
      found_category = True

    if re.search("(j|ge)ant(e|a|ă)|(g|j)en(t|ț)i", lower_title):
      if re.search("(r| )15( |'|\"|”|;|x)", lower_title):
        self.ad_filters["Jante"]["R15"].append(title)
      elif re.search("(r| )16( |'|\"|”|;|x)", lower_title):
        self.ad_filters["Jante"]["R16"].append(title)
      elif re.search("(r| )17( |'|\"|”|;|x)", lower_title):
        self.ad_filters["Jante"]["R17"].append(title)
      elif re.search("(r| )18( |'|\"|”|;|x)", lower_title):
        self.ad_filters["Jante"]["R18"].append(title)
      elif re.search("(r| )19( |'|\"|”|;|x)", lower_title):
        self.ad_filters["Jante"]["R19"].append(title)
      elif re.search("(r| )20( |'|\"|”|;|x)", lower_title):
        self.ad_filters["Jante"]["R20"].append(title)
      elif re.search("(r| )21( |'|\"|”|;|x)", lower_title):
        self.ad_filters["Jante"]["R21"].append(title)
      else:
        self.ad_filters["Jante"]["Altele"].append(title)
      found_category = True
      
    if re.search("senzor", lower_title):
      self.ad_filters["Electronice"]["Senzori"].append(title)
      found_category = True
    if re.search("computer|calculator|bluetooth", lower_title):
      self.ad_filters["Electronice"]["Computer"].append(title)
      found_category = True
    if re.search("box(e|a) |subwoofer|difuzo(r|are)|audio|amplificator|sunet|radio", lower_title):
      self.ad_filters["Electronice"]["Audio"].append(title)
      found_category = True
    if re.search("navi(gatie)", lower_title):
      self.ad_filters["Electronice"]["Navigatie"].append(title)
      found_category = True
    
    if re.search("scaun(e)|banchet(ă|a|e)", lower_title):
      self.ad_filters["Interior"]["Scaune"].append(title)
      found_category = True
    if re.search("volan", lower_title):
      self.ad_filters["Interior"]["Volane"].append(title)
      found_category = True
    if re.search("mochet(a|e|ă)|cov(o|oa)r| pre(s |ș )", lower_title):
      self.ad_filters["Interior"]["Mochete"].append(title)
      found_category = True
    if re.search("tapi(t|ț)erie|capitonaj", lower_title):
      self.ad_filters["Interior"]["Tapiterie"].append(title)
      found_category = True
    if re.search("interior", lower_title) and not found_category:
      self.ad_filters["Interior"]["Altele"].append(title)
      found_category = True

    if re.search("far(uri)?|bec(uri)?|stop(uri)?|led(uri)?", lower_title):
      self.ad_filters["Exterior"]["Faruri/Stopuri/Alte beculete"].append(title)
      found_category = True
    if re.search("portier(a|e|ă)|u(s|ș)(a|ă|i|e)|haio(a)n(e)", lower_title):
      self.ad_filters["Exterior"]["Portiere/Haioane"].append(title)
      found_category = True
    if re.search("elero(a)n(e)|bar(e|a|ă)", lower_title):
      self.ad_filters["Exterior"]["Eleron/Bare"].append(title)
      found_category = True
    if re.search("arip(e|i|a|ă)", lower_title):
      self.ad_filters["Exterior"]["Aripi"].append(title)
      found_category = True
    if re.search("exterio(a)r(e|i)", lower_title) and not found_category:
      self.ad_filters["Exterior"]["Altele"].append(title)
      found_category = True

    if re.search("parbriz", lower_title):
      self.ad_filters["Geamuri"]["Parbrize"].append(title)
      found_category = True
    if re.search("lunet(a|ă|e|uri)", lower_title):
      self.ad_filters["Geamuri"]["Lunete"].append(title)
      found_category = True
    if re.search("geam", lower_title) and not found_category:
      self.ad_filters["Geamuri"]["Altele"].append(title)
      found_category = True

    if re.search("ambreiaj", lower_title):
      self.ad_filters["Motor"]["Ambreiaje"].append(title)
      found_category = True
    if re.search("turb(in(a|ă)|o)", lower_title):
      self.ad_filters["Motor"]["Turbine"].append(title)
      found_category = True
    if re.search("injecto(r|are)", lower_title):
      self.ad_filters["Motor"]["Injectoare"].append(title)
      found_category = True
    if re.search("volant(a|ă|e)", lower_title):
      self.ad_filters["Motor"]["Volante"].append(title)
      found_category = True
    if re.search("chi(u)?l(o)?as(a|ă)", lower_title):
      self.ad_filters["Motor"]["Chiuloase"].append(title)
      found_category = True
    if re.search("motor", lower_title) and not found_category:
      self.ad_filters["Motor"]["Altele"].append(title)
      found_category = True

    if re.search("viteze", lower_title):
      self.ad_filters["Transimisie"]["Cutii de viteze"].append(title)
      found_category = True
    if re.search("diferen(t|ț)ial|grup|transfer"):
      self.ad_filters["Transimisie"]["Diferentiale/Cutii de transfer"].append(title)
      found_category = True
    if re.search("transmisie", lower_title) and not found_category:
      self.ad_filters["Transmisie"]["Altele"].append(title)
      found_category = True

    if re.search("dezmembr", lower_title):
      if re.search("dacia", lower_title):
        self.ad_filters["Dezmembrari"]["Dacia"].append(title)
        found_category = True
      if re.search("audi", lower_title):
        self.ad_filters["Dezmembrari"]["Audi"].append(title)
        found_category = True
      if re.search("bmw", lower_title):
        self.ad_filters["Dezmembrari"]["BMW"].append(title)
        found_category = True
      if re.search("ford", lower_title):
        self.ad_filters["Dezmembrari"]["Ford"].append(title)
        found_category = True
      if re.search("mercedes", lower_title):
        self.ad_filters["Dezmembrari"]["Mercedes"].append(title)
        found_category = True
      if re.search("opel", lower_title):
        self.ad_filters["Dezmembrari"]["Opel"].append(title)
        found_category = True
      if re.search("renault", lower_title):
        self.ad_filters["Dezmembrari"]["Renault"].append(title)
        found_category = True
      
      
      
      
    if not found_category:
      self.ad_filters["Altele"].append(title)
    

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
    time.sleep(10)
    print(f"Found {len(self.titles)} ads")

  def pickAllFilters(self):
    for item in self.titles:
      self.pickFilters(item)


crawler = Crawler()
crawler.fetchAllTitles()
crawler.pickAllFilters()

time.sleep(1)
app = Flask(__name__)
@app.route("/")
def home():
  return render_template('index.html', ad_filters = crawler.ad_filters)

if __name__ == "__main__":
  app.run()