import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import pickle
import datetime

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

def getwidths(edges):
	raw = [item[2]['weight'] for item in edges]
	return [2*item/max(raw) for item in raw]
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

date = datetime.datetime(2020, 1, 1, 0, 0)
end_date = date
tt=7
for i in range(12):
	#start_date = date
	start_date = end_date
	end_date = start_date + datetime.timedelta(days=tt)
	#aapos, aaG,aa_dates =sub_graph(aG,a_dates,apos,start_date,end_date)
	aapos, aaG,aa_dates = sub_graph(mG,m_dates,mpos,start_date,end_date)
	'''print(len(aG.nodes()),len(aaG.nodes()))
	print(len(aG.edges.data()), len(aaG.edges.data()))
	print(len(a_dates),len(aa_dates))'''

	# draw
	plt.figure(figsize = (10,9))
	m = Basemap(llcrnrlon=-160, llcrnrlat=-60,urcrnrlon=160,urcrnrlat=70,resolution='l',suppress_ticks=True)
	nx.draw_networkx_nodes(aaG,aapos,node_list = aaG.nodes(),node_color = 'r', alpha = 1, node_size = 40)
	nx.draw_networkx_edges(aaG,aapos,width = getwidths(aaG.edges.data()), edge_color='w', alpha=1,arrows = True)
	# Now draw the map
	m.drawcountries(linewidth = 1.5)
	m.drawstates(linewidth = 0.6)
	m.bluemarble()
	m.drawcoastlines(linewidth=1.5)
	plt.tight_layout()
	plt.title('Date Range: From '+start_date.strftime("%Y-%m-%d")+ ' to '+end_date.strftime("%Y-%m-%d"))
	plt.savefig('pic_actual/'+str(i+1)+'.png', format = "png", dpi = 300,bbox_inches='tight')
	print(i+1)
	#plt.show()
