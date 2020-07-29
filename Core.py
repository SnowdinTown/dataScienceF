import json
import numpy as np
from matplotlib import pyplot as plt



def getData(file_path):
    f = open(file_path, encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    return data


def getCases(data):
    cases = []
    for user_key in data:
        for case_key in data[user_key]['cases']:
            temp_id = case_key['case_id']
            if len(cases) == 0:
                temp = {}
                temp['case_id'] = case_key['case_id']
                temp['case_type'] = case_key['case_type']
                temp['case_zip'] = case_key['case_zip']
                cases.append(temp)
            else:
                flag = True
                for case in cases:
                    if case['case_id'] == temp_id:
                        flag = False
                        break
                if flag:
                    temp = {}
                    temp['case_id'] = case_key['case_id']
                    temp['case_type'] = case_key['case_type']
                    temp['case_zip'] = case_key['case_zip']
                    cases.append(temp)
    print('题目总数: {}'.format(len(cases)))
    cases.sort(key=lambda x: int(x['case_id']))
    return cases


def outputJSONFile(file, data):
    filename = file
    with open(filename, 'w') as file_obj:
        json.dump(data, file_obj)


def sortStudent():
    data = getData('test_data.json')
    res = []
    for student in data:
        temp = {}
        count = 0
        cases = data[str(student)]['cases']
        for case in cases:
            if case['final_score'] == 100:
                count += 1
        temp['user_id'] = data[str(student)]['user_id']
        temp['pass_num'] = count
        res.append(temp)
    res.sort(key=lambda x: x['pass_num'], reverse=True)
    full = 0
    for i in res:
        if i['pass_num'] >= 200:
            full += 1
        print('{}: {}'.format(i['user_id'], i['pass_num']))
    print('全对人数：{}'.format(full))
    print('总人数：{}'.format(len(res)))
    return res


def findStudentCases(user_id):
    data = getData('test_data.json')
    user = data[user_id]
    cases = user['cases']
    caseNO = []
    for case in cases:
        if int(case['case_id']) not in caseNO:
            caseNO.append(int(case['case_id']))
    caseNO.sort()
    return caseNO


def outputCases_group():
    data = getData('student_pass.json')
    temp = []
    for student in data:
        if student['pass_num'] > 200:
            continue
        elif 195 <= student['pass_num'] <= 200:
            cases = findStudentCases(str(student['user_id']))
            if len(temp) == 0:
                temp.append(cases)
            else:
                sign = False
                for i in temp:
                    flag = True
                    for j in cases:
                        if j not in i:
                            flag = False
                            break
                    sign = sign or flag
                if not sign:
                    temp.append(cases)
        else:
            break
    outputJSONFile('cases_group.json', temp)


def outputCase_repeat():
    data = getData('casesNO.json')
    group = getData('cases_group.json')
    cases = []
    for i in data:
        temp = {}
        count = 0
        for j in group:
            if i in j:
                count += 1
        temp['case_id'] = i
        temp['repeat'] = count
        cases.append(temp)
    outputJSONFile('case_repeat.json', cases)
    for i in cases:
        print('{}: {}'.format(i['case_id'], i['repeat']))


def findData(data, id):
    left = 0
    right = len(data)-1
    while left < right:
        mid = (left + right) >> 1
        if data[mid] >= id:
            right = mid
        else:
            left = mid + 1
    return left


def outputCAse_average_difficulty():
    casesNO = getData('casesNO.json')
    repeat = getData('case_repeat.json')
    res = []
    for i in range(len(casesNO)):
        temp = {'case_id': casesNO[i], 'sum': 0, 'repeat': repeat[i]['repeat'], 'average': 0, 'count': 0,
                'difficulty': 0}
        res.append(temp)

    data = getData('test_data.json')
    for student in data.values():
        cases = student['cases']
        for case in cases:
            idx = findData(casesNO, int(case['case_id']))
            res[idx]['sum'] += case['final_score']
            res[idx]['count'] += 1

    for i in range(len(res)):
        if res[i]['count'] > res[i]['repeat'] * 55:
            res[i]['average'] = res[i]['sum'] / res[i]['count']
        else:
            res[i]['average'] = res[i]['sum'] / (res[i]['repeat'] * 55)
        res[i]['difficulty'] = 1 - res[i]['average'] / 100

    res.sort(key=lambda x: x['average'], reverse=True)

    for i in range(len(res)):
        print('case: {}\taverage: {}\tsum: {}\trepeat: {}\tcount: {}\tdifficulty: {}'.
              format(res[i]['case_id'], res[i]['average'], res[i]['sum'], res[i]['repeat'], res[i]['count'],
                     res[i]['difficulty']))


def drawDifficulty():
    data = getData('case_average&difficulty.json')
    x_list = []
    y_list = []
    for i in range(20):
        x_list.append(i * 0.05)
        y_list.append(0)

    for i in range(len(data)):
        diff = data[i]['difficulty']
        for j in range(len(x_list)):
            if j == 0:
                if diff <= x_list[j]:
                    y_list[j] += 1
            else:
                if x_list[j - 1] < diff <= x_list[j]:
                    y_list[j] += 1
    print(x_list)
    print(y_list)
    plt.scatter(x_list, y_list, s=10)
    plt.title("Matplotlib demo")
    plt.xlabel("difficulty")
    plt.ylabel("case_num")
    plt.show()


def draw_case_average_time():
    data = getData('test_data.json')
    caseNo = getData('casesNO.json')
    case_data = getData('case_average&difficulty.json')
    res = []
    for i in range(len(caseNo)):
        temp = {'case_id': caseNo[i], 'case_difficulty': case_data[i]['difficulty'],
                'count': case_data[i]['count'], 'case_totalTime': 0, 'case_averageTime': 0}
        res.append(temp)
    for student in data.values():
        cases = student['cases']
        for case in cases:
            case_id = int(case['case_id'])
            idx = findData(caseNo, case_id)
            upload_records = case['upload_records']
            if len(upload_records) > 0:
                time = (upload_records[len(upload_records) - 1]['upload_time'] - upload_records[0][
                    'upload_time']) / 60000
                if time <= 10 * 60:
                    res[idx]['case_totalTime'] += time
                else:
                    res[idx]['count'] -= 1
    for i in range(len(res)):
        res[i]['case_averageTime'] = res[i]['case_totalTime'] / res[i]['count']
    res.sort(key=lambda x: x['case_difficulty'])
    for i in res:
        print('case_id: {}\tcase_difficulty: {}\tcase_averageTime: {}min\tcase_totalTime: {}\tcount: {}'.format(
            i['case_id'], i['case_difficulty'], i['case_averageTime'], i['case_totalTime'], i['count']
        ))

    x = []
    y1 = []
    y2 = []
    for i in range(len(caseNo)):
        x.append(i + 1)
        y1.append(res[i]['case_difficulty'] * 50)
        y2.append(res[i]['case_averageTime'])
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()


def outputType_cases():
    data = getData('TotalCases.json')
    caseType = ['字符串', '线性表', '数组', '查找算法', '数字操作', '树结构', '图结构', '排序算法']
    typeCases = {}
    for i in caseType:
        typeCases[i] = []
    for case in data:
        for i in caseType:
            if case['case_type'] == i:
                typeCases[i].append(case)
    outputJSONFile('type_cases.json', typeCases)
    for i in caseType:
        print(i)
        for j in typeCases[i]:
            print(j)


def output_type_case_difficulty():
    typeCases = getData('type_cases.json')
    data = getData('case_average&difficulty.json')
    caseType = ['字符串', '线性表', '数组', '查找算法', '数字操作', '树结构', '图结构', '排序算法']
    for i in caseType:
        for j in typeCases[i]:
            idx = findData(getData('casesNO.json'), int(j['case_id']))
            diff = data[idx]['difficulty']
            j['difficulty'] = diff
    outputJSONFile('type_cases.json', typeCases)
    for i in caseType:
        typeCases[i].sort(key=lambda x: x['difficulty'])
    for i in caseType:
        print(i)
        sum_diff = 0
        for j in typeCases[i]:
            print(j)
            sum_diff += j['difficulty']
        print('总题数: {}'.format(len(typeCases[i])))
        average = sum_diff / len(typeCases[i])
        print('平均难度: {}'.format(average))


def draw_rank_zone():
    caseType = ['字符串', '线性表', '数组', '查找算法', '数字操作', '树结构', '图结构', '排序算法']
    data = getData('type_cases.json')
    x = []
    y = []
    for i in range(20):
        x.append((i + 1))
        y.append(0)
    for j in caseType:
        for i in data[j]:
            score = i['rank_score']
            idx = int(score / 100) + 1
            y[idx] += 1
        print('{}: {}'.format(j, len(data[j])))
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.bar(x=x, height=y, label='rank_case_num', color='steelblue', alpha=0.8)
        for x1, yy in zip(x, y):
            plt.text(x1, yy + 1, str(yy), ha='center', va='bottom', fontsize=20, rotation=0)
        # 设置标题
        plt.title("{}_rank_分布".format(j))
        # 为两条坐标轴设置名称
        plt.xlabel("分数段")
        plt.ylabel("数量")
        # 显示图例
        plt.legend()
        plt.savefig('{}.jpg'.format(j))
        plt.show()
        x = []
        y = []
        for i in range(20):
            x.append((i + 1))
            y.append(0)


def draw_rank_distribution():
    data = getData('case_average&difficulty.json')
    data.sort(key=lambda x: x['difficulty'])
    x = []
    y = []
    for i in data:
        i['rank'] = i['difficulty'] * 2000
    for i in range(150):
        x.append(i)
        y.append(0)
    for j in data:
        idx = int(j['rank'] / 10)
        y[idx] += 1
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(x=x, height=y, label='rank_case_num', color='steelblue', alpha=0.8)
    for x1, yy in zip(x, y):
        plt.text(x1, yy + 1, str(yy), ha='center', va='bottom', fontsize=10, rotation=0)
    # 设置标题
    plt.title("rank_分布")
    # 为两条坐标轴设置名称
    plt.xlabel("分数段")
    plt.ylabel("数量")
    # 显示图例
    plt.legend()
    plt.show()


if __name__ == '__main__':
    pass
