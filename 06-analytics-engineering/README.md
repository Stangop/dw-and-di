# Analytics Engineering

Create a dbt project

```sh
dbt init
```

Edit the dbt profiles

```sh
code ~/.dbt/profiles.yml
```

```yml
jaffle:
  outputs:

    dev:
      type: postgres
      threads: 1
      host: localhost
      port: 5432
      user: postgres
      pass: postgres
      dbname: postgres
      schema: public

    prod:
      type: postgres
      threads: 1
      host: localhost
      port: 5432
      user: postgres
      pass: postgres
      dbname: postgres
      schema: prod

  target: dev
```

Test dbt connection

```sh
cd jaffle
dbt debug 
```

You should see "All checks passed!".

To create models

```sh
dbt run
```

To test models

```sh
dbt test
```

To view docs (on Gitpod)

```sh
dbt docs generate
dbt docs serve
```

# Analytics Engineer using dbt

## สร้าง virtual environment โดยใช้คำสั่ง
```sh
python -m venv ENV
```
```
# ทำการ activate ENV
```sh
source ENV/bin/activate
```

## ทำการติดตั้ง packages จาก requirement.txt
```sh
pip install -r requirement.txt 
```

## ทำการสร้าง DBT Project (initiate project)
```sh
pip install dbt-core dbt postgres
```
```

```sh
dbt init
```
### Setup project
```
name project -ds525
```

> ทำการ setup profile เป็นส่วนที่ใช้เก็บข้อมูล ที่จะนำไป connect กับ data warehouse

```
code | profile directory
```
> ทำการสร้าง profile.yml เพื่อเก็บข้อมูลทั้งหมดที่เราสร้างไว้

## ทำการตรวจสอบว่าตัว connection ที่เราสร้างใช้งานใน postgres ได้โดยใช้คำสั่ง
```
dbt debug
```
All checks passed! หมายถึง สามารถใช้งานได้แล้ว

## ทำการ read models โดยผลลัพธ์จะแสดงในหน้าเว็บ

- สร้าง model 

> run automate test
```
dbt test
```

- สร้าง layer โดย source จะ link กับ staging แบบ 1:1 
> staging
create model in staging

> marts

- materization
> by staging and marts

# Documentation

- Create init.sql file to create table and insert data 
```
CREATE TABLE IF NOT EXISTS jaffle_shop_customers (
    id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
);

INSERT INTO jaffle_shop_customers (
    id,
    first_name,
    last_name
)
VALUES
    (1, 'Michael', 'P.'),
    (2, 'Shawn', 'M.'),
    (3, 'Kathleen', 'P.'),
    (4, 'Jimmy', 'C.'),
    (5, 'Katherine', 'R.'),
```

- Create file .sql to contain SQL script to run on dbt

ใน staging folder จะเก็บข้อมูลที่เตรียมไว้สำหรับใช้ใน staging layer 
ซึ่งจะถูกนำไป extract transform และ load ใน data warehouse 

- ประโยชน์ของ dbt

- ใน dbt สามารถใช้ client SQL เพื่อ query ได้

- สามารถทำ script ให้ SQL ทำซ้ำได้

- ตัวอย่างการสร้าง staging sql script 
```
select * from {{ source('jaffle_shop', 'jaffle_shop_customers') }}
```
- การสร้าง sql script ใน data mart 
```
select
    o.id as order_id
    , o.user_id
    , c.first_name
    , c.last_name
    , o.order_date
    , o.status as order_status

from {{ ref('stg__jaffle_shop_orders') }} as o
join {{ ref('stg__jaffle_shop_customers') }} as c
on o.user_id = c.id
```