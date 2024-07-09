import requests
from datetime import datetime
import smtplib
import time

username = "wanumair0912@gmail.com"
password = "yhpu naha oqwo adnw"

MY_LAT = 3.139003
MY_LONG = 101.686852


def near_iss():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    # your position is within +5 or -5
    if iss_latitude - MY_LAT == 0 and iss_longitude - MY_LONG == 0:
        return True
    elif iss_latitude - MY_LAT < 5 and iss_longitude - MY_LONG < 5:
        return True
    elif iss_latitude - MY_LAT < -5 and iss_longitude - MY_LONG < -5:
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(data['results']['sunset'].split("T")[1].split(":")[0])
    time_now = int(datetime.now().hour)

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if near_iss() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(username, password)
        connection.sendmail(
            from_addr=username,
            to_addrs=username,
            msg="Subject:Look up \n\n The ISS is above you."
        )
