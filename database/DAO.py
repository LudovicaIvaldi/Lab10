from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():
    @staticmethod
    def getAllStates():
        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)
        query="""select * 
                from country"""
        result=[]
        cursor.execute(query)
        for row in cursor:
            result.append(Stato(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStatesAnno(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select c.state1no as s
                        from contiguity c 
                    where `year` <=%s
                        group by c.state1no"""
        result = []
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row["s"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select c.state1no as s1,c.state2no as s2
                    from contiguity c 
                    where `year` <=%s and conttype =1
                    group by c.state1no,c.state2no"""
        result = []
        cursor.execute(query,(anno,))
        for row in cursor:
            result.append((row["s1"],row["s2"]))
        cursor.close()
        conn.close()
        return result

