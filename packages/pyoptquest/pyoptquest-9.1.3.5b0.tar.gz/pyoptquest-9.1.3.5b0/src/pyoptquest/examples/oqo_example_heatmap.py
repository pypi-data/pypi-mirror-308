from matplotlib import pyplot as plt
import math

from pyoptquest import OptQuestOptimizer, SampleMethods

# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -20, 'max': 20},
    'y': {'type': 'continuous', 'min': -20, 'max': 20}
}

# define the output(s)
output_space = ['p', 'u']

# define the objective(s)
objectives = {
    'metric': {'type': 'min', 'expression': 'p', 'uncertainty_expression': 'u'},
}

# evaluate the outputs


def evaluator(inputs):
    x = inputs['x']
    y = inputs['y']
    r = math.sqrt(x**2 + y**2)
    p = (1 + math.cos(r)) / 2
    u = math.sqrt(p * (1 - p))
    outputs = {'p': p, 'u': u}
    return outputs


# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    output_space=output_space,
    evaluator=evaluator,
    sample_method=SampleMethods.STOCHASTIC | SampleMethods.ROOT_FINDER,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')

# do the optimization
opt.search(n_iter=1000, parallel_evaluators=20)

# plot the results
plt.scatter(opt.search_data['x'], opt.search_data['y'], c=opt.search_data['p'])
plt.show()
