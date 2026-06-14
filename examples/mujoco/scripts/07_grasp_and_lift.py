"""Close the gripper, lift it, and apply a simple grasp-success rule."""

from pathlib import Path
import time

import mujoco
import mujoco.viewer


MODEL_PATH = Path(__file__).parents[1] / "models" / "gripper.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    object_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "object")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running() and data.time < 6.0:
            step_start = time.time()

            close_ratio = min(max((data.time - 0.5) / 1.5, 0.0), 1.0)
            lift_ratio = min(max((data.time - 2.5) / 2.0, 0.0), 1.0)
            data.ctrl[1:3] = 0.045 * close_ratio
            data.ctrl[0] = 0.12 * lift_ratio

            mujoco.mj_step(model, data)
            viewer.sync()

            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)

    object_height = data.xpos[object_id, 2]
    success = object_height > 0.08
    print(f"object height={object_height:.3f} m")
    print(f"grasp success={success}")


if __name__ == "__main__":
    main()
