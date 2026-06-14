"""Inspect model dimensions and read simulation state without a viewer."""

from pathlib import Path

import mujoco


MODEL_PATH = Path(__file__).parents[1] / "models" / "free_fall.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    ball_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "ball")

    print(f"nq={model.nq}, nv={model.nv}, nu={model.nu}")
    print(f"ball body id={ball_id}")

    for step in range(1001):
        mujoco.mj_step(model, data)

        if step % 100 == 0:
            ball_z = data.xpos[ball_id, 2]
            print(
                f"time={data.time:5.2f}s "
                f"qpos_z={data.qpos[2]:.3f} "
                f"xpos_z={ball_z:.3f} "
                f"contacts={data.ncon}"
            )


if __name__ == "__main__":
    main()
