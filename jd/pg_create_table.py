import psycopg2
conn = psycopg2.connect(database="caspian", user="hugo", password="Hugo1234", host="47.96.127.162", port="5432")
cur = conn.cursor()
cur.execute("""
CREATE TABLE jd_meizhuang(
            sku varchar(11) primary key,
            category1 varchar(4),
            category2 varchar(7),
            category3 varchar(9),
            name varchar(100),
            shopname varchar(35),
            shoptype1 varchar(3),
            shoptype2 varchar(3),
            score1 numeric(6,2),
            score2 numeric(6,2),
            score3 numeric(6,2),
            score4 numeric(6,2),
            detail varchar(500),
            brand varchar(50),
            originalprice numeric(10,2),
            price numeric(10,2),
            commentCount int,
            goodCount int,
            generalCount int,
            poorCount int,
            afterCount int,
            hotcomments varchar(200)
            );""")
conn.commit()
cur.close()
conn.close()