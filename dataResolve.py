import json

DATA_SOURCE_FILE = "test_data.json"
RES_CASE_FILE = "total_cases.json"
CASE_TYPES = ['字符串', '线性表', '数组', '查找算法','排序算法', '数字操作', '树结构', '图结构']
GROUP_PEOPLE_NUM = 54
CASE_MIN_SCORE = 80

CASE_GROUPS = []
CASES = {}
RAW_DATA = {}



def getRawData():
	f = open(DATA_SOURCE_FILE, encoding='utf-8')
	return json.loads(f.read())


def getGroup():
	case_groups = []
	for value in RAW_DATA.values():
		if len(value['cases']) > 195:
			group = set()
			for case in value['cases']:
				group.add(case['case_id'])
			
			flag = True
			for i in range(len(case_groups)):
				if group.issubset(case_groups[i]):
					flag = False
					break
				elif group.issuperset(case_groups[i]):
					case_groups[i] = group
					flag = False
					break
			if flag:
				case_groups.append(group)
	
	repeat = set()
	for i in range(len(case_groups)):
		for j in range(len(case_groups)):
			if i != j and case_groups[i].issubset(case_groups[j]):
				repeat.add(i)
				break

	for i in range(len(case_groups)):
		if i not in repeat and len(case_groups[i]) != 204:
			print(len(case_groups[i]))
			CASE_GROUPS.append(list(case_groups[i]))
	print(len(CASE_GROUPS))
	
	
def getCases():
	for value in RAW_DATA.values():
		for case in value['cases']:
			if case['case_id'] not in CASES:
				CASES[case['case_id']] = {
					'case_id': case['case_id'],
					'case_zip': case['case_zip'],
					'case_type': case['case_type'],
					'total_score': case['final_score'],
					'total_people': 1,
					'group_people': 0
				}
			else:
				CASES[case['case_id']]['total_score'] += case['final_score']
				CASES[case['case_id']]['total_people'] += 1
				
	for group in CASE_GROUPS:
		for case in group:
			CASES[case]['group_people'] += GROUP_PEOPLE_NUM
	

def getDifficulty(score):
	return 1 - score/100


def getRank(difficulty):
	rank = int(difficulty*2000)
	if rank <= CASE_MIN_SCORE:
		return CASE_MIN_SCORE
	else:
		return rank


def filterCaseInfo():
	case_dir = {}
	for type in CASE_TYPES:
		case_dir[type] = []
		
	for case in CASES.values():
		if case['total_people'] > case['group_people']:
			average_score = case['total_score']/case['total_people']
		else:
			average_score = case['total_score']/case['group_people']
		case_dir[case['case_type']].append({
			'case_id': case['case_id'], 'case_zip': case['case_zip'], 'case_type': case['case_type'], 'average_score': average_score,
			'difficulty': getDifficulty(average_score), 'rank_score': getRank(getDifficulty(average_score))
		})
	
	for cases in case_dir.values():
		cases.sort(key=lambda x:x['rank_score'])
		# 测试用
		print("'"+cases[0]['case_type']+"':"+str(cases[int(len(cases)/2)]['rank_score'])+",")
	
	with open(RES_CASE_FILE,'w') as f:
		json.dump(case_dir, f)
		
		
if __name__ == '__main__':
	RAW_DATA = getRawData()
	getGroup()
	getCases()
	filterCaseInfo()