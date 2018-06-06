
# coding: utf-8
"""
用来整理并且连接items，price和comment，输出到jd_meizhuang_items里
原本是jupyter notebook里写的，pycharm可能看起来有点乱
"""
# In[1]:


items = []
with open('/Users/conghua/jd/items','r') as file:
    for line in file:
        items.append(line.strip().split(';'))
print(len(items))


# In[2]:


import demjson
for i in range(1,len(items)):
    try:
        if i % 1000 == 0:
            print(i)
        line = items[i]
        if "'店铺:  '," in line[12]:
            line[12] = line[12].replace("'店铺:  ',", '')
            if "<a href=" in line[12]:
                line[12] = line[12][:line[12].index("<a href=")]+line[12][line[12].index("</a>")+5:]
        tmp_list = demjson.decode(line[12])
        tmp_dict = {}
        for string in tmp_list:
            tmp_dict[string.split(': ')[0]] = string.split(': ')[1]
        line[12] = str(tmp_dict)
    except:
        print(line)


# In[16]:


comments = []
with open('/Users/conghua/jd/items_comment','r') as file:
    for line in file:
        comments.append(line.strip().split(';',6))
print(len(comments))


# In[17]:


for i in range(1, len(comments)):
    try:
        line = comments[i]
        if len(line)<7:
            line.append(str({}))
        else:
            tmp_dict = {}
            tmp_list = line[6].split(';')
            for i in range(0,len(tmp_list),2):
                tmp_dict[tmp_list[i]] = int(tmp_list[i+1])
            line[6] = str(tmp_dict)
    except:
        print(line,i)


# In[19]:


prices = []
with open('/Users/conghua/jd/items_price','r') as file:
    for line in file:
        prices.append(line.strip().split(';'))
print(len(prices))


# In[20]:


from collections import defaultdict
res = defaultdict(dict)
for line in items[1:]:
    for i in range(8,12):
        if not line[i]:
            line[i] = 'null'
    res[line[0]]['item'] = line


# In[21]:


for line in prices[1:]:
    if line[0] in res:
        res[line[0]]['price'] = line[1:]


# In[22]:


for line in comments[1:]:
    if line[0] in res:
        res[line[0]]['comments'] = line[1:]


# In[24]:


res_lst = []
for key in res:
    if 'price' not in res[key] or 'comments' not in res[key]:
        continue
    res_lst.append(res[key]['item'] + res[key]['price'] + res[key]['comments'])



# In[60]:


with open('/Users/conghua/jd/jd_meizhuang_items','a') as file:
    for line in res_lst:
        file.write(';'.join(line) + '\n')



