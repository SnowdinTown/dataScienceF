import random

PASS = '100 0 300000 4\n'
FAIL = '50 0 7200000 6\n'
ABILITY = {
	'字符串': 200,
	'线性表': 144,
	'数组': 100,
	'查找算法': 370,
	'排序算法': 119,
	'数字操作': 200,
	'树结构': 301,
	'图结构': 400,

}


def testRank(num):
	with open('rankTest', 'w') as f:
		f.write("n\n")
		f.write("snow\n")
		for i in range(num):
			f.write("T\n")
			f.write("\n")
			if i % 5 == 0:
				f.write("50 0 7200000 6\n")
			else:
				f.write("100 0 300000 4\n")
			# f.write("100 0 300000 4\n")
		# f.write("D\n")
		f.write("Q\n")


def getRate(type, score):
	if score <= ABILITY[type]*0.5:
		return  PASS
	elif score <= ABILITY[type]*1.1:
		if random.random() < 0.6:
			return PASS
		else:
			return FAIL
	elif score <= ABILITY[type]*1.5:
		if random.random() < 0.2:
			return PASS
		else:
			return FAIL
	else:
		return FAIL



def testSingle(case):
	writeLine(getRate(case['case_type'],case['rank_score'])+'\n')


def writeLine(line):
	with open('rankTest', 'w') as f:
		f.write(line)

if __name__ == '__main__':
	testRank(100)