

def solution_stat(solution):
    result = {
        "execution_time": 0,
        "distance": 0,
        "trucks": 0
    }
    result["distance"] = solution["total_distance"]
    result["execution_time"] = solution["execution_time"]

    for vehicle in solution["vehicles"]:
        if vehicle["distance"] > 0:
            result["trucks"] += 1
    return result
