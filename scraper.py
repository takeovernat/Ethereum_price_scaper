import datetime
import requests
import csv
import sys


def ethPriceRequest(startDate : str, interval : str) -> object:
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M")
    URL = "https://production.api.coindesk.com/v2/tb/price/values/ETH?start_date={}&end_date={}&interval={}&ohlc=true".format(startDate, now_string, interval)
    res = requests.get(URL)
    d = res.json()
    data = (d['data'])
    return data['entries']

def convertMstoSeconds(epochMs: int) -> int:
    return epochMs/1000

def convertEpochToDateTime(epochMs: int) -> datetime:
    epochS = convertMstoSeconds(epochMs)
    time = datetime.datetime.fromtimestamp(epochS)
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
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("\nERROR! this script requires only 4 command prompt arguments and an optional 5th argument")
        print("example usage: python3 index.py filename1, filename2, filename3, filename4, and True as an optional argument to use epoch dates as a key\n") 
        exit()

    oneMinStartDateStr, fifteenMinStartDateStr, oneHourStartDateStr, oneDayStartDateStr  = "2024-02-21T15:40", "2024-02-15T15:00", "2021-01-01T02:41", "2016-12-26T02:41"
    oneMinFileName, fifteenMinFileName, oneHourFileName, oneDayFileName = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    epoch = False
    if len(sys.argv) == 6 and sys.argv[5] == "True" or sys.argv[5] == "true":
        epoch = True

    #one min chart
    oneMinData = ethPriceRequest(oneMinStartDateStr, "1m")
    oneMinDict = createDict(oneMinData, epoch)
    createCSVraw(oneMinDict, oneMinFileName)    

    #15 min chart
    fifteenMinData = ethPriceRequest(fifteenMinStartDateStr, "15m")
    fifteenMinDict = createDict(fifteenMinData, epoch)
    createCSVraw(fifteenMinDict, fifteenMinFileName)

    #1 hour chart
    oneHourData = ethPriceRequest(oneDayStartDateStr, "1h")
    oneHourDict = createDict(oneHourData, epoch)
    createCSVraw(oneHourDict, oneHourFileName)

    #1 day chart
    oneDayData = ethPriceRequest(oneDayStartDateStr, "1d")
    oneDayDict = createDict(oneDayData, epoch)
    createCSVraw(oneDayDict, oneDayFileName)



