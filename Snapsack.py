from ortools.algorithms import pywrapknapsack_solver
import os
import errno
import time


class Utils:
    @staticmethod
    def writeListToFile(filename, list):
        with open(filename, 'a+') as f:
            f.write("[")
            for item in list:
                f.write("%s, " % item)
            f.write("]")

    @staticmethod
    def writeStringToFile(filename, string):
        with open(filename, 'a+') as f:
            f.write(str(string))

    @staticmethod
    def initFile(filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(filename, 'w') as f:
            f.write(str(""))


class TestCase:
    Type = ""
    data = []
    N = 0
    R = 0
    capacities = 0
    values = []
    weights = [[]]
    path = ""
    pathOutput = ""
    pathStatistic = ""

    def load(self, Type, N, R, S):
        # N=10, R=50,S=1
        # n00050, R01000, S=001.kp
        self.R = R
        self.Type = Type
        l1 = "/n{:05d}/".format(N)
        l2 = "R{:05d}/".format(R)
        l3 = "s{:03d}.kp".format(S)
        self.path = "Test Cases/"+Type+l1+l2+l3
        self.pathOutput = "Result/"+Type+l1+l2+l3
        self.pathStatistic = "Statistic/"+Type+".txt"
        with open(self.path) as level_file:
            rows = level_file.read().split('\n')
            self.data = rows
            self.N = rows[1]
            self.capacities = rows[2]
            index = 3
            self.values = []
            self.weights[0] = []
            while (index < len(rows)):
                if(rows[index] != ""):
                    item_infor = rows[index].split(" ")
                    self.values.append(int(item_infor[0]))
                    self.weights[0].append(int(item_infor[1]))
                index = index+1
        # print(self.values);
        # print(self.weights);

    def output(self, computed_value, total_weight, packed_items, packed_weights, time_consuming):
        Utils.initFile(self.pathOutput)
        Utils.writeStringToFile(filename=self.pathStatistic, string=str(self.Type)+"\t"+str(self.N)+"\t"+str(
            self.R)+"\t"+str(self.capacities)+"\t"+str(total_weight)+"\t"+str(computed_value)+"\t"+str(time_consuming)+"\t")
        # Utils.writeListToFile(filename=self.pathStatistic,list=self.values)
        # Utils.writeStringToFile(filename=self.pathStatistic,string="\t")
        # Utils.writeListToFile(filename=self.pathStatistic,list=self.weights[0])
        # Utils.writeStringToFile(filename=self.pathStatistic,string="\t")
        # Utils.writeListToFile(filename=self.pathStatistic,list=packed_items)
        # Utils.writeStringToFile(filename=self.pathStatistic,string="\t")
        # Utils.writeListToFile(filename=self.pathStatistic,list=packed_weights)
        Utils.writeStringToFile(filename=self.pathStatistic, string="\n")

        Utils.writeStringToFile(filename=self.pathOutput,
                                string="N: " + str(self.N) + "\n")
        Utils.writeStringToFile(filename=self.pathOutput,
                                string="R: " + str(self.R) + "\n")
        Utils.writeStringToFile(
            filename=self.pathOutput, string="Capacities: " + str(self.capacities) + "\n")
        Utils.writeStringToFile(filename=self.pathOutput, string="------\n")
        Utils.writeStringToFile(
            filename=self.pathOutput, string="Total value: ")
        Utils.writeStringToFile(
            filename=self.pathOutput, string=computed_value)
        Utils.writeStringToFile(filename=self.pathOutput,
                                string="\nTotal weight: ")
        Utils.writeStringToFile(filename=self.pathOutput, string=total_weight)
        Utils.writeStringToFile(filename=self.pathOutput,
                                string="\nPacked Items: ")
        Utils.writeListToFile(filename=self.pathOutput, list=packed_items)
        Utils.writeStringToFile(filename=self.pathOutput,
                                string="\nPacked Weights: ")
        Utils.writeListToFile(filename=self.pathOutput, list=packed_weights)
        Utils.writeStringToFile(filename=self.pathOutput,
                                string="\nTime Consuming: ")
        Utils.writeStringToFile(
            filename=self.pathOutput, string=time_consuming)


def solveProblem(Type, N, R, S):
    testcase = TestCase()
    testcase.load(Type, N, R, S)
    values = testcase.values
    weights = testcase.weights
    capacities = [int(testcase.capacities)]
    start = time.time()
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    solver.set_time_limit(60)
    solver.Init(values, weights, capacities)
    print("start")
    computed_value = solver.Solve()
    print("end")
    time_consuming = time.time() - start
    # isOptimal = solver.IsSolutionOptimal();

    packed_items = []
    packed_weights = []
    total_weight = 0
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    # print('Total value =', computed_value)
    testcase.output(computed_value, total_weight, packed_items,
                    packed_weights, time_consuming)


def main():
    listN = [50, 100, 200, 500, 1000, 2000, 5000, 10000]
    listR = [1000, 10000]
    listType = [
        "00Uncorrelated",
        "01WeaklyCorrelated",
        "02StronglyCorrelated",
        "03InverseStronglyCorrelated",
        "04AlmostStronglyCorrelated",
        "05SubsetSum",
        "06UncorrelatedWithSimilarWeights",
        "07SpannerUncorrelated",
        "08SpannerWeaklyCorrelated",
        "09SpannerStronglyCorrelated",
        "10MultipleStronglyCorrelated",
        "11ProfitCeiling",
        "12Circle",
    ]

    typeIndex = int(input("please input:"))
    while typeIndex < len(listType):
        type = listType[int(typeIndex)]
        typeIndex += 1
        pathStatistic = "Statistic/"+type+".txt"
        Utils.initFile(pathStatistic)
        Utils.writeStringToFile(
            filename=pathStatistic, string="Type\tN\tR\tCapacities\tTotal Weight\tComputed Value\tTime Consuming\n")

        print(pathStatistic)
        for n in listN:
            for r in listR:
                for s in range(5):
                    solveProblem(type, n, r, s)
                Utils.writeStringToFile(
                    filename=pathStatistic, string="\n")
                # break;
            # break;

    solveProblem("04AlmostStronglyCorrelated", 50, 10000, 0)


main()

testcase = TestCase()
