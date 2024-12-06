# Copyright 2024 Agnostiq Inc.
"""Blueprint that implements a batched Optuna optimization."""

import warnings
from typing import Callable, Optional

from covalent_blueprints import blueprint, get_blueprint
from covalent_cloud import CloudExecutor

from covalent_blueprints_ai._prefix import PREFIX
from covalent_blueprints_ai.optuna_opt_bp.utilities import StudyResultsWrapper, optuna

NO_EXECUTOR_WARNING = """Using default environment ('{name}') with minimal dependencies.

If `func` relies on external dependencies, please create a new \
environment with the required dependencies and specify this \
environment's name as `env` inside a valid `CloudExecutor`.

Example:

```
import covalent_cloud as cc
from covalent_blueprints_ai import optuna_opt

# ----------------------------------------- #
# 1. Create custom environment and executor #
# ----------------------------------------- #
cc.create_env(
    name='pytorch-optuna',
    pip={pip},
    wait=True,
)

trial_executor = cc.CloudExecutor(
    env='pytorch-optuna',
    num_gpus=1,
    gpu_type='l40',
    num_cpus=2,
    memory='24GB',
    time_limit='3 hours',
)

# --------------------------------------------- #
# 2. Pass new executor to blueprint initializer #
# --------------------------------------------- #
bp = optuna_opt(
    func={func_name},
    trial_executor=trial_executor,
    create_study_kwargs={create_study_kwargs},
)
```
"""


@blueprint("Optuna Optimization")
def optuna_opt(
    func: Optional[Callable] = None,
    trial_executor: Optional[CloudExecutor] = None,
    create_study_kwargs: Optional[dict] = None,
    fixed_distributions: Optional[dict] = None,
    n_batches: int = 5,
    n_trials_per_batch: int = 10,
):
    """A blueprint that runs a batched and parallelized Optuna
    optimization of a target function.

    Args:
        func: The target function to optimize. If the function has a
            `trial` argument, the corresponding trial object is
            automatically passed to the function during each trial.
            Similarly, if the function has a `study` argument, the
            current study object is also passed to the function.
            If neither argument is present, the function is called
            without any additional arguments.
        trial_executor: Optional CloudExecutor for trials.
        create_study_kwargs: Keyword arguments for creating a study.
        fixed_distributions: Fixed distributions for study.ask().
        n_batches: Number of batches to run. Defaults to 5.
        n_trials_per_batch: Trials per each batch. Defaults to 10.

    Returns:
        Covalent blueprint that runs the Optuna optimization.

    Example:
        ```
        import optuna
        from covalent_blueprints_ai import optuna_opt

        def target_func(x, y, *, trial):
            print(f"inside func, trial: {trial._trial_id}")
            return (x - 2) ** 2 + (y - 2) ** 2

        dists = {
            "x": optuna.distributions.FloatDistribution(-5, 5),
            "y": optuna.distributions.FloatDistribution(-5, 5),
        }

        bp = optuna_opt(
            func=target_func,
            fixed_distributions=dists,
            create_study_kwargs={"direction": "minimize"},
            n_batches=5,
            n_trials_per_batch=10,
        )

        study_results = bp.run()
        study = study_results.study

        print("Best parameters:", study.best_params)
    """
    if func is None:
        warnings.warn(
            "Please provide a function `func` to optimize.\n\n"
            "=== EXECUTION WILL FAIL IF `func` IS NOT SPECIFIED! ===\n",
        )

    create_study_kwargs = create_study_kwargs or {}

    study = optuna.create_study(**create_study_kwargs)
    results = StudyResultsWrapper(study=study, fixed_distributions=fixed_distributions)

    bp = get_blueprint(f"{PREFIX}/optuna_opt")

    if trial_executor is not None:
        # Set the executor for electron that runs `func`.
        bp.executors["trial_runner"] = trial_executor
        bp.executors["batch_run"].env = trial_executor.env
    else:
        # Raise a warning if no executor is set.
        envs = bp.script.environments
        executor = bp.executors["trial_runner"]
        env = next(filter(lambda e: e.name == executor.env, envs))
        warnings.warn(
            "Initializer parameter `trial_executor` is not set.",
            stacklevel=3,
        )
        func_name = "target_function"
        if func is not None:
            func_name = func.__name__
        print(
            NO_EXECUTOR_WARNING.format(
                name=executor.env,
                pip=["torch==2.4.0"] + env.pip,
                base_image=env.base_image,
                func_name=func_name,
                create_study_kwargs=create_study_kwargs,
            )
        )

    bp.set_default_inputs(
        results=results,
        func=func,
        n_batches=n_batches,
        n_trials_per_batch=n_trials_per_batch,
    )

    return bp
