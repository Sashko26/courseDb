from pymongo import MongoClient

class database(object):
    db=''
    client=''
    def __init__(self):
        self._connect()
    def _connect(self):

        client = MongoClient('localhost', 50000)
        db = client['olxdb']
        self.data_coll = db['smartphones']
        self.data_coll_request =db['request_smartphones']

    def insert(self,title,price,link,time_of_request):
        return self.data_coll.insert_one({'type': 'smartphone','title': title,'price':price,"link":link,"time_of_request":time_of_request})
    def find_all(self):
        return self.data_coll.find({})
    def remove_all(self):
        return self.data_coll.delete_many({})

    def getAllDevicesFromReques(self, time):
        return self.data_coll.find({"time_of_request": time})




    def insert_request(self,search_title,time_of_request):
        print(self.data_coll_request)
        return self.data_coll_request.insert_one({'type':'request','time':time_of_request,'search': search_title})
    def remove_all_request(self):
        return self.data_coll_request.delete_many({})
    def find_all_request(self):
        return self.data_coll_request.find({})

    def get_by_time_id(self, time):
        return self.data_coll_request.find({'time': time})



db = database()
#db.remove_all()
#db.remove_all_request()
#db.data_coll.delete_many({})











