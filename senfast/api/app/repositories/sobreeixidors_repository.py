class SobreeixidorsRepository:
    @staticmethod
    def get_all(page: int, per_page: int) -> list:
        offset = (page - 1) * per_page
        with get_db_cursor() as cursor:
            logger.debug(f"Ejecutando consulta: {read_query_sobreeixidors.READ_ALL_SOBREEIXIDORS}")
            cursor.execute(read_query_sobreeixidors.READ_ALL_SOBREEIXIDORS)
            columns = [col[0] for col in cursor.description]
            records = cursor.fetchall()
            if not records:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron sobreeixidors")
            # return {"data": records, "count": len(records)}
            return [DataSobreeixidor(**dict(zip(columns, row))) for row in records]