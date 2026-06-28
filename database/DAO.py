from database.DB_connect import DBConnect
from model.attori import Attore


class DAO():

    @staticmethod
    def getAllRate():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.avg_rating 
                    from ratings r
                    order by r.avg_rating asc"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllActors(rate1, rate2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.*
                    from names n, role_mapping rm , movie m ,ratings r 
                    WHERE n.id = rm.name_id AND m.id = rm.movie_id AND r.movie_id = m.id
                    and r.avg_rating between %s and %s
                    and n.date_of_birth is not null
                    order by n.name asc
                    """

        cursor.execute(query, (rate1, rate2))


        for row in cursor:
            results.append(Attore(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(rate1, rate2, idMapAttori):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select rm1.name_id as a1, rm2.name_id as a2, SUM(CAST(REPLACE(m.worlwide_gross_income, '$', '') AS UNSIGNED)) AS peso
                    from role_mapping rm1 , role_mapping rm2 , movie m ,ratings r
                    where m.id = rm1.movie_id and r.movie_id = m.id 
                    and rm1.movie_id = rm2.movie_id 
                    and rm1.name_id < rm2.name_id 
                    and r.avg_rating between  %s and  %s
                    and m.worlwide_gross_income is not null
                    group by rm1.name_id , rm2.name_id 
                    """

        cursor.execute(query, (rate1, rate2))

        for row in cursor:
            if row["a1"] in idMapAttori and row["a2"] in idMapAttori:
                results.append(
                    (
                        idMapAttori[row["a1"]],
                        idMapAttori[row["a2"]],
                        row["peso"]
                    )
            )

        cursor.close()
        conn.close()
        return results