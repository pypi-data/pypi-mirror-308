# Copyright 2024 Agnostiq Inc.
"""Implements a batched Optuna optimization."""

from typing import Callable

import cloudpickle
import covalent as ct
import covalent_cloud as cc

import covalent_blueprints_ai.optuna_opt_bp.utilities
from covalent_blueprints_ai._versions import covalent_blueprints_pkg
from covalent_blueprints_ai.optuna_opt_bp.utilities import (
    StudyResultsWrapper,
    TrialWrapper,
)

cloudpickle.register_pickle_by_value(covalent_blueprints_ai.optuna_opt_bp.utilities)

ENV_NAME = "optuna@blueprints"

cc.create_env(
    name=ENV_NAME,
    pip=[
        "numpy==1.23.5",
        "optuna==4.0.0",
        covalent_blueprints_pkg,
    ],
    wait=True,
)


cpu_ex = cc.CloudExecutor(
    env=ENV_NAME,
    num_cpus=2,
    memory="2GB",
    time_limit="3 hours",
)


trial_ex = cc.CloudExecutor(
    env=ENV_NAME,
    num_cpus=2,
    memory="2GB",
    time_limit="3 hours",
)


@ct.electron(executor=cpu_ex)
def get_new_trials(
    n_trials: int,
    results: StudyResultsWrapper,
) -> StudyResultsWrapper:
    """Generate new trials using Optuna's study.ask method."""
    for _ in range(n_trials):
        dists = results.fixed_distributions
        trial = results.study.ask(fixed_distributions=dists)
        results.add_trial(trial)

    return results


@ct.electron(executor=trial_ex)
def trial_runner(func: Callable, trial: TrialWrapper) -> TrialWrapper:
    """Run the function with trial params and return the result."""
    print(f"Running trial {trial.number} with params: {trial.params}")
    y = trial.run(func)  # updates result inside trial wrapper
    print(f"Trial {trial.number} result: {y}")
    return trial


@ct.electron(executor=cpu_ex)
def update_results(results: StudyResultsWrapper) -> StudyResultsWrapper:
    """Create a new results wrapper with updated trial results."""
    results.tell()
    return results


@ct.electron(executor=cpu_ex)
@ct.lattice(executor=cpu_ex, workflow_executor=cpu_ex)
def batch_run(func: Callable, results: StudyResultsWrapper) -> StudyResultsWrapper:
    """Run all trials on the function in parallel."""
    complete_trials = []
    for trial in results.incomplete_trials:
        complete_trials.append(trial_runner(func, trial))
    updated_results = update_results(results)
    updated_results.wait_for(complete_trials)
    return updated_results


@ct.lattice(executor=cpu_ex, workflow_executor=cpu_ex)
def optuna_optimize(
    results: StudyResultsWrapper,
    func: Callable,
    n_batches: int,
    n_trials_per_batch: int,
) -> StudyResultsWrapper:
    """Global Optuna optimization lattice. Runs several batches of
    trials to evolve the best parameters."""
    for _ in range(n_batches):
        # Generate new trials
        results = get_new_trials(n_trials_per_batch, results)
        # Evaluate trials and collect results
        results = batch_run(func=func, results=results)

    return results


dispatch_id = cc.dispatch(optuna_optimize)(
    results=None,
    func=None,
    n_batches=2,
    n_trials_per_batch=5,
)
