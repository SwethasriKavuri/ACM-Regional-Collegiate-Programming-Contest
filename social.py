
import sys
from sys import exit
MAX_NODES=20
MAX_QUERIES=20
query1=[0 for _ in range(MAX_QUERIES)]
query2=[0 for _ in range(MAX_QUERIES)]
Adjacent=list()

def AdjacentInit(nnodes,nqueries):
	global Adjacent 
	Adjacent = [[0 for _ in range(30)] for _ in range(21)]
	for i in range(0,nnodes+1):
		for j in range(0,nnodes+nqueries):
			Adjacent[i][j] = 0.0
	for k in range(0,nnodes):
		Adjacent[nnodes][k] = 1.0
	return			
    
def ScanEdgeData(nnodes,pb):
	# print('pb={}'.format(pb))
	global Adjacent
	node = count = i =0
	while((i < len(pb))  and (pb[i] == ' ')):
		i+=1
	if((i >= len(pb))  or pb[i].isdigit() is False ):
		return -1
	while(pb[i].isdigit()):
		node = (node * 10) + int(pb[i])
		i+=1
	if((i >= len(pb))  or pb[i].isspace() is False ):
	    return -2
	while((i < len(pb))  and (pb[i].isspace())):
		i+=1
	if((i >= len(pb))  or pb[i].isdigit() is False ):
		return -3
	while(pb[i].isdigit()):
		count = (count * 10) + int(pb[i])
		i+=1
	Adjacent[node-1][node-1] += float(count)
	 
	for j in range(0,count): 
		if((i >= len(pb))  or pb[i] != ' '):
			print('node={}, count={}'.format(node, count))
			return -4
		while((i < len(pb))  and (pb[i].isspace())):
			i+=1
		if((i >= len(pb))  or pb[i].isdigit() is False): 
			return -5
		val = 0
		while(i< len(pb) and pb[i].isdigit()):
			val = (val * 10) + int(pb[i])
			i+=1
		if((val == 0) or (val > nnodes)):
			print("node %d val %d not in range 1 .. %d \n", i, val, nnodes)
			return -6
		Adjacent[node-1][val-1] = -1.0
		Adjacent[val-1][node-1] = -1.0
		Adjacent[val-1][val-1] += 1.0
	return count 

def FindMaxRow(nnodes,nqueries,currow):
	global Adjacent

	maxV = abs(Adjacent[currow][currow]);
	maxrow = currow;

	for i in range(currow+1,nnodes+1):
		tmp = abs(Adjacent[i][currow])
		if (tmp > maxV):
			maxV = tmp
			maxrow = i

	# maxrow = max([abs(x[currow]) for x in Adjacent[currow+1:nnodes+1]])		
	return maxrow		

def SwapRows(maxrow,currow,nnodes,nqueries):
	global Adjacent
	maxrow = int(maxrow)
	ncols = nnodes + nqueries;
	for i in range(0,ncols):
		tmp = Adjacent[currow][i]
		Adjacent[currow][i] = Adjacent[maxrow][i]
		Adjacent[maxrow][i] = tmp
	return
	
def Eliminate(currow,nrows,ncols):
	global Adjacent
	for i in range(0,nrows):
		if i == currow:
			continue
		factor = Adjacent[i][currow]

		for j in range(currow,ncols):

			Adjacent[i][j] -= factor*Adjacent[currow][j]
		
	return 0

def DumpMatrix(nrows,ncols):
	global Adjacent
	for i in range(0,nrows):
		for j in range(0,ncols):
			print("{0:.2f}".format(Adjacent[i][j]))
		
		print("\n")
	
	print("\n")

def SolveMatrix(nnodes,nqueries):
	global Adjacent
	global MAX_NODES 
	global MAX_QUERIES
	global query1 
	global query2
	ncols = nnodes + nqueries;
	nrows = nnodes + 1;
	for currow in range(nnodes):
		maxrow = FindMaxRow(nnodes, nqueries, currow)
		if maxrow != currow :
			SwapRows(maxrow, currow, nnodes, nqueries)
		pivot = Adjacent[currow][currow]
		if (abs(pivot) < .001): 
			print('pivot = {}'.format(pivot))
			return -1
		pivot = 1.0/pivot
		for i in range(currow,ncols):
			Adjacent[currow][i] = Adjacent[currow][i]*pivot
		Eliminate(currow, nrows, ncols)
	return 0

if len(sys.argv) != 2:
	print('Incorrect number of arguments')
else:
	filename = sys.argv[1]
	f = open(filename)
	nprob = int(f.readline().strip('\n'))
	for curprob in range(1,nprob+1):
		l = f.readline().strip('\n')
		if l == '':
			print('Read failed on problem {} header'.format(curprob))
			exit()
		x = [int(a) for a in l.split(' ')]
		if len(x) != 4:
			print('scan failed on problem {}'.format(curprob))
			exit()
		index = x[0]
		nnodes = x[1]
		nqueries = x[2]
		nedges = x[3]
		if index != curprob:
			print('problem index {} not = expected problem {}'.format(index, curprob))
			exit()
		if nnodes > MAX_NODES or nqueries > MAX_QUERIES:
			print('prob {}: nnodes {} > max {} or nqueries {} > max {}'.format(curprob, nnodes, MAX_NODES, nqueries, MAX_QUERIES))
			exit()
		AdjacentInit(nnodes, nqueries)
		# read edge data
		edgecnt = edgelines = 0
		while edgecnt < nedges:
			l = f.readline().strip('\n')
			if l == '':
				print('Read failed on problem {} edgeline {}'.format(curprob, edgelines))
				exit()
			i = ScanEdgeData(nnodes, l)
			if i < 0:
				print ("i:{}".format(i))
				print('scan failed on problem {} edgelines {} '.format(curprob, edgelines))
				exit()
			edgelines += 1
			edgecnt += i
		for i in range(0,nqueries):
			p = f.readline().strip('\n')
			if p == '':
				print('Read failed on problem {} query {}'.format(curprob, i+1))
				exit()
			x = [int(a) for a in p.split(' ')]
			if len(x) != 3:
				print('scan failed on problem {}'.format(curprob))
				exit()
			queryno = x[0]
			query1[i] = x[1]
			query2[i] = x[2]
			if  i+1 != queryno:
				print('read query num {} != expected {} problem {}'.format(queryno, i+1, curprob))
				exit()
			if((query1[i] < 1) or (query1[i] > nnodes) or (query2[i] < 1) or (query2[i] > nnodes) or (query1[i] == query2[i])): 
				print('bad queryid1 {} or queryid2 {} problem {} query {}'.format(query1, query2, curprob, i+1))
				exit()
			Adjacent[query1[i]-1][nnodes + i] = 1.0	
			Adjacent[query2[i]-1][nnodes + i] = -1.0
		i = SolveMatrix(nnodes, nqueries)
		if i != 0:
			print("error return {} from SolveMatrix problem {}".format(i, curprob));
			exit();
		else:
			print(curprob,end='')
			for i in range(0,nqueries):
				dist = abs(Adjacent[query1[i]-1][nnodes + i] - Adjacent[query2[i]-1][nnodes + i])
				print(" {0:.3f}".format(dist), end='')
			print('')