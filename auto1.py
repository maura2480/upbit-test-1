import time
import pyupbit
import datetime

# 업비트 api키
access = "mbaZfS5Ap7gocMkyVyqpcx1IMjq1kIc7piWwRidr"
secret = "exj2CPhXgqlQRbvZqlV1PD6Kwjj08tk9NfEauqhz"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

df = pyupbit.get_ohlcv("KRW-eth", interval="minute1", count=2)

# ror(수익률), np .where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = pyupbit.get_ohlcv(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작 - krw-etc 코인 1분 봉 3개의 기울기가 +면 매수, 3분 봉 2개의 기울기가 -면 매도
while True:
    try:
        now = datetime.datetime.now() # 현재 시간
        start_time = get_start_time("KRW-ETH") # 9:00 (시작 시간)
        end_time = start_time + datetime.timedelta(days=1) # 9:00 + 1일 (끝나는 시간)

        if start_time < now < end_time - datetime.timedelta(seconds=10): # 오전 9시부터 다음날 오전 8시 50분 50초까지 동작
            target_price = get_target_price("KRW-ETH", 0.5) # 전략 수정 필요 (이름, k값)
            current_price = get_current_price("KRW-ETH")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)
            else:
                if (df['high'] / df['current']) >= 1.10 :
                    omg = get_balance("ETH")
                    if omg > 0.0016:
                        upbit.sell_market_order("KRW-ETH", omg*0.9995)
                else:
                    if (df['low'] / df['current']) <= 0.90:
                        omg = get_balance("ETH")
                        if omg > 0.0016:
                            upbit.sell_market_order("KRW-ETH", omg*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)