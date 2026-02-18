from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.power_schedules.abstract_power_schedule import AbstractPowerSchedule


class URLPowerSchedule(AbstractPowerSchedule):
    """URL power schedule implementation. Assign more energy to seeds that execute faster and yield coverage increases more often."""

    def _assign_energy(self, seeds: list[AbstractSeed]) -> list[AbstractSeed]:
        mean_coverage = sum(seed.coverage for seed in seeds) / len(seeds) if seeds else 0
        for seed in seeds:
            # Assign based on coverage and length (shorter is better)
            seed.energy = (max(seed.coverage - mean_coverage, 0) *1000 + 1) / (len(seed.data) + 1)  # +1 to avoid division by zero
        return seeds
