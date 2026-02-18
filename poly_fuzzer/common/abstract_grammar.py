import random
import re



class AbstractGrammar:
    """
    # The `AbstractGrammar` class is used to generate strings based on a given grammar.
    Code partially taken from https://www.fuzzingbook.org/html/Grammars.html#"""

    def __init__(
        self,
        gram: dict,
        start_symbol: str = "<start>",
        nonterminal_open: str = "<",
        nonterminal_close: str = ">",
    ):
        self.START_SYMBOL = start_symbol
        delimiter_chars = re.escape(nonterminal_open + nonterminal_close)
        pattern = (
            re.escape(nonterminal_open)
            + r"[^\s"
            + delimiter_chars
            + r"]*"
            + re.escape(nonterminal_close)
        )
        self.RE_NONTERMINAL = re.compile(f"({pattern})")
        self.gram = gram

    def is_nonterminal(self, s):
        return self.RE_NONTERMINAL.match(s)

    def nonterminals(self, expansion):
        # In later chapters, we allow expansions to be tuples,
        # with the expansion being the first element
        if isinstance(expansion, tuple):
            expansion = expansion[0]

        return [symbol for symbol in self.RE_NONTERMINAL.findall(expansion) if symbol in self.gram]

    def generate_input(
        self,
        start_symbol=None,
        max_nonterminals: int = 10,
        max_expansion_trials: int = 100,
        log: bool = False,
    ) -> str:
        """Produce a string from `grammar`.
        `start_symbol`: use a start symbol other than `<start>` (default).
        `max_nonterminals`: the maximum number of nonterminals
            still left for expansion
        `max_expansion_trials`: maximum # of attempts to produce a string
        `log`: print expansion progress if True"""
        if start_symbol is None:
            start_symbol = self.START_SYMBOL

        term = start_symbol
        expansion_trials = 0
        grammar = self.gram

        while len(self.nonterminals(term)) > 0:
            current_nonterminals = self.nonterminals(term)
            symbol_to_expand = random.choice(current_nonterminals)
            expansions = grammar[symbol_to_expand]
            candidate_terms = []

            for expansion in expansions:
                # In later chapters, we allow expansions to be tuples,
                # with the expansion being the first element
                if isinstance(expansion, tuple):
                    expansion = expansion[0]

                new_term = term.replace(symbol_to_expand, expansion, 1)
                nonterminal_count = len(self.nonterminals(new_term))
                candidate_terms.append((expansion, new_term, nonterminal_count))

            acceptable_candidates = [
                candidate for candidate in candidate_terms if candidate[2] <= max_nonterminals
            ]

            if acceptable_candidates:
                expansion, term, _ = random.choice(acceptable_candidates)
                if log:
                    print("%-40s" % (symbol_to_expand + " -> " + expansion), term)
                expansion_trials = 0
                continue

            # Fallback: choose candidate with the fewest remaining nonterminals.
            # This helps recursive grammars eventually converge.
            expansion, term, new_count = min(candidate_terms, key=lambda candidate: candidate[2])

            if log:
                print("%-40s" % (symbol_to_expand + " -> " + expansion), term)

            if new_count >= len(current_nonterminals):
                expansion_trials += 1
            else:
                expansion_trials = 0

            if expansion_trials >= max_expansion_trials:
                raise RuntimeError(
                    "Cannot expand grammar within max_expansion_trials. "
                    f"Current term: {term!r}"
                )

        return term


