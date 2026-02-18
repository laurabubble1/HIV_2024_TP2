from poly_fuzzer.fuzzers.abstract_fuzzer import AbstractFuzzer
import random
import numpy as np
from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.power_schedules.abstract_power_schedule import AbstractPowerSchedule
from poly_fuzzer.common.abstract_grammar import AbstractGrammar


class CGIFuzzer(AbstractFuzzer):

    def __init__(
        self,
        executor,
        seeds: list[AbstractSeed],
        power_schedule: AbstractPowerSchedule = None,
        grammar: AbstractGrammar = None,
        min_mutations: int = 1,
        max_mutations: int = 10,
    ):
        super().__init__(executor)
        self.seeds = seeds
        self.grammar = grammar
        self.seed_index = 0
        self.executor = executor
        self.power_schedule = power_schedule
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.mutators = [self._delete_random_character, self._replace_random_character, self._insert_random_character]
        self.max_seeds = 10
        
        if len(self.seeds) > self.max_seeds:
            self.seeds = self.seeds[:self.max_seeds]
        if self.grammar:
            self.mutators.append(self._grammar_mutation)
    def generate_input(self):
        """Mutate the seed to generate input for fuzzing.
        With this function we first use the gien seeds to generate inputs 
        and then we mutate the seeds to generate new inputs."""
        if self.seed_index < len(self.seeds):
            # Still seeding
            inp = self.seeds[self.seed_index].data
            self.seed_index += 1
        else:
            # Mutating
            inp = self._create_candidate()

        return inp

    def _update(self, input):
        """Update the fuzzer with the input and its coverage."""
        if len(self.data["coverage"]) > 1:
            if self.data["coverage"][-1] > self.data["coverage"][-2]:
                if len(self.seeds) < self.max_seeds:
                    self.seeds.append(AbstractSeed(input))
    

    def _create_candidate(self):
        seed = np.random.choice(self.seeds)

        # Stacking: Apply multiple mutations to generate the candidate
        if self.power_schedule:
            candidate = self.power_schedule.choose(self.seeds).data
        else:
            candidate = seed.data

        num_mutations = random.randint(self.min_mutations, self.max_mutations)
        for _ in range(num_mutations):
            candidate = self.mutate(candidate)

        return candidate

    def mutate(self, s):
        """Return s with a random mutation applied"""
        mutator = random.choice(self.mutators)
        return mutator(s)

    def _delete_random_character(self, s):
    
        if len(s) == 0:
            return s
        index = random.randint(0, len(s) - 1)
        return s[:index] + s[index + 1 :]

    def _replace_random_character(self, s):
        if len(s) == 0:
            return s
        index = random.randint(0, len(s) - 1)
        random_char = chr(random.randint(32, 126))
        return s[:index] + random_char + s[index + 1 :]
    
    def _insert_random_character(self, s):
        index = random.randint(0, len(s))
        random_char = chr(random.randint(32, 126))
        return s[:index] + random_char + s[index:]
    
    def _grammar_mutation(self, s):
        if self.grammar:
            return self.grammar.generate_input()
        else:
            return s