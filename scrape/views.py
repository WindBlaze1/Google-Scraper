from django.shortcuts import render
import functools
from threading import *
from time import sleep
from bs4 import BeautifulSoup
import pygsheets
import os
import requests
# Create your views here.



def index(request):
    return render(request,'index.html')




def result(request):
    url = []
    # print = functools.partial(print, flush=True)
    print('here')
    query = request.POST['inp_text']
    print(query)
    queries = query.split('\r\n')
    # if query == '':
    #     return render(request,'index.html')
    print('queries recieved: ',queries)
    t1 = Thread(target=call_scrape,args=[url,queries])
    # t1 = Thread(target=main_scrape,args=[url,query])
    t1.start()
    while len(url) == 0:
        None
    text = (','.join(queries))
    if len(text) > 40:
        text = text[0:40] + '...'
    data = {'sheets_url':url[0], 'query_str': text}
    return render(request,'output.html',data)


def call_scrape(url, queries):
    wks_title = ''
    for i in queries:
        wks_title = wks_title + '_' + i.split(' ')[0]
    wks_title = wks_title[1:]
    k = 1
    id = 0
    for i in queries:
        k,id = main_scrape(url,i,wks_title,id,k)

def main_scrape(URL,query,wks_title,id,k):
    
    # open the google sheet
    gc = pygsheets.authorize(service_account_file='service_account_sheets.json')
    try:
        sh = gc.open(title='test google')
    except pygsheets.PyGsheetsException:
        print('Spreadsheet Not Found!\nCreating New Spreadsheet...')
        sh = gc.create(title='test google')
        # sh.share('store3age@gmail.com',role='writer',type='user')
        sh.share('', role='reader', type='anyone')

    srch_str = "+".join(query.split(' '))
    print('search string: ',srch_str)

    headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    # print(srch_str)
    print('k is: ',k)
    if k==1:
        # create a different worksheet for storing result of current query
        try:
            # find a unique name for the worksheet 
            # since same names can give errors
            while(1):
                wks = sh.worksheet('title',wks_title)
                x = wks_title.rfind('#0')
                if x==-1:
                    wks_title = wks_title + '#01'
                else:
                    # print('Found:',x)
                    wks_title = wks_title[0:x+2] + str(int(wks_title[x+2])+1)
                # print(wks_title)

        # Found a unique name, then create the worksheet
        except pygsheets.PyGsheetsException:
            print('Worksheet Title:',wks_title)
            wks = sh.add_worksheet(title=wks_title,rows=50000,cols=14)
            id = wks.id
        
        # Update heading value in the sheet
        wks.update_value('A1','Title')
        wks.update_value('B1','Link')
        wks.cell('A1').set_text_format(attribute='bold',value=True)
        wks.cell('B1').set_text_format(attribute='bold',value=True)
        k = 2
    
    else:
        # work in same wks
        wks = sh.worksheet('id',id)
    i = 1

    # Link for accessing the Google Sheet
    your_sheet_link = sh.url + '/view#gid=' + str(wks.id)
    URL.append(your_sheet_link)
    print(f'Sheet Link[ {query} ]:',your_sheet_link)

    # Get the search results
    url = "https://www.google.com/search?q="+srch_str+"&start=0"

    n = 6
    # Scrape all results until link reaches the last page
    while(n):

        # Uncomment this for getting only first 'n' pages
        # n-=1
        print('Scraping page ',i,'[ ',query,' ]...',end='',flush=True,sep='')
        req = requests.get(url,headers=headers).text
        i+=1
        soup = BeautifulSoup(req,'lxml')
        # print(BeautifulSoup.prettify(soup))
        
        # Find all links in a page
        # and store them in the worksheet
        # wks.unlink()
        sleep(10)
        for container in soup.findAll('div', class_='tF2Cxc') + soup.findAll('div',class_="ct3b9e"):
            # print(f'Results: {len(container)}')
            head_link = container.a['href']
            head_text = container.find('h3', class_='LC20lb MBeuO DKV0Md').text
            l = 'A' + str(k)
            wks.update_value(l,head_text)
            l = 'B' + str(k)
            wks.update_value(l,head_link)
            k+=1
            # print(head_text)
            # print(head_link)
            # print()
        # wks.link()
        print('   Saved!',flush=True)

        url = soup.select_one("a#pnnext")
        if url:
            url = "https://www.google.com/" + url['href']
        else:
            print('Successfully scraped all pages!')
            break
    # print('Link to Result: ',your_sheet_link)
    return k,id