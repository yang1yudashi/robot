"""Close the gripper, lift it, and apply a simple grasp-success rule."""

from pathlib import Path

import mujoco
import json

MODEL_PATH = Path(__file__).parents[1] / "models" / "gripper.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    object_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "object")
    max_contacts = 0  # 目前见过的最大值
    while data.time < 6.0:

        close_ratio = min(max((data.time - 0.5) / 1.5, 0.0), 1.0)
        lift_ratio = min(max((data.time - 2.5) / 2.0, 0.0), 1.0)
        # 目标位置   ctrl[] 里面的数字是执行器的索引，顺序来自 gripper.xml 中 <actuator> 的排列顺序
        data.ctrl[1:3] = 0.045 * close_ratio
        data.ctrl[0] = 0.12 * lift_ratio
        mujoco.mj_step(model, data)
        max_contacts = max(max_contacts, data.ncon)


    object_height = data.xpos[object_id, 2]
    success = object_height > 0.08

    # print(f"object height={object_height:.3f} m")
    # print(f"grasp success={success}")
    # print(f"max contacts={max_contacts}")


    # JSON 只认识 Python 原生的 float、bool、int 等类型。
    print(json.dumps(
        {
            "object_height": float(object_height),
            "grasp_success": bool(success),
            "max_contacts": int(max_contacts),
        },indent=2
    ))


if __name__ == "__main__":
    main()
