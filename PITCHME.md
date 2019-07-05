# The DATA Project

---

# Summary:

1. The problem
2. Google's solution
3. Our tools
4. Our researches
5. Live demonstration
6. Sum up

---

# The problem

+++

![cvrp](https://developers.google.com/optimization/images/routing/cvrp.svg)

+++

![cvrp_solution](https://developers.google.com/optimization/images/routing/cvrp_solution.svg)

---

# Google's solution

## OR-Tools

![orLogo](https://developers.google.com/optimization/images/orLogo.png)

+++

Open source software for combinatorial optimization.

- Vehicle routing
- Scheduling
- Bin packing

Note:

- Vehicle routing: Find optimal routes for vehicle fleets that pick up and deliver packages given constraints (e.g., "this truck can't hold more than 20,000 pounds" or "all deliveries must be made within a two-hour window").
- Scheduling: find the optimal schedule for complex set of tasks, some of which need to be performed before others, on a fixed set of machines, or other resources.
- Bin packing: pack as many objects of various sizes as possible into a fixed number of bins with maximum capacities.

+++

The intersting part

```python
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    ...
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        data['vehicle_capacities'],
        True,
        'Capacity')

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    assignment = routing.SolveWithParameters(search_parameters)
```

@[1-2](manager)
@[4-9](dimension)
@[12-13](strategy)
@[15](solver)

Note:

- The index manager keeps track of the solver's internal variables corresponding to locations
- The routing solver uses an object called a dimension to keep track of quantities that accumulate along a vehicle's route

+++

### Solver

![guidedLocalSearch](https://www.researchgate.net/profile/Sergio_Consoli/publication/49399511/figure/fig7/AS:644639283503106@1530705390538/Guided-Local-Search-strategy-escaping-from-traps-increasing-the-relative-objective.png)

---

# Our tools

+++

## Manage dataset

- Generate
- Import
- Export

+++

## Manage solutions

- Generate
- Import
- Export

+++

## Find a complexity

+++

## Visualize the solution

- Graph
- Graph without depot
- Quality chart

+++

## Stats

- Show scatter plot
- Show uniformity

+++

![graph](https://raw.githubusercontent.com/Exia-Aix-2016/Data-Project/master/screenshots/graphs/guided_local_search.png)

+++

![graph_no_depot](https://raw.githubusercontent.com/Exia-Aix-2016/Data-Project/master/screenshots/graphs_no_depot/guided_local_search.png)

---

# Our researches

+++

![scatter](https://raw.githubusercontent.com/Exia-Aix-2016/Data-Project/master/screenshots/scatter_plot/distance/guided_local_search.png)

+++

![complexity](https://raw.githubusercontent.com/Exia-Aix-2016/Data-Project/master/screenshots/complexity.png)

+++

![quality](https://raw.githubusercontent.com/Exia-Aix-2016/Data-Project/master/screenshots/chart_quality.png)

---

# Live demo

---

# Sum up

- Existing tooling: OR-Tools
- Creation of Command Line Interface
- Choice of algorithm: Heuristic vs Metaheuristic
