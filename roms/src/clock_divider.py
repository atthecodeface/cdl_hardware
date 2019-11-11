class diff:
    def __init__(self, add, sub):
        self.add=add
        self.sub=sub
        pass
    def value(self):
        return self.add / (self.add+self.sub+0.)
    def add_diff(self, other):
        return diff(self.add+other.add, self.sub+other.sub)
def find_best_differential(target, max_add, max_subtract, accuracy=0.001):
    upper = diff(1,0)
    lower = diff(0,1)
    mid = diff(1,int(target-1))
    while True:
        best_mid = mid
        error = mid.value()*target - 1
        if abs(error) < accuracy: break
        if error<0: # next step between mid and upper
            lower = mid
            mid = mid.add_diff(upper)
            pass
        else:  # next step between mid and lower
            upper = mid
            mid = mid.add_diff(lower)
            pass
        if (mid.add > max_add) or (mid.sub > max_subtract): break
        pass
    mis = best_mid
    print "Best differential for",target,"of",mid.add, mid.sub, mid.value(), 1/mid.value()
    return (mid.add, mid.sub)

def config_for_value(d, accuracy=0.00005):
    def get_err(add,sub):
        actual = (add+sub) / (add+0.)
        return abs(actual-d)/d
    d_int = int(d-1)
    err = get_err(1,d_int)
    if err<accuracy: return d_int
    (add,sub) = find_best_differential(d, max_add=65535, max_subtract=32767, accuracy=accuracy)
    return (1<<31) | (add<<16) | sub

def config_for_frequency(f, clk=100, accuracy=0.005):
    ns_per_clk = 1000. / clk
    ns_per_f   = 1000. / f
    divider_value = ns_per_f / ns_per_clk
    return config_for_value(divider_value, accuracy)
