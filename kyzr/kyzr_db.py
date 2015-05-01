from pymongo import MongoClient
import json
from math import radians, cos, sin, asin, sqrt

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
        user = self.users.find_one({'torch':pid})
        
        return user

    def compute_stats(self, pid):
        user = self.find_user(pid)
        stats = {}
        stats["USERNAME"] = user["username"]
        stats["USERID"] = pid
        stats["DISTANCE"] = self.compute_distance(user["locs"])
        stats["NUMTRANSACTION"] = len(user["locs"])-1
        stats["TORCH"] = self.find_user(user["torch"])["username"]

        return stats

    def compute_distance( self, transactions):
        total_distance = 0.0
        for i in range(len(transactions)-1):
            loc1 = transactions[i]
            loc2 = transactions[i+1]
            total_distance += self.haversine(loc1, loc2)

        return total_distance

    def haversine(self, loc1, loc2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        rad_earth = 3956 # Radius of earth in kilometers. Use 3956 for miles
        return c * rad_earth

