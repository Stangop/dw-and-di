import psycopg2


drop_table_queries = [
    "DROP TABLE IF EXISTS events",
]
create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS staging_events (
        id text,
        type text,
        actor_id text,
        actor_login text,
        repo_id text,
        repo_name text,
        created_at text
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS events (
        id text,
        type text,
        actor_id text,
        actor_login text,
        repo_id text,
        repo_name text,
        created_at text
    )
    """,
]
copy_table_queries = [
    """
    COPY staging_events FROM 's3://stangds525/github_events_01.json'
    CREDENTIALS 'aws_iam_role=arn:aws:iam::891377209493:role/LabRole'
    JSON 's3://stangds525/github_events_01.json'
    REGION 'us-east-1'
    """,
]
insert_table_queries = [
    """
    INSERT INTO 
        events (
            id, 
            type, 
            actor_id, 
            actor_login, 
            repo_id, 
            repo_name, 
            created_at
        )

    SELECT
      DISTINCT id,
    FROM
      staging_events
    WHERE
      id NOT IN (SELECT DISTINCT id FROM events)
    """,
]


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    host = "redshift-cluster-st.cs9x9kh1y2jp.us-east-1.redshift.amazonaws.com"
    dbname = "dev"
    user = "awsuser"
    password = ""
    port = "5439"
    conn_str = f"host={host} dbname={dbname} user={user} password={password} port={port}"
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    # drop_tables(cur, conn)
    # create_tables(cur, conn)
    # load_tables(cur, conn)
    # insert_tables(cur, conn)

    query = "select * from category"
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        print(row)

    conn.close()


if __name__ == "__main__":
    main()