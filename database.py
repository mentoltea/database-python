from typing import *
import mysql.connector as sql
import read_settings

settings = read_settings.read()
host = settings["host"]
username =  settings["username"]
password = settings["password"]
db_name = settings["db_name"]

DB =  None #sql.connect(host= host, 
     #           user= username,
     #           passwd= password)

def GET_TABLES(db_name: str) -> list[str]:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    cur.execute("SHOW TABLES;")
    result: list[tuple[str]] = cur.fetchall()
    return list(map(lambda s: s[0].replace("(", "").replace(")", "").replace("'", "").replace(",", ""),result))

def GET_FIELDS(db_name: str, table: str) -> list[tuple[str,str,str,str,str,str]]:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    cur.execute("DESC {0}".format(table))
    result = cur.fetchall()
    return result

def READ_ALL(db_name:str, table: str) -> list[Any]:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    cur.execute("SELECT * FROM {0};".format(table))
    result = cur.fetchall()
    cur.close()
    return result

def WRITE_ROW(db_name:str, table:str, data: tuple) -> None:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    cur.execute(("INSERT INTO {0} VALUES".format(table) + str(data)).replace(" None,", " NULL,").replace("(None,", "(NULL,"))
    DB.commit()
    cur.close()

def DELETE_ROW(db_name:str, table:str, data: list[Any]) -> None:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    fields = GET_FIELDS(db_name, table)
    field_names = []
    for field in fields:
        field_names.append(field[0])
    if (len(field_names) != len(data)): return
    command = "DELETE FROM {0} ".format(table) + "WHERE " + field_names[0] + "="
    if (type(data[0])==str):
        command += '"' + data[0] + '"'
    else:
        command += str(data[0])
    cur.execute(command)
    DB.commit()
    cur.close()
    
def CHECK_CONNECTION() -> bool:
    if (DB == None): return False
    return DB.is_connected()

def CONNECT(host: str, username: str, password: str) -> None:
    global DB
    if (DB != None): DB.close()
    DB = sql.connect(host= host, 
                user= username,
                passwd= password)

def DISCONNECT() -> None:
    global DB
    if (DB != None):
        DB.commit()
        DB.disconnect()
        DB.close()

def main():
    CONNECT(host, username, password)

    tables = GET_TABLES(db_name)
    for table in tables:
        print('\n'*2+"#"*10)
        print('* '+table, end=" *\n")
        rows = READ_ALL(db_name, table)
        for row in rows:
            print('| ', end="")
            for x in row:
                print(x, end=" | ")
            print('\n'+'-'*10)
        print("#"*10+'\n')
    
    DISCONNECT()
    
    
if (__name__ == "__main__"):
    main()


