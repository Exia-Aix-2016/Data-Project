from subprocess import Popen, PIPE, STDOUT


def stdOutput_catching(procName, argv, logfile):
    proc = Popen(['py', procName] + [argv[0], str(argv[1])],
                 stdout=PIPE, stderr=STDOUT, close_fds=True)

    output = proc.stdout.read()
    return output


logfile = open("log.txt", "w")
result = stdOutput_catching('cvrp.py', ['small', 0], logfile)
print(result)
