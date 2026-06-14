"""Send a time-varying target to a position actuator."""

from pathlib import Path
import math
import time

import mujoco
import mujoco.viewer


MODEL_PATH = Path(__file__).parents[1] / "models" / "hinge.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running() and data.time < 8.0:
            step_start = time.time()

            target = 0.8 * math.sin(2 * math.pi * 0.25 * data.time)
            data.ctrl[0] = target

            mujoco.mj_step(model, data)
            viewer.sync()

            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    main()
