def check_for_convergence(prefs,degrees,epsilon):
  """checks whether we can stop iterating as the change in degree is smaller than epsilon, or the weights we have obey the required preference ordering.
  Input: prefs is a list of lists representing the preferences over arguments; anything in the same list is equally preferred. The first list is the most preferred argument. Checks for epsilon are relative to the degree"""
  cur=degrees[list(prefs[0])[0]]

  for p2 in list(prefs[0])[1:]:
        if abs(cur-degrees[p2])/degrees[p2]>epsilon:
          return False

  for ps in prefs[1:]:
        p=list(ps)
        for p2 in p[1:]:
                if degrees[p2]-cur>0:
                        return False
                if abs(degrees[p[0]]-degrees[p2])/degrees[p2]>epsilon:
                        return False
        cur=degrees[p[0]]

  return True


#####################################################

def bisect(g,arg,target,iters,epsilon,semantics,start_a):
  """runs iters iterations of the bisection method over graph g for argument arg,
  with a target value of target.
  Epsilon is the permitted relative difference between min and max for early
   termination.
   Finally, semantics is the function used to compute the semantics.
   start_a is the initial value given to a

   a is the upper bound
   b the lower bound
   """
  a=start_a#min(1,target+target*g.in_degree(arg)) #N.B., h-cat dependent; FIX ME
  b=target
  #mid = g.nodes[arg]["weight"] #preinitialise the midpoint
  #if a<mid or b>mid:
  mid=(a+b)/2

  for i in range(iters):
    hca=semantics(g)[arg]
    if hca>target:
      a=mid
    elif hca<target:
      b=mid
    else: #found target, return
      a=mid
      b=mid
    mid=(a+b)/2
    g.nodes[arg]["weight"]=mid
    if (a-b)/b<epsilon:
      return

#####################################################
def compute_weights(g,prefs,zeta,pick_arg_strategy,semantics,set_initial_weights,start_a,iters=1000,epsilon=0.001,max_error=0.001,max_iters=1000,timeout_iters_value=10000):
  """g a graph
    prefs a list of list of preferences
    zeta the fudge factor used when setting target values h-cat dependent, fix
    pick_arg_strategy the strategy used to pick arguments
    semantics the semantics we use to compute degree
    set_initial_weights the semantics related way to set target weights
    start_a allows us to identify the top bound of the bisection method
    iters the number of iterations used by the bisection method
    epsilon the epsilon used in the bisection method
    max_error the maximum error used for determining early termination
    max_iters the maximum number of times we can call the bisection method
    timeout_iters_value the value returned if we time out based on max_iters
  """
  target=set_initial_weights(g,prefs,zeta)
  finished=False
  data={"target":target,"max_error":max_error}
  tot_iters=0
  deg=semantics(g)
  data["degree"]=deg
  while not finished:
   if check_for_convergence(prefs,deg,max_error): #early termination based on preferences being ok
           finished=True
           #print("early termination")
           break
   tot_iters+=1
   arg=pick_arg_strategy(g,prefs,data)
   if arg!=-1:
     bisect(g,arg,target[arg],iters,epsilon,semantics,start_a(target[arg],g,arg,zeta))
   deg=semantics(g)
   data["degree"]=deg
   finished=True
   for a in g:
     if abs(target[a]-deg[a])/deg[a]>max_error:
       finished=False
   if tot_iters>=max_iters: #timeout condition
     tot_iters=timeout_iters_value
     print("timeout")
     finished=True
  return tot_iters
