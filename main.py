import requests
import pandas as pd
import json
import datetime as dt 
import math
import scipy.stats as stats

api = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjIwOTc0NzA1NDciLCJhdXRoX2lkIjoiMiIsImV4cCI6MTY4NzA2NjI4MiwiaWF0IjoxNjcxNTE0MjgyLCJuYmYiOjE2NzE1MTQyODIsInNlcnZpY2VfaWQiOiI0MzAwMTEzOTciLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.Oq2FtkLydQBlNAg3p8RXCTszi_SQ1HEvpNhZky9_XXk"
count = 1000
date = "2022-12-18"
cursor = ""
rv = stats.norm(0,1)
s = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
t = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
m = [1,3,3,2,3]
c = ["수상한 큐브","레드 큐브","블랙 큐브","장인의 큐브","명장의 큐브","수상한 큐브","레드 큐브","블랙 큐브","장인의 큐브","명장의 큐브"]
o = ["레어","에픽","유니크","레전드리","(미)에픽","(미)유니크","(미)레전드리"]
cp = [[0.9901,6,15,4.7619,7.9994],[0,1.8,3.5,1.1858,1.6959],[0,0.3,1.2,0,0.1996],[0.9901*2,6*2,15*2,4.7619*2,7.9994*2],[0*2,1.8*2,3.5*2,1.1858*2,1.6959*2],[0*2,0.3*2,1.2*2,0*2,0.1996*2]]
sdate = input()
fdate = input()
sdate = dt.datetime.strptime(sdate,"%Y%m%d")
fdate = dt.datetime.strptime(fdate,"%Y%m%d")
ddate = dt.timedelta(days=1)
headers = {'Authorization' : api}

while fdate>=sdate:
    date = sdate.strftime("%Y-%m-%d")
    url = f'https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results?count={count}&date={date}&cursor={cursor}'
    while True:
        res = requests.get(url,headers=headers)
        data = res.json()
        if "cube_histories" in data:
            break
    while True:
        if len(data) == 2 :
            break
        for i in range(0,data['count']):
            cube = data['cube_histories'][i]['cube_type']
            potential = data['cube_histories'][i]['before_potential_options'][0]['grade']
            ds = 0
            if data['cube_histories'][i]['item_upgrade_result'] == "성공":
                ds = 1
            dj = 0
            if data['cube_histories'][i]['miracle_time_flag'] != "이벤트 적용되지 않음":
                dj = 4
            for j in range(0,5):
                if cube == c[j]:
                    for k in range(0,m[j]):
                        if potential == o[k]:
                            t[k][j+dj]+=1
                            s[k][j+dj]+=ds
        if data['next_cursor'] == '':
            break
        else :
            date=""
            cursor=data['next_cursor']
            url = f'https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results?count={count}&date={date}&cursor={cursor}'
            res = requests.get(url,headers=headers)
            data = res.json()
    sdate+=ddate
result = 0
tsum = 0
for i in range(0,5):
    print(c[i])
    for j in range(0,6):
        if t[j][i] > 0 :
            print(o[j+1])
            fun=stats.norm(cp[j][i]*t[j][i]/100,(cp[j][i]*t[j][i]/100*(1-cp[j][i]/100))**(1/2))
            print(100-fun.cdf(s[j][i])*100)
            tsum += t[j][i]
            result += (100-fun.cdf(s[j][i])*100)*t[j][i]
print(result/tsum)