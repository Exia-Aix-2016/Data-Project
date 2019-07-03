import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys
import json



def graphiqueQuality(argv):
    with open("algorithms.json".format(), 'r') as json_file:
        data = json.load(json_file)
        algorithms = data['algorithms']
        
    trucks_fleet = 0
    trucks_used = 0
    total_distance = 0
    whole_distance = 0

    quality = []
    

    for algorithm in algorithms:
        with open("results/{}_{}.json".format(argv[1], algorithm), 'r') as json_file:
            data = json.load(json_file)
            trucks_fleet = int(data['trucks_fleet'])
            total_distance = int(data['total_distance'])
            
            for truck in data["vehicles"]:
                if(len(truck["route"]) > 1):
                    trucks_used += 1 
        
        with open("datasets/{}.json".format(argv[1]), 'r') as json_file:
            data = json.load(json_file)
            whole_distance = 0
            indexX = 0
            indexY = 0
            for i in data["distance_matrix"]:
                for j in i:
                    if indexX > indexY:
                        whole_distance += j
                    indexX += 1
                indexX = 0
                indexY += 1

        quality.append( (total_distance / whole_distance) * (trucks_used / trucks_fleet) )
        trucks_used = 0

    fig = plt.figure()
    x = [1,2,3]
    width = 0.5

    plt.bar(x, quality, width, color=(0.65098041296005249, 0.80784314870834351, 0.89019608497619629, 1.0) )
    #plt.scatter([i+width/2.0 for i in x],height,color='k',s=40)

    plt.xlim(0,4)
    plt.ylim(0,sorted(quality, reverse=True)[0] + sorted(quality, reverse=True)[0] * 0.1)
    #plt.grid()

    plt.title('Quality Diagram')

    pylab.xticks(x, algorithms, rotation=20)

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