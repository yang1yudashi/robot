"""Close a simple two-finger gripper around a cube."""

from pathlib import Path
import time

import mujoco
import mujoco.viewer


MODEL_PATH = Path(__file__).parents[1] / "models" / "gripper.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running() and data.time < 4.0:
            step_start = time.time()

            close_ratio = min(max((data.time - 0.5) / 1.5, 0.0), 1.0)
            data.ctrl[1] = 0.045 * close_ratio
            data.ctrl[2] = 0.045 * close_ratio

            mujoco.mj_step(model, data)
            viewer.sync()

            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)

    print(f"left finger qpos={data.qpos[8]:.4f}")
    print(f"right finger qpos={data.qpos[9]:.4f}")
    print(f"contacts at final step={data.ncon}")


if __name__ == "__main__":
    main()
