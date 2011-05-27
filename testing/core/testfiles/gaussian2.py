import pystoch
from pystoch import gaussian, MetropolisHastings

mean = 1.0
std = 0.5

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        return gaussian(mean, std)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = mean
