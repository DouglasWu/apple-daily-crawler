from datetime import timedelta, date

archive_url = 'http://www.appledaily.com.tw/appledaily/archive/{}'
host_url = 'http://www.appledaily.com.tw'

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_start_urls():
    date_strings = []
    start_date = date(2017, 4, 1)
    end_date = date(2017, 4, 10)
    for single_date in daterange(start_date, end_date):
        date_strings.append(single_date.strftime("%Y%m%d"))
    urls = []
    for date_str in date_strings:
        urls.append(archive_url.format(date_str))
    return urls
