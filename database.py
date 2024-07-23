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

def READ_BY_KEY(db_name:str, table:str, key_name:str, key:Any) -> list[Any]:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    command = "SELECT * FROM {0} ".format(table) + "WHERE " + key_name + "="
    if (type(key)==str):
        command += '"' + key + '"'
    else:
        command += str(key)
    command += ";"
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    return result

def READ_BY_KEYS(db_name:str, table:str, key_names:list[str], keys:list[Any]) -> list[Any]:
    global DB
    if len(key_names)!=len(keys): return
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    command = "SELECT * FROM {0} ".format(table) + "WHERE "
    for i in range(len(keys)):
        key_name = key_names[i]
        key = keys[i]
        command += key_name + "="
        if (type(key)==str):
            command += '"' + key + '"'
        else:
            command += str(key)
        if (i!=len(keys)-1): command+=" AND"
        command += " "
    command += ";"
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    return result

def READ_CUSTOM(db_name:str, table:str, where_condition:str) -> list[Any]:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    command = "SELECT * FROM {0} ".format(table) + " " + where_condition + ";"
    cur.execute(command)
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

def DELETE_ROW_BY_KEYPOS(db_name:str, table:str, key_pos:int, key:Any) -> None:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    fields = GET_FIELDS(db_name, table)
    field_names = []
    for field in fields:
        field_names.append(field[0])
    if (len(field_names) <= key_pos): return
    command = "DELETE FROM {0} ".format(table) + "WHERE " + field_names[key_pos] + "="
    if (type(key)==str):
        command += '"' + key + '"'
    else:
        command += str(key)
    cur.execute(command)
    DB.commit()
    cur.close()

def DELETE_ROW_BY_KEY(db_name:str, table:str, key_name:str, key:Any) -> None:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    command = "DELETE FROM {0} ".format(table) + "WHERE " + key_name + "="
    if (type(key)==str):
        command += '"' + key + '"'
    else:
        command += str(key)
    command += ";"
    cur.execute(command)
    DB.commit()
    cur.close()

def DELETE_ROW_BY_KEYS(db_name:str, table:str, key_names:list[str], keys:list[Any]) -> None:
    global DB
    if len(key_names)!=len(keys): return
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    command = "DELETE FROM {0} ".format(table) + "WHERE "
    for i in range(len(keys)):
        key_name = key_names[i]
        key = keys[i]
        command += key_name + "="
        if (type(key)==str):
            command += '"' + key + '"'
        else:
            command += str(key)
        if (i!=len(keys)-1): command+=" AND"
        command += " "
    command += ";"
    cur.execute(command)
    DB.commit()
    cur.close()

def DELETE_ROW(db_name:str, table:str, row:list[Any]) -> None:
    global DB
    
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    fields = GET_FIELDS(db_name, table)
    if len(fields)!=len(row): return
    field_names = []
    for field in fields:
        field_names.append(field[0])
    command = "DELETE FROM {0} ".format(table) + "WHERE "
    for i in range(len(row)):
        key_name = field_names[i]
        key = row[i]
        command += key_name + "="
        if (type(key)==str):
            command += '"' + key + '"'
        else:
            command += str(key)
        if (i!=len(row)-1): command+=" AND"
        command += " "
    command += ";"
    cur.execute(command)
    DB.commit()
    cur.close()

def DELETE_CUSTOM(db_name:str, table:str, where_condition:str) -> None:
    global DB
    cur = DB.cursor()
    cur.execute("USE {0};".format(db_name))
    command = "DELETE FROM {0} ".format(table) + " " + where_condition + ";"
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

def EXEC(command: str, multi:bool = True) -> list[Any]:
    global DB
    cur = DB.cursor()
    cur.execute(command, multi= multi)
    result = cur.fetchall()
    DB.commit()
    cur.close()
    return result

def main():
    CONNECT(host, username, password)
    
    tables = GET_TABLES(db_name)
    for table in tables:
        print('\n'*2+"#"*30)
        print('* '+table, end=" *\n")
        rows = READ_BY_KEYS(db_name, table, ["age"], [55])
        #rows = READ_ALL(db_name, table)
        for row in rows:
            print('| ', end="")
            for x in row:
                print(x, end=" | ")
            print('\n'+'-'*30)
        print("#"*30+'\n')
    
    DISCONNECT()
    
    
if (__name__ == "__main__"):
    main()


