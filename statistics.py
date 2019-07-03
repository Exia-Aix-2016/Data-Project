

def solution_stat(solution):
    return {
        "execution_time": solution["execution_time"],
        "distance": solution["total_distance"],
        "trucks": len(list(filter(lambda x: x["distance"] > 0, solution["vehicles"])))
    }


def config_stat(solution_stats, generator):
    return {
        "cities": generator.cities,
        "stats":  solution_stats
    }
