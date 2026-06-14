"""Load an MJCF model and watch a ball fall under gravity."""

from pathlib import Path
import time

import mujoco
import mujoco.viewer


MODEL_PATH = Path(__file__).parents[1] / "models" / "free_fall.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running() and data.time < 3.0:
            step_start = time.time()
            mujoco.mj_step(model, data)
            viewer.sync()

            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    main()
