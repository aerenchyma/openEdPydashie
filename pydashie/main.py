import os
import json
import Queue
import random
import logging
import datetime
import collections
import coffeescript
import SocketServer
import requests, json
import infofile
from bs4 import BeautifulSoup
import urllib, urllib2
from datetime import date, timedelta
from repeated_timer import RepeatedTimer
from flask import Flask, render_template, Response, send_from_directory, request, current_app
from googleanalytics_apiaccess_timeseries_try import GA_Text_Info as gti 
from googleanalytics_apiaccess_timeseries_try import get_country


## TODO: choose time range (html5 date input management? or jquery?)
## TODO: include total reach numbers in all global reach widgets

app = Flask(__name__)

events_queue = {}
items = collections.deque()
last_events = {}
seedX = 0
#seedX2 = 0
# days_back -- default 90 -- but want to get this value from input; if no input, 90
# if not db:
#     days_back = 90
# else:
#     days_back = db

@app.route("/")
def hello():
    return render_template('main.html', title='pyDashie')

@app.route("/assets/application.js")
def javascripts():
#    scripts = [
#        'assets/javascripts/jquery.js',
#        'assets/javascripts/es5-shim.js',
#        'assets/javascripts/d3.v2.min.js',
#        'assets/javascripts/batman.js',
#        'assets/javascripts/batman.jquery.js',
#        'assets/javascripts/jquery.gridster.js',
#        'assets/javascripts/jquery.leanModal.min.js',
#        'assets/javascripts/dashing.coffee',
#        'assets/javascripts/jquery.knob.js',
#        'assets/javascripts/rickshaw.min.js',
#        'assets/javascripts/application.coffee',
#        'assets/javascripts/dashing.gridster.coffee'
#    ]
    scripts = ['assets/javascripts/application.js']
    
    base_directory = os.getcwd()
    full_paths = [os.path.join(base_directory, script_name) for script_name in scripts]
    output = ''
    for path in full_paths:
        if '.coffee' in path:
            print('Compiling Coffee on %s ' % path)
            output = output + coffeescript.compile(open(path).read())
        else:
            output = output + open(path).read()
    return Response(output, mimetype='application/javascript')

@app.route('/assets/application.css')
def application_css():
    scripts = [
        'assets/stylesheets/application.css',
    ]
    base_directory = os.getcwd()
    full_paths = [os.path.join(base_directory, script_name) for script_name in scripts]
    output = ''
    for path in full_paths:
        output = output + open(path).read()
    return Response(output, mimetype='text/css')

@app.route('/assets/images/<path:filename>')
def send_static_img(filename):
    directory = os.path.join(os.getcwd(), 'assets', 'images')
    return send_from_directory(directory, filename)

@app.route('/views/<widget_name>.html')
def widget_html(widget_name):
    base_directory = os.getcwd()
    path = os.path.join(base_directory, 'widgets', widget_name, '%s.html' % widget_name)
    return open(path).read()

@app.route('/events')
def events():
    event_stream_port = request.environ['REMOTE_PORT']
    current_event_queue = Queue.Queue()
    events_queue[event_stream_port] = current_event_queue
    current_app.logger.info('New Client %s connected. Total Clients: %s' % (event_stream_port, len(events_queue)))
    
    #Start the newly connected client off by pushing the current last events
    for event in last_events.values():
        print 'Pushed %s' % event
        current_event_queue.put(event)
    return Response(pop_queue(current_event_queue), mimetype='text/event-stream')

def pop_queue(current_event_queue):
    while True:
        data = current_event_queue.get()
        print 'Popping data %s' % data
        yield data
        
def send_event(widget_id, body):
    body['id'] = widget_id
    body['updateAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')
    formatted_json = 'data: %s\n\n' % (json.dumps(body))
    last_events[widget_id] = formatted_json
    for event_queue in events_queue.values():
        event_queue.put(formatted_json)
    
def sample_synergy():
    # some single number event that changes often enough to make this widget interesting, ?
    synergy_data = {'value': random.randint(0, 100)}
    send_event('synergy', synergy_data)                
    
def sample_buzzwords():
    """Nations the given page/path(s) was viewed from + number of times viewed"""
    df = gti(90)
    nations_vals = df.get_more_info_tups()
    print nations_vals
    items = [{'label': country[0], 'value': country[1]} for country in nations_vals]
    buzzwords_data = {'items':items}
    send_event('buzzwords', buzzwords_data)

def sec_buzzwords():
    """Cities, same otherwise"""
    dt = gti(90)
    cities_vals = dt.get_cities_tups()
    print cities_vals
    cvals = [(city[0],get_country(city[0]),city[1]) for city in cities_vals]
    items = [{'label':city[0]+", "+city[1], 'value': city[2]} for city in cvals]
    buzzwords_data = {'items':items}
    send_event('secbuzzwords', buzzwords_data)

# this is making the graph happen
# TODO make the graphs real data, careful about limit hits and updates
def sample_convergence(): # this needs to refresh and change, which it isn't now doing
    # TODO need new class like gti, except for ONE DAY at a time range -- put it in, start and end
    # TODO cont: be able to specify a time range and then have it do the days OVER TIME
    smp = gti()
    #smp.return_info()["Total Page Views"]

    # global seedX
    # if not seedX:
    #     seedX = 0
    items.append({'x':seedX, 
                  'y':random.randint(0,26)})
    s = sum([d['y'] for d in items])
    items.append({'x':seedX,'y':s})
    seedX += 1


    if len(items) > 32:
        items.popleft()
    item_data = {'points': list(items)}
    totalval = sum([item['y'] for item in items])
    displayedValue = totalval
    #item_data['current'] = 111111
    #print "total:", displayedValue
    send_event('convergence', item_data)

def sec_convergence(days_back=30):
    global seedX
    if not seedX:
        seedX = 0
    items.append({'x':seedX, 
                  'y':random.randint(21,75)})
    seedX += 1

    if len(items) > 10:
        items.popleft()
    item_data = {'points': list(items)}
    send_event('sec_convergence', item_data)

## Python port of @ephigenia's youtube_video job for original Dashing: https://github.com/foobugs/foobugs-dashboard/blob/master/jobs/youtube_video.rb
## alterations for aggregate vids instead of single video
# def youtube_stats(days_back=30):
#     ## code to get all YT urls in course or unit / all vid-ids is important part
#     ## TODO how to generalize appropriately
#     ## TODO (aggr by unit still a problem)
#     mats = "http://open.umich.edu%s" % (infofile.pgpath) + "/materials"
#     vids = ["p4hIzgqA9io"] # placeholder list for all relevant yt vid ids (see above)
#     baseurl = "http://gdata.youtube.com/feeds/api/videos?q=%s&v=2&alt=jsonc"
#     aggregateStats = {'ratings':0,'views':0,'likes':0,'comments':0,'favs':0}

#     ok = False
#     for vid in vids:
#         resp = requests.get(baseurl % (vid))
#         # try: resp.status_code != "200":
#         #     print "YouTube API error (status code %s)" % (resp.status_code)
#         if resp.status_code == 200:
#             ok = True
#             videos = json.loads(resp.text)['data']['items']
#             aggregateStats['ratings'] += int(videos[0]['ratingCount'])
#             aggregateStats['views'] += int(videos[0]['viewCount'])
#             aggregateStats['likes'] += int(videos[0]['likeCount'])
#             aggregateStats['comments'] += int(videos[0]['commentCount'])
#             aggregateStats['favs'] += int(videos[0]['favoriteCount'])

#         else:
#             print "YouTube API error (status code %s)" % (resp.status_code)
#     if ok:
#         # send_event('youtube_vid_rating', aggregateStats['ratings'])
#         # send_event('youtube_vid_views', aggregateStats['views'])
#         # send_event('youtube_vid_likes', aggregateStats['likes'])
#         # send_event('youtube_vid_comments', aggregateStats['comments'])
#         # send_event('youtube_vid_favs', aggregateStats['favs'])
#             # these should be able to use the number widget 
#         print "Views: %s" % aggregateStats['views']
#         item_data = {'value': aggregateStats['views']}
#         send_event('number', item_data)
 
def id_from_url(url):
    index = url.find("watch?v=") + 8
    return url[index:index+11]

def get_vid_ids():
    url = "http://open.umich.edu%s%s" % (infofile.pgpath, "/materials")
    soup = BeautifulSoup(urllib2.urlopen(url))
    yt_links = [str(x.get('href')) for x in soup.find_all('a') if "youtube" in str(x.get('href'))]# if "youtube" in x.get('href')]
    #print yt_links
    vid_ids = [id_from_url(x) for x in yt_links][1:] # first is always not an id but part of youtube url bit??
    return vid_ids

def youtube_stats(days_back=30):
    """Let's try doing YT stuff with the buzzwordsy widget"""
    # TODO get actual vids from page
    #mats = "http://open.umich.edu%s" % (infofile.pgpath) + "/materials" # hmm
    vids = get_vid_ids() #["IT3i6KIXfhc"] # placeholder    
    baseurl = "http://gdata.youtube.com/feeds/api/videos?q=%s&v=2&alt=jsonc"
    aggregateStats = {'ratings':0,'views':0,'likes':0,'comments':0,'favs':0}
    items = []
    items_tags = ["views","comments","likes"] # in case want to limit pieces of aggregateStats shown
    for k in items_tags:
        items.append({'label':'Total YouTube %s: ' % k, 'value': 0})
    #ok = False
    for vid in vids:
        resp = requests.get(baseurl % (vid))
        if resp.status_code == 200:
            #ok = True
            videos = json.loads(resp.text)['data']['items']
            #aggregateStats['ratings'] += int(videos[0]['ratingCount'])
            aggregateStats['views'] += int(videos[0]['viewCount'])
            aggregateStats['likes'] += int(videos[0]['likeCount'])
            aggregateStats['comments'] += int(videos[0]['commentCount'])
            #aggregateStats['favs'] += int(videos[0]['favoriteCount'])

            for i in items:
                if i['label'] == "Total YouTube views: ":
                    i['value'] += aggregateStats['views']
                if i['label'] == "Total YouTube comments: ":
                    i['value'] += aggregateStats['comments']
                if i['label'] == "Total YouTube likes: ":
                    i['value'] += aggregateStats['likes']
            
        else:
            print "YouTube API error (status code %s)" % (resp.status_code)

    item_data = {'items':items}
    send_event('youtubestats', item_data)

def close_stream(*args, **kwargs):
    event_stream_port = args[2][1]
    del events_queue[event_stream_port]
    print('Client %s disconnected. Total Clients: %s' % (event_stream_port, len(events_queue)))

if __name__ == "__main__":
    SocketServer.BaseServer.handle_error = close_stream
    
    # TODO make this neater
    # calling functions at first so immediate data on run; update after a day of time
    get_vid_ids()
    youtube_stats()

    sample_buzzwords()
    sec_buzzwords()

    sample_convergence()
    sample_convergence()
    sample_convergence()
    sample_convergence()

    sec_convergence()
    sec_convergence()
    sec_convergence()
    sec_convergence()

    refreshJobs = [
        (sample_synergy, 10,), # TODO replace this w/ YT (?) or figure out what to do with it
        (sample_buzzwords, 86400,), # 86400 seconds in a day
        (sec_buzzwords, 86400,),
        (sample_convergence, 86400,),
        (sec_convergence, 86400,),
        (youtube_stats, 86400,),
    ]

    timers = [RepeatedTimer(time, function) for function, time in refreshJobs]
    
    try:
        app.run(debug=True, port=5000, threaded=True, use_reloader=False, use_debugger=True)
    finally:
        for timer in timers:
            timer.stop()
