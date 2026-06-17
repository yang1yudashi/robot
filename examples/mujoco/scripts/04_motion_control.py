"""给位置执行器发送随时间变化的目标值。"""

# Path 用来拼接模型文件路径。
from pathlib import Path

# math 用来计算正弦函数，让目标角度来回变化。
import math

# time 用来控制循环速度，让 Viewer 里的播放速度接近真实时间。
import time

# mujoco 是 MuJoCo 的 Python API，用来加载模型、创建状态、推进仿真。
import mujoco

# mujoco.viewer 用来打开可视化窗口。
import mujoco.viewer


# 这个示例继续使用单关节模型 hinge.xml。
MODEL_PATH = Path(__file__).parents[1] / "models" / "hinge.xml"


def main() -> None:
    # 加载 XML 模型。
    # model 保存关节、执行器、几何体、时间步长等静态信息。
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))

    # 创建仿真状态。
    # data 保存 time、qpos、qvel、ctrl 等会随仿真变化的信息。
    data = mujoco.MjData(model)

    # 打开被动 Viewer。
    # 物理仿真由下面的 while 循环手动推进。
    with mujoco.viewer.launch_passive(model, data) as viewer:
        # 运行 8 秒，观察关节在正负方向之间平滑摆动。
        while viewer.is_running() and data.time < 8.0:
            # 记录这一轮循环开始的真实时间。
            step_start = time.time()

            # 生成一个随时间变化的目标角度。
            # sin 的输出范围是 -1 到 1，所以 target 的范围大约是 -0.8 到 0.8 rad。
            # 0.25 表示频率是 0.25Hz，也就是 4 秒完成一次完整来回周期。
            target = 0.8 * math.sin(2 * math.pi * 0.25 * data.time)

            # data.ctrl[0] 是给第 0 个执行器的控制目标。
            # 注意：ctrl 是“目标值/命令”，不是关节实际走过的路线。
            # 关节的实际位置要看 data.qpos[0]，它会被物理仿真慢慢拉向 target。
            data.ctrl[0] = target

            # 推进一步仿真。
            # MuJoCo 会根据当前 ctrl、关节状态、质量、阻尼等计算新的 qpos/qvel。
            mujoco.mj_step(model, data)

            # 把最新状态同步到 Viewer 中显示。
            viewer.sync()

            # 如果这一轮计算比 timestep 快，就等待剩余时间，避免画面播放过快。
            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    # 直接运行本文件时，启动主函数。
    main()
