from django.shortcuts import render
import random
from threading import *
from time import sleep
from bs4 import BeautifulSoup
import pygsheets
import requests
import gc
# Create your views here.



def index(request):
    return render(request,'index.html')




def result(request):
    url = []
    # print = functools.partial(print, flush=True)
    query = request.POST['inp_text']
    proxy = request.POST['proxies']
    proxy_url = request.POST['proxy_url']
    req = ''
    try:
        req = requests.get(proxy_url).text
        print('url parse success:',proxy_url)
    except:
        print('Error: Proxy url could not be parsed!')
    query = query.split('\r\n')
    proxy = proxy.split('\r\n') + req.split('\r\n')
    queries = []
    proxies = []
    for q in query:
        q = q.strip(' ')
        if q!='':
            queries.append(q)
    print(len(queries),'queries recieved:',queries)
    for p in proxy:
        p = p.strip(' ')
        c = p.count(':')
        if c==1:
            proxies.append(p)
        if c==3:
            p = p.split(':')
            proxies.append(p[2]+':'+p[3]+'@'+p[0]+':'+p[1])
    if len(proxies) > 0:
        print(len(proxies),'proxies recieved:',proxies)
    # if query == '':
    #     return render(request,'index.html')
    t1 = Thread(target=call_scrape,args=[url,queries,proxies])
    t1.start()
    while len(url) == 0:
        None
    text = (','.join(queries))
    if len(text) > 45:
        text = text[0:45] + '...'
    data = {'sheets_url':url[0], 'query_str': text}
    return render(request,'output.html',data)

# def get_proxy_list():
#     resp = requests.get('https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&filterUpTime=100&protocols=http%2Chttps')
#     return resp

def proxy_request(user_proxy_list, url, **kwargs):
    # proxy_list = get_proxy_list()
    if user_proxy_list=='':
        return requests.get(url,**kwargs)
    random.shuffle(user_proxy_list)
    # proxy = random.randint(0,len(user_proxy_list))
    proxy = 0
    while proxy<len(user_proxy_list):
        print('current proxy -->',user_proxy_list[proxy],end='')
        try:

            proxies = {"http": 'http://' + user_proxy_list[proxy], "https": 'http://' + user_proxy_list[proxy]}
            response = requests.get(url, proxies=proxies, timeout=8)
            t = response.text
            if t.find('unusual traffic from ') != -1 or t.find('Google Zoeken') != -1 or t.find('solveSimpleChallenge') != -1:
                raise Exception('')
                return requests.get(url,**kwargs)
            print("... SUCCESS!")
            if response.text.find('error'):
                return requests.get(url,**kwargs)
            print(' ')
            return response
        except:
            print("...   Failed!")
            # print(user_proxy_list)
        
        # proxies = {"http": 'http://' + user_proxy_list[proxy], "https": 'http://' + user_proxy_list[proxy]}
        # response = requests.get(url, proxies=proxies, timeout=10,**kwargs)
        # print(f"Proxy success: {proxies['https']}")
        proxy += 1

    return requests.get(url,**kwargs)

def call_scrape(url, queries,proxies):
    wks_title = ''
    for i in queries:
        wks_title = wks_title + '_' + i.split(' ')[0]
    wks_title = wks_title[1:]
    if len(wks_title)>15:
        wks_title = wks_title[0:15]

    # open the google sheet
    gc = pygsheets.authorize(service_account_file='service_account_sheets.json')
    try:
        sh = gc.open(title='scrape google')
    except pygsheets.PyGsheetsException:
        print('Spreadsheet Not Found!\nCreating New Spreadsheet...')
        sh = gc.create(title='scrape google')
        sh.share('store3age@gmail.com',role='writer',type='user')
        sh.share('', role='reader', type='anyone')

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
                wks_title = wks_title[0:x+2] + str(int(wks_title[x+2:])+1)
            # print(wks_title)

    # Found a unique name, then create the worksheet
    except pygsheets.PyGsheetsException:
        print('Worksheet Title:',wks_title)
        wks = sh.add_worksheet(title=wks_title,rows=450*len(queries),cols=1)
    
    url.append(str(wks.url))

    # Update heading value in the sheet
    wks.update_value('A1','Link')
    wks.cell('A1').set_text_format(attribute='bold',value=True)
    k = 2
    t = 1
    
    # if gc.isenabled() == False:
    # gc.enable()

    for i in queries:
        print('\n\t:: QUERY #',t,' ::\n',sep='')
        k = main_scrape(i,k,proxies,wks)
        print(f'{t}: {i}')
        t += 1
        # gc.collect()
    print('All queries completed!')
    exit()

def main_scrape(query,k,proxies,wks):
    
    srch_str = "+".join(query.split(' '))
    print('search string: ',srch_str)

    headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    
    print('k is: ',k)
    i = 1

    # Link for accessing the Google Sheet
    print(f'Sheet Link[ {query} ]:',str(wks.url))

    # Get the search results
    url = "https://www.google.com/search?q="+srch_str+"&start=0"

    n = 6
    # Scrape all results until link reaches the last page
    while(n):

        # Uncomment this for getting only first 'n' pages of every search result
        # n-=1
        print('Scraping page ',i,'[ ',query,' ]...   ',end='',flush=True,sep='')
        # req = requests.get(url,headers=headers).text
        req = proxy_request(proxies,url,headers=headers)
        i+=1
        soup = BeautifulSoup(req.text,'lxml')
        # print(BeautifulSoup.prettify(soup))
        
        # Find all links in a page
        # and store them in the worksheet
        # wks.unlink()
        for container in soup.findAll('div', class_='tF2Cxc') + soup.findAll('div',class_="ct3b9e"):
            # print(f'Results: {len(container)}')
            head_link = container.a['href']
            l = 'A' + str(k)
            wks.update_value(l,head_link)
            t = random.uniform(0.000,3.214)
            sleep(t)
            k+=1
            # print(head_link)
        # wks.link()
        print('   Saved!',flush=True)

        url = soup.select_one("a#pnnext")
        if url:
            url = "https://www.google.com/" + url['href']
        else:
            print('completed query#',end='')
            break
    # print('Link to Result: ',your_sheet_link)
    del url,soup,req,srch_str
    gc.collect()
    return k