def dda_of_ratio(r):
    if r is None: return (0,0)
    (n,d) = r
    dda_add = n-1
    dda_sub = d-2-dda_add
    return (dda_add, dda_sub)
    
def find_closest_ratio(f, max):
    def ratio_compare(f, r):
        (n,d) = r
        diff = f*d - n
        if abs(diff)<1.0/max/3: return 0
        if diff<0: return -1
        return 1
    must_be_above = (0, 1)
    must_be_below = (1, 0)
    while True:
        ratio_to_test = (must_be_below[0] + must_be_above[0],
                         must_be_below[1] + must_be_above[1])
        (dda_add, dda_sub) = dda_of_ratio(ratio_to_test)
        if (dda_add>=max) or (dda_sub>=max):
            break
        c = ratio_compare(f,ratio_to_test)
        if (c==0): return ratio_to_test
        if (c==1):
            must_be_above = ratio_to_test
            pass
        else:
            must_be_below = ratio_to_test
            pass
        pass
    if must_be_above[0]==0: return None
    return must_be_above
                     
def clock_timer_adder_bonus(ns):
    ns_times_16 = (16.0*ns+1E-16)
    adder = int(ns_times_16)
    bonus = ns_times_16 - adder
    bonus = find_closest_ratio(bonus, 256)
    bonus = dda_of_ratio(bonus)
    adder = (adder/16, adder%16)
    #print "Adder and bonus for %f is %s, %s"%(ns, str(adder), str(bonus))
    return (adder, bonus)

def clock_timer_period(adder, bonus):
    ns_times_16 = adder[0]*16 + adder[1]
    if (bonus[0]==0) and (bonus[1]==0):
        bonus=0.
    else:
        bonus = (bonus[0]+1.) / (bonus[0] + bonus[1] + 2)
        pass
    return (ns_times_16 + bonus) / 16.0
