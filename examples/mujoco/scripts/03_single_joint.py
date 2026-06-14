"""Control one hinge joint with a position actuator."""

from pathlib import Path
import time

import mujoco
import mujoco.viewer


MODEL_PATH = Path(__file__).parents[1] / "models" / "hinge.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    data.ctrl[0] = 0.8

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running() and data.time < 4.0:
            step_start = time.time()
            mujoco.mj_step(model, data)
            viewer.sync()

            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)

    print(f"target=0.800 rad, final qpos={data.qpos[0]:.3f} rad")


if __name__ == "__main__":
    main()
