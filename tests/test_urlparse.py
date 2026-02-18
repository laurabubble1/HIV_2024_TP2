from urllib.parse import urlparse

from poly_fuzzer.fuzzers.url_fuzzer import URLFuzzer
from poly_fuzzer.power_schedules.url_schedule import URLPowerSchedule
from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.common.abstract_grammar import AbstractGrammar
from poly_fuzzer.common.abstract_executor import AbstractExecutor


URL_GRAMMAR = AbstractGrammar({
    "<start>": ["<scheme><domain><path><query>"],
    "<scheme>": ["http://", "https://", "ftp://"],
    "<domain>": ["<subdomain>.<tld>", "<host>"],
    "<subdomain>": ["www", "api", "mail", "test"],
    "<host>": ["example", "localhost", "google", "github"],
    "<tld>": ["com", "org", "net", "io", "dev"],
    "<path>": ["", "/<segment>", "/<segment>/<segment>"],
    "<segment>": ["index", "api", "search", "user", "product"],
    "<query>": ["", "?<param>", "?<param>&<param>"],
    "<param>": ["q=<value>", "id=<number>", "type=<word>"],
    "<value>": ["search", "query", "test"],
    "<word>": ["user", "admin", "guest", "product"],
    "<number>": ["1", "2", "123", "456", "789"],
})

SEEDS = [
    AbstractSeed("http://mlp.com/"),
    AbstractSeed("https://test.com/index.html?q=hello"),
    AbstractSeed("http://localhost/search?id=123&type=test"),
    AbstractSeed(""),
    AbstractSeed("www.example.org:8080/"),
    AbstractSeed("vf9tepQ://HA[}g^o:t@O]6og}glcR$e/K6^6.-9f,if?wKn(kCex|!sc<d/api"),
    AbstractSeed("http://www.dev.net/user/profile?id=456"),
    AbstractSeed("https://api.io/product?id=789&type=product"),
    AbstractSeed("\'f}CV%ki&\\[9/w/fVvU;o?yfcATDsstpVR\\r]WA-tMUJ2L#eNrO(;@E :C=tUu1kh=}1t%kKX-7utPx&DzMLdzx\"hkX_#"),
    AbstractSeed("google.com")
]

def test_url_fuzzer(test_module):
    # Test with power schedule and grammar
    executor = AbstractExecutor(test_module)
    power_schedule = URLPowerSchedule()
    fuzzer = URLFuzzer(executor, SEEDS, power_schedule=power_schedule, grammar=URL_GRAMMAR)

    output = fuzzer.run_fuzzer(budget=200)
    assert output is not None
    
    return output


def test_url_fuzzer_no_power_schedule(test_module):
    # Test with grammar but no power schedule
    executor = AbstractExecutor(test_module)
    fuzzer_no_power = URLFuzzer(executor, SEEDS, grammar=URL_GRAMMAR)
    output_no_power = fuzzer_no_power.run_fuzzer(budget=200)
    assert output_no_power is not None
    
    return output_no_power


def test_url_fuzzer_no_grammar(test_module):
    # Test without grammar but with power schedule
    executor = AbstractExecutor(test_module)
    power_schedule = URLPowerSchedule()

    fuzzer_no_grammar = URLFuzzer(executor, SEEDS, power_schedule=power_schedule)
    output_no_grammar = fuzzer_no_grammar.run_fuzzer(budget=200)
    assert output_no_grammar is not None
    return output_no_grammar


# Print mean of ten execution times and coverages for each configuration
import matplotlib.pyplot as plt
import numpy as np
test_module = urlparse
outputs_power_grammar = []
outputs_no_power = []
outputs_no_grammar = []

for _ in range(10):
    output_power_grammar = test_url_fuzzer(test_module)
    output_no_power = test_url_fuzzer_no_power_schedule(test_module)
    output_no_grammar = test_url_fuzzer_no_grammar(test_module)
    outputs_power_grammar.append(output_power_grammar)
    outputs_no_power.append(output_no_power)
    outputs_no_grammar.append(output_no_grammar)



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