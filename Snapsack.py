from ortools.algorithms import pywrapknapsack_solver
import os
import errno

class Utils:
    @staticmethod
    def writeListToFile(filename,list):
        with open(filename, 'a+') as f:
            f.write("[")
            for item in list:
                f.write("%s, " % item)
            f.write("]\n")

    @staticmethod
    def writeStringToFile(filename,string):
        with open(filename, 'a+') as f:
            f.write(str(string))

class TestCase:
    data=[]
    N=0
    R=0
    capacities=0
    values=[]
    weights=[[]]
    path=""
    pathOutput=""
    

    def load(self,Type,N,R,S):
        #N=10, R=50,S=1
        #n00050, R01000, S=001.kp
        self.R=R
        l1="/n{:05d}/".format(N);
        l2="R{:05d}/".format(R);
        l3="S{:03d}.kp".format(S);
        self.path = "Test Cases/"+Type+l1+l2+l3;
        self.pathOutput = "Result/"+Type+l1+l2+l3;
        with open(self.path) as level_file:
            rows = level_file.read().split('\n')
            self.data= rows;
            self.N = rows[1]
            self.capacities=rows[2]
            index = 3
            while (index < len(rows)):
                if(rows[index]!=""):
                    item_infor = rows[index].split(" ");
                    self.values.append(int(item_infor[0]));
                    self.weights[0].append(int(item_infor[1]));
                index = index+1;
    
    
    def output(self,computed_value,total_weight,packed_items,packed_weights):
        if not os.path.exists(os.path.dirname(self.pathOutput)):
            try:
                os.makedirs(os.path.dirname(self.pathOutput))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(self.pathOutput, 'w') as f:
            f.write(str("Solution \n"))
        Utils.writeStringToFile(filename=self.pathOutput,string="N: " + str(self.N)+ "\n")
        Utils.writeStringToFile(filename=self.pathOutput,string="R: " + str(self.R)+ "\n")
        Utils.writeStringToFile(filename=self.pathOutput,string="Capacities: " + str(self.capacities) + "\n")
        Utils.writeStringToFile(filename=self.pathOutput,string="------\n")
        Utils.writeStringToFile(filename=self.pathOutput,string="Total value: ")
        Utils.writeStringToFile(filename=self.pathOutput,string=computed_value)
        Utils.writeStringToFile(filename=self.pathOutput,string="\nTotal weight: ")
        Utils.writeStringToFile(filename=self.pathOutput,string=total_weight)
        Utils.writeStringToFile(filename=self.pathOutput,string="\nPacked Items: ")
        Utils.writeListToFile(filename=self.pathOutput,list=packed_items)
        Utils.writeStringToFile(filename=self.pathOutput,string="Packed Weights: ")
        Utils.writeListToFile(filename=self.pathOutput,list=packed_weights)

def solveProblem(Type,N,R,S):
    testcase = TestCase();
    testcase.load(Type,N,R,S);
    values = testcase.values;
    weights = testcase.weights;
    capacities = [int(testcase.capacities)]

    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    solver.Init(values, weights, capacities)
    solver.set_time_limit(1);
    computed_value = solver.Solve()
    # isOptimal = solver.IsSolutionOptimal();
    packed_items = []
    packed_weights = []
    total_weight = 0
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print('Total value =', computed_value)
    testcase.output(computed_value,total_weight,packed_items,packed_weights);


def main():
    listN = [50,100,200,500,1000,2000,5000,1000]
    listR = [1000,10000]
    listType=[
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
    for type in listType:
        for n in listN:
            for r in listR:
                solveProblem(type,n,r,0);

    

main()

testcase = TestCase();


