# -*- coding: utf-8 -*-
import random
from datetime import date, datetime
from configurationenvironment import configuration_environment
from configurationroom import configuration_room
random.seed(1000000007)

Y = 2000 # dummy leap year
seasons = [(1, (date(Y,  1,  1),  date(Y,  3, 20))),
           (2, (date(Y,  3, 21),  date(Y,  6, 20))),
           (3, (date(Y,  6, 21),  date(Y,  9, 22))),
           (4, (date(Y,  9, 23),  date(Y, 12, 20))),
           (1, (date(Y, 12, 21),  date(Y, 12, 31)))]
         
class Environment():

    def __init__(self):
        self.season = self.get_season(date.today()) # get actual season
        self.intensity = 0
        self.flux_profile = self.sun_flux_season()
        self.n_people = 0
        self.flux = 0
    
    def sun_flux_season(self):
        sun_irradiation = configuration_environment["sun_irradiation"][self.season]
        l = []
        for x in sun_irradiation:
            if x == 0:
                l.append(x)
            
            elif x >= 0.1 and x <= 0.3:
                l.append(x * 250000 + random.randint(-1000, 1000))
                
            elif x >= 0.4 and x <= 0.6:
                l.append(x * 250000 + random.randint(-2000, 2000))
                
            elif x >= 0.6:
                l.append(x * 250000 + random.randint(-3000, 3000))
        flux_profile = [x * configuration_room["Room"]["daylight_factor"]*configuration_room["Room"]["desks_surface"] for x in l] # convert solar irradiance in luminous flux
        return flux_profile       
                                
    def generate_flux(self):
        now = datetime.now().hour
        self.flux = self.flux_profile[now] + random.randint(-3000, 3000) # add some noise to the flux 
        if self.flux < 0:
            self.flux = 0

    def generate_intensity(self):
        now = datetime.now().hour  
        intensity = configuration_environment["sun_irradiation"][self.season][now]    # get intensity of solar irradiaton
        self.intensity = intensity

    def get_season(self, now):
        if isinstance(now, datetime):
            now = now.date()
        now = now.replace(year=Y)
        return next(season for season, (start, end) in seasons if start <= now <= end)

    def run_environment(self):
        self.generate_intensity()
        self.generate_n_person()
        self.season = self.get_season(date.today())
        self.generate_flux() 

    def generate_n_person(self):
        week_day = datetime.now().weekday() # get week in a range [0,6]
        now_hour = datetime.now().hour       
        self.n_people = int(random.uniform(configuration_environment["n_people_min"][now_hour],\
                                           configuration_environment["n_people_max"][now_hour])*configuration_environment["week_days"][week_day])
                        # return number of people as a random between an interval according to the hour and the week day
        return self.n_people 

