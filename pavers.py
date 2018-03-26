import sys

def comp_tiles():

	global F
	global F1
	global F2
	global F3
	global G
	global G1
	global G2
	global G3

	global MAX_SIZE

	F = [1,2,11]
	F1 = [0,2,16]
	F2 = [0,1,8]
	F3 = [0,0,4]

	G = [0,0,2]
	G1 = [0,0,1]
	G2 = [0,0,1]
	G3 = [0,0,1]

	for n in range(2,MAX_SIZE):
		F.append(2*F[n] + 7*F[n-1] + 4*G[n])
		F1.append(2*F1[n] + 2*F[n] + 7*F1[n-1] + 8*F[n-1] + 4*G1[n]+2*G[n])
		F2.append(2*F2[n] + F[n] + 7*F2[n-1] + 4*F[n-1] + 4*G2[n]+2*G[n])
		F3.append(2*F3[n] + 7*F3[n-1] + 4*F[n-1] + 4*G3[n]+2*G[n])
		test = 2.0*(n+1)*F[n+1]
		test1 = F1[n+1] + 2.0*F2[n+1] + 3.0*F3[n+1]
		if(abs(test - test1) > .0000001*test):
			print("mismatch {}: {} != {}".format(n+1, test, test1))
		G.append(2*F[n-1] + G[n])
		G1.append(2*F1[n-1] + F[n-1] + G1[n])
		G2.append(2*F2[n-1] + F[n-1] + G2[n] + G[n])
		G3.append(2*F3[n-1] + F[n-1] + G3[n])

	MAX_SIZE = len(F)
	return

DO_FLOAT = False

F = list()
F1 = list()
F2 = list()
F3 = list()
G = list()
G1 = list()
G2 = list()
G3 = list()

MAX_SIZE = 400

if len(sys.argv) != 2:
	print('Incorrect number of arguments')
else:
	filename = sys.argv[1]
	f = open(filename)
	nprob = int(f.readline().strip('\n'))
	comp_tiles()
	for curprob in range(1,nprob+1):
		l = f.readline().strip('\n')
		x = [int(a) for a in l.split(' ')]
		if x[0] != curprob:
			print('problem index {} not = expected problem {}'.format(index, curprob))
			exit()
		index = x[0]
		n = x[1]
		if n == 1:
			print('{} 2 2 1 0'.format(curprob))
		elif n<2 or n>MAX_SIZE:
			print('array width {} not in range 2 .. {} problem {}\n'.format(n, MAX_SIZE, curprob))
		else:
			if DO_FLOAT is True:
				print('{} {} {} {} {} {}'.format(curprob, F[n], F1[n], F2[n], F3[n],
					F1[n]/(F1[n]+F2[n]+F3[n])))
			else:
				print('{} {} {} {} {}'.format(curprob, F[n], F1[n], F2[n], F3[n]))
	f.close()