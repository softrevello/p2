import pymysql

def mysqlconnect():
    conn=pymysql.connect(
        host="localhost",
        user="root",
        port="3306",
        password="",
        db="bd_seguridad"
    )
    
    cur=conn.cursor()
    cur.execute("SHOW DATABASE;")
    output=cur.fetchall()
    print(output)
    print(output)
    print(output)
    print(output)
    print(output)
    
    conn.close()
    
   # if __name__=="__main__" :
   #     mysqlconnect()