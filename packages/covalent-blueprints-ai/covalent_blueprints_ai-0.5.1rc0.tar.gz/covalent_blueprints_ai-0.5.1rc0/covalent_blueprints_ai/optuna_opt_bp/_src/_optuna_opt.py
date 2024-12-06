from typing import Callable, List

import cloudpickle
import covalent as ct
import covalent_cloud as cc

import covalent_blueprints_ai.optuna_opt_bp.utilities
from covalent_blueprints_ai._versions import covalent_blueprints_pkg
from covalent_blueprints_ai.optuna_opt_bp.utilities import StudyWrapper, TrialWrapper

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
def get_new_trials(n_trials: int, study_obj: StudyWrapper) -> StudyWrapper:
    """Generate new trials using Optuna's study.ask method."""
    for _ in range(n_trials):
        trial = study_obj.ask()
        study_obj.add_trial(trial)

    return study_obj


@ct.electron(executor=trial_ex)
def trial_runner(func: Callable, trial: TrialWrapper) -> TrialWrapper:
    """Run the function with trial params and return the result."""
    print(f"Running trial {trial.number} with params: {trial.params}")
    y = trial.run(func)  # updates result inside trial wrapper
    print(f"Trial {trial.number} result: {y}")
    return trial


@ct.electron(executor=cpu_ex)
def update_results(
    study_obj: StudyWrapper, complete_trials: List[TrialWrapper]
) -> StudyWrapper:
    """Update trials in the study object."""
    study_obj.tell(complete_trials)
    return study_obj


@ct.electron(executor=cpu_ex)
@ct.lattice(executor=cpu_ex, workflow_executor=cpu_ex)
def batch_run(func: Callable, study_obj: StudyWrapper) -> StudyWrapper:
    """Run all trials on the function in parallel."""
    complete_trials = []
    for trial in study_obj.incomplete_trials:
        complete_trials.append(trial_runner(func, trial))
    updated_results = update_results(study_obj, complete_trials)
    return updated_results


@ct.lattice(executor=cpu_ex, workflow_executor=cpu_ex)
def optuna_optimize(
    study_obj: StudyWrapper,
    func: Callable,
    n_batches: int,
    n_trials_per_batch: int,
) -> StudyWrapper:
    """Global Optuna optimization lattice. Runs several batches of
    trials to evolve the best parameters."""
    for _ in range(n_batches):
        # Generate new trials
        study_obj = get_new_trials(n_trials_per_batch, study_obj)
        # Evaluate trials and tell results
        study_obj = batch_run(func=func, study_obj=study_obj)

    return study_obj


dispatch_id = cc.dispatch(optuna_optimize)(
    study_obj=None,
    func=None,
    n_batches=2,
    n_trials_per_batch=5,
)
