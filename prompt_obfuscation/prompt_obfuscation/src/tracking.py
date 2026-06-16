from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any


logger = logging.getLogger(__name__)


def init_wandb(
    *,
    enabled: bool,
    project: str,
    run_name: str | None,
    entity: str | None,
    config: dict[str, Any],
    tags: list[str] | None = None,
) -> Any | None:
    if not enabled:
        return None

    try:
        import wandb
    except ImportError:
        logger.warning("wandb is not installed; continuing without W&B logging.")
        return None

    try:
        return wandb.init(
            project=project,
            entity=entity,
            name=run_name,
            config=config,
            tags=tags,
        )
    except Exception as exc:
        logger.warning("Failed to initialize W&B; continuing without W&B logging: %s", exc)
        return None


def log_wandb(metrics: dict[str, Any], step: int | None = None) -> None:
    try:
        import wandb
    except ImportError:
        return

    if wandb.run is not None:
        wandb.log(metrics, step=step)


def finish_wandb(summary: dict[str, Any] | None = None) -> None:
    try:
        import wandb
    except ImportError:
        return

    if wandb.run is None:
        return

    if summary:
        for key, value in summary.items():
            wandb.run.summary[key] = value
    wandb.finish()


class EnergyTracker:
    def __init__(
        self,
        *,
        enabled: bool,
        project_name: str,
        output_dir: str | Path,
        measure_power_secs: int = 15,
    ) -> None:
        self.enabled = enabled
        self.project_name = project_name
        self.output_dir = Path(output_dir)
        self.measure_power_secs = measure_power_secs
        self.tracker = None
        self.started = False

    def start(self) -> None:
        if not self.enabled:
            return

        try:
            from codecarbon import EmissionsTracker
        except ImportError:
            logger.warning("codecarbon is not installed; continuing without energy logging.")
            return

        self.output_dir.mkdir(parents=True, exist_ok=True)
        try:
            self.tracker = EmissionsTracker(
                project_name=self.project_name,
                output_dir=str(self.output_dir),
                measure_power_secs=self.measure_power_secs,
                save_to_file=True,
                log_level="warning",
            )
            self.tracker.start()
            self.started = True
        except Exception as exc:
            logger.warning("Failed to start CodeCarbon; continuing without energy logging: %s", exc)
            self.tracker = None
            self.started = False

    def stop(self) -> dict[str, float]:
        if not self.started or self.tracker is None:
            return {}

        try:
            emissions_kg = self.tracker.stop()
        except Exception as exc:
            logger.warning("Failed to stop CodeCarbon cleanly: %s", exc)
            return {}
        data = getattr(self.tracker, "final_emissions_data", None)
        metrics = {"emissions_kg": emissions_kg}

        energy_kwh = getattr(data, "energy_consumed", None)
        if energy_kwh is not None:
            metrics["energy_kwh"] = energy_kwh

        return metrics


class WallTimer:
    def __init__(self) -> None:
        self.start_time = time.perf_counter()

    def elapsed(self) -> float:
        return time.perf_counter() - self.start_time
