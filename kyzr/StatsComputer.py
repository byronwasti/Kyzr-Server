import json
from math import radians, cos, sin, asin, sqrt

class StatsComputer:

    def compute_stats(self, user):
        user = json.loads(user)
        username = user["username"]
        transactions = user["locs"]
        u_id = user["_id"]

        stats = {}
        stats["username"] = username
        stats["u_id"] = u_id
        stats["distance"] = self.compute_distance_traveled(transactions)

        return stats


    def compute_distance_traveled(self, transactions):
        total_distance = 0.0
        for i in range(len(transactions)-1):
            loc1 = transactions[i]
            loc2 = transactions[i+1]
            print loc1, loc2
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



# if __name__ == "__main__":
    # sc = StatsComputer()

    # test_user = json.dumps({u'username': u'byron', u'locs': [[42.29082, -71.266214], [40.764638, -73.984156], [38.256893, -79.699032], [28.499291, -81.764462], [51.895243, -2.338384], [31.422155, -6.347217], [22.293637, -79.014279], [29.219712, -98.620313], [40.103645, -121.559765]], u'_id': u'awesome',u'torch': u'awesome'})

    # print sc.compute_stats(test_user)


