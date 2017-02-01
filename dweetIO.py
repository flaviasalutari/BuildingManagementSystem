from datetime import date as dt
from datetime import datetime 
import environment as env
from six.moves import urllib


def dweet_sensor_params(shadow_system, light_controller, air_quality_controller):
    dweetIo= "https://dweet.io/dweet/for/"
    my_thing = "sensors_parameters" 
    flux = str(light_controller.total_flux)
    intensity = str(shadow_system.ex_intensity)
    n_people = str(air_quality_controller.n_people)
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
    url = dweetIo + my_thing + "?" + "VOC" + "=" + VOC  + "&" + "tint" + "=" + tint
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
    week_day = datetime.now().weekday()
    if week_day == 0:
        week_day="Monday"
    elif week_day == 1:
        week_day="Tuesday"
    elif week_day == 2:
        week_day="Wednesday"
    elif week_day == 3:
        week_day="Thursday"
    elif week_day == 4:
        week_day="Friday"
    elif week_day == 5:
        week_day="Saturday"
    elif week_day == 6:
        week_day="Sunday"
    seasons=env.seasons
    Y=2000
    today = dt.today()
    if isinstance(today, datetime):
            today = today.date()
    today = today.replace(year=Y)
    # season = next(season for season, (start, end) in seasons if start <= today <= end)
    # if season == 1:
    #     season="Winter"
    # elif season == 2:
    #     season="Spring"
    # elif season == 3:
    #     season="Summer"
    # elif season == 4:
    #     season="Fall"
    day = today.day
    if day < 10:
        day = "0" + str(day)
    else: day = str(day)
    month = today.month
    if month == 1:
        month = "January"
    elif month == 2:
        month = "February"
    elif month == 3:
        month = "March"
    elif month == 4:
        month = "April"
    elif month == 5:
        month = "May"
    elif month == 6:
        month = "June"
    elif month == 7:
        month = "July"
    elif month == 8:
        month = "August"
    elif month == 9:
        month = "September"
    elif month == 10:
        month = "October"
    elif month == 11:
        month = "November"
    elif month == 12:
        month = "December"
    date = day + "-" + month
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



