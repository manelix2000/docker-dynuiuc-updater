from apscheduler.schedulers.background import BackgroundScheduler

import envvars
import apicalls
import history_server
import database
import time
from apiresponse import ApiResponse

def mainTask(envs):
    print("\n\n")

    timestamp = int(round(time.time() * 1000))
    
    newIpApiResponse = apicalls.getCurrentIp(envs)
    dynuApiResponse = apicalls.updateDynuIp(newIpApiResponse.ip, envs)
    if dynuApiResponse.msg != "nochg":
        print(f"-> Success - dynuiuc - saving values to db: {dynuApiResponse.msg}")
        database.update_db(envs.dbFile, dynuApiResponse.api, dynuApiResponse.code, dynuApiResponse.msg, timestamp, dynuApiResponse.ip)
    else:
        print(f"-> Success - No IP change detected - not saving values")


def scheduled_task(envs):
    mainTask(envs)


# run the first time
print("STARTING SCRIPT..")

# get all env vars
print("Reading global vars..")
globalEnvs = envvars.read_envs()

# initialize the db
print("Initializing sqlite database..")
database.init_db(globalEnvs.dbFile)

# run for the first time
mainTask(globalEnvs)

scheduler = BackgroundScheduler()
job = scheduler.add_job(lambda: scheduled_task(globalEnvs), 'interval', seconds=globalEnvs.refreshTime)

scheduler.start()

history_server.runApi()
