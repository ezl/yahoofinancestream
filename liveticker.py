import httplib
import sys
import re
import simplejson as json
from threading import Thread

from yfinance import YahooSymbol


# available data items
yahoo_items = {
    'a00': 'ask price',
    'b00': 'bid price',
    'g00': "day's range low",
    'h00': "day's range high",
    'j10': 'market cap',
    'v00': 'volume',
    'a50': 'ask size',
    'b60': 'bid size',
    'b30': 'ecn bid',
    'o50': 'ecn bid size',
    'z03': 'ecn ext hr bid',
    'z04': 'ecn ext hr bid size',
    'b20': 'ecn ask',
    'o40': 'ecn ask size',
    'z05': 'ecn ext hr ask',
    'z07': 'ecn ext hr ask size',
    'h01': "ecn day's high",
    'g01': "ecn day's low",
    'h02': "ecn ext hr day's high",
    'g11': "ecn ext hr day's low",
    't10': 'last trade time, will be in unix epoch format',
    't50': 'ecnQuote/last/time',
    't51': 'ecn ext hour time',
    't53': 'RTQuote/last/time',
    't54': 'RTExthourQuote/last/time',
    'l10': 'last trade',
    'l90': 'ecnQuote/last/value',
    'l91': 'ecn ext hour price',
    'l84': 'RTQuote/last/value',
    'l86': 'RTExthourQuote/last/value',
    'c10': 'quote/change/absolute',
    'c81': 'ecnQuote/afterHourChange/absolute',
    'c60': 'ecnQuote/change/absolute',
    'z02': 'ecn ext hour change',
    'z08': 'ecn ext hour change',
    'c63': 'RTQuote/change/absolute',
    'c85': 'RTExthourQuote/afterHourChange/absolute',
    'c64': 'RTExthourQuote/change/absolute',
    'p20': 'quote/change/percent',
    'c82': 'ecnQuote/afterHourChange/percent',
    'p40': 'ecnQuote/change/percent',
    'p41': 'ecn ext hour percent change',
    'z09': 'ecn ext hour percent change',
    'p43': 'RTQuote/change/percent',
    'c86': 'RTExtHourQuote/afterHourChange/percent',
    'p44': 'RTExtHourQuote/change/percent',
}

def open(symbols="SPY,T,MSFT",data="l10,v00"):
  conn = httplib.HTTPConnection("streamerapi.finance.yahoo.com") 
  conn.request("GET","/streamer/1.0?s=%s&k=%s&callback=parent.yfs_u1f&\
mktmcb=parent.yfs_mktmcb&gencallback=parent.yfs_gencb" % (symbols , data)) 
  return conn.getresponse()

def parse_line(line):
  if line.find('yfs_u1f') != -1:
    #return 'data: '+line
    #{"MSFT":{l10:"25.81",v00:"108,482,336"}}
    try:
      line = re.match(r".*?\((.*?)\)",line) # grab between the parentheses
      line = line.group(1)
      line = re.sub(r"(\w\d\d):",'"\\1":',line) # line isn't valid JSON
      return json.loads(line)
    except:
      return 'ERR: '+line
  elif line.find('yfs_mktmcb') != -1:
    line = re.match(r".*?\((.*?)\)",line) # grab between the parentheses
    line = line.group(1)
    return json.loads(line)
    return 'PING PONG DING DONG: ' + line
  else:
    return
    

def doStuff(symbols="", pretty=True):
  if symbols == "":
    symbols = "SPY"
  conn = ''
  r = open(symbols,"l90")

  line = ''

  while True:
    char = r.read(1)
    if char == '>':
      line += char
      data = parse_line(line)
      if data:
        if pretty:
          try:
            k, v = data.items()[0]
            print "%s: %s" % (k, v['l90'])
          except:
            print(data)
        else:
           print(data)
      line = ''
    else:
      line += char

  con.close();

if __name__ == "__main__":
  try:
    symbols = ",".join(sys.argv[1:])
  except:
    symbols = ""
  doStuff(symbols=symbols)
