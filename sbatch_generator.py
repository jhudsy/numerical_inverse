semantics=["hcat","mbs","card"]
strategies=["pick_arg_most_to_least_pref","pick_arg_least_to_most_pref","pick_arg_largest_to_smallest_error","pick_arg_smallest_to_largest_error","pick_arg_order"]
graph_generators=["nx.generators.erdos_renyi_graph(%s,p=0.1,seed=i,directed=True)","nx.generators.erdos_renyi_graph(%s,p=0.3,seed=i,directed=True)","nx.generators.erdos_renyi_graph(%s,p=0.5,seed=i,directed=True)","nx.generators.erdos_renyi_graph(%s,p=0.7,seed=i,directed=True)","nx.generators.directed.scale_free_graph(%s,seed=i)","nx.generators.complete_graph(%s,nx.DiGraph())"]

j=0
for s in semantics:
        for t in strategies:
                for g  in graph_generators:
                        for i in [10,100,2000]:
                                with open(f"{s}_{t}_{g}_{i}_w.job","w") as f:
                                    f.write("#!/bin/bash\n")
                                    f.write(f"python3 run_test.py {s} {t} set_initial_weights_{s} start_a_{s} {i} \"{g}\"\n")
                                with open(f"{s}_{t}_{g}_{i}_d.job","w") as f:
                                    f.write("#!/bin/bash\n")
                                    f.write(f"python3 run_test.py {s} {t} set_initial_weights_{s} start_a_default {i} \"{g}\"\n")
