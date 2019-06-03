import cProfile,  pstats, io, math
from pstats import SortKey

if __name__=='__main__':
    pr=cProfile.Profile()
    pr.enable()
    for i in range(1,1000):
        for j in range(1,10000):
            x= math.sqrt(i*j)
        y=x
    pr.disable()

    pr.print_stats()

    s = io.StringIO ()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats (pr, stream=s).sort_stats (sortby)
    ps.print_stats ()
    print (s.getvalue ())



