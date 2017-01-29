configuration_room = {
                        "default":  {     
                                        "perc_tints" : {
                                                            1 : 0.58, 
                                                            2: 0.40, 
                                                            3 : 0.10, 
                                                            4: 0.01
                                                        },
                                        "classA" : 100 # get from a configuration file
                                    },
                        "Room": {
                                    "room_name": "TheOne",
                                    "room_type" : "office",
                                    "q_iaq" : 47,
                                    "f_occupation" : 8/24, 
                                    "volume" : 4.44 * 5 * 5,
                                    "type" : "Office",
                                    "name": "TheOne",
                                    "total_lamps": 24,
                                    "required_flux" : 55000,
                                    "lumen_lamp" : 2300,
                                    "default_tint" : 1,
                                    "threshold" : 0.3, # 
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
                           4 :1, 
                           5: 0, 
                           6:0
                       } 
}


















