#STRATEGIES; all take a graph, a list of list of preferences and a data dictionary used to store information between picking arguments.

#####################################################
#all of these return data which we can use next iteration
def pick_arg_most_to_least_pref(g,prefs,data):
  ordering=data.get("ordering",[])
  if ordering == []: #need to initialise ordering
   for p in prefs:
     for a in p:
       ordering.append(a)
  data["ordering"]=ordering
  picked=data.get("picked",0)
  data["picked"]=(picked+1)%len(ordering)
  return ordering[picked]

#####################################################

def pick_arg_least_to_most_pref(g,prefs,data):
  ordering=data.get("ordering",[])
  if ordering == []: #need to initialise ordering
   prefs.reverse()
   for p in prefs:
     for a in p:
       ordering.append(a)
   prefs.reverse()
  data["ordering"]=ordering
  picked=data.get("picked",0)
  data["picked"]=(picked+1)%len(ordering)
  return ordering[picked]

#####################################################
def pick_arg_largest_to_smallest_error(g,prefs,data):
  degree=data.get("degree")
  target=data.get("target")
  max_error=data.get("max_error")
  error=0
  picked=-1
  for n in g.nodes:
    e = abs((target[n]-degree[n])/degree[n])
    if e>error and e>max_error:
      error=abs((target[n]-degree[n])/degree[n])
      picked=n
  return picked


#####################################################
def pick_arg_smallest_to_largest_error(g,prefs,data):
  degree=data.get("degree")
  target=data.get("target")
  max_error=data.get("max_error")
  error=9999999
  picked=-1
  for n in g.nodes:
    e = abs((target[n]-degree[n])/degree[n])
    if e<error and e>max_error:
      error=abs((target[n]-degree[n])/degree[n])
      picked=n
  return picked

#####################################################
def pick_arg_random(g,prefs,data):
  return random.sample(g.nodes,1)

#####################################################
def pick_arg_order(g,prefs,data):
  picked=data.get("picked",0)
  data["picked"]=(picked+1)%len(g.nodes)
  return picked  
