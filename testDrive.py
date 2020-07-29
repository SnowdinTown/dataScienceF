import random

PASS = '100 0 300000 4\n'
HALF_PASS = '80 0 3600000 2\n'
FAIL1 = '60 0 3600000 3\n'
FAIL2 = '50 0 3600000 6\n'
FAIL3 = '20 0 1 2\n'

ABILITY = {
	'字符串': 400,
	'线性表': 400,
	'数组': 400,
	'查找算法': 400,
	'排序算法': 400,
	'数字操作': 400,
	'树结构': 400,
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
	if score <= ABILITY[type]:
		num = random.random()
		if num < 0.1:
			return HALF_PASS
		else:
			return PASS
	elif score <= ABILITY[type] + 200:
		num = random.random()
		if num < 0.3:
			return PASS
		elif num < 0.6:
			return HALF_PASS
		elif num < 0.8:
			return FAIL1
		else:
			return FAIL2
	elif score <= ABILITY[type] + 400:
		num = random.random()
		if num < 0.1:
			return PASS
		elif num < 0.3:
			return HALF_PASS
		elif num < 0.7:
			return FAIL1
		else:
			return FAIL2
	else:
		num = random.random()
		if num < 0.1:
			return FAIL1
		elif num < 0.4:
			return FAIL2
		else:
			return FAIL3



def testSingle(case):
	writeLine(getRate(case['case_type'],case['rank_score'])+'\n')


def writeLine(line):
	with open('rankTest', 'w') as f:
		f.write(line)

if __name__ == '__main__':
	testRank(100)