import datetime as dt, json, pathlib, re, urllib.request
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).parent
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
JST=dt.timezone(dt.timedelta(hours=9))
NOW=dt.datetime.now(JST)
DATE=NOW.date().isoformat()
CUTOFF={9:'18:54',10:'19:24',11:'19:57',12:'20:30'}
TYPES={'tanshou':'単勝','nirentan':'2連単','sanrentan':'3連単'}
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.tokens=[]
 def handle_data(self,data):
  s=data.strip()
  if s:self.tokens.append(s)
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; OddsMonitor/1.0)'})
 with urllib.request.urlopen(req,timeout=20) as response:return response.read().decode('utf-8','replace')
def parse(html,kind):
 # Conservative parsing: reject data unless validated. Never fabricate odds.
 p=Parser();p.feed(html)
 tokens=p.tokens
 m=re.search(r'オッズ更新時刻[：:]\s*(\d{1,2}:\d{2})', ' '.join(tokens))
 updated=m.group(1) if m else None
 odds={}
 if kind=='tanshou' and updated:
  for i,t in enumerate(tokens):
   if t=='単勝' and '複勝' in tokens[i:i+4]:
    tail=tokens[i+1:]
    # Detect racer rows by registration numbers is unreliable; use table extraction only when explicit markers present.
    break
 return updated,odds

def main():
 output={'checked_at':NOW.isoformat(),'date':DATE,'races':{},'alerts':[],'warning':'取得方式は未検証です。オッズが空の場合、変動は判定できません。'}
 for race,deadline in CUTOFF.items():
  end=dt.datetime.fromisoformat(f'{DATE}T{deadline}:00').replace(tzinfo=JST)
  if NOW>end:continue
  rec={}
  for kind,label in TYPES.items():
   url=f'https://boaters-boatrace.com/race/suminoe/{DATE}/{race}R/odds?odds-content={kind}'
   try:
    updated,odds=parse(fetch(url),kind)
    rec[label]={'updated':updated,'odds':odds,'status':'要パーサー検証' if updated else '取得形式を確認できません','url':url}
   except Exception as e:rec[label]={'status':'取得失敗','error':str(e)[:150],'url':url}
  output['races'][str(race)]=rec
 (DATA/'latest.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
 with (DATA/'history.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(output,ensure_ascii=False)+'\n')
 print(json.dumps({'time':NOW.isoformat(),'status':'saved','alerts':len(output['alerts'])},ensure_ascii=False))
if __name__=='__main__':main()
