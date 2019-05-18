import requests
import json
import bs4

listS3 = [
    1101,
    1102,
    1216,
    1301,
    1303,
    1326,
    1402,
    2002,
    2105,
    2207,
    2301,
    2303,
    2308,
    2317,
    2327,
    2330,
    2357,
    2382,
    2395,
    2408,
    2409,
    2412,
    2454,
    2474,
    2633,
    2801,
    2880,
    2881,
    2882,
    2883,
    2884,
    2885,
    2886,
    2887,
    2890,
    2891,
    2892,
    2912,
    3008,
    3045,
    3481,
    3711,
    4904,
    4938,
    5971,
    5876,
    5880,
    6505,
    9904,
    1210,
    1227,
    1229,
    1319,
    1434,
    1476,
    1477,
    1504,
    1507,
    1536,
    1590,
    1605,
    1707,
    1722,
    1723,
    1789,
    1802,
    2027,
    2049,
    2059,
    2103,
    2104,
    2201,
    2204,
    2227,
    2231,
    2313,
    2324,
    2337,
    2345,
    2347,
    2352,
    2353,
    2354,
    2356,
    2360,
    2371,
    2376,
    2377,
    2379,
    2383,
    2385,
    2439,
    2441,
    2448,
    2449,
    2451,
    2458,
    2492,
    2498,
    2542,
    2603,
    2606,
    2610,
    2615,
    2723,
    2809,
    2812,
    2834,
    2845,
    2867,
    2888,
    2889,
    2915,
    3005,
    3034,
    3037,
    3044,
    3231,
    3406,
    3443,
    3532,
    3682,
    3702,
    3706,
    4958,
    5269,
    5522,
    5534,
    6116,
    6176,
    6269,
    6285,
    6409,
    6415,
    6456,
    8341,
    8454,
    8464,
    9910,
    9914,
    9917,
    9921,
    9933,
    9941,
    9945
]



# 抓取凱基權證網的網頁原始碼 (HTML)

url ="https://warrant.kgi.com/EDWebService/WSInterfaceSwap.asmx/GetService"
urlStock = "http://moneydj.emega.com.tw/js/T50_100.htm"

# 建立一個Request 物件，附加Request Headers 的資訊
header = {
    ''"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"''
}

data = {'Menukey': 'S0600013_GetWarrants',
 'ParametersOfJson': '{"NORMAL_OR_CATTLE_BEAR":0,"INSWRT_ISSUER_NAME":"凱基","STRIKE_FROM":-1,"STRIKE_TO":-1,"VOLUME":-1,"UND_INSTR_INSNBR":"10786","LAST_DAYS_FROM":"30","LAST_DAYS_TO":"180","IMP_VOL":"-1","CP":"認售","IN_OUT_PERCENT_FROM":-1,"IN_OUT_PERCENT_TO":-1,"BID_ASK_SPREAD_PERCENT":2,"LEVERAGE":"-1","EXECRATE":"-1","OUTSTANDING_PERCENT":"-1","BARRIER_DEAL_PERCENT":-1,"LocationPathName":"/EDWebSite/Views/WarrantSearch/WarrantSearch.aspx"}'
}
dicjson = []
def readParametersOfJsonObj(INSNBR):
    INSNBR = str(INSNBR)
    INSWRT_ISSUER_NAME = ["元大","凱基"]
    for NAME in INSWRT_ISSUER_NAME:
        ParametersOfJson = json.loads(data['ParametersOfJson'])
        ParametersOfJson["INSWRT_ISSUER_NAME"] = NAME
        ParametersOfJson["UND_INSTR_INSNBR"] = INSNBR
        data['ParametersOfJson']= ParametersOfJson
        data['ParametersOfJson'] = json.dumps(data['ParametersOfJson'],ensure_ascii=False)

        r = requests.post(url,headers=header, data = data)
        
        soup = bs4.BeautifulSoup(r.text,"xml")
        str1 = soup.ValueOfJson.string
       
        text = json.loads(str1)
        
        temp = 0
        
        for i in text:
            if(text[temp]["DEAL"] > 0.2 and text[temp]["VOLUME"] >= 1000):
                # OK_print(json.dumps([{'INSTR_NAME':text[temp]["INSTR_NAME"],'INSTR_STKID':text[temp]["INSTR_STKID"],'VOLUME':text[temp]["VOLUME"],'BID_ASK_SPREAD_PERCENT':text[temp]["BID_ASK_SPREAD_PERCENT"],'LAST_DAYS':text[temp]["LAST_DAYS"]}], ensure_ascii=False, indent=4, separators=(',', ': ')))
                dicjson.append(json.dumps({'INSTR_NAME':text[temp]["INSTR_NAME"],'INSTR_STKID':text[temp]["INSTR_STKID"],'VOLUME':text[temp]["VOLUME"],'BID_ASK_SPREAD_PERCENT':text[temp]["BID_ASK_SPREAD_PERCENT"],'LAST_DAYS':text[temp]["LAST_DAYS"]}, ensure_ascii=False, indent=4,separators=(',', ': ')))
                # with open("test.json",mode="a",encoding="utf-8") as file:
                #     file.writelines(json.dumps({'INSTR_NAME':text[temp]["INSTR_NAME"],'INSTR_STKID':text[temp]["INSTR_STKID"],'VOLUME':text[temp]["VOLUME"],'BID_ASK_SPREAD_PERCENT':text[temp]["BID_ASK_SPREAD_PERCENT"],'LAST_DAYS':text[temp]["LAST_DAYS"]}, ensure_ascii=False, indent=4)+",\n")  
                print("權證名稱：" +text[temp]["INSTR_NAME"] + "\t\t" + "權證代號：" +text[temp]["INSTR_STKID"] + "\t\t" + "成交價：%.2f" % text[temp]["DEAL"] + "\t\t" + "成交量：%d" % text[temp]["VOLUME"] + "\t\t" + "買賣價差比：%.2f" % text[temp]["BID_ASK_SPREAD_PERCENT"] + "\t\t" + "天數：%d" % text[temp]["LAST_DAYS"])
            temp += 1
    

with open("targetId.json",mode ="r",encoding ="utf-8") as file:
    PyList = json.load(file)
    for stock in listS3:
        stock = json.dumps(stock)
        try:
            readParametersOfJsonObj(PyList[stock]["INSTR_INSNBR"])
        except:
            continue

# print(json.dumps(dicjson, ensure_ascii=False, indent=4,separators=(',', ': ')))       
with open("test.json",mode="a",encoding="utf-8") as file:
    file.writelines(json.dumps(dicjson, ensure_ascii=False, indent=4,separators=(',', ': '))) 
