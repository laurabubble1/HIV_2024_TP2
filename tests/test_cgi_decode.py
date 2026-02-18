from poly_fuzzer.fuzzers.cgi_fuzzer import CGIFuzzer
from poly_fuzzer.power_schedules.cgi_schedule import CGIPowerSchedule
from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.common.abstract_grammar import AbstractGrammar
from poly_fuzzer.common.abstract_executor import AbstractExecutor
from cgi_decode import cgi_decode



CGI_GRAMMAR = AbstractGrammar({
    "<start>": ["<cgi-input>"],
    "<cgi-input>": ["<param>=<value>", "<param>=<value>&<cgi-input>"],
    "<param>": ["name", "id", "search", "query"],
    "<value>": ["<chars>"],
    "<chars>": ["<char>", "<char><chars>"],
    "<char>": ["A", "B", "C", "D", "E", "+", "%20", "%3F", "%", "%GG"],
})

SEEDS = [
    AbstractSeed("+"),
    AbstractSeed("hello+world"),
    AbstractSeed("hello%20world"),
    AbstractSeed("%3F"),
    AbstractSeed("%"),
    AbstractSeed("%GG"),
]
def test_cgi_fuzzer(test_module):
    # Test with power schedule and grammar
    executor = AbstractExecutor(test_module)
    power_schedule = CGIPowerSchedule()
    fuzzer = CGIFuzzer(executor, SEEDS, power_schedule=power_schedule, grammar=CGI_GRAMMAR)

    output = fuzzer.run_fuzzer(budget=100)
    assert output is not None
    print("CGI Fuzzer Output with power schedule and grammar:")
    print(output)
    return output

def test_cgi_fuzzer_no_power_schedule(test_module):
    # Test with grammar but no power schedule
    executor = AbstractExecutor(test_module)
    fuzzer_no_power = CGIFuzzer(executor, SEEDS, grammar=CGI_GRAMMAR)
    output_no_power = fuzzer_no_power.run_fuzzer(budget=100)
    assert output_no_power is not None
    print("CGI Fuzzer Output without power schedule:")
    print(output_no_power)
    return output_no_power
    
def test_cgi_fuzzer_no_grammar(test_module):
    # Test without grammar but with power schedule
    executor = AbstractExecutor(test_module)
    power_schedule = CGIPowerSchedule()

    fuzzer_no_grammar = CGIFuzzer(executor, SEEDS, power_schedule=power_schedule)
    output_no_grammar = fuzzer_no_grammar.run_fuzzer(budget=100)
    assert output_no_grammar is not None
    print("CGI Fuzzer Output without grammar but with power schedule:")
    print(output_no_grammar)
    return output_no_grammar



# Print mean of ten execution times and coverages for each configuration
import matplotlib.pyplot as plt
import numpy as np
test_module = cgi_decode
outputs_power_grammar = []
outputs_no_power = []
outputs_no_grammar = []

for _ in range(10):
    output_power_grammar = test_cgi_fuzzer(test_module)
    output_no_power = test_cgi_fuzzer_no_power_schedule(test_module)
    output_no_grammar = test_cgi_fuzzer_no_grammar(test_module)
    outputs_power_grammar.append(output_power_grammar)
    outputs_no_power.append(output_no_power)
    outputs_no_grammar.append(output_no_grammar)


if not outputs_power_grammar or not outputs_no_power or not outputs_no_grammar:
    raise RuntimeError("No fuzzer outputs were collected.")

mean_power_grammar = {
    "execution_times": np.mean(
        np.array([out["execution_times"] for out in outputs_power_grammar]), axis=0
    ),
    "coverage": np.mean(
        np.array([out["coverage"] for out in outputs_power_grammar]), axis=0
    ),
}
mean_no_power = {
    "execution_times": np.mean(
        np.array([out["execution_times"] for out in outputs_no_power]), axis=0
    ),
    "coverage": np.mean(
        np.array([out["coverage"] for out in outputs_no_power]), axis=0
    ),
}
mean_no_grammar = {
    "execution_times": np.mean(
        np.array([out["execution_times"] for out in outputs_no_grammar]), axis=0
    ),
    "coverage": np.mean(
        np.array([out["coverage"] for out in outputs_no_grammar]), axis=0
    ),
}

plt.figure(figsize=(12, 5))

plt.plot(mean_power_grammar["coverage"], label='Power Schedule + Grammar')
plt.plot(mean_no_power["coverage"], label='No Power Schedule')
plt.plot(mean_no_grammar["coverage"], label='No Grammar')
plt.title("Mean Coverage")
plt.xlabel("Input Index")
plt.ylabel("Coverage (lines)")
plt.legend()
plt.show()








