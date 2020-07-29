

def testRank(num):
	with open('rankTest', 'w') as f:
		f.write("n\n")
		f.write("snow\n")
		for i in range(num):
			f.write("T\n")
			f.write("\n")
			# if i % 5 == 0:
			# 	print("50 0 7200000 6")
			# else:
			# 	print("100 0 300000 4")
			f.write("100 0 300000 4\n")
		# f.write("D\n")
		f.write("Q\n")

if __name__ == '__main__':
	testRank(100)