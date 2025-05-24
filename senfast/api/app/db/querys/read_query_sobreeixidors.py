class ReadQuerySobreeixidors:
    READ_ALL_SOBREEIXIDORS = '''
            SELECT "component", 
                   "descripcio", 
                   "latitud", 
                   "longitud", 
                   "color" as clase, 
                   concat(to_char("darrera_lectura",'DD/MM/YYYY, HH24:MI'),'h') as data_darrera_lectura, 
                   "dayly_threshold", 
                   "lectura" 
            FROM SC.SOFREL_GEO_COMPONENTS 
            ORDER BY "component"
        '''
read_query_sobreeixidors = ReadQuerySobreeixidors()
