#!/Users/rohan/miniconda/bin/python
import billboard
from datetime import date
from datetime import timedelta
from datetime import datetime
import argparse

def get_dates_by_month(year):
    ret = []
    d = date(year = year, month = 1, day = 1)
    ret.append(d)
    while d.month < 12:
        d = d.replace(month = d.month + 1)
        ret.append(d)
    return ret


def get_dates_by_week(year):
    ret = []
    d = date(year = year, month = 1, day = 1)
    delta = timedelta(days = 7)
    while d.year == year:
        ret.append(d)
        d = d + delta
    return ret

def get_chart_entries(playlist, date):
    chart = billboard.ChartData(playlist, str(date))
    delta = timedelta(days = 1)
    total_delta = timedelta(days = 0)
    while len(chart.entries) == 0:
        total_delta += delta
        chart = billboard.ChartData(playlist, str(date + total_delta))
    return (chart, total_delta)


def get_charts(playlist, dates):
    ret = []
    delta = timedelta(days = 0)
    for d in dates:
        if d > datetime.today().date():
            continue
        chart, delta = get_chart_entries(playlist, d + delta)
        ret.append(chart)
    return ret

def get_n_most_frequent_entries(charts, n):
    d = {}
    for chart in charts:
        for song in chart.entries:
            key = song.title + " " + song.artist
            if key not in d:
                d[key] = 1
            else:
                d[key] += 1

    l = [(k,v) for k,v in d.items()]
    l.sort(key=lambda x: x[1])
    l.reverse()
    
    return [title for title,freq in l[:n]]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="fetch songs for given year",
                        type=int)
    parser.add_argument("number", help="choose <number> most frequently appearing songs",
                        type=int)
    parser.add_argument("-c", "--chart", help="choose billboard playlist",
                        default='r-b-hip-hop-songs')

    args = parser.parse_args()
    
    charts = get_charts(args.chart, get_dates_by_month(args.year))
	
    top_songs = get_n_most_frequent_entries(charts, args.number)
        
    for song in top_songs:
        print song


if __name__ == "__main__":
    main()


