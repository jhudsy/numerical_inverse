from compute_weights import *
from semantics import *
from strategies import *
import random
import time
import sys
import math

def do_test(strat,semantics,set_initial_weights,start_a,maxiters,graph_generator,max_size=15,num_trials=15):
 out=[]
 for a in range(1,max_size+1):
  SIZE=a*10
  tme=0
  iters=0
  iterssq=0
  tmesq=0
  to=0

  for i in range(num_trials):
    random.seed(i)
    g=eval(graph_generator % SIZE)
    h=nx.DiGraph()
    h.add_nodes_from(sorted(g.nodes(data=True)))
    h.add_edges_from(g.edges(data=True))
    g=h

    n=[x for x in range(0,SIZE)]
    prefs=[]
    while len(n)>0:
      c=set(random.choices(n,k=random.randint(1,5)))
      for i in c:
        n.remove(i)
      prefs.append(c)

    s=time.process_time()
    it=compute_weights(g,prefs,1,strat,semantics,set_initial_weights,start_a,iters=maxiters)
    if it!=10000: #timeout_iters_value
      tt=time.process_time()-s #total time
    #print(f"finished {len(g.nodes)},{strat},{maxiters}, time: {tt}, iters: {it}")
      iters+=it
      iterssq+=it*it
      tmesq+=tt*tt
      tme+=tt
    else:
      to+=1
  if (num_trials!=to and num_trials-to-1!=0):
      out.append((SIZE,tme/(num_trials-to),iters/(num_trials-to),math.sqrt((tmesq-tme*tme/(num_trials-to))/(num_trials-to-1)),math.sqrt((iterssq-iters*iters/(num_trials-to))/(num_trials-to-1)),to))
  else:
      out.append((SIZE,tme,iters,0,0,to))

 return out

#read parameters from command line
semantics=eval(sys.argv[1]) #e.g., card or hcat or mbs
strat=eval(sys.argv[2]) # e.g., pick_arg_most_to_least_pref
init_weights=eval(sys.argv[3]) # e.g., set_initial_weights_hcat
init_a=eval(sys.argv[4]) #e.g., start_a_hcat
iters=int(sys.argv[5])
graph_generator=sys.argv[6] #should be of the form "nx.generators.erdos_renyi_graph(%s,p=0.5,seed=i,directed=True)

with open(f"{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_{sys.argv[4]}_{sys.argv[5]}_{sys.argv[6]}.csv","w") as f:
    for l in do_test(strat,semantics,init_weights,init_a,iters,graph_generator,num_trials=15):
        f.write(f"{l[0]}, {l[1]}, {l[2]}, {l[3]}, {l[4]}, {l[5]}\n")
