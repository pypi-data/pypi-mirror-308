# Copyright 2024 Agnostiq Inc.
"""Utilities for Optuna optimization."""

from typing import Any, Callable, Dict, List, Optional

try:
    import optuna
except ImportError as e:
    raise ModuleNotFoundError(
        "optuna is required in the local environment to run this "
        "blueprint, please install it using\n\n"
        "    `pip install optuna==4.0.0`"
    ) from e


class TrialWrapper:
    """Container that associates trials and their results."""

    def __init__(self, trial: optuna.Trial, result: Any):
        self.trial = trial
        self.number = trial.number
        self.params = trial.params
        self.result = result

    def run(self, func: Callable) -> Any:
        """Run a function with the trial parameters."""
        kwargs = self.get_kwargs(func)
        self.result = func(**kwargs)
        return self.result

    def get_kwargs(self, func: Callable) -> dict:
        """Get the keyword arguments for a function."""
        kwargs = self.params.copy()
        varnames = func.__code__.co_varnames

        if "trial" in varnames:
            kwargs["trial"] = self.trial
        if "study" in varnames:
            kwargs["study"] = self.trial.study

        return kwargs


class StudyWrapper:
    """Container that associates a study and its trials."""

    def __init__(
        self,
        study: optuna.Study,
        fixed_distributions: Optional[dict] = None,
    ):
        self.study = study
        self.fixed_distributions = fixed_distributions
        self.trials: Dict[int, TrialWrapper] = {}

    def ask(self) -> optuna.Trial:
        """Ask the wrapper study"""
        return self.study.ask(fixed_distributions=self.fixed_distributions)

    def add_trial(self, trial: optuna.Trial, result: Any = None) -> None:
        """Add new trials and their results to the container."""
        self.trials[trial.number] = TrialWrapper(trial, result)

    @property
    def incomplete_trials(self) -> List[TrialWrapper]:
        """Return the trials in the study."""
        incomplete = []
        for _trial in self.study.trials:
            if _trial.state is not optuna.trial.TrialState.COMPLETE:
                incomplete.append(self.trials[_trial.number])
        return incomplete

    def tell(self, trials: List[TrialWrapper]) -> None:
        """Tell the study about the trials and their results."""
        for trial in trials:
            self.study.tell(trial.trial, trial.result)
