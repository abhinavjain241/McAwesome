import collections
import sys
# import scikit_learn
# from sklearn.linear_model import LinearRegression

a = raw_input()

numticks = int(a.split()[1])
ticksEngine = collections.defaultdict(dict)

while(numticks):
	field_value_dict = {}
	tick = raw_input()
	argList = tick.split()
	for i in xrange(2, len(argList) - 1, 2):
		field_value_dict[argList[i]] = int(argList[i + 1])
	ticksEngine[int(argList[0])][argList[1]] = field_value_dict
	numticks = numticks - 1

print("tickfile completed")

for b in sys.stdin:
	query = b.split()
	if (query[0] == 'sum'):
		start_time = int(query[1])
		end_time = int(query[2])
		symbol = query[3]
		field = query[4]
		sum = 0
		for j in range(start_time, end_time + 1):
			if j in ticksEngine:
				if symbol in ticksEngine[j]:
					if field in ticksEngine[j][symbol]:
						sum += ticksEngine[j][symbol][field]
		print sum

	elif (query[0] == 'product'):
		start_time = int(query[1])
		end_time = int(query[2])
		symbol = query[3]
		field1 = query[4]
		field2 = query[5]
		product = 0
		for j in range(start_time, end_time + 1):
			if j in ticksEngine:
				if symbol in ticksEngine[j]:
					if field1 and field2 in ticksEngine[j][symbol]:
						product += ticksEngine[j][symbol][field1] * ticksEngine[j][symbol][field2]
		print product

	elif (query[0] == 'max'):
		values = list()
		start_time = int(query[1])
		end_time = int(query[2])
		symbol = query[3]
		field = query[4]
		k = query[5]
		for j in range(start_time, end_time + 1):
			if j in ticksEngine:
				if symbol in ticksEngine[j]:
					if field in ticksEngine[j][symbol]:
						values.append(ticksEngine[j][symbol][field])
		values = sorted(values, reverse = True)
		if (len(values) < k):
			for value in values:
				print(value), 
		else:
			for i in range(0, k):
				print(values[i]),
		print

	elif (query[0] == 'delta'):
		ordered_pair_list = list()
		symbol = query[1]
		field = query[2]
		k = query[3]
		for timestamp, v in ticksEngine.items():
			if symbol in v:
				if field in v[symbol]:
					tup = (timestamp), v[symbol][field]
					ordered_pair_list.append(tup)



