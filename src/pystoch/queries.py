import erps
import numpy as np
from pystoch.exceptions import TraceInvalidatedException

def random(func):
    func.random = True
    return func

class RejectionQuery(object):
    global random

    def __init__(self):
        pass

    @random
    def run(self, PYSTOCHOBJ=None):
        test = False
        while (not test):
            PYSTOCHOBJ.clear_trace()
            PYSTOCHOBJ.db = {}
            PYSTOCHOBJ.call(self.query_model)
            test = PYSTOCHOBJ.call(self.condition)

        return PYSTOCHOBJ.call(self.sample)

class MetropolisHastings(object):
    global random

    def __init__(self):
        pass

    @random
    def init_rejection_query(self, PYSTOCHOBJ):
        print "Initializing...",
        test = False
        while (not test):
            PYSTOCHOBJ.clear_trace()
            PYSTOCHOBJ.db = {}
            PYSTOCHOBJ.call(self.query_model)
            test = PYSTOCHOBJ.call(self.condition)
        print "Done"

    def do_trace_update(self, func, db, PYSTOCHOBJ):
        trace_loglh, db, trace = PYSTOCHOBJ.trace_update(func, db)
        if not PYSTOCHOBJ.call(self.condition):
            trace_loglh = -np.inf
        return trace_loglh, db, trace

    @random
    def run(self, num_samples, num_steps, PYSTOCHOBJ=None):
        """Take samples from the MCMC trace sampler.

        Paramters
        ---------
        num_samples : int
            The number of samples to take
        num_steps : int
            The number of traces to accept between taking samples
        PYSTOCHOBJ : pystoch.PyStochObj
            The PYSTOCHOBJ containing the trace state

        """

        num_traces = 0
        num_accepted = 0

        # initialize the database of randomness using a rejection
        # query; this starts off the MCMC from a state that we know is
        # acceptable
        trace_loglh, db, trace = self.do_trace_update(self.init_rejection_query, {}, PYSTOCHOBJ)
        sample = PYSTOCHOBJ.call(self.sample)

        # initialize the list of samples that we will return
        samples = []

        # loop over the number of samples that we want to take
        while num_samples > 0:
            # loop over the number of steps between samples
            steps = num_steps
            while steps > 0:

                # get the number of random variables and the list of
                # random variables used in the last trace
                num_rvs = PYSTOCHOBJ.num_rvs
                rvs = PYSTOCHOBJ.rvs

                print rvs
                
                # uniformly select a random choice
                name = rvs[np.random.randint(num_rvs)]
                
                # look up the erp type, the value, and likelihood, the
                # arguments, and the most recent trace that the random
                # choice was used in from the database
                erp, val, erp_loglh, args_db, trace = db[name]

                # propose a new value using the erp's proposal kernel
                new_val = erp.kernel(val, *args_db[0], **args_db[1])

                if new_val == val:
                    continue

                # using the proposed value, calculate the forward and
                # backward probability, as well as the log likelihood
                # for that probability
                forward = np.log(erp.kernel.prob(new_val, val, *args_db[0], **args_db[1]))
                backward = np.log(erp.kernel.prob(val, new_val, *args_db[0], **args_db[1]))
                new_erp_loglh = np.log(erp.prob(new_val, *args_db[0], **args_db[1]))

                # propose a new trace by creating a copy of the
                # current database, updating it with the new value and
                # log likelihood, and then updating the trace
                new_db = db.copy()
                new_db[name] = (erp, new_val, new_erp_loglh, args_db, trace)

                try:
                    new_trace_loglh, new_db, new_trace = self.do_trace_update(self.query_model, new_db, PYSTOCHOBJ)
                    # score the new trace
                    a = new_trace_loglh - trace_loglh + backward - forward

                    # print "ERP:", erp.__name__
                    # print "Old val:", val
                    # print "New val:", new_val
                    # print "Old erp likelihood", erp_loglh
                    # print "New erp likelihood", new_erp_loglh
                    # print "Old trace likelihood", trace_loglh
                    # print "New trace likelihood", new_trace_loglh
                    # print "a:", a
                    # print new_db

                except TraceInvalidatedException:
                    # changing the value of the ERP caused the program
                    # to become unrunnable, so reject this trace
                    a = -np.inf

                    print "trace invalidated"

                num_traces += 1

                # accept the new state
                if np.log(erps._uniform(0, 1)) < a:
                    
                    # set the database, trace number, and trace
                    # likelihood to the ones generated by the new
                    # trace
                    db = new_db
                    trace = new_trace
                    trace_loglh = new_trace_loglh
                    sample = PYSTOCHOBJ.call(self.sample)                    
                    
                    # clean out the database of stale values
                    db = self.clean_db(trace, db)
                    
                    num_accepted += 1
                    
                # update the number of steps we have to go
                steps -= 1

            # update the number of samples we still have to go, and
            # add the current sample to our list of samples
            num_samples -= 1
            samples.append(sample)

        if num_traces > 0:
            print "Average acceptance rate: %s%%" % (np.round(float(num_accepted) / num_traces, decimals=4)*100)
            
        return samples

    def clean_db(self, trace, db):
        for name in db.keys():
            if db[name][4] < trace:
                del db[name]

        return db

    run.random = True
