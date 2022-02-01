import pandas as pd
import glob
import re

semantics=['mbs','card','hcat']
strategies=["pick_arg_most_to_least_pref","pick_arg_least_to_most_pref","pick_arg_largest_to_smallest_error","pick_arg_smallest_to_largest_error","pick_arg_order"]
graph_names={"nx.generators.erdos_renyi_graph(%s,p=0.1,seed=i,directed=True)":"erdos0.1","nx.generators.erdos_renyi_graph(%s,p=0.3,seed=i,directed=True)":"erdos0.3","nx.generators.erdos_renyi_graph(%s,p=0.5,seed=i,directed=True)":"erdos0.5","nx.generators.erdos_renyi_graph(%s,p=0.7,seed=i,directed=True)":"erdos0.7","nx.generators.directed.scale_free_graph(%s,seed=i)":"scale_free","nx.generators.complete_graph(%s,nx.DiGraph())":"complete"}
sizes=[10,100,2000]

headers=["size","runtime","iters","time variance","iters variance","num timeouts"]

dfs=[]

for s in semantics:
  for t in strategies:
    for g in graph_names:
      for i in sizes:
        for k in [s,"default"]:
          df=pd.read_csv(f"{s}_{t}_set_initial_weights_{s}_start_a_{k}_{i}_{g}.csv",header=None,names=headers,index_col=0)
          df["semantics"]=s
          df["start weights"]=k
          df["strategy"]=t
          df["graph"]=graph_names[g]
          df["iterations per argument"]=i
          dfs.append(df)
result=pd.concat(dfs)
result.to_csv("out.csv")
