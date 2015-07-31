# USAGE: awk -f pyprofiler.py <py prog> <num data points>
# Runs a profiler on the python script, and formats the profiler output.
#
# The profielr ouput table has the following fields:
# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# 1       2        3        4        5       6
#
# This program outputs a table with the following fields:
# n ncalls tottime cumtime function

function filter(l, prog, rgx, n, m, a, b) {
    
    # Filters the output to chose lines matching functions names
    # specified in the regex 'rgx'. Neater function names are
    # extracted from the last field, a[n].

    n = split(l, a, " ")
    if (match(a[n], rgx)) {
	gsub(/[()]/, " ", a[n])
	m = split(a[n], b, " ")
	return sprintf("%d %5.3f %5.3f %s", a[1], a[2], a[4], b[m])
    }
    return ""
}

BEGIN{

    # Runs cProfile on the specified Python program 'prog', filters,
    # formats and prints its output as a compact table for easier
    # processing through R.
    
    prog  = ARGV[1]
    np    = ARGV[2]
    step  = 100
    n     = 100
    rgx   = "(f)|(f1)|(g)|(g1)|(h)"
    head  = "n ncalls  tottime cumtime function"
    printf("%s\n",head)
    while(n < np*(step+1)) {
	#print  "python -m cProfile " prog " " n
	cmd  = "python -m cProfile " prog " " n
	line = 1
	while ((cmd | getline var) > 0) {
	    if (line > 5 && var != "") {
		s = filter(var, prog, rgx)
		if (s) {
		    printf("%d %s\n", n, s)
		}
	    }
	    line++
	}
	close(cmd)
	n+=step
    }
}
