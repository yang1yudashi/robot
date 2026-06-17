"""用位置执行器控制一个 hinge 转动关节。"""

# Path 用来拼接模型文件路径。
from pathlib import Path

# time 用来控制循环速度，让 Viewer 里的播放速度接近真实时间。
import time

# mujoco 是 MuJoCo 的 Python API，用来加载模型、创建状态、推进仿真。
import mujoco

# mujoco.viewer 用来打开可视化窗口。
import mujoco.viewer


# 当前脚本在 examples/mujoco/scripts/ 目录中。
# parents[1] 会回到 examples/mujoco/，再拼接 models/hinge.xml。
MODEL_PATH = Path(__file__).parents[1] / "models" / "hinge.xml"


def main() -> None:
    # 从 XML 文件加载静态模型。
    # model 里保存关节、执行器、几何体、时间步长等不随时间变化的信息。
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))

    # 创建动态仿真数据。
    # data 里保存 qpos、qvel、ctrl、time 等会随着仿真变化的信息。
    data = mujoco.MjData(model)

    # data.ctrl 是控制输入数组。
    # hinge.xml 里只有一个 position 执行器，所以 data.ctrl[0] 控制 arm_joint 的目标角度。
    # -0.8 rad 表示让关节转到 -0.8 弧度附近，而不是让它一直旋转。
    data.ctrl[0] = -0.8

    # 打开被动 Viewer。
    # 被动 Viewer 只负责显示画面，物理仿真仍然需要下面的 while 循环手动推进。
    with mujoco.viewer.launch_passive(model, data) as viewer:
        # 当窗口没有关闭，并且仿真时间小于 4 秒时，持续运行。
        while viewer.is_running() and data.time < 4.0:
            # 记录这一轮循环开始的真实时间。
            step_start = time.time()

            # 推进一步物理仿真。
            # 执行器会根据 data.ctrl[0] 的目标角度拉动关节。
            mujoco.mj_step(model, data)

            # 把最新仿真状态同步到 Viewer。
            viewer.sync()

            # 如果这一轮计算用时小于 MuJoCo 的 timestep，就等待剩余时间。
            # 这样可以避免仿真画面跑得太快。
            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)

    # data.qpos[0] 是 arm_joint 的实际角度。
    # 它会逐渐接近 ctrl 给定的目标角度，但不一定完全相等。
    print(f"target=0.800 rad, final qpos={data.qpos[0]:.3f} rad")


if __name__ == "__main__":
    # 直接运行本文件时，启动主函数。
    main()
