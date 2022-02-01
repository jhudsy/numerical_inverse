import networkx as nx
import numpy as np
################################################
def card(g,**kwargs):
  """weighted cardinality semantics"""
  weight=kwargs.get("weight","weight")
  epsilon=kwargs.get("epsilon",0.001)
  t=nx.get_node_attributes(g,name=weight)
  nodelist=list(t)
  start_weights=np.array(list(t.values()))
  adj=nx.convert_matrix.to_numpy_array(g,nodelist)
  adj=adj.T

  weights=start_weights
  finished=False
  adjsum=np.sum(adj,axis=1)
  while not finished:
    new_weights=start_weights/(1+adjsum+np.divide(np.matmul(adj,weights),adjsum,out=np.zeros_like(weights), where=adjsum!=0))
    if np.linalg.norm(abs(new_weights-weights)/new_weights)<epsilon:
      finished=True
    weights=new_weights
  return weights

def set_initial_weights_card(g,prefs,zeta):
  """sets the target degrees for arguments."""
  mx=1
  target={}

  for p in prefs:
    #max_attacks = max(g.in_degree(a) for a in p)
    mn=mx/(2+max(g.in_degree(a) for a  in p)+zeta)
    for a in p:
      target[a]=mn
      g.nodes[a]["weight"]=(mx+mn)/2
    mx=mn
  return target

def start_a_card(target,g,arg,zeta):
    return min(1,2*zeta+2*target+2*g.in_degree(arg))

################################################
def hcat(g,**kwargs):
  """weighted h-categoriser semantics. Takes an argumentation graph as input. Each node must have a weight parameter, default "weight". Epsilon tells us when to stop iterating"""
  weight=kwargs.get("weight","weight")
  epsilon=kwargs.get("epsilon",0.001)
  t=nx.get_node_attributes(g,name=weight)
  nodelist=list(t)
  start_weights=np.array(list(t.values()))
  adj=nx.convert_matrix.to_numpy_array(g,nodelist)
  adj=adj.T

  weights=start_weights
  finished=False
  while not finished:
    new_weights=start_weights/(np.matmul(adj,weights)+1)
    if np.linalg.norm(abs(new_weights-weights)/new_weights)<epsilon:
      finished=True
    weights=new_weights
  return weights

def set_initial_weights_hcat(g,prefs,zeta):
  """sets the target degrees for arguments."""
  mx=1
  target={}

  for p in prefs:
    max_attacks = max(g.in_degree(a) for a in p)
    mn=mx/(1+zeta+max_attacks)
    for a in p:
      target[a]=mn
      g.nodes[a]["weight"]=(mx+mn)/2
    mx=mn
  return target

def start_a_hcat(target,g,arg,zeta):
    return min(1,zeta+target+target*g.in_degree(arg))
################################################
def mbs(g,**kwargs):
  """max categoriser semantics"""
  weight=kwargs.get("weight","weight")
  epsilon=kwargs.get("epsilon",0.001)
  t=nx.get_node_attributes(g,name=weight)
  nodelist=list(t)
  start_weights=np.array(list(t.values()))
  adj=nx.convert_matrix.to_numpy_array(g,nodelist)
  adj=adj.T

  weights=start_weights
  finished=False
  while not finished:
    new_weights=start_weights/(1+np.max(adj*weights,axis=1))
    if np.linalg.norm(abs(new_weights-weights)/new_weights)<epsilon:
      finished=True
    weights=new_weights
  return weights

def set_initial_weights_mbs(g,prefs,zeta):
  """sets the target degrees for arguments."""
  mx=1
  target={}

  for p in prefs:
    #max_attacks = max(g.in_degree(a) for a in p)
    mn=mx/(2+zeta)
    for a in p:
      target[a]=mn
      g.nodes[a]["weight"]=(mx+mn)/2
    mx=mn
  return target

def start_a_mbs(target,g,arg,zeta):
    return min(1,2*target+2*zeta)
################################################
def start_a_default(target,g,arg,zeta):
    return 1
################################################
def trust(g,**kwargs):
  """trust based semantics; d^a_t=0.5*d^a_{t-1}+0.5*min(w,1-max(d^b_{t-1})) where b attacks a. d^a_0=w. """
  weight=kwargs.get("weight","weight")
  epsilon=kwargs.get("epsilon",0.001)
  t=nx.get_node_attributes(g,name=weight)
  nodelist=list(t)
  start_weights=np.array(list(t.values()))
  adj=nx.convert_matrix.to_numpy_array(g,nodelist)
  adj=adj.T

  weights=start_weights
  finished=False
  while not finished:
    att_weights=1-np.max(adj*weights,axis=1)
    new_weights=0.5*weights+0.5*np.min(np.array([start_weights,att_weights]),axis=0)
    if np.linalg.norm(abs(new_weights-weights)/new_weights)<epsilon:
      finished=True
    weights=new_weights
  return weights
