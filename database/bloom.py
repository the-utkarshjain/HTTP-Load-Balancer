import sqlite3

conn = sqlite3.connect('test.db')

conn.execute('''DROP TABLE IF EXISTS USERS;''')
conn.execute('''CREATE TABLE USERS (email CHAR(500) PRIMARY KEY NOT NULL, password  CHAR(100) NOT NULL);''')

emails = ["akzelxw@hotmail.com","elum@gmail.com","akbar.ca","akaterasu@gmail.com","akarui.kibuno@gmail.com","ajsparkchick@hotmail.com","ajmeia@yahoo.com","ajhnstn87@gmail.com","ailuvzhoko4@hotmail.com","ailuvzhoko3@hotmail.com","ailuvzhoko2@hotmail.com","ailuvzhoko@hotmail.com","aillensiquioco@aol.com","ahmovic_ines@hotmail.com","ahmed_g300@yahoo.com","ahmadjazlan@gmail.com","ahmad_ridho19@yahoo.com","ahgou_9@hotmail.com","ahan221@yahoo.com","agungarifiyanto@yahoo.com","agnestenerife@yahoo.com","agian_ee@yahoo.com","afrodzac007@aol.com","affinboy@hotmail.com","afdal_hair1303@yahoo.com","afd1944@gmail.com","afandi.ilham@yahoo.com","aerongreg@yahoo.com","adria@jbi.com","ado97_madero@hotmail.com","aditye55@yahoo.com","adhie.impossible@gmail.com","adeeldaftary@gmail.com","adam_petre@hotmail.com","adam_khaldoon911@yahoo.com","ium@yahoo.com"]
for email in emails:
    password = email.split("@")[0]
    conn.execute("INSERT INTO USERS (email,password) VALUES ('" + email + "', '" + password + "')")

conn.commit()
conn.close()