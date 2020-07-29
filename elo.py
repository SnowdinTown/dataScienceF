import json
import Core

# 预设值
USER_FILE = 'user.json'
CASE_FILE = 'total_cases.json'
CASE_TYPES = ['字符串', '线性表', '数组', '查找算法', '排序算法', '数字操作', '树结构', '图结构']
WEIGHT = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]
WEIGHT2 = [1.0, 0.7, 0.5, 0.3, 0]
EXTEND_NUM = 0.1
HIDE_NUM = 0.1   # 隐藏分系数


def getUserData():
    f = open(USER_FILE, encoding='utf-8')
    return json.loads(f.read())


def getCaseData():
    f = open(CASE_FILE, encoding='utf-8')
    return json.loads(f.read())


def record_model(case_id, case_type, case_rank, user_rank, record_type, start, score, final, times, change, is_pass):
    return {
        "case_id": case_id,
        "case_type": case_type,
        "case_rank": case_rank,
        "user_rank": user_rank,
        "record_type": record_type,
        "start_time": start,
        "final_score": score,
        "final_time": final,
        "test_times": times,
        "rank_change": change,
        "pass": is_pass
    }


def process_rank(user, case_type, case_id, score, start, end, times):
    cases = getCaseData()
    case = list(filter(lambda x: x['case_id'] == case_id, cases[case_type]))[0]
    type_info = user['type_info'][case_type]
    
    is_pass = computeS(score, start, end) >= 0.8
    rank_change = process_method(user, case, score, start, end)
    if is_pass:
        rank_change += type_info['hide_score']
        type_info['hide_score'] = 0
    
    type_info['rank'] += rank_change
    if type_info['rank'] < 0:
        type_info['rank'] = 0
    rank_change_adjust = rank_change * (case['difficulty'] + EXTEND_NUM) * 0.5   # 考虑难度分布，使难度分布中心趋近0.5
    user['rank_score'] += rank_change_adjust
    if user['rank_score'] < 0:
        user['rank_score'] = 0
    
    record = record_model(case_id, case_type, case['rank_score'], type_info['rank'], 'rank', start, score, end, times, rank_change_adjust, is_pass)
    updateUser(user, record)


def process_exercise(user, case_type, case_id, score, start, end, times):
    cases = getCaseData()
    case = list(filter(lambda x: x['case_id'] == case_id, cases[case_type]))[0]
    type_info = user['type_info'][case_type]

    is_pass = score == 100
    rank_change = process_method(user, case, score, start, end)
    
    type_info['hide_score'] += rank_change * HIDE_NUM * (case['difficulty'] + EXTEND_NUM) * 0.5    # 隐藏分系数
    if type_info['hide_score'] < 0:
        type_info['hide_score'] = 0
    if type_info['hide_score'] > 30:
        type_info['hide_score'] = 30

    record = record_model(case_id, case_type, case['rank_score'], type_info['rank'], 'exercise', start, score, end, times, 0, is_pass)
    updateUser(user, record)


# 计算用户rank分数变动
def process_method(user, case, score, start, end):
    type_pass_rate = user['type_info'][case['case_type']]['offset']
    if type_pass_rate == 0:
        type_pass_rate = 1
    return getrankChange(user['type_info'][case['case_type']]['rank'], case['rank_score'], computeS(score, start, end), computeK(type_pass_rate))


def getrankChange(user_rank, case_rank, S, K):
    E = 1 / (1 + pow(10, (case_rank - user_rank) / 400))
    return K * (S - E)


def computeS(score, start, end):
    time = end - start
    idx1 = int(time / (1000 * 60 * 60))
    if score == 100:
        idx2 = 0
    elif score >= 80:
        idx2 = 1
    elif score >= 60:
        idx2 = 2
    elif score >= 40:
        idx2 = 3
    else:
        idx2 = 4
    return WEIGHT2[idx2] * WEIGHT[idx1]


def computeK(value):
    percent = value
    if percent >= 0.75:
        return 60
    elif percent >= 0.50:
        return 35
    else:
        return 15


def updateUser(user, record):
    user['records'].append(record)
    
    records = user['records']
    type_records = list(filter(lambda x: x['case_type'] == record['case_type'], records))
    
    rank_records = list(filter(lambda x: x['record_type'] == 'rank', type_records))
    exc_records = list(filter(lambda x: x['record_type'] == 'exercise', type_records))
    rank_pass_records = list(filter(lambda x: x['pass'], rank_records))
    exc_pass_records = list(filter(lambda x: x['pass'], exc_records))

    pass_rate = ((len(rank_pass_records) / len(rank_records)) if len(rank_records) != 0 else 1) * 0.7 + \
                 ((len(exc_pass_records) / len(exc_records)) if len(exc_records) != 0 else 1) * 0.3
    
    user['type_info'][record['case_type']]['offset'] = pass_rate
    data = Core.getData('user.json')
    data[user['user_name']] = user
    Core.outputJSONFile('user.json', data)

if __name__ == '__main__':
    uses = getUserData()
    process_exercise(uses['snow'], '树结构', '2698', 100, 0, 60 * 60 * 1000 - 1, 3)
