import requests
import re
from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

currentYear = str(datetime.now().year)


class GetJson(Resource):
    def get(self):
        def convDate(date):
            date_object = datetime.strptime(date, '%Y %b %d')
            return str(date_object.strftime('%d/%m/%Y'))

        def convTime(time):
            time_object = datetime.strptime(time, "%H %M %S")
            return str(time_object.strftime('%H:%M:%S'))

        url = "http://www.gein.noa.gr/services/monthlynew-list_el.php"

        try:
            r = requests.get(url)
            if (r.status_code != 200):
                retJson = {
                    "Status Code": 301,
                    "Message": "Gein Website is Down"
                }
                return jsonify(retJson)
            se = re.search(currentYear+"((.|\n)*)\d.\d", r.text)

            earthquakes = se.group(0)

            earthquakeslist = earthquakes.splitlines()

            earthList = []

            for i in range(len(earthquakeslist)):
                date = re.search(
                    currentYear+"\s[A-Z]+\s+\d+", earthquakeslist[i]).group(0)
                time = re.search(r"\d+ \d+ \d+", earthquakeslist[i]).group(0)
                coordinates = re.findall(r"\d+\.\d\d+", earthquakeslist[i])
                focal = float(re.search(r"\s\s+\d+\s\s\s\s",
                                        earthquakeslist[i]).group(0).strip())
                magnitude = float(re.search(
                    r"\s\d\.\d", earthquakeslist[i]).group(0).strip())
                latitude = coordinates[0]
                longitude = coordinates[1]

                dicCords = {'latitude': latitude, 'longitude': longitude}
                dictionary = {'date': convDate(date), 'time': convTime(
                    time), 'coordinates': dicCords, 'focal': focal, 'magnitude': magnitude}

                earthList.append(dictionary)

            retJson = {
                "Status Code": 200,
                "Earthquakes": earthList
            }

            return(jsonify(retJson))
        except:
            retJson = {
                "Status Code": 302,
                "Message": "Server's Internet Connection is Down"
            }
            return jsonify(retJson)


api.add_resource(GetJson, "/")
if __name__ == "__main__":
    app.run(debug=False)
