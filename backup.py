# MysqlBackup-Module-for-Python
# Version 1.0
# Coded By TheMirkin
# themirkin[at]hotmail.com
# http://www.themirkin.org
# https://github.com/TheMirkin
# 06.02.2023

import mysql.connector
import json

class Backup:
    def __init__(self, config_file='config.json'):
        with open(config_file) as f:
            self.config = json.load(f)

    def mysql(self):
        try:
            self.db = mysql.connector.connect(
                host=self.config['db']['host'],
                user=self.config['db']['user'],
                password=self.config['db']['pass'],
                database=self.config['db']['dbname'],
                charset='utf8'
            )
        except mysql.connector.Error as e:
            print("MySQL'e bağlanırken hata oluştu", e)

        cursor = self.db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        self.sql = ""
        
        for table in tables:
            table_name = table[0]
            cursor.execute("SELECT * FROM {}".format(table_name))
            rows = cursor.fetchall()
            self.sql += "-- Table Name: {}\n-- Row Count: {}\n\n".format(table_name, len(rows))
            
            cursor.execute("SHOW CREATE TABLE {}".format(table_name))
            table_detail = cursor.fetchone()
            self.sql += table_detail[1] + ";\n\n"
            
            if len(rows) > 0:
                cursor.execute("SHOW COLUMNS FROM {}".format(table_name))
                columns = cursor.fetchall()
                columns = [column[0] for column in columns]
                self.sql += "INSERT INTO `{}` (`{}`) VALUES\n".format(table_name, "`,`".join(columns))
                
                columns_data = []
                for row in rows:
                    row = ["'{}'".format(str(item)) for item in row]
                    columns_data.append("({})".format(", ".join(row)))
                self.sql += ",\n".join(columns_data) + ";\n\n"
        
        self.db.close()
        return open(self.config['db']['file'], "w").write(self.sql)


if __name__ == '__main__':
    backup = Backup()
    backup.mysql()
