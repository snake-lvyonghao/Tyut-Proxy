import json
import re
import string
from datetime import datetime


def get_course(data, week=None):
    start_date = datetime(2020, 2, 17)
    now_date = datetime.today()
    if week is None:
        week = int(start_date.__rsub__(now_date).days / 7 + 1)
    week = week - 1
    # 初始化课程表
    result = {}

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
        if res[-1] == 0:
            continue
        weeks = re.findall(r"\d+\.?\d*",res[1])
        for i in range(0,len(weeks),2):
            start = int(weeks[i])
            end = int(weeks[i + 1])
            print(start,end)
            if start <= week + 1 <= end:
                result[str(res[-1])][res[-2]] = res
    return result
