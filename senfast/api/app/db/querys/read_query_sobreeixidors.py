class ReadQuerySobreeixidors:
    READ_ALL_SOBREEIXIDORS = """
        SELECT "component", "descripcio", "latitud", "longitud", "color" AS "clase",
               concat(to_char("darrera_lectura",'DD/MM/YYYY, HH24:MI'),'h') AS "data_darrera_lectura",
               "dayly_threshold", "lectura"
        FROM SC.SOFREL_GEO_COMPONENTS
        WHERE "latitud" IS NOT NULL
        ORDER BY "component"
    """
read_query_sobreeixidors = ReadQuerySobreeixidors()
