import pandas as pd
from tqdm import tqdm
from binance.client import Client

client = Client()

info=client.get_exchange_info()

#print(info)

## Filtrando symbols

symbols = [x['symbol'] for x in info['symbols']]

#print(symbols)

## hay que excluir cierto tokens (leveraged tokens)

exclude = ['UP','DOWN','BEAR','BULL']

non_lev = [symbol for symbol in symbols if all(excludes not in symbol for excludes in exclude)]

## ya filtrados up, down, bear, bull
##print(non_lev)

#busquemos aquellos que están relacionados con dolar USDT

relevant = [symbol for symbol in non_lev if symbol.endswith("USDT")]

klines = {}

#historias más importantes de hace 1 hora
for symbol in tqdm(relevant):
    klines[symbol] = client.get_historical_klines(symbol,'1m','1 hour ago UTC')

## print(klines)

## obteniendo ptc change en porcentaje cada minuto
#pd.DataFrame(klines['BTCUSDT'])[4].astype(float).pct_change()+1).prod()-1

returns, symbols = [], []

for symbol in relevant:
    if len(klines[symbol])> 0:
        cumret= (pd.DataFrame(klines[symbol])[4].astype(float).pct_change()+1).prod()-1
        returns.append(cumret)
        symbols.append(symbol)

retdf= pd.DataFrame(returns, index=symbols, columns=['ret'])

## 10 mejores criptos con retorno en USDT
retdf.ret.nlargest(10)
