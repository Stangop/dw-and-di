# Building a Data Modeling with Cassandra (NoSQL)#
#Documentation
1.ทำการศึกษาความสัมพันธ์ของข้อมูล ใน json file 

2.สร้าง Data Model ด้วย Cassandra ซึ่งเป็น NoSQL Database ด้วยคำสั่ง

 pip install cqlsh

3.ทำการแก้ไข code etl.py file
 โดยดำเนินการ ดังนี้

    - ทำการ Drop Table ก่อนเพื่อป้องกันความผิดพลาดหากมีตารางอยู่แล้ว 
    - ทำการ create table โดยใช้คำสั่งดังนี้

    ```table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors
    (
        id text,
        login text,
        public boolean,
        PRIMARY KEY (
            id
        )
    )
    """

    table_create_repo = """
    CREATE TABLE IF NOT EXISTS repo
    (
        id text,
        type text,
        public boolean,
        PRIMARY KEY (
            id
        )
    )
    """
    table_create_events = """
    CREATE TABLE IF NOT EXISTS events
    (
        id text,
        type text,
        actor_id text,
        actor_login text,
        repo_id text,
        repo_name text,
        created_at timestamp,
        public boolean,
        PRIMARY KEY (
            id,
            type
        )
    )
    """
    ```

    จากคำสั่งข้างต้นจะเห็นได้ว่า
      public จะเก็บข้อมูลเป็น boolean เนื่องจากการเก็บข้อมูล public จะแสดงให้เห็นว่า events นี้เปิดให้ดูเป็น public หรือไ่ม่ 
      โดยจะสามารถ query เรียกดูแค่ข้อมูลได้ว่าหากเป็น true = public
 * ในการออกแบบนี้จะให้ id , type เป็น primary key และ created_at เป็น clustering key เพื่อเรียงลำดับข้อมูลภายใน partition ของคอลัมน์ id

    - จัดการข้อมูลที่ได้จากไฟล์ .json เข้าสู่ Table ใน Database
        ```query = f"""
                   INSERT INTO events (
                        id,
                        type,
                        actor_id,
                        actor_login,
                        repo_id,
                        repo_name,
                        created_at,
                        public) 
                    VALUES ('{each["id"]}', '{each["type"]}', 
                            '{each["actor"]["id"]}','{each["actor"]["login"]}',
                            '{each["repo"]["id"]}', '{each["repo"]["name"]}', 
                            '{each["created_at"]}',{each["public"]})
                """
                session.execute(query)
   

4. ทำการตรวจสอบข้อมูลใน Database ด้วยคำสั่ง cqlsh เพื่อเชื่อมต่อกับ Cassandra database เพื่อ Test Cluster
5. ทำการ Query และจัดการกับข้อมูลผ่าน CQL
   ```
   cqlsh> select * from github_events.events ;

ตารางแสดงผลดังภาพ

[Alt text](screenshot-event table.png)

6.ทำการออกจากคำสั่งก่อนหน้า
 cqlsh> exit 

 ## Instruction Data Modeling 2 ##
1. open file in folder 02-data-modeling-2  --> cd 02-data-modeling-2
2. link to connect with Cassandra -- > $ pip install cqlsh
3. link to connect with file docker -->$  docker compose up 
4. open ports 9042 --> click ports --> open browser 9042 
5. load data in etl.py to Cassandra -->$  python etl.py 
6. Connected to Test Cluster -->$  cqlsh
7. run code to connect data --> cqlsh> select * from github_events.events ; 
8. exit from Test Cluster -- > cqlsh> exit
