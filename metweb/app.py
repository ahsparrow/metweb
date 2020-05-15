from datetime import datetime, timedelta
import sqlite3

from flask import Flask, render_template, current_app

def get_met(dbc, dt):
        like_str = dt.strftime("%Y-%m-%d%%")
        res = dbc.execute("select ts, wind, gust, temp from metlog where ts like ?", (like_str,))

        # Y-data in mph
        today = [{'ts': x[0].strftime("%Y-%m-%d %H:%M"),
                  'wind': x[1] * 2.237,
                  'gust': x[2] * 2.237,
                  'temp': x[3]} for x in res.fetchall()]

        wind = [{'t': x['ts'], 'y': x['wind']} for x in today]
        gust = [{'t': x['ts'], 'y': x['gust']} for x in today]
        temp = [{'t': x['ts'], 'y': x['temp']} for x in today]

        return wind, gust, temp

def index():
    db_file = current_app.config['DB_FILE']
    dbc = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)

    dt = datetime.utcnow()
    midnight = dt.strftime("%Y-%m-%dT24:00:00")

    wind_tday, gust_tday, temp_tday = get_met(dbc, dt)
    wind_yday, gust_yday, temp_yday = get_met(dbc, dt - timedelta(days=1))

    dbc.close()

    wind = wind_yday + wind_tday
    gust = gust_yday + gust_tday
    temp = temp_yday + temp_tday

    return render_template("index.html",
                           wind=wind,
                           gust=gust,
                           temp=temp,
                           midnight=midnight)

def create_app():
    app = Flask(__name__)
    app.config.from_envvar("METWEB_SETTINGS")

    app.add_url_rule("/", view_func=index)
    return app


