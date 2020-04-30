import networkx as nx
import pickle
import datetime
import numpy as np

def sub_graph(G,dates,pos,start,end):
    nG = nx.DiGraph()
    ndates = {}
    npos={}
    for tran in dates:
        init = dates[tran]
        new = []
        for date in init:
            if date >= start and date <= end:
                new.append(date)
        if len(new) > 0:
            ndates[tran] = new
            nG.add_node(tran[0])
            nG.add_node(tran[1])
            nG.add_edge(tran[0],tran[1],weight=len(new))
            npos[tran[0]] =  pos[tran[0]]
            npos[tran[1]] =  pos[tran[1]] 
    return npos, nG, ndates

#decryption
aG = nx.read_gpickle("agraph.gpickle")
pickle_in = open("adates.pickle","rb")
a_dates = pickle.load(pickle_in)
pickle_in = open("apos.pickle","rb")
apos = pickle.load(pickle_in)

mG = nx.read_gpickle("mgraph.gpickle")
pickle_in = open("mdates.pickle","rb")
m_dates = pickle.load(pickle_in)
pickle_in = open("mpos.pickle","rb")
mpos = pickle.load(pickle_in)

dates = [datetime.datetime(2020, 1, 20, 0, 0),datetime.datetime(2020, 3, 1, 0, 0)]
duration = [11,5]

#dates = [datetime.datetime(2020, 3, 1, 0, 0)]
#duration = [5]

#adjacency_matrix_Difference

'''
#################
deltas = [1,2,4,6,8]
#################
for delta in deltas:
	total_predict=0
	total_sum = 0
	for i in range(len(dates)):
		current_date = dates[i]
		end_date = current_date + datetime.timedelta(days=duration[i])
		while(current_date <= end_date):
			next_date = current_date + datetime.timedelta(days=delta -1)
			aapos, aaG,aa_dates =sub_graph(aG,a_dates,apos,current_date,next_date)
			mmpos, mmG,mm_dates =sub_graph(mG,m_dates,mpos,current_date,next_date)
			result = 0
			total = 0
			for date in mm_dates:
				found = 0
				if date in aa_dates:
					found = len(aa_dates[date])
				temp = len(mm_dates[date]) - found
				total += len(mm_dates[date])
				if temp > 0:
					result += temp	
			#print((1-result/total)*100,len(mm_dates))
			#print(mm_dates.keys(),len(mm_dates))
			#print()
			#print(aa_dates.keys(),len(aa_dates))
			current_date = current_date + datetime.timedelta(days=delta)
			if total == 0:
				continue
			correct_predict = (1-result/total)*100
			total_predict += correct_predict*len(mm_dates)
			total_sum += len(mm_dates)
			#x = int(input('Enter a number: '))
	print('AVG accuracy is: ',total_predict/total_sum,'     delta: ',delta)		
'''
#snapshot_comparing()
#################
epsilons = [0,2,4,6,8,10]
#################
TP = 0
FP = 0
TN = 0
FN = 0
for epsilon in epsilons:
	for i in range(len(dates)):
		start_date = dates[i]
		end_date = start_date + datetime.timedelta(days=duration[i])
		mmpos, mmG,mm_dates =sub_graph(mG,m_dates,mpos,start_date,end_date)
		for key in mm_dates:
			predicted_dates = []
			if key in a_dates: 
				predicted_dates = a_dates[key]
			if len(predicted_dates) > 0:
				for date in mm_dates[key]:
					found = False
					span_start = date - datetime.timedelta(days=epsilon)
					span_end = date + datetime.timedelta(days=epsilon)
					for predicted in predicted_dates:
						if predicted >= span_start and predicted <= span_end:
							found = True
							break
					if found == True:
						TP += 1
					else:
						FP += 1
			else:
				FP += len(mm_dates[key])

		aapos, aaG,aa_dates = sub_graph(aG,a_dates,apos,start_date,end_date)
		for key in aa_dates:
			actual_dates = []
			if key in m_dates: 
				actual_dates = m_dates[key]
			if len(actual_dates) > 0:
				for date in aa_dates[key]:
					found = False
					span_start = date - datetime.timedelta(days=epsilon)
					span_end = date + datetime.timedelta(days=epsilon)
					for actual in actual_dates:
						if actual >= span_start and actual <= span_end:
							found = True
							break
					if found == True:
						pass
					else:
						FN += 1
			else:
				FN += 1
	
		nodes = mmG.nodes()
		nodes = list(nodes)
		for i in range(len(nodes)):
			for j in range(i+1,len(nodes)):
				if(nodes[i] != nodes[j]):
					e1 = (nodes[i],nodes[j])
					if e1 not in mm_dates and e1 not in aa_dates:
						TN += 1
	accuracy = (TP+TN)/(TP+FP + TN + FN)
	sensitivity = TP/(TP+FN) #sensitivity
	specificity = TN/(TN+FP)
	print('accuracy: ',accuracy,'\tsensitivity: ',sensitivity,'\tspecificity: ',specificity,'\tepsilon: ',epsilon)
