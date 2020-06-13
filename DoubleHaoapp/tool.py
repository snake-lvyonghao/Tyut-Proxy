import json
import re
from datetime import datetime


def get_course(data, week=None):
    start_date = datetime(2020, 2, 17)
    now_date = datetime.today()
    # 初始化课程表
    result = {}
    if week is None:
        week = int(start_date.__rsub__(now_date).days / 7 + 1)
        result['week'] = []
        for i in range(1, 19):
            result['week'].append(0)
        result['week'][week - 1] = 1
    week = week - 1

    for i in range(1, 8):
        result[str(i)] = {}
    x = json.loads(data)


    def course_detail(kcb):
        result = []
        result.append(kcb["Kcm"])
        result.append(kcb["Zcsm"])
        result.append(kcb["Dd"])
        result.append(kcb['Jsm'])
        result.append(kcb["Jc"])
        result.append(kcb['Skxq'])
        return result

    for i in x["rows"]:
        res = course_detail(i)
        if res[-1] == 0 or res[-1] == '':
            continue
        weeks = re.findall(r"\d+\.?\d*", res[1])
        if len(weeks) <= 1:
            start = int(weeks[0])
            end = int(weeks[0])
            if start <= week + 1 <= end:
                result[str(res[-1])][res[-2]] = res
        else:
            for i in range(0, len(weeks), 2):
                start = int(weeks[i])
                end = int(weeks[i + 1])
                if start <= week + 1 <= end:
                    result[str(res[-1])][res[-2]] = res
    return result

def get_kssj(data):
    print(data)
    result = []

    # 初始数据转化为json格式
    x = json.loads(data)

    def course_detail(kssj):
        res = []
        result = {}
        result['Zxjxjhm1'] = kssj["Zxjxjhm1"]
        result['Bmkcm'] = kssj["Bmkcm"]
        result['Kssj'] = kssj["Kssj"]
        result['Ksrq'] = kssj["Ksrq"]
        result['Ksdd'] = kssj["Ksdd"]
        res.append(result)
        return res

    for i in x["rows"]:
        res = course_detail(i)
        result.append(res)

    return result