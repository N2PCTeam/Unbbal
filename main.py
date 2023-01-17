import requests
import pandas as pd
import json
import datetime as dt 
import math
import scipy.stats as stats

api = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjIwOTc0NzA1NDciLCJhdXRoX2lkIjoiMiIsImV4cCI6MTY4NzA2NjI4MiwiaWF0IjoxNjcxNTE0MjgyLCJuYmYiOjE2NzE1MTQyODIsInNlcnZpY2VfaWQiOiI0MzAwMTEzOTciLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.Oq2FtkLydQBlNAg3p8RXCTszi_SQ1HEvpNhZky9_XXk2"
count = 1000
date = "2022-12-18"
cursor = ""
rv = stats.norm(0,1)
s = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
t = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
m = [1,3,3,2,3]
c = ["수상한 큐브","레드 큐브","블랙 큐브","장인의 큐브","명장의 큐브","수상한 큐브","레드 큐브","블랙 큐브","장인의 큐브","명장의 큐브"]
o = ["레어","에픽","유니크","레전드리","(미)에픽","(미)유니크","(미)레전드리"]
e = ["무기","엠블렘","보조무기", "포스실드","소울링","방패","모자","상의","한벌옷","하의","신발","장갑","망토","벨트","어깨장식","얼굴장식","눈장식","귀고리","반지","펜던트","기계심장"]
u = ["보스","방어율","공격력","마력","STR","DEX","INT","LUK","올스탯","모든 스킬의","크리티컬 데미지"]
#       0      1       2        3     4      5    6     7      8       9             10
eu = [[[0,1,2],[1,2],[0,1,2],[0,1,2],[0,1,2],[0,1,2],[4,8,9],[4,8],[4,8],[4,8],[4,8],[4,8,10],[4,8],[4,8],[4,8],[4,8],[4,8],[4,8],[4,8],[4,8],[4,8]],
[[0,1,2],[1,2],[0,1,2],[0,1,2],[0,1,2],[0,1,2],[5,8,9],[5,8],[5,8],[5,8],[5,8],[5,8,10],[5,8],[5,8],[5,8],[5,8],[5,8],[5,8],[5,8],[5,8],[5,8]],
[[0,1,2],[1,2],[0,1,2],[0,1,2],[0,1,2],[0,1,2],[7,8,9],[7,8],[7,8],[7,8],[7,8],[7,8,10],[7,8],[7,8],[7,8],[7,8],[7,8],[7,8],[7,8],[7,8],[7,8]],
[[0,1,3],[1,3],[0,1,3],[0,1,3],[0,1,3],[0,1,3],[6,8,9],[6,8],[6,8],[6,8],[6,8],[6,8,10],[6,8],[6,8],[6,8],[6,8],[6,8],[6,8],[6,8],[6,8],[6,8]]]
ep = [[1.2090,0.3238,0.6637,0.6637,0.6637,0.1593,0.6551,0.2922,0.2922,0.4711,0.4333,0.5382,0.5725,0.5725,0.5725,0.6658,0.6658,0.6658,0.6658,0.6658,0.9556],[1.2680,0.3266,0.6637,0.6637,0.6637,0.1593,0.6551,0.2922,0.2922,0.4711,0.4333,0.5382,0.5725,0.5725,0.5725,0.6658,0.6658,0.6658,0.6658,0.6658,0.9556]]
es = [[0 for i in range(len(e))],[0 for i in range(len(e))]]
et = [[0 for i in range(len(e))],[0 for i in range(len(e))]]
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
            dj = 0
            if data['cube_histories'][i]['item_upgrade_result'] == "성공":
                ds = 1
            if data['cube_histories'][i]['miracle_time_flag'] != "이벤트 적용되지 않음":
                dj = 3
            for j in range(0,5):
                if cube == c[j]:
                    for k in range(0,m[j]):
                        if potential == o[k]:
                            t[k+dj][j]+=1
                            s[k+dj][j]+=ds
            for k in range(0,2):
                if cube == c[k+1] and data['cube_histories'][i]['potential_option_grade'] == o[3]:
                    for j in range(0,len(e)):
                        if data['cube_histories'][i]['item_equip_part'] == e[j] :
                            et[k][j] += 1
                            item = data['cube_histories'][i]['target_item']
                            job = 0
                            if item.find("워리어") >= 0 or item.find("나이트") >= 0:
                                job = 0
                            if item.find("레인져") >= 0 or item.find("아처") >= 0 :
                                job = 1
                            if item.find("어새신") >= 0 or item.find("시프") >= 0 :
                                job = 2
                            if item.find("던위치") >= 0 or item.find("메이지") >= 0 :
                                job = 3
                            af_po = data['cube_histories'][i]['after_potential_options']
                            for l in range(0,len(af_po)):
                                escape = 1
                                for x in range(0,len(eu[job][j])):
                                    if af_po[l]['value'].find(u[eu[job][j][x]]) == 0 :
                                        escape = 0
                                        break
                                if escape : break
                                if l == 2 :
                                    es[k][j] += 1
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
result2 = 0
sum = 0
for i in range(0,1):
    for j in range(0,len(e)):
        if et[i][j] > 0:
            sum+=et[i][j]
            fun=stats.norm(ep[i][j]*et[i][j]/100,(ep[i][j]*et[i][j]/100*(1-ep[i][j]/100))**(1/2))
            result2 += (100-fun.cdf(es[i][j])*100)*et[i][j]
            #print(100-fun.cdf(es[i][j])*100)
if tsum > 0 : print(result/tsum)
if sum > 0 : print(result2/sum)