from pymongo import MongoClient

class dbEditor:
    def __init__(self):
        self.client = MongoClient()
        self.users = self.client.kyzr.users
    def swap_torch (self,pid1, pid2, lat, lng):
        pid1_d = self.users.find_one({'_id':pid1})
        pid2_d = self.users.find_one({'_id':pid2})

        if pid1_d:
            torch1 = pid1_d['torch']
        else:
            torch1 = pid1

        if pid2_d: 
            torch2 = pid2_d['torch']
        else:
            torch2 = pid2

        # Torch held updates
        self.users.update_one(
                {'_id':pid1},
                {'$set':{'torch':torch2}},
                True)
        self.users.update_one(
                {'_id':pid2},
                {'$set':{'torch':torch1}},
                True)

        # Location updates
        self.users.update_one(
                {'_id':torch1},
                {'$push':{'locs':[lat,lng]}},
                True)
        self.users.update_one(
                {'_id':torch2},
                {'$push':{'locs':[lat,lng]}},
                True)


    def add_user(self, pid, username, lat, lng):
        self.users.update_one(
            {'_id':pid},
            {'$set':{'username':username}},
            True)

        self.users.update_one(
            {'_id':pid},
            {'$set':{'torch':pid}},
            True)

        self.users.update_one(
            {'_id':pid},
            {'$push':{'locs':[lat, lng]}})

    def verify_user(self,pid, username):
        user = self.users.find_one({'_id':pid})
        if user is None:
            user = self.users.find_one({'username':username.lower()})

        return user

    def find_user(self,pid):
        user = self.users.find_one({'_id':pid})
        if user is None:
            user = self.users.find_one({'username':pid.lower()})

        return user
