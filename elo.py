import json
import Core

# 预设值
USER_FILE = 'user.json'
CASE_FILE = 'TotalCases.json'
CASE_TYPES = ['字符串', '线性表', '数组', '查找算法', '排序算法', '数字操作', '树结构', '图结构']
WEIGHT = [1.1, 1.0, 0.9, 0.8, 0.7, 0.6]


def getUserData():
    f = open(USER_FILE, encoding='utf-8')
    return json.loads(f.read())


def getCaseData():
    f = open(CASE_FILE, encoding='utf-8')
    return json.loads(f.read())


def record_model(case_id, case_type, record_type, start, score, final, times, change, is_pass):
    return {
        "case_id": case_id,
        "case_type": case_type,
        "record_type": record_type,
        "start_time": start,
        "final_score": score,
        "final_time": final,
        "test_times": times,
        "rank_change": change,
        "pass": is_pass
    }


# 计算用户rank分数变动以及保存记录
def process_method(user, case_id, score, start, end, times, type):
    # 获取题目信息
    cases = getCaseData()
    case = list(filter(lambda x: x['case_id'] == case_id, cases))[0]

    records = user['records']

    if type == 'rank':
        user['rank_num'] += 1
    else:
        user['ecx_num'] += 1

    record = record_model(case_id, case['case_type'], 'rank' if type == 'rank' else 'exercise', start, score, end,
                          times, 0, 0)

    user['records'].append(record)

    if type == 'rank':
        time = end - start
        idx = int(time / (1000 * 60 * 60))
        s = score / 100 * WEIGHT[idx]
    else:
        s = score / 100 * WEIGHT[len(WEIGHT) - 1]

    is_pass = False
    if s > 0.8:
        is_pass = True

    user['records'][len(user['records']) - 1]['pass'] = is_pass

    type_records = list(filter(lambda x: x['case_type'] == case['case_type'], records))
    rank_type_records = list(filter(lambda x: x['record_type'] == 'rank', type_records))
    exc_type_records = list(filter(lambda x: x['record_type'] == 'exc', type_records))
    pass_records = list(filter(lambda x: x['pass'] == True, records))
    rank_pass_records = list(filter(lambda x: x['record_type'] == 'rank', pass_records))
    exc_pass_records = list(filter(lambda x: x['record_type'] == 'exercise', pass_records))
    type_pass_records = list(filter(lambda x: x['case_type'] == case['case_type'], pass_records))
    rank_type_pass_records = list(filter(lambda x: x['record_type'] == 'rank', type_pass_records))
    exc_type_pass_records = list(filter(lambda x: x['record_type'] == 'exercise', type_pass_records))

    user_rank = user['rank_score']

    all_value = ((len(rank_pass_records) / user['rank_num']) if user['rank_num'] != 0 else 1) * 0.7 + \
                ((len(exc_pass_records) / user['exc_num']) if user['exc_num'] != 0 else 1) * 0.3
    all_K = compute_k(all_value)

    type_value = ((len(rank_type_pass_records) / len(rank_type_records)) if len(rank_type_records) != 0 else 1) * 0.7 + \
                 ((len(exc_type_pass_records) / len(exc_type_records)) if len(exc_type_records) != 0 else 1) * 0.3
    type_K = compute_k(type_value)

    E = 1 / (1 + pow(10, (case['rank'] - user_rank) / 400))

    all_change = all_K * (s - E)
    type_change = type_K * (s - E)

    user['rank_score'] += all_change
    user['type_info'][case['case_type']]['rank'] += type_change

    if user['rank_score'] < 0:
        user['rank_score'] = 0

    if user['type_info'][case['case_type']]['rank'] < 0:
        user['type_info'][case['case_type']]['rank'] = 0

    type_rank = list(map(lambda x: x['rank'], filter(lambda x: x['case_type'] == case['case_type'], cases)))
    type_rank.sort()
    idx = Core.findData(type_rank, user['type_info'][case['case_type']]['rank'])
    evaluate = idx / len(type_rank) * 100

    user['type_info'][case['case_type']]['evaluate'] = evaluate
    user['type_info'][case['case_type']]['offset'] = len(type_pass_records) / len(type_records)
    user['records'][len(user['records']) - 1]['rank_change'] = all_change

    Core.outputJSONFile('user.json', {'snow': user})


def compute_k(value):
    percent = value
    if percent >= 0.75:
        return 30
    elif percent >= 0.50:
        return 20
    elif percent >= 0.25:
        return 10
    else:
        return 5


if __name__ == '__main__':
    uses = getUserData()
    process_method(uses['snow'], '2061', 80, 0, 60 * 60 * 1000 - 1, 3, 'rank')
