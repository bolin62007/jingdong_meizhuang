import oss2
from itertools import islice
def upload_oss():
    endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
    auth1 = open('/Users/conghua/gaode/config.yml').readlines()[1][7:]
    auth2 = open('/Users/conghua/gaode/config.yml').readlines()[2][7:]
    auth = oss2.Auth(auth1, auth2)
    bucket = oss2.Bucket(auth, endpoint, 'caspian')

    file_name = '/Users/conghua/gaode/pois/poi'
    # bucket.delete_object('gaode_pois2') #删除

    # for b in islice(oss2.ObjectIterator(bucket), 10): #查询
    #     print(b.key)
    # with open('/Users/conghua/jd/jd_meizhuang_items', 'rb') as f:
    #     bucket.put_object('jd_meizhuang_items', f)
    # bucket.get_object_to_file('gaode_pois', '/Users/conghua/gaode/pois/poi') #下载
if __name__=="__main__":
    upload_oss()