"""控制一个简单两指夹爪闭合并夹住方块。"""

# Path 用来拼接模型文件路径。
from pathlib import Path

# time 用来控制循环速度，让 Viewer 里的播放速度接近真实时间。
import time

# mujoco 是 MuJoCo 的 Python API，用来加载模型、创建状态、推进仿真。
import mujoco

# mujoco.viewer 用来打开可视化窗口。
import mujoco.viewer


# 这个示例使用两指夹爪模型。
MODEL_PATH = Path(__file__).parents[1] / "models" / "gripper.xml"


def main() -> None:
    # 加载夹爪 XML 模型。
    # model 里包含 body、geom、joint、actuator 等静态结构。
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))

    # 创建动态仿真数据。
    # data 里包含 qpos、qvel、ctrl、contact 等实时变化的状态。
    data = mujoco.MjData(model)

    # 打开 Viewer，观察夹爪闭合过程。
    with mujoco.viewer.launch_passive(model, data) as viewer:
        # 运行 4 秒。
        while viewer.is_running() and data.time < 4.0:
            # 记录循环开始时间，用来控制播放速度。
            step_start = time.time()

            # close_ratio 表示夹爪闭合进度，范围是 0 到 1。
            # data.time < 0.5 时保持 0，让画面先稳定半秒。
            # 之后用 1.5 秒从 0 平滑增加到 1。
            close_ratio = min(max((data.time - 0.5) / 1.5, 0.0), 1.0)

            # gripper.xml 的 actuator 顺序是：
            # ctrl[0] -> hand_lift，控制手掌上下移动。
            # ctrl[1] -> left_finger_joint，控制左手指向中间滑动。
            # ctrl[2] -> right_finger_joint，控制右手指向中间滑动。
            # 这里不抬升手掌，只让两个手指逐渐闭合到 0.045m。
            data.ctrl[1] = 0.045 * close_ratio
            data.ctrl[2] = 0.045 * close_ratio

            # 推进一步物理仿真。
            # MuJoCo 会根据 ctrl 目标值、质量、摩擦和接触计算新的状态。
            mujoco.mj_step(model, data)

            # 同步到 Viewer 画面。
            viewer.sync()

            # 控制循环速度，避免仿真显示过快。
            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)

    # qpos[8] 和 qpos[9] 是左右手指滑动关节的实际位置。
    # 它们是实际结果，不是程序给的目标命令。
    print(f"left finger qpos={data.qpos[8]:.4f}")
    print(f"right finger qpos={data.qpos[9]:.4f}")

    # data.ncon 是最后一个仿真步检测到的接触数量。
    print(f"contacts at final step={data.ncon}")


if __name__ == "__main__":
    # 直接运行本文件时，启动主函数。
    main()
