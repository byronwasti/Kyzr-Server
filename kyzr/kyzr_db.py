from pymongo import MongoClient
import json
from math import radians, cos, sin, asin, sqrt
import string


# Our pyMongo wrapper for this project
# to make our lives a hell of a lot easier
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

        # Update total number of transactions +1
        comstat_tran = int(self.find_user('comstat')['total_trans'] + 1)
        self.users.update_one(
                {'_id':'comstat'},
                {'$set':{'total_trans':comstat_tran}}
        )

        # Update the queue for newest transactions
        self.update_queue(pid1, pid2)


    def add_user(self, pid, username, lat, lng):
        #TODO: See if we can merge all of these updates
        #      into one update call
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

    
    # Differs from find_user because it takes in a username
    # TODO: Merge with add_user because we never actually
    #       call this function unless we are going to
    #       add a user
    def verify_user(self,pid, username):
        user = self.users.find_one({'_id':pid})
        if user is None:
            user = self.users.find_one({'username':username.lower()})

        return user


    # The one and only...
    def find_user(self,pid):
        user = self.users.find_one({'_id':pid})
        if user is None:
            user = self.users.find_one({'username':pid.lower()})

        return user


    #TODO: Merge with compute_stats, cus this is a stat
    def find_torch(self,tid):
        user = self.users.find_one({'torch':tid})
        return user


    def compute_stats(self, pid):
        user = self.find_user(pid)
        stats = {}
        stats['USERNAME'] = user['username']
        stats['USERID'] = pid
        stats['DISTANCE'] = self.compute_distance(user['locs'])
        stats['NUMTRANSACTION'] = len(user['locs'])-1
        stats["TORCH"] = user["torch"]

        torcher = self.find_torch(user['_id'])
        if torcher is None:
            stats['CURRENTOWNER'] = 'NONE FOUND'
            return stats

        stats['CURRENTOWNER'] = torcher['username']
        return stats


    # Thanks to Michael Dunn on stackoverflow for
    # the general idea of this code (it has been modified)
    def compute_distance( self, transactions):
        total_distance = 0.0
        for i in range(len(transactions)-1):
            loc1 = transactions[i]
            loc2 = transactions[i+1]
            total_distance += self.haversine(loc1, loc2)

        total_distance = "{0:.2f}".format(total_distance) + " mi."

        return total_distance

    # More Michael Dunn business
    # <3 you bro!
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


    # Updates queue for newest transactions
    # using only 2 updates files
    def update_queue(self, pid1, pid2):
        comstat = self.find_user('comstat')
        cur_num = comstat['#']
        new_num = int((cur_num+1)%5)

        self.users.update_one(
            {'_id':'comstat'},
            {'$set':{'#': new_num }},
            True)
        USERS = [self.find_user(pid1)['username'], self.find_user(pid2)['username'] ]

        cur_num = str(cur_num)

        self.users.update_one(
            {'_id':'comstat'},
            {'$set':{ cur_num:USERS }},
            True)


    # Return the current state of the queue
    def get_queue(self):
        comstat = self.find_user('comstat')
        cur_num = comstat['#']

        return [ comstat[str(int((i+cur_num)%5)) ] for i in xrange(5)] 
