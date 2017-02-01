configuration_room = {
                        "default":  {     
                                        "perc_tints" : {
                                                            1 : 0.58, 
                                                            2: 0.40, 
                                                            3 : 0.10, 
                                                            4: 0.01
                                                        },
                                        "classA" : 100.0, # get from a configuration file,
                                        "occupancy_coefficient" : 0.9
                                    },
                        "Room": {
                                    "room_name": "TheOne",
                                    "room_type" : "office",
                                    "q_iaq" : 48.5,
                                    "f_occupation" : 8.0/24.0, 
                                    "daylight_factor" : 0.088,
                                    "desks_surface" : 4,
                                    "volume" : 4.44 * 5 * 5,
                                    "type" : "Office",
                                    "name": "TheOne",
                                    "total_lamps_desk": 12,
                                    "lamps_per_ambient": 4,
                                    "total_ambients" : 3,
                                    "required_flux" : 55000,
                                    "lumen_lamp_desk" : 3000,
                                    "lumen_lamp_ambient" : 1900,

                                    "default_tint" : 1,
                                    "threshold" : 0.3, # 
                                    "TVOC" : {
                                                "f_emission" : {
                                                                  "wall":   48,
                                                                  "floor" : 25,
                                                                  "ceiling" : 48,
                                                                  "desk" : 110,
                                                                  "desk_panels" : 68,
                                                                  "hydroponic_cultivation": 10,
                                                                  "chairs" : 110

                                                                },
                                                 "surface" : {
                                                                  "wall":  66.6,
                                                                  "floor" :  25,
                                                                  "ceiling" : 25,
                                                                  "desk" : 4,
                                                                  "desk_panels" :  0.9,
                                                                  "hydroponic_cultivation" : 5,
                                                                  "chairs" : 1.758
                                                              }               
                                              }
                                }                            
}


configuration_broker = {
"IPbroker": "localhost",
"port" : 1883
}


configuration_environment =  {
        "flux_season_min" : { 
                                 1: 1, 
                                 2: 100, 
                                 3: 100, 
                                 4: 50
                             },
        "flux_season_max" : { 
                                 1: 400, 
                                 2: 700, 
                                 3: 1000, 
                                 4: 500
                             },

        "sun_irradiation" : {
                      1:  [0, 0, 0, 0, 0.15, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.89, 0.8, 0.6, 0.5, 0.4, 0.25, 0.1, 0, 0, 0, 0],
                      2:  [0, 0, 0, 0, 0.17, 0.27, 0.34, 0.45, 0.55, 0.65, 0.74, 0.85, 0.94, 0.85, 0.74, 0.65, 0.54, 0.43, 0.3, 0.2, 0.1, 0, 0, 0],
                      3:  [0, 0, 0, 0, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.3, 0.2, 0, 0, 0],
                      4:  [0, 0, 0, 0, 0.16, 0.26, 0.33, 0.43, 0.54, 0.64, 0.73, 0.84, 0.95, 0.84, 0.73, 0.65, 0.53, 0.42, 0.29, 0.2, 0.1, 0, 0, 0]
                    },


        "n_people_min" : {
                              0 : 0, 
                              1 : 0, 
                              2 : 0, 
                              3: 0, 
                              4: 0, 
                              5: 0, 
                              6: 0, 
                              7: 0, 
                              8 : 1, 
                              9: 2, 
                              10: 2, 
                              11: 2, 
                              12:1, 
                              13: 0,
                              14: 1, 
                              15: 2,
                              16: 2, 
                              17: 2, 
                              18: 1,
                              19: 1,
                              20: 0, 
                              21: 0,
                              22:0 ,
                              23: 0 
                          },
        "n_people_max" : {
                              0 : 0, 
                              1 : 0, 
                              2 : 0, 
                              3: 0, 
                              4 : 0, 
                              5: 0, 
                              6: 2, 
                              7: 2, 
                              8 : 4, 
                              9: 5, 
                              10: 6,
                              11: 8, 
                              12:4, 
                              13: 2,
                              14: 4, 
                              15: 4, 
                              16: 5, 
                              17: 4, 
                              18: 4,
                              19: 4, 
                              20: 2, 
                              21: 2, 
                              22: 0,
                              23: 0 
                          },
        "week_days" : {
                           0: 1, 
                           1: 1, 
                           2: 1, 
                           3: 1, 
                           4: 1, 
                           5: 0, 
                           6: 0
                       } 
}


















