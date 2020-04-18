import json


def get_course(data):
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
            break
        result[str(res[-1])][res[-2]].append(res)
    return result
