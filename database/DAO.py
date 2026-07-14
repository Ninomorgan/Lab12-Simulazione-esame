from database.DB_connect import DBConnect
from model.attori import Attore
from model.films import Film


class DAO():

    @staticmethod
    def getAllDate():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct m.year
                from movie m
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllFilms(date1, date2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct m.*
                from movie m, ratings r , genre g
                where m.`year` between %s and %s
                and m.id = r.movie_id 
                and r.median_rating is not null
                and g.movie_id = m.id 
                and g.genre is not null
                and m.worlwide_gross_income  is not null
                order by m.title ASC
                """

        cursor.execute(query, (date1, date2))


        for row in cursor:
            results.append(Film(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getInfoFilm(date1, date2):
        conn = DBConnect.get_connection()

        idMapInfo = {}


        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select m.id, r.median_rating , CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(m.worlwide_gross_income,'$',''),'INR',''),'EUR',''),',',''),' ','') AS UNSIGNED) AS incasso
                from movie m, ratings r , genre g
                where m.`year` between %s and %s
                and m.id = r.movie_id 
                and r.median_rating is not null
                and g.movie_id = m.id 
                and g.genre is not null
                and m.worlwide_gross_income  is not null
                order by m.title ASC
                """

        cursor.execute(query, (date1, date2))


        for row in cursor:
            idMapInfo[row["id"]] = row["median_rating"], row["incasso"]


        cursor.close()
        conn.close()
        return idMapInfo

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query ="""
        select rm1.movie_id as id1, rm2.movie_id as id2, count(distinct rm1.name_id)  as AttoriComuni 
        from role_mapping rm1, role_mapping rm2
        where rm1.name_id = rm2.name_id 
        and rm1.movie_id < rm2.movie_id 
        group by rm1.movie_id , rm2.movie_id 
        
        """

        cursor.execute(query,)

        for row in cursor:

                results.append(
                    (
                       row["id1"],
                       row["id2"],
                       row["AttoriComuni"],
                    )
            )

        cursor.close()
        conn.close()
        return results
