import datetime
import requests
import csv
import sys

def oneMinPriceRequest() -> object:
    URL = "https://production.api.coindesk.com/v2/tb/price/values/ETH?start_date=2024-02-21T15:40&end_date=2024-02-22T04:41&interval=1m&ohlc=true"
    res = requests.get(URL)
    d = res.json()
    data = (d['data'])
    return data['entries']

def fifteenMinPriceRequest() -> object:
    URL = "https://production.api.coindesk.com/v2/tb/price/values/ETH?start_date=2024-02-15T15:00&end_date=2024-02-22T04:41&interval=15m&ohlc=true"
    res = requests.get(URL)
    d = res.json()
    data = (d['data'])
    return data['entries']

def oneHourPriceRequest() -> object:
    URL = "https://production.api.coindesk.com/v2/tb/price/values/ETH?start_date=2021-01-01T02:41&end_date=2024-02-22T04:41&interval=1h&ohlc=true"
    res = requests.get(URL)
    d = res.json()
    data = (d['data'])
    return data['entries']

def oneDayPriceRequest() -> object:
    URL = "https://production.api.coindesk.com/v2/tb/price/values/ETH?start_date=2016-12-26T02:41&end_date=2024-02-22T04:41&interval=1d&ohlc=true"
    res = requests.get(URL)
    d = res.json()
    data = (d['data'])
    return data['entries']

def convertMstoSeconds(epochMs: int) -> int:
    return epochMs/1000

def convertEpochToDateTime(epochMs: int) -> datetime:
    epochS = convertMstoSeconds(epochMs)
    time = datetime.datetime.fromtimestamp(epochS)
    # date_time = time.strftime("%m/%d/%Y, %H:%M:%S")
    return time


def createDict(data: object, epoch: bool ) -> object:
    di = {}
    li = []
    for it in data:
        for i in range(1,5):
            li.append(it[i])

        if epoch == True:
            di[it[0]] = li
        else:
            di[convertEpochToDateTime(it[0])] = li

        li = []
    return di
        
def createCSVraw(dict: object, filename: str) -> None:
    fields = ['date', 'price']
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        for data in dict.items():
            writer.writerow(data)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("\nERROR! this script requires 4 command prompt arguments")
        print("example usage: python3 index.py filename1, filename2, filename3, filename4, True or False as a last argument\n") 
        exit()

    oneMinFileName, fifteenMinFileName, oneHourFileName, oneDayFileName = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    epoch = True if sys.argv[5] == "True" else False

    #one min chart
    oneMinData = oneMinPriceRequest()
    oneMinDict = createDict(oneMinData, epoch)
    createCSVraw(oneMinDict, oneMinFileName)    

    #15 min chart
    fifteenMinData = fifteenMinPriceRequest()
    fifteenMinDict = createDict(fifteenMinData, epoch)
    createCSVraw(fifteenMinDict, fifteenMinFileName)

    #1 hour chart
    oneHourData = oneHourPriceRequest()
    oneHourDict = createDict(oneHourData, epoch)
    createCSVraw(oneHourDict, oneHourFileName)

    #1 day chart
    oneDayData = oneDayPriceRequest()
    oneDayDict = createDict(oneDayData, epoch)
    createCSVraw(oneDayDict, oneDayFileName)



