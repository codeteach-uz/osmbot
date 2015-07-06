# -*- coding: utf-8 -*-
import re
import nominatim
import os
import sched, time
from osmapi import OsmApi
from bot import OSMbot


def attend(sc):
    if os.path.isfile("last.id"):
        f = open("last.id", "r")
        last_id = int(f.read())
        f.close()
        updates = bot.getUpdates(offset=last_id+1)
    else:
        updates = bot.getUpdates()
    if updates['ok']:
        print "Attending "+str(len(updates["result"]))+" "
        for query in updates['result']:
            if "text" in query["message"]:
                message = query["message"]["text"]
                usr_id = query["message"]["chat"]["id"]
                if message.startswith("@osmbot"):
                    message = message[8:]
                if message == "/start":
                    response = "Hi,how I can help you?"
                elif message.startswith("/details"):
                    id = message[8:].strip()
                    try:
                        osm_data = api.NodeGet(int(id))
                        if osm_data is None:
                            osm_data = api.WayGet(int(id))
                    except:
                        osm_data = None
                    if osm_data is None:
                            response = 'Sorry but I couldn\'t find any result,check the id'
                    else:
                        response = ""
                        if 'name' in osm_data['tag']:
                            response = "\xF0\x9F\x93\xAE "+str(osm_data['tag']['name'])
                        if 'addr:housenumber' in osm_data['tag'] or 'addr:street' in osm_data['tag'] or 'addr:city' in osm_data['tag'] or 'addr:country' in osm_data['tag']:
                            response += "\n"
                            if 'addr:housenumber' in osm_data['tag']:
                                response += osm_data['tag']['addr:housenumber']+" "
                            if 'addr:street' in osm_data['tag']:
                                response += osm_data['tag']['addr:street']+" "
                            if 'addr:city' in osm_data['tag']:
                                response += osm_data['tag']['addr:city']+" "
                            if 'addr:country' in osm_data['tag']:
                                response += osm_data['tag']['addr:country']+" "
                        if response != "":
                            bot.sendMessage(usr_id, response,disable_web_page_preview='true')
                        if 'phone' in osm_data['tag']:
                            response = "\xF0\x9F\x93\x9E "+str(osm_data['tag']['phone'])
                            bot.sendMessage(usr_id, response,disable_web_page_preview='true')
                        if 'fax' in osm_data['tag']:
                            response = "\xF0\x9F\x93\xA0 "+str(osm_data['tag']['fax'])
                            bot.sendMessage(usr_id, response,disable_web_page_preview='true')
                        if 'email' in osm_data['tag']:
                            response = "\xE2\x9C\x89 "+str(osm_data['tag']['email'])
                            bot.sendMessage(usr_id, response,disable_web_page_preview='false')
                        if 'website' in osm_data['tag']:
                            response = "\xF0\x9F\x8C\x8D "+str(osm_data['tag']['website'])
                            bot.sendMessage(usr_id, response,disable_web_page_preview='true')
                            response = ""
                            response += "\xF0\x9F\x93\x8D http://www.openstreetmap.org/?minlat={0}&maxlat={1}&minlon={2}&maxlon={3}&mlat={4}&mlon={5}\n".format(result['boundingbox'][0],result['boundingbox'][1],result['boundingbox'][2],result['boundingbox'][3],result['lat'],result['lon'])+"\n\n\xC2\xA9 OpenStreetMap contributors"

                elif message.startswith("/about"):
                    response = "OpenStreetMap bot info:\n\nCREDITS&CODE\n\xF0\x9F\x91\xA5 Author: OSM català (Catalan OpenStreetMap community)\n\xF0\x9F\x94\xA7 Code: https://github.com/Xevib/osmbot\n\xE2\x99\xBB License: GPLv3, http://www.gnu.org/licenses/gpl-3.0.en.html\n\nNEWS\n\xF0\x9F\x90\xA4 Twitter: https://twitter.com/osmbot_telegram\n\nRATING\n\xE2\xAD\x90 Rating&reviews: http://storebot.me/bot/osmbot\n\xF0\x9F\x91\x8D Please rate me at: https://telegram.me/storebot?start=osmbot\n\nThanks for use @OSMbot!!"
                elif re.match("/search.*",message) is not None and message[8:] != "":
                    search = message[8:].replace("\n","").replace("\r","")
                    response = 'Results for "{0}":\n\n'.format(search)
                    results = nom.query(search)
                    if len(results) ==0:
                        response = 'Sorry but I couldn\'t find any result for "{0}" \xF0\x9F\x98\xA2\nBut you can try to improve OpenStreetMap\xF0\x9F\x94\x8D\nhttp://www.openstreetmap.org'.format(search)
                    if len(results) ==1:
                        for result in results:
                            response += "\xF0\x9F\x93\xAE "+result["display_name"]+"\n"
                            try:
                                if result['osm_type'] == 'node':
                                    osm_data = api.NodeGet(int(result['osm_id']))
                                else:
                                    osm_data = api.WayGet(int(result['osm_id']))
                            except:
                                osm_data = None
                            if osm_data is not None and 'phone' in osm_data['tag']:
                                bot.sendMessage(usr_id, response,disable_web_page_preview='true')
                                response = "\xF0\x9F\x93\x9E "+osm_data['tag']['phone']+"\n"
                                bot.sendMessage(usr_id, response,disable_web_page_preview='true')
                                response = ""
                            response += "\xF0\x9F\x93\x8D http://www.openstreetmap.org/?minlat={0}&maxlat={1}&minlon={2}&maxlon={3}&mlat={4}&mlon={5}\n".format(result['boundingbox'][0],result['boundingbox'][1],result['boundingbox'][2],result['boundingbox'][3],result['lat'],result['lon'])
                            bot.sendMessage(usr_id, response,disable_web_page_preview='true')
                            response = ""
                    else:
                        for result in results:
                            response += "\xE2\x96\xB6 "+result["display_name"]+"\n\n"+"More info /details{0}".format(result['osm_id'])+"\n\n"
                        response += "\xC2\xA9 OpenStreetMap contributors\n"
                elif re.match("/search.*",message) is not None:
                    response = "Please indicate what are you searching with command /search <search term>"
                else:
                    response = "Use /search <search term> command to indicate what you are searching"
                bot.sendMessage(usr_id, response,disable_web_page_preview='true')
            last_id = query["update_id"]
            f = open("last.id" , "w")
            f.write(str(last_id))
            f.close()
    sc.enter(15, 1, attend, (sc,))

f = open("token", "r")
token = f.read()
f.close()

token = token.replace("\n", "").replace("\r", "")
api = OsmApi()
nom = nominatim.Nominatim()
bot = OSMbot(token)

s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, attend, (s,))
s.run()


