#!/usr/bin/env python3
import html,json,re,sys
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parent.parent; DATA=ROOT/'data'/'car-market-history.json'; H={'User-Agent':'Mozilla/5.0 (Carloson market monitor)'}
def get(url,data=None):
 r=Request(url,data=urlencode(data).encode() if data else None,headers=H)
 with urlopen(r,timeout=45) as x:return x.read().decode('utf-8','replace')
def clean(x):return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
def norm(x):return re.sub(r'\s+',' ',re.sub(r'[^a-zа-я0-9]+',' ',x.lower().replace('mercedes-benz','mercedes').replace('lixiang','li xiang'))).strip()
def elite_cards(raw):
 out=[]
 for b in re.findall(r'<div class="car-item\b.*?(?=<div class="car-item\b|<button id="loadMoreBtn"|</section>)',raw,re.S):
  a=re.search(r'<a class="akct"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',b,re.S);p=re.search(r'data-minprice="(\d+)"',b)
  if a and p: out.append({'name':clean(a.group(2)),'model_key':norm(clean(a.group(2))),'url':html.unescape(a.group(1)),'price_day':int(p.group(1))})
 return out
def elite():
 raw=get('https://elitecar.rent/prokat-avto/');nonce=re.search(r'elitecarCatalog\s*=\s*\{[^}]*"nonce":"([a-f0-9]+)"',raw)
 if not nonce:raise RuntimeError('EliteCar nonce not found')
 out=elite_cards(raw);page=2
 while True:
  j=json.loads(get('https://elitecar.rent/wp-admin/admin-ajax.php',{'action':'elitecar_catalog','nonce':nonce.group(1),'page':str(page),'class':'','mark':'','search':'','sort':'DESC','pinned':'0'}));more=elite_cards(j.get('data',{}).get('html',''));out+=more
  if not more or not j.get('data',{}).get('has_more'):return out
  page+=1
def carloson():
 raw=get('https://carloson.ru/car');out=[]
 for url,b in re.findall(r'<a\s+href="(https://carloson\.ru/car/[^"]+)"[^>]*class="col-xl-4[^>]*>(.*?)</a>',raw,re.S):
  n=re.search(r'two__block_slide__car_name[^>]*>(.*?)</div>',b,re.S);p=re.search(r'current-price[^>]*>\s*([^<]+)',b,re.S)
  if n and p:
   name=clean(n.group(1));out.append({'name':name,'model_key':norm(name),'url':url,'price_day':int(re.sub(r'\D','',p.group(1)))})
 return out
def main():
 DATA.parent.mkdir(exist_ok=True);history=json.loads(DATA.read_text()) if DATA.exists() else []
 snap={'collected_at':datetime.now(timezone.utc).isoformat(),'elitecar':elite(),'carloson':carloson()}
 history.append(snap);DATA.write_text(json.dumps(history[-60:],ensure_ascii=False,separators=(',',':')))
 print('Collected',len(snap['elitecar']),'EliteCar and',len(snap['carloson']),'Carloson cards')
if __name__=='__main__':
 try:main()
 except Exception as e:print(e,file=sys.stderr);sys.exit(1)
