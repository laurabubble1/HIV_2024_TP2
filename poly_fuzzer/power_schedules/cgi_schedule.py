from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.power_schedules.abstract_power_schedule import AbstractPowerSchedule


class CGIPowerSchedule(AbstractPowerSchedule):
    """CGI power schedule implementation. Assign more energy to seeds that execute faster and yield coverage increases more often."""

    def _assign_energy(self, seeds: list[AbstractSeed]) -> list[AbstractSeed]:
        for seed in seeds:
            # Assign based on coverage and length (shorter is better)
            seed.energy = (seed.coverage + 1) / (len(seed.data) + 1)  # +1 to avoid division by zero
        return seeds
