import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys
import json



def graphiqueQuality(argv):
    # algorithms = {}

    with open("algorithms.json".format(), 'r') as json_file:
        data = json.load(json_file)
        algorithms = data['algorithms']

    for algorithm in algorithms

    fig = plt.figure()
    x = [1,2,3,4,5,6,7,8,9,10]
    height = [8,12,8,5,4,3,2,1,2,4]
    width = 0.05
    BarName = ['a','b','c','d','e','f','g','h','i','j']

    plt.bar(x, height, width, color=(0.65098041296005249, 0.80784314870834351, 0.89019608497619629, 1.0) )
    plt.scatter([i+width/2.0 for i in x],height,color='k',s=40)

    plt.xlim(0,11)
    plt.ylim(0,14)
    plt.grid()

    plt.ylabel('Counts')
    plt.title('Diagramme en Batons !')

    pylab.xticks(x, BarName, rotation=40)

    # plt.savefig('SimpleBar.png')
    plt.show()


def graphiqueComplexity(argv):
    print("test")


def main(argv):
    if argv[0] == "0":
        graphiqueQuality(argv)
    if argv[0] == "1":
        graphiqueComplexity(argv)

if __name__ == "__main__":
    main(sys.argv[1:])