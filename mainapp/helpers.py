from .serializers import ActivityFeedSerializer

def activity_feed(feed, type):
    try:
        feed_data = {}
        feed_data['data'] = feed
        if type == "DEL":
            feed_data['message'] = f"You have deleted task {feed['name']}."
        elif type == "CREATE": 
            feed_data['message'] = f"You have added task {feed['name']}."
        # elif type == "CREATE": 
        #     feed_data['message'] = f"You have added task {feed['name']}."
        ser = ActivityFeedSerializer(data={"user":feed['user'], "data":feed_data})
        if ser.is_valid():
            ser.save()
    except:
        pass