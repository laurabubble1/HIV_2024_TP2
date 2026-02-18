from html.parser import HTMLParser

from poly_fuzzer.fuzzers.html_parser_fuzzer import HTMLParserFuzzer
from poly_fuzzer.power_schedules.html_parser_schedule import HTMLParserPowerSchedule
from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.common.abstract_grammar import AbstractGrammar
from poly_fuzzer.common.abstract_executor import AbstractExecutor



HTML_GRAMMAR = AbstractGrammar({
    "{start}": ["<!DOCTYPE html>\n<html>\n<head>\n<title>{text}</title>\n</head>\n<body>\n{content}\n</body>\n</html>"],
    "{content}": ["{element}", "{element}{content}"],
    "{element}": ["{heading}", "{paragraph}", "{link}", "{image}", "{div}"],
    "{heading}": ["{h1}", "{h2}", "{h3}"],
    "{h1}": ["<h1>{safe_text}</h1>"],
    "{h2}": ["<h2>{safe_text}</h2>"],
    "{h3}": ["<h3>{safe_text}</h3>"],
    "{paragraph}": ["<p>{safe_text}</p>"],
    "{link}": ["<a href=\"{url}\">{safe_text}</a>"],
    "{image}": ["<img src=\"{url}\" alt=\"{safe_text}\">"],
    "{div}": ["<div>{content}</div>"],
    "{text}": [" ", "-", "_"],
    "{safe_text}": ["{word}", "{word}{text}{word}"],
    "{word}": ["{letter}", "{letter}{word}", "{number}"],
    "{number}": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    "{letter}": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
    "{url}": ["{scheme}{domain}{path}{query}"],
    "{scheme}": ["http://", "https://", "ftp://"],
    "{domain}": ["{subdomain}.{tld}", "{host}"],
    "{subdomain}": ["www", "api", "mail", "test"],
    "{host}": ["example", "localhost", "google", "github"],
    "{tld}": ["com", "org", "net", "io", "dev"],
    "{path}": ["", "/{segment}", "/{segment}/{segment}"],
    "{segment}": ["index", "api", "search", "user", "product"],
    "{query}": ["", "?{param}", "?{param}&{param}"],
    "{param}": ["q={value}", "id={number}", "type={word}"],
    "{value}": ["search", "query", "test"],
}, start_symbol="{start}", nonterminal_open="{", nonterminal_close="}")

SEEDS = [
    AbstractSeed("<!DOCTYPE html>\n<html>\n<head>\n<title> kjziehfhoirbgrbg béjotbibrizgbfzronvporzjgiirhg</title>\n</head>\n<body>\n<div><div><p>4</p><h2>b</h2></div><div><p>v0 2</p></div><div><img src=\"ftp://example\" alt=\"j\"></div></div>\n</body>\n</html>"),
    AbstractSeed("<!DlO\"J,?CTYP:&E PZlhtml>$>\n<hVhtml>B\n(Vk<heaTd>9\n<tiYt/4lXN1(?Q71GNe> <{/titlYe>j\n<q/sQhenWad;3_1>\n1w\\COJ4<bYody>\n/<h2>R&@x<FpB/Zh_2>H<?p0>{WgMsc1iYk-;cjv)</_p><G!&Nnh:3ih>1L<;h/hlu+&3><=diTqv[><imgZ s/hy\'o[i-CDzlirp;OKc=\"mg0fYtbpK:/`  x4/e0xX~ZampljQew2\"D 4I^a@tlyf#{2t=O\"f_x0?_QN(|2fP\"5>N>b</divp>,<7p&` a>?fij;<I/p0>\n<%d/1boNdy>e\n+<R/um?%htmQK@$l.>"),
    AbstractSeed("<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Hello World</h1></body></html>"),
    AbstractSeed("!DOCTYPE html>\n<html>\n<head>\n<title> </title>\n</head>\n<body>\n<div><div><p>4</p><h2>b</h2></div><div><p>v0 2</p></div><div><img src=\"ftp://example\" alt=\"j\"></div></div>\n</body>\n</html>"),
    AbstractSeed("<html>hello html parser</html>"),
    AbstractSeed("mtm/h<?OJp7USbAaepifguegvuir  pgévbgruvouehiphpfabejobjfpiaehihf"),
    AbstractSeed("!lO\"J,& P<l\n(V/41(7G><Z/tqsa_CJ4b<h&xb<F/>>{gc;cj<_<N:3><;huiqv>< ilrpOm0pK/`e0j\"D Ia@lft=0?N(\"b&/\n<d/oNye\n%hKl.>"),
    AbstractSeed("<!|=v.@a]Q=~2l><ho@#>WheapSl1!n}u>\\Dat</Gikl0N<W*-LL>g~oe1q<aohLc:m}hltpP/0GxOmZle.QtjijExagm@E(`u/N/7>d-><~ht|l>', 28), ('<!DlO\"J,?CTYP:&E PZlhtml>$>\n<hVhtml>B\n(Vk<heaTd>9\n<tiYt/4lXN1(?Q71GNe> <{/titlYe>j\n<q/sQhenWad;3_1>\n1w\\COJ4<bYody>\n/<h2>R&@x<FpB/Zh_2>H<?p0>{WgMsc1iYk-;cjv)</_p><G!&Nnh:3ih>1L<;h/hlu+&3><=diTqv[><imgZ s/hy\'o[i-CDzlirp;OKc=\"mg0fYtbpK:/`  x4/e0xX~ZampljQew2\"D 4I^a@tlyf#{2t=O\"f_x0?_QN(|2fP\"5>N>b</divp>,<7p&` a>?fij;<I/p0>\n<%d/1boNdy>e\n+<R/um?%htmQK@$l.>"),
    AbstractSeed("<!DOCTYPE html>\n<html>\n<head>\n<title> </title>\n</head>\n<body>\n<div><div><p>4</p><h2>b</h2></div><div><p>v0 2</p></div><div><img src=\"ftp://example\" alt=\"j\"></div></div>\n</body>\n</html>"),
]
def test_html_fuzzer(test_module):
    # Test with power schedule and grammar
    executor = AbstractExecutor(test_module)
    power_schedule = HTMLParserPowerSchedule()
    fuzzer = HTMLParserFuzzer(executor, SEEDS, power_schedule=power_schedule, grammar=HTML_GRAMMAR)

    output = fuzzer.run_fuzzer(budget=500)
    assert output is not None
    
    return output


def test_html_fuzzer_no_power_schedule(test_module):
    # Test with grammar but no power schedule
    executor = AbstractExecutor(test_module)
    fuzzer_no_power = HTMLParserFuzzer(executor, SEEDS, grammar=HTML_GRAMMAR)
    output_no_power = fuzzer_no_power.run_fuzzer(budget=500)
    assert output_no_power is not None
    
    return output_no_power


def test_html_fuzzer_no_grammar(test_module):
    # Test without grammar but with power schedule
    executor = AbstractExecutor(test_module)
    power_schedule = HTMLParserPowerSchedule()

    fuzzer_no_grammar = HTMLParserFuzzer(executor, SEEDS, power_schedule=power_schedule)
    output_no_grammar = fuzzer_no_grammar.run_fuzzer(budget=500)
    assert output_no_grammar is not None
    return output_no_grammar


# Print mean of ten execution times and coverages for each configuration
import matplotlib.pyplot as plt
import numpy as np
test_module = HTMLParser().feed
outputs_power_grammar = []
outputs_no_power = []
outputs_no_grammar = []

for _ in range(10):
    output_power_grammar = test_html_fuzzer(test_module)
    output_no_power = test_html_fuzzer_no_power_schedule(test_module)
    output_no_grammar = test_html_fuzzer_no_grammar(test_module)
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