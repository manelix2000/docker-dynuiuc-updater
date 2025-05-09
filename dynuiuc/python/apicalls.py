import requests
import hashlib
import time
from apiresponse import ApiResponse

def getCurrentIp(envs):
    print("Calling ipSource (ipfy) api..")
    timestamp = int(round(time.time() * 1000))
    try:
        ipfyResponse = requests.get(envs.ipSource, timeout=10)
        if ipfyResponse.status_code == 200:
            currentIp = str(ipfyResponse.json()["ip"])
            print(f"Current public IP is: {currentIp}")
            return ApiResponse(api="ipfy", code=ipfyResponse.status_code, msg=str(currentIp), timestamp=timestamp, ip=str(currentIp))
        else:
            strErr = f"Error: Cannot get current public IP address from {envs.ipSource}"
            print(strErr)
            return ApiResponse(api="ipfy", code=ipfyResponse.status_code, msg=strErr, timestamp=timestamp)
    except requests.exceptions.Timeout:
        strErr = f"WARN! Timeout has occurred while calling {envs.ipSource}! Will try again in {envs.refreshTime} seconds."
        print(strErr)
        return ApiResponse(api="ipfy", code=408, msg=strErr, timestamp=timestamp)
    except Exception as e:
        strErr = f"WARN! Error \'{str(e)}\' has occurred while calling {envs.ipSource}! Will try again in {envs.refreshTime} seconds."
        print(strErr)
        return ApiResponse(api="ipfy", code=500, msg=strErr, timestamp=timestamp)


def updateDynuIp(newIp: str, envs):
    timestamp = int(round(time.time() * 1000))
    if newIp is not None:
        print("Calling dynu Api..")

        md5Pass = hashlib.md5(envs.password.encode('utf-8')).hexdigest()
        requestUrl = f"{envs.dynuUpdateUrl}?hostname={envs.hostnames}&myip={newIp}&password={md5Pass}&username={envs.username}"

        try:
            response = requests.get(requestUrl, timeout=15)

            if response.status_code == 200 and (response.text == "nochg" or response.text.startswith("good")):
                print(f"-> Success - Response from dynu: {response.text}")
                return ApiResponse(api="dynu", code=response.status_code, msg=response.text, timestamp=timestamp, ip=newIp)
            else:
                strErr = f"-> Error - response code: {response.status_code} from DYNU api with message: \'{response.text.strip()}\'. Will try again in {envs.refreshTime} seconds."
                print(strErr)
                return ApiResponse(api="dynu", code=response.status_code, msg=response.text, timestamp=timestamp, ip=newIp)
        except requests.exceptions.Timeout:
            strErr = f"WARN! Timeout has occurred while calling {envs.dynuUpdateUrl}! Will try again in {envs.refreshTime} seconds."
            print(strErr)
            return ApiResponse(api="dynu", code=408, msg=strErr, timestamp=timestamp, ip=newIp)
        except Exception as e:
            strErr = f"WARN! Error \'{str(e)}\' has occurred while calling {envs.dynuUpdateUrl}! Will try again in {envs.refreshTime} seconds."
            print(strErr)
            return ApiResponse(api="dynu", code=500, msg=strErr, timestamp=timestamp, ip=newIp)

    else:
        strErr = f"WARN! Before calling dynu API: Public IP address pulled from {envs.ipSource} is not valid - dynu api is not called!"
        print(strErr)
        return ApiResponse(api="dynu", code=0, msg=strErr, timestamp=timestamp, ip=newIp)
