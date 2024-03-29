import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import numpy as np
import pylab
import sys
import json
from scipy import interpolate
import random


class Chart:
    def __init__(self, store):
        self.store = store

    def norm(self, data):
        # y = (max(data)-min(data))
        mx = max(data)
        return list(map(lambda x: x/mx, data))

    def showQuality(self):
        quality = 0
        data = []
        qualities = []
        executionTimes = []
        trucks_useds = []
        total_distances = []

        whole_distance = 0
        indexX = 0
        indexY = 0
        for i in self.store.data["distance_matrix"]:
            for j in i:
                if indexX > indexY:
                    whole_distance += j
                indexX += 1
            indexX = 0
            indexY += 1

        for algo, solution in self.store.solutions.items():
            trucks_used = 0
            trucks_fleet = int(solution['trucks_fleet'])
            total_distance = int(solution['total_distance'])
            executionTime = int(solution['execution_time'])

            # CALCULE wholedistance & truckused
            for truck in solution["vehicles"]:
                if(len(truck["route"]) > 1):
                    trucks_used += 1

            quality = (total_distance / whole_distance) * \
                (trucks_used / trucks_fleet)

            qualities.append(quality)
            executionTimes.append(executionTime)
            trucks_useds.append(trucks_used)
            total_distances.append(total_distance)

        for q, e, tr, to in zip(self.norm(qualities), self.norm(executionTimes), self.norm(trucks_useds), self.norm(total_distances)):
            data.append([q, e, tr, to])

            # PRINT HISTO
        x = [0, 1, 2, 3]
        gap = .8 / len(data)
        # colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        #           for i in range(3)]
        colors = ["r", "g", "b"]
        for i, row in enumerate(data):

            X = np.arange(len(row))

            plt.bar(X + i * gap, row,
                    width=gap,
                    color=colors[i])
        pylab.xticks(x, ["quality", "executionTime",
                         "trucks_used", "total_distance"], rotation=20)
        plt.show()

    def showComplexity(self):

        for algorithm, values in self.store.complexity.items():
            x = []
            y = []
            for point in values:
                x.append(point['cities'])
                y.append(point['duration'])

            plt.plot(x, y, label=algorithm)

        plt.xlabel("Nodes")
        plt.ylabel("Time")
        plt.legend()

        plt.title('Complexity Diagram')
        plt.show()

    def showUniformity(self, config):
        x = []
        y = []
        i = 0

        for stat in config['stats']:
            i += 1
            x.append(i)
            y.append(stat['execution_time'])

        width = 0.5

        plt.bar(x, y, width, color=(0.65098041296005249,
                                    0.80784314870834351, 0.89019608497619629, 1.0))

        plt.xlim(0, len(x) + 1)
        plt.ylim(0, sorted(y, reverse=True)[0] * 1.1)

        plt.title('Uniformity Diagram')
        plt.ylabel("Time")

        average = np.mean(y)
        standard_deviation = np.std(y)
        variance = np.var(y)
        median = np.median(y)
        first_quartile = round(np.percentile(y, 25))
        third_quartile = round(np.percentile(y, 75))

        plt.legend(title="average: " + str(round(average, 2)) +
                   "\nstandard_deviation: " + str(round(standard_deviation, 2)) +
                   "\nvariance: " + str(round(variance, 2)) +
                   "\nmedian: " + str(round(median, 2)) +
                   "\nfirst_quartile: " + str(round(first_quartile, 2)) +
                   "\nthird_quartile: " + str(round(third_quartile, 2)))

        plt.show()

    def showScatterPlot(self, stat, variable):
        x = []
        y = []
        averageX = []
        averageY = []
        listY = []

        for bundles in stat:
            for bundle in bundles['stats']:
                x.append(bundles['cities'])
                y.append(bundle[variable])
                listY.append(bundle[variable])
            averageX.append(x[-1])
            averageY.append(np.mean(listY))
            listY.clear()

        spl = interpolate.UnivariateSpline(averageX, averageY, s=0)
        xs = np.linspace(min(averageX), max(averageX) * 1.5, 1000)
        plt.plot(xs, spl(xs), 'b', lw=3)

        plt.scatter(x, y, c='r')

        plt.xlabel('Cities')
        plt.ylabel(variable)
        plt.title('Scatter Plot Diagram')

        plt.show()
