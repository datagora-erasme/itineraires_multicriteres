import sys
sys.path.append("../")
from global_variable import *
"""Tous les paramètres ayant été testés pour faire l'analyse du score"""

meta_params = {
    "P1O8At2Ar10C6E7Ca8" : {
        "graph_path": "./output_data/network/graph/final_network_P1O8At2Ar10C6E7Ca8.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 8*(1-x),
            "alpha": 8
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 8*(1-x),
            "alpha": 8
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 8*(1-x),
            "alpha": 8
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 2*(1-x),
            "alpha": 2
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 6*(1-x),
            "alpha": 6
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 8*(1-x),
            "alpha": 8
            },
        },
    },
    "P1O1At1Ar10C1E1Ca1" : {
        "graph_path": "./output_data/network/graph/final_network_P1O1At1Ar10C1E1Ca1.gpkg",
        "params" : {
            "prairies_prop" : {
                "edges_path": edges_buffer_prairies_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_08_prop" : {
                "edges_path": edges_buffer_ombres_08_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_13_prop" : {
                "edges_path": edges_buffer_ombres_13_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_18_prop" : {
                "edges_path": edges_buffer_ombres_18_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbustes_prop": {
                "edges_path": edges_buffer_arbustes_prop_path,
                # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbres_prop": {
                "edges_path": edges_buffer_arbres_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
                "fn_cont": lambda x: 10*(1-x),
                "alpha": 10
                },
            "C_wavg_scaled": {
                "edges_path": edges_buffer_temp_wavg_path,
                # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "eaux_prop": {
                "edges_path": edges_buffer_eaux_prop_path,
                # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "canop": {
                "edges_path": edges_buffer_parcs_prop_path,
                # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
        }
    },
    "P1O1At1Ar100C1E1Ca1" : {
        "graph_path": "./output_data/network/graph/final_network_P1O1At1Ar100C1E1Ca1.gpkg",
        "params" : {
            "prairies_prop" : {
                "edges_path": edges_buffer_prairies_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_08_prop" : {
                "edges_path": edges_buffer_ombres_08_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_13_prop" : {
                "edges_path": edges_buffer_ombres_13_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_18_prop" : {
                "edges_path": edges_buffer_ombres_18_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbustes_prop": {
                "edges_path": edges_buffer_arbustes_prop_path,
                # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbres_prop": {
                "edges_path": edges_buffer_arbres_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
                "fn_cont": lambda x: 100*(1-x),
                "alpha": 100
                },
            "C_wavg_scaled": {
                "edges_path": edges_buffer_temp_wavg_path,
                # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "eaux_prop": {
                "edges_path": edges_buffer_eaux_prop_path,
                # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "canop": {
                "edges_path": edges_buffer_parcs_prop_path,
                # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
        }
    },
    "P1O8At1Ar10C1E1Ca1" : {
        "graph_path": "./output_data/network/graph/final_network_P1O8At1Ar10C1E1Ca1.gpkg",
        "params" : {
            "prairies_prop" : {
                "edges_path": edges_buffer_prairies_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_08_prop" : {
                "edges_path": edges_buffer_ombres_08_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 8*(1-x),
                "alpha": 8
                },
            "ombres_13_prop" : {
                "edges_path": edges_buffer_ombres_13_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 8*(1-x),
                "alpha": 8
                },
            "ombres_18_prop" : {
                "edges_path": edges_buffer_ombres_18_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 8*(1-x),
                "alpha": 8
                },
            "arbustes_prop": {
                "edges_path": edges_buffer_arbustes_prop_path,
                # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbres_prop": {
                "edges_path": edges_buffer_arbres_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
                "fn_cont": lambda x: 10*(1-x),
                "alpha": 10
                },
            "C_wavg_scaled": {
                "edges_path": edges_buffer_temp_wavg_path,
                # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "eaux_prop": {
                "edges_path": edges_buffer_eaux_prop_path,
                # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "canop": {
                "edges_path": edges_buffer_parcs_prop_path,
                # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
        }
    }
}

meta_params_2807 = {
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O0_01At0_01Ar100C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar100C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 100*(1-x),
            "alpha": 100
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    
}

meta_params_0708 = {
    "P0_01O9At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O9At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O7At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O7At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O3At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O3At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O1At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O1At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },  
}

meta_params_1008 = {
        "P0_01O10At0_01Ar0_01C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O10At0_01Ar0_01C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O0_0At0_01Ar0_01C0_01E0_01Ca10" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar0_01C0_01E0_01Ca10.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        },
    },
    "P0_01O10At0_01Ar10C0_01E0_01Ca10" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O10At0_01Ar10C0_01E0_01Ca10.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        },
    },
}

meta_params_1008_2 = {
        "P0_01O0_01At0_01Ar0_01C10E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar0_01C10E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca9" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca9.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca7" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca7.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca5" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca5.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca1" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca1.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        },
    },
}

meta_params_1108 = {
        "P0_01O9At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O9At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O7At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O7At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O3At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O3At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O1At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O1At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
}

#### ATTENTION, pas alpha*(1-x) pour la température mais bien alpha*x !! 

meta_params_1308 = {
        "P0_01O0_01At0_01Ar0_01C10E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C9E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 10*x,
            "alpha": 10
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C9E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C9E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 9*x,
            "alpha": 9
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C7E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C7E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 7*x,
            "alpha": 7
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C5E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C5E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 5*x,
            "alpha": 5
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C3E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C3E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 3*x,
            "alpha": 3
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C1E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C1E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 1*x,
            "alpha": 1
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
}

meta_params_1408 = {
    "P0_01O0_01At0_01Ar0_01C0_01E10Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar0_01C0_01E10Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E9Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E9Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E7Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E7Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E3Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E3Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E1Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E1Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        },
    },
}

meta_params_1408_arbustes = {
    "P0_01O0_01At0_01Ar0_01C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At9Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At9Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At7Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At7Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At5Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At5Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At3Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At3Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At1Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At1Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
}

meta_params_1508_prairies = {
    "P10O0_01At0_01Ar0_01C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P10O0_01At0_01Ar0_01C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P9O5At0_01Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P9O5At0_01Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P7O5At0_01Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P7O5At0_01Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P5O5At0_01Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P5O5At0_01Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P3O5At0_01Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P3O5At0_01Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 3
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P1O5At0_01Ar10C0_01E5Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P1O5At0_01Ar10C0_01E5Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 0.01*x,
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
}
