import psycopg2
import threading
import time
def action(txt):
    conn = psycopg2.connect(database="caspian", user="hugo", password="Hugo1234", host="47.96.127.162", port="5432")
    cur = conn.cursor()
    count = 1
    for line in txt:
        count += 1
        if count % 1000 == 0:
            conn.commit()
            print(count)
        line = line.strip().replace("'","''").split(';')
        cur.execute("INSERT INTO jd_meizhuang( \
            sku, category1, category2, category3, name, shopname, shoptype1, shoptype2, score1, \
            score2, score3, score4, detail, brand, originalprice, price, commentCount, goodCount, generalCount,\
            poorCount, afterCount, hotcomments) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, \
            %s, %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, '%s')"%
                    (line[0], line[1], line[2], line[3], line[4], line[5],
                       line[6], line[7], line[8], line[9], line[10], line[11],
                     line[12], line[13], line[14], line[15], line[16], line[17],
                     line[18], line[19], line[20], line[21]))
    conn.commit()
    cur.close()
    conn.close()
txt = []
while len(txt)<278200:
    with open('/Users/conghua/jd/jd_meizhuang_items', 'r') as file:
        txt = file.readlines()
    time.sleep(1)
thread_num = 10
for i in range(thread_num):
    t =threading.Thread(target=action,args=(txt[int(i*len(txt)/thread_num):int((i+1)*len(txt)/thread_num)],))
    t.start()