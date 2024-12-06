import pyoptquest
import math
import matplotlib.pyplot as plt

# Tell pyoptquest where the jar is. This initializes the JVM and creates all COptQuestClasses
pyoptquest.InitializeOptQuest(r'optquest.jar')


def Evaluate(var1, var2, response, uncertainty):
    # The function evaluated each iteration for optimization
    # Must have the call signature (sol)
    # This is done as a nested fuction to show how state can be stored between calls
    _var1 = var1
    _var2 = var2
    _response = response
    _uncertainty = uncertainty

    def _Evaluate(sol):
        # get the values OptQuest provides for this run
        val1 = sol.GetVariableValue(_var1)
        val2 = sol.GetVariableValue(_var2)

        r = math.sqrt(val1**2 + val2**2)
        p = (1 + math.cos(r)) / 2
        u = math.sqrt(p * (1 - p))
        sol.SetObjectiveValue(_response, p)
        sol.SetObjectiveValue(_uncertainty, u)

    return _Evaluate


# use MonitorStatus to incremntally accumulat the results
# we could do something more interesting here if we wanted to
def MonitorStatus(var1, var2, response, uncertainty, x, y, z, e):
    _var1 = var1
    _var2 = var2
    _response = response
    _uncertainty = uncertainty
    _x = x
    _y = y
    _z = z
    _e = e

    def _MonitorStatus(sol):
        _x.append(sol.GetVariableValue(_var1))
        _y.append(sol.GetVariableValue(_var2))
        _z.append(sol.GetObjectiveValue(_response))
        _e.append(sol.GetObjectiveValue(_uncertainty))

    return _MonitorStatus


# define variables
var1 = pyoptquest.COptQuestContinuousVariable('var1', -20, 20)
var2 = pyoptquest.COptQuestContinuousVariable('var2', -20, 20)

# define objective(s)
response = pyoptquest.COptQuestUserControlledObjective("Response")
uncertainty = pyoptquest.COptQuestUserControlledObjective("Uncertainty")

# a metric is a paired objective
metric = pyoptquest.COptQuestHeatmapObjective()
metric.AddObjective(response, uncertainty, True)

# lists to store the incremental results
x = []
y = []
z = []
e = []

# create the object needed to callbacks for evaluation
evaluator = pyoptquest.COptQuestOptimizationEvaluator(Evaluate(var1, var2, response, uncertainty), MonitorStatus(var1, var2, response, uncertainty, x, y, z, e))

# change search parameters
search = pyoptquest.COptQuestSearchParameters()

# creates the optimization object
optimization = pyoptquest.COptQuestOptimization(evaluator)  # initialize the optimizer with the evaluator
optimization.SetMetaHeuristic(pyoptquest.SampleMethods.SAMPLE | pyoptquest.SampleMethods.MAX_VARIANCE)

# set up the optimization
optimization.SetLicenseID(999999999)  # trial license
optimization.AddVariable(var1)
optimization.AddVariable(var2)
optimization.AddObjective(metric)

# set stopping condition and optimize
optimization.SetMaximumIterations(300)
optimization.Optimize()

# plot the results
plt.scatter(x, y, c=z)
plt.show()
