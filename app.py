from collections import namedtuple

from olxScrapyBot import BLogSpider
from scrapy import signals
import crochet
import os
from dbSettings import db
from datetime import datetime
import matplotlib.pyplot as plt

from scrapy.signalmanager import dispatcher
crochet.setup()  # initialize crochet before further imports
from scrapy.crawler import CrawlerRunner
from flask import Flask, render_template,redirect,url_for,request

import statistics



app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner()
Message =namedtuple('Message','text tag')
messages = []





@app.route('/request/<time>', methods=['GET'])
def get_devices_from_request(time):
    time = time.replace('%',' ')
    arrayOfAllDevices=[]
    element = db.getAllDevicesFromReques(time)
    for doc in element:
        arrayOfAllDevices.append(doc)
    return render_template('list.html',arrayOfAllDevices=arrayOfAllDevices,bool_arrayOfAllDevices=True)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/index', methods=['GET'])
def begin():
    return render_template('index.html')
@app.route('/listOfRequest', methods=['GET'])
def listOfRequest():
    arrayOfElementsInRequest = []
    request = db.find_all_request()
    for doc in request:
        arrayOfElementsInRequest.append(doc)

    return render_template('list.html',requests=arrayOfElementsInRequest,bool_requests=True)
@app.route('/pageForCreatingRequest', methods=['GET'])
def main():
    return render_template('olx.html', messages=messages)

@crochet.wait_for(timeout=60.0)
def scrape_with_crochet(start_url,search_request,time_of_request):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(
        BLogSpider,start_url=start_url,search_request=search_request,time_of_request=time_of_request)
    return eventual  # returns a twisted.internet.defer.Deferred


def _crawler_result(item, response, spider):
    output_data.append(dict(item))

@app.route('/versus_action',methods=['POST'])
def versus_action():
    if request.method == 'POST':
        if os.path.exists('./static/images/saved-figure.png'):
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), './static/images/saved-figure.png')
            os.remove(path)
        first_versus_select = request.form.get('first_versus_select')
        second_versus_select = request.form.get('second_versus_select')
        Array1grapic =[]
        Array2grapic =[]
        cursorArray1 = db.getAllDevicesFromReques(first_versus_select)
        cursorArray2 = db.getAllDevicesFromReques(second_versus_select)
        for el in cursorArray1:
            price = el['price']
            price = price[:-5]
            price = price.replace(' ', '')
            if price.isdigit():
                Array1grapic.append(int(price))
        for el in cursorArray2:
            price = el['price']
            price = price[:-5]
            price = price.replace(' ', '')
            price.replace(' ','')
            if price.isdigit():
                Array2grapic.append(int(price))

        bigLen1=len(Array1grapic)
        bigLen2=len(Array2grapic)
        median1 = statistics.median(Array1grapic)
        median2 = statistics.median(Array2grapic)
        newLess1ArrayGrapic=[]
        newLess2ArrayGrapic=[]


        if bigLen2>1000:
                i=1
                while i<bigLen2:
                    newLess2ArrayGrapic.append(Array2grapic[i-1])
                    i=i+50
                Array2grapic=newLess2ArrayGrapic
        elif bigLen2 > 100:
                i = 1
                while i < bigLen2:
                    newLess2ArrayGrapic.append(Array2grapic[i - 1])
                    i=i + 15
                Array2grapic=newLess2ArrayGrapic
        if bigLen1>1000:
                i=1
                while i<bigLen1:
                    newLess1ArrayGrapic.append(Array1grapic[i-1])
                    i=i+50
                Array1grapic=newLess1ArrayGrapic

        elif bigLen1>100:
                i=1
                while i<bigLen1:
                    newLess1ArrayGrapic.append(Array1grapic[i-1])
                    i=i+15
                Array1grapic = newLess1ArrayGrapic
        print("hi man")
        print(len(Array1grapic))
        print(len(Array2grapic))
        print(Array2grapic)
        plt.plot(Array1grapic, c='r')
        plt.plot(Array2grapic, c='b')

        plt.grid(True)
        plt.savefig('./static/images/saved-figure.png')
        plt.close('all')




        firstCursorRequest  = db.get_by_time_id(first_versus_select)
        secondCursorRequest = db.get_by_time_id(second_versus_select)
        firstRequest=''
        secondRequest=''
        for doc in firstCursorRequest:
            firstRequest = doc
        for doc in secondCursorRequest:
            secondRequest = doc



        vals = [bigLen1,bigLen2]
        labels = [firstRequest['search'], secondRequest['search']]
        fig, ax = plt.subplots()
        ax.pie(vals, labels=labels, autopct='%1.1f%%', shadow=True,
               wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"}, rotatelabels=True)
        ax.axis("equal")
        fig.savefig('./static/images/saved-figure-circle.png')
        plt.close('all')
        return render_template('versusAction.html',firstRequest=firstRequest,secondRequest=secondRequest,median1=median1,median2=median2,amountOfads1=bigLen1,amountOfads2=bigLen2)


@app.route('/olx_request',methods=['POST'])
def olx_request():
    if request.method == 'POST':
        producer = request.form.get('producer')  # запрос к данным формы
        search_request = request.form.get('search_request')
        state = request.form.get('state')




        if search_request==None:
            search_request=''
        if state == 'all' or state == None:
            state=''
        if producer == 'all' or producer == None:
            producer=''


        if state == "used":
            state='/?search%5Bfilter_enum_state%5D%5B0%5D=used'
        if state == "new":
            state = '/?search%5Bfilter_enum_state%5D%5B0%5D=new'

        if producer!='all' and producer!=None and producer!='':
            producer='/'+producer
        search_requestForSearching=''
        old_search_request=''
        time_of_request=''
        time_of_request = str(datetime.today())
        if search_request!=None and search_request!='':
            old_search_request=search_request
            search_request=search_request.replace(' ','-')
            search_requestForSearching ='/q-'+search_request



        START_URLS = 'https://www.olx.ua/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony'+producer+search_requestForSearching+state+'/'


        scrape_with_crochet(START_URLS,old_search_request,time_of_request)
        if search_request == None:
            search_request="all"
        db.insert_request(search_request, time_of_request)
        return redirect(url_for('main'))



@app.route('/versusRequests',methods=['GET'])
def add_message():
    arrayOfElementsInRequest = []
    request = db.find_all_request()
    for doc in request:
        arrayOfElementsInRequest.append(doc)
    return render_template('versusRequests.html',requests =arrayOfElementsInRequest)




@app.route('/smartphoneAdvertisementOlx', methods=['POST'])
def hello_world():
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run()

























