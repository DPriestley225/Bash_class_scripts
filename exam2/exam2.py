import sys

def read_data(file_name):
	fr = open(file_name, 'r')
	List = []
	line = fr.readline()
	while line:
		item = line.strip().split(',')
		#convert items to floats here as I only need them as strings for the output
		item[0] = float(item[0])
		item[1] = float(item[1])
		List.append(item)
		line = fr.readline()
	fr.close()
	return List

#using a double for loop to traverse both Arrays
def compute_distances(A, B, D):
	for a in A:
		#declaring empty for know
		index = 0
		closest = []
		for b in B:
			#extracted the actual calculation to its own function
			distance = calculate_distance(a[0], b[0], a[1], b[1])
			current = [index, distance]
			#checking proximity statements
			#edge case of the first distance since there is nothing to compare
			if index == 0:
				closest = current
			elif current[1] < closest[1]:
				closest = current

			index += 1

		D.append(closest)
#Bonus
#I modified the computedistance function and modified it to get averages
def compute_average_distances(A, B, C):
	for a in A:
		#declaring empty for know
		count = 1
		closest = []
		average = 0
		for b in B:
			distance = calculate_distance(a[0], b[0], a[1], b[1])
			average = average + distance 
			count+= 1
		average = average/count

		C.append(average)


#helper function
def calculate_distance(x1, x2, y1, y2):
	d = ((x2-x1)**2 + (y2-y1)**2)**0.5
	return d

def output(D):
	i = 0
	for d in D:
		#trimming distance
		distance = str(d[1]+0.0005)
		distance = distance[0:5]
		print("The closest point to A["+str(i)+"] is point B["+str(d[0])+"]. Distance = "+ distance)
		i += 1

#for the bonus
def output_b(C):
	i = 0
	for c in C:
		#trimming distance
		distance = str(c+0.0005)
		distance = distance[0:5]
		print("average distance of point A["+str(i)+"] to all points in B = " + distance)
		i += 1

#declaring file_names
A_local = sys.argv[1]
B_local = sys.argv[2]
#declaring lists
A = read_data(A_local)
B =read_data(B_local)
D =[]

compute_distances(A, B, D)
output(D)
#going for bonus
C = []
compute_average_distances(A, B, C)
output_b(C)
