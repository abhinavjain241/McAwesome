import collections
import sys
import math
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LinearRegression

a = raw_input()

numticks = int(a.split()[1])
ticksEngine = collections.defaultdict(dict)

for z in range(0, numticks):
	field_value_dict = {}
	tick = raw_input()
	argList = tick.split()
	for i in xrange(2, len(argList) - 1, 2):
		field_value_dict[argList[i]] = int(argList[i + 1])
	ticksEngine[int(argList[0])][argList[1]] = field_value_dict
	

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
					if field1 in ticksEngine[j][symbol] and field2 in ticksEngine[j][symbol]:
						product += ticksEngine[j][symbol][field1] * ticksEngine[j][symbol][field2]
		print product

	elif (query[0] == 'max'):
		values = list()
		start_time = int(query[1])
		end_time = int(query[2])
		symbol = query[3]
		field = query[4]
		k = int(query[5])
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
		counter = 0	# Set counter to 0
		# Parse arguments in query
		symbol = query[1]
		field = query[2]
		k = int(query[3])
		# Set Final Cost to zero.
		finalcost = 0 
		#Create list of segments
		segment_list = list()
		#Create initial segment
		segment = list()
		t = list() 
		y = list()
		segment.append(t)
		segment.append(y)
		segment.append(0) # This is the cost value in the segment data structure. Which is zero for the first.
		segment_list.append(segment)
		#End of creation of initial segment
		lm = LinearRegression()	# Instantiate LinearRegression model/object
		for timestamp, v in ticksEngine.items():
			if symbol in v:
				if field in v[symbol]:
					if counter == 0 or counter == 1:	# For the first two ticks in the time series just put them in segment 1
						segment_list[0][0].append(timestamp)
						segment_list[0][1].append(v[symbol][field])
					else:
						mincost = sys.maxint	# Set minimum cost to +infinity
						for j in range(0, len(segment_list)):	# Loop through all segments
							segment_list[j][0].append(timestamp)	# Add current tick's t 
							segment_list[j][1].append(v[symbol][field])	# Add current tick's y
							T = np.array(segment_list[j][0])	# Create numpy array from vector of timestamps
							Y = np.array(segment_list[j][1]) 	# Create numpy array from vector of values
							T = T[:, np.newaxis] # Take transpose of T
							lm.fit(T, Y) # Fit arrays T and Y into LinearRegression Model and get new approximation function
							sse = 0	# This will store Residual Sum of Squares / Sum of Square of Error
							for i in range(0, len(segment_list[j][0])):	# Loop through all points (t, y) in a segment
								sse += (segment_list[j][1][i] - lm.coef_[0] * segment_list[j][0][i] - lm.intercept_)**2 # sigma (y[i] - a*t[i] - b)^2
							if (sse - segment_list[j][2] < mincost): # If (sse with new element) - (segment's existing cost) < minimum cost
								mincost = sse - segment_list[j][2]	# Set new minimum cost
								seg_index = j # Store index of segment with minimum cost
							segment_list[j][0].pop() # Remove the new element from the segment which was added 
							segment_list[j][1].pop() # Remove the new element from the segment which was added

						if mincost < k: # In the case when adding an element to a particular segment yields us lower cost than creating a new one
							segment_list[seg_index][0].append(timestamp)
							segment_list[seg_index][1].append(v[symbol][field])
							segment_list[seg_index][2] += mincost
						else: # In the case when creating a new segment is more feasible
							segment = list()
							t = list()
							t.append(timestamp)
							y = list()
							y.append(v[symbol][field])
							segment.append(t)
							segment.append(y)
							segment.append(0)
							segment_list.append(segment)

					counter = counter + 1 # Increment the counter for ticks

		for i in range(0, len(segment_list)):
			finalcost += segment_list[i][2]

 		finalcost += len(segment_list) * k # Finally , sum up the penalties for all segments, which is basically (n * k), and add to final cost
		finalcost = int(math.ceil(finalcost))
		print finalcost