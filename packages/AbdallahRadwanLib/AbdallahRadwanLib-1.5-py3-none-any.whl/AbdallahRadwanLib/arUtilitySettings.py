BasicSettings = {                
                    "Version" : "1.0.0.0",    
                    "Language" : "Python",
                    "Framework" : "FastAPI",
                    "enviroments": [
                        "dev",
                        "test",
                        "prod"
                    ],                    
                    "connectionStrings": [
                                            {
                                                "type": "Oracle",
                                                "alias": "AbhaTest",
                                                "name": "",
                                                "userName": "RCAPH",
                                                "password": "RCAPH",
                                                "host": "AIPHDSVM",
                                                "port": 1521,
                                                "serviceName": "AIPHTEST"
                                            },
                                            {
                                                "type": "Oracle",
                                                "alias": "AbhaProduction",
                                                "name": "",
                                                "userName": "RCAPH",
                                                "password": "SCRC5DEVAPH18",
                                                "host": "AIPHDSVM",
                                                "port": 1521,
                                                "serviceName": "aiphdb"
                                            },
                                            {
                                                "type": "Oracle",
                                                "alias": "Abdallah_W",
                                                "name": "",
                                                "userName": "ABDALLAH",
                                                "password": "ABDALLAH",
                                                "host": "AIPHDSVM",
                                                "port": 1521,
                                                "serviceName": "AIPHTEST"
                                            },
                                            {
                                                "type": "Oracle",
                                                "alias": "Abdallah_H",
                                                "name": "",
                                                "userName": "ABDALLAH",
                                                "password": "ABDALLAH",
                                                "host": "Abdallah-Lat5540",
                                                "port": 1521,
                                                "serviceName": "XE"
                                            },
                                            {
                                                "type": "SQLite",
                                                "alias": "dbSQLite",
                                                "name": "hospital",
                                                "userName": "",
                                                "password": "",
                                                "host": "",
                                                "port": 0,
                                                "serviceName": ""
                                            },
                                            {
                                                "type": "MongoDB",
                                                "alias": "dbMongoDB",
                                                "name": "",
                                                "userName": "",
                                                "password": "",
                                                "host": "localhost",
                                                "port": 27017,
                                                "serviceName": ""
                                            },                                            
                                        ],                
                }

VariableSettings = {
                        "DefaultEnviroment": "dev",
                        "DefaultConnectionString" : "Abdallah_W",                        
                        "ServerIP" : "127.0.0.1",
                        "ServerPort" : 15500,
                        "FetchCount" : 10
                   }    