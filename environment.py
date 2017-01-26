import random
from datetime import date, datetime
from fileconfigdicts import *


Y = 2000 # dummy leap year
seasons = [(1, (date(Y,  1,  1),  date(Y,  3, 20))),
           (2, (date(Y,  3, 21),  date(Y,  6, 20))),
           (3, (date(Y,  6, 21),  date(Y,  9, 22))),
           (4, (date(Y,  9, 23),  date(Y, 12, 20))),
           (1, (date(Y, 12, 21),  date(Y, 12, 31)))]


           
class Environment():

    def __init__(self):
        self.season = self.get_season(date.today())
        self.intensity = ""
        self.flux = ""
               
                                
    def generate_flux(self):
        flux = random.uniform(flux_season_min[self.season], flux_season_max[self.season])*20
        self.flux = flux
        return flux

    def generate_intensity(self):
		#to be DONE 
		# intensity = algoritmochegeneraintensita(self.season)
        self.intensity = random.uniform(0,1)

        
    def get_season(self, now):
        if isinstance(now, datetime):
            now = now.date()
        now = now.replace(year=Y)
        return next(season for season, (start, end) in seasons if start <= now <= end)

    def run_environment(self):
        self.generate_flux()
        self.generate_intensity()
        self.generate_n_person()
    
    def generate_n_person(self):
        week_day = datetime.now().weekday()
        now_hour = datetime.now().hour       
        self.n_people = int(random.uniform(n_people_min[now_hour], n_people_max[now_hour])*week_days[week_day])
        return self.n_people    
