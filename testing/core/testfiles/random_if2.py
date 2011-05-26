import pystoch
from pystoch import flip, MetropolisHastings

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        if flip(0.7):
            return flip(0.2)
        else:
            return flip(0.8)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = 0.7*0.2 + 0.3*0.8

