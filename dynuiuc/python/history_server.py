from flask import Flask, abort, Response, render_template

import database
import dataclasses
import pytz
import envvars
from datetime import datetime

globalEnvs = envvars.read_envs()
app = Flask("IpHistory", template_folder=globalEnvs.templatesDir)

def convert_timestamp_to_date(timestamp, timezone='Europe/Madrid'):
    # Convert milliseconds to seconds
    timestamp_s = timestamp / 1000.0

    # Convert the timestamp to a datetime object
    dt = datetime.fromtimestamp(timestamp_s, pytz.utc)
    # Convert to the specified timezone
    tz = pytz.timezone(timezone)
    local_dt = dt.astimezone(tz)
    # Format the date and time
    return local_dt.strftime('%Y-%m-%d %H:%M:%S')

@app.route("/status")
def get_status_html():
    dynuResp_list = database.get_from_db(globalEnvs.dbFile)

    def process_response(response):
        response_dict = dataclasses.asdict(response)
        response_dict['date'] = convert_timestamp_to_date(response_dict['timestamp'])
        return response_dict

    dynuDicts = [process_response(response) for response in dynuResp_list]

    # Render the HTML template using Flask
    return render_template('status_template.html', rows=dynuDicts)

def runApi():
    app.run(host='0.0.0.0', port=1050)
