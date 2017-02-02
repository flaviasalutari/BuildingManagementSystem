configuration_room = {
                        "default":  {     
                                        "perc_tints" : {
                                                            1 : 0.58, 
                                                            2: 0.40, 
                                                            3 : 0.10, 
                                                            4: 0.01
                                                        },
                                        "classA" : 100.0, 
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
                                    "name": "TeamSpace",
                                    "avg_npeople" : 4,
                                    "floor" : 4,
                                    "room_ID" : 3,
                                    "total_lamps_desk": 12,
                                    "lamps_per_ambient": 4,
                                    "total_ambients" : 3,
                                    "required_flux" : 55000,
                                    "lumen_lamp_desk" : 3000,
                                    "lumen_lamp_ambient" : 1900,
                                    "default_tint" : 1,
                                    "threshold_intensity" : 0.3, # 
                                    "TVOC" : {
                                                "f_emission" : {
                                                                  "wall":   48.0,
                                                                  "floor" : 25.0,
                                                                  "ceiling" : 48.0,
                                                                  "desk" : 110.0,
                                                                  "desk_panels" : 68.0,
                                                                  "hydroponic_cultivation": 10.0,
                                                                  "chairs" : 110.0

                                                                },
                                                 "surface" : {
                                                                  "wall":  66.6,
                                                                  "floor" :  25.0,
                                                                  "ceiling" : 25.0,
                                                                  "desk" : 4.0,
                                                                  "desk_panels" :  0.9,
                                                                  "hydroponic_cultivation" : 5.0,
                                                                  "chairs" : 1.758
                                                              }               
                                              }
                                }                            
}




