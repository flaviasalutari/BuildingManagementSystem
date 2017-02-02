# -*- coding: utf-8 -*-
from datetime import date as dt
from datetime import datetime 
import environment as env
from six.moves import urllib


def dweet_sensor_params(shadow_system, light_controller, air_quality_controller):
    dweetIo= "https://dweet.io/dweet/for/"
    my_thing = "sensors_parameters" 
    flux = str(int(light_controller.total_flux)) # get flux parameter from light controller
    intensity = str(round(shadow_system.ex_intensity, 2)) # get intensity parameter from shading controller
    n_people = air_quality_controller.n_people # get number of people in the room
    if n_people==0:
        n_people = "No_people"
    else:
        n_people = str(n_people)
    url = dweetIo + my_thing + "?" + "flux" + "=" + flux  + "&" + "intensity" + "=" + intensity + "&" + "n_people" + "=" + n_people
    urllib.request.urlopen(url)

def dweet_actuators_params(shadow_system, air_quality_controller):
    dweetIo= "https://dweet.io/dweet/for/"
    my_thing = "actuators_parameters" 
    if air_quality_controller.ACH == 0:
        VOC = str(0)
    else:
        VOC=str((1.0*air_quality_controller.voc_numerator)/air_quality_controller.ACH)
    tint = str(shadow_system.tint)
    ACH = str(round(air_quality_controller.ACH,2))
    url = dweetIo + my_thing + "?" + "ACH" + "=" + ACH  + "&" + "tint" + "=" + tint
    urllib.request.urlopen(url)

def dweet_light_control(light_controller):
    dweetIo= "https://dweet.io/dweet/for/"
    my_thing = "light_control" 
    d_light=str(light_controller.active_lamps_desk)

    # showing which ambients are active
    am_light_1=str(0)
    am_light_2=str(0)
    am_light_3=str(0)
    if light_controller.active_ambients == 1:
        am_light_1=str(1)
    elif light_controller.active_ambients == 2:
        am_light_1=str(1)
        am_light_2=str(1)
    elif light_controller.active_ambients == 3:
        am_light_1=str(1)
        am_light_2=str(1)
        am_light_3=str(1)

    my_thing2= "lumens"
    lumen_desk=str(int(light_controller.total_lamps_desk * light_controller.lumen_lamp_desk))+"lm"
    lumen_ambient=str(int(light_controller.lamps_per_ambient*light_controller.lumen_lamp_ambient))+"lm"
    url = dweetIo + my_thing + "?" + "d_light" + "=" + d_light + "&" + "am_light_1" + "=" + am_light_1 + "&" + "am_light_2" + "=" + am_light_2 + "&" + "am_light_3" + "=" + am_light_3 
    url2 = dweetIo + my_thing2 + "?" + "lumen_desk" + "=" + lumen_desk + "&" + "lumen_ambient" + "=" + lumen_ambient
    urllib.request.urlopen(url)
    urllib.request.urlopen(url2)

def dweet_datetime():
    dweetIo = "https://dweet.io/dweet/for/"
    my_thing = "datetime"
    week_day = datetime.now().strftime('%A')

    seasons=env.seasons
    Y=2000
    today = dt.today()
    if isinstance(today, datetime):
            today = today.date()
    today = today.replace(year=Y)

    day = today.day
    if day < 10:
        day = "0" + str(day)
    else: day = str(day)

    date = day + "-" + today.strftime("%B")
    hour = str(datetime.now().hour)
    if hour < 10:
        hour = "0" + str(hour)
    else: hour = str(hour)
    minutes = datetime.now().minute
    if minutes < 10:
        minutes = "0" + str(minutes)
    else: minutes = str(minutes)
    time = hour + ":" + minutes
    url = dweetIo + my_thing + "?" + "week_day" + "=" + week_day + "&" + "time" + "=" + time + "&" + "date" + "=" + date#+ "&" + "season" + "=" + season
    urllib.request.urlopen(url)



