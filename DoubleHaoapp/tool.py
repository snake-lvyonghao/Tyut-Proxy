import json
from datetime import datetime


def get_course(data):
    start_date = datetime(2020, 2, 17)
    now_date = datetime.today()
    week = int(start_date.__rsub__(now_date).days / 7 + 1)
    result = {}
    for i in range(1, 8):
        result[str(i)] = {"1-2": [], "3-4": [], "5-6": [], "7-8": []}
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
        start = int(res[1][0]);
        end = int(res[1][2:].replace('周', ''));
        if start <= week <= end:
            result[str(res[-1])][res[-2]].append(res)
    return result
