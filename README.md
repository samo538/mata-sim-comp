# Reduction benchmarking

This benchmark aims to compare 4 reduction algorithms for nfa.

The compared algorithms are: Hopcroft, Brzozowski, Simulation, Residual.
They are implemented in Mata (https://github.com/VeriFIT/mata)

The main metrics are speed, number of states and number of transitions in
the resulting automaton

# Instalation

Firstly, benchmarks need to be compiled

```
cd src
make
```

# How to evaluate
I am using pycobench to evaluate the algortihm.
To evaluate speed:
```
./pycobench -c input/bench-reduction.yaml -m [algorithm] -o results/output.out < input/single-automata.input
```
instead of `[algorithm]` write the name of the algorithm you want to benchmark

# How to parse the output
Pycobench output may not be in optimal format. Parsing the output:
```
cd results
../pyco_proc --csv output.out > result.csv
```

# Visualising the output

TODO
