import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import bs4 as bs
import pickle
import requests
import datetime as dt

pd.plotting.register_matplotlib_converters()


def set_dates():
    """
    asks for user input regarding start and end dates
    :return: start,end dates as datatime library objects
    """
    syear, smonth, sday = (
        input('provide starting year,month,day:').split(','))
    syear, smonth, sday = int(syear), int(smonth), int(sday)
    eyear, emonth, eday = input('provide ending year,month,day:').split(',')
    eyear, emonth, eday = int(eyear), int(emonth), int(eday)
    start = dt.datetime(syear, smonth, sday)
    end = dt.datetime(eyear, emonth, eday)
    return start, end


def read_data(csv_format, stock, source, start, end):
    """

    :param csv_format:
    :param stock:
    :param source:
    :param start:
    :param end:
    :return:
    """
    all_data = web.DataReader(stock, source, start, end)
    all_data.to_csv(csv_format)
    all_data = pd.read_csv(csv_format, parse_dates=True, index_col=0)
    return all_data


def plot_graph(df, information):
    """

    :param df:
    :param information:
    :return:
    """
    name = information[0]
    ticker = information[1][0]
    info = information[1][1]
    df[['Open']].plot()
    title = name + ' (' + ticker + ') -' + info
    plt.title(title)
    plt.ylabel('USD $')
    plt.xlabel('Date')
    plt.grid()
    plt.show()


def get_sp500():
    """

    :return:
    """
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_'
                        'companies')
    soup = bs.BeautifulSoup(resp.text, features='lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        name = row.findAll('td')[1].text.replace(' Inc', '') \
            .replace(',', '').replace('.', '').lower()
        sector = row.findAll('td')[4].text
        tickers.append([name,ticker[:-1], sector])
    with open('sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)
    return tickers


def get_TA35():
    """

    :return:
    """
    resp = requests.get('https://en.wikipedia.org/wiki/TA-35_Index')
    soup = bs.BeautifulSoup(resp.text, features='lxml')
    table = soup.find('table', {'class': 'wikitable'})
    tickers = []
    for row in table.findAll('tr')[2:]:
        ticker = row.findAll('td')[2].text[6:-1] + ".TA"
        name = row.findAll('td')[1].text.replace(' Ltd', '') \
                   .replace('.', '').replace('.', '').lower()[:-1]
        sector = row.findAll('td')[3].text[:-1]
        tickers.append([name,ticker,sector])
    with open('TA35tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)
    return tickers


def scrape_stock_data(ticker):
    """

    :param ticker:
    :return:
    """
    all_data = dict()
    webpage = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    resp = requests.get(webpage)
    soup = bs.BeautifulSoup(resp.text, features='lxml')
    stock_data = soup.find_all("table")
    for table in stock_data:
        tds = table.findAll('td')
        for i in range(1, len(tds), 2):
            name = str(tds[i]).split('test=\"')[1].split("-value")[0]
            try:
                value = str(tds[i]).split('</')[0].split('>', 2)[2]
            except IndexError:
                value = str(tds[i]).split('</')[0].split('>')[1]
            all_data[name] = value
    return all_data


def sort_according_to(lst,value):
    tickers = [item[1] for item in lst]
    if str(value).lower()=='tickers':
        return tickers.sort()


print(sort_according_to(get_sp500(),1))
#
# for item in get_sp500()[:10]:
#     ticker = item[1]
#     data = scrape_stock_data(ticker)
#     print(ticker)
#     print(data)

def main():
    """

    :return:
    """
    source = 'yahoo'
    sp = get_sp500()
    stock_name = 'apple'
    # stock_name = input('Which stock to show?').lower()

    if stock_name in sp:
        symbol_sector = sp[stock_name]
    else:
        symbol_sector = stock_name, None
    csv_format = stock_name + '.csv'
    # start, end = set_dates()
    start = dt.datetime(2020, 1, 1)
    end = dt.datetime(2020, 3, 1)
    data_to_plot = read_data(csv_format, symbol_sector[0], source, start, end)
    plot_graph(data_to_plot, [stock_name, symbol_sector])

# main()

# start = dt.datetime(2020,1,1)
# end = dt.datetime(2020,3,1)
# all_data =[]
# names_lst = []
# for item in get_TA35()[:10]:
#     name = item[0]
#     names_lst.append(name)
#     ticker = item[1]
#     info = item[2]
#     csv_format = name +'.csv'
#     data = read_data(csv_format,ticker,'yahoo',start,end)
#     all_data.append(data)
#     print("Finished loading data of:",name)
#     print("plotting graph for:",name)
# for stock in all_data:
#     plt.plot(stock[['Open']])
#
# plt.legend(names_lst)
# plt.show()
