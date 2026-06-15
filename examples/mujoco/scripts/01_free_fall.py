"""加载 MJCF 模型，并通过 MuJoCo Viewer 观察小球自由落体。"""

# 导入 Path，用面向对象的方式拼接和处理模型文件路径。
from pathlib import Path

# 导入 time，用于控制仿真循环的运行速度，使画面接近真实时间。
import time

# 导入 MuJoCo Python API，用于加载模型、创建状态和推进物理仿真。
import mujoco

# 导入 MuJoCo Viewer，用于打开交互式三维可视化窗口。
import mujoco.viewer


# __file__ 是当前 Python 文件的路径。
# parents[1] 从 scripts/ 返回到 mujoco/，然后定位 models/free_fall.xml。
MODEL_PATH = Path(__file__).parents[1] / "models" / "free_fall.xml"


# 定义程序主函数；-> None 表示这个函数没有返回值。
def main() -> None:
    # 从 XML 文件加载静态模型信息，例如重力、刚体、关节、质量和时间步长。
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))

    # 根据模型创建动态仿真数据，用于保存时间、位置、速度和接触等状态。
    data = mujoco.MjData(model)

    # 打开被动 Viewer。程序负责推进仿真，Viewer 只负责显示和交互。
    # with 代码块结束时，Viewer 窗口及相关资源会被自动释放。
    with mujoco.viewer.launch_passive(model, data) as viewer:
        # Viewer 未被关闭并且仿真时间小于 3 秒时，持续运行仿真。
        while viewer.is_running() and data.time < 3.0:
            # 记录本轮循环开始的真实时间，用于后面控制播放速度。
            step_start = time.time()

            # 将物理仿真向前推进一个 timestep，本模型中是 0.002 秒。
            mujoco.mj_step(model, data)

            # 把最新仿真状态同步到 Viewer，使窗口显示小球的新位置。
            viewer.sync()

            # 计算本轮物理计算完成后，本时间步还剩多少真实时间。
            remaining = model.opt.timestep - (time.time() - step_start)

            # 如果计算速度快于真实时间，就等待剩余时间，避免画面播放过快。
            if remaining > 0:
                # 暂停 remaining 秒，使仿真尽量按照实时速度显示。
                time.sleep(remaining)


# 只有直接运行本文件时条件才成立；被其他文件导入时不会自动执行。
if __name__ == "__main__":
    # 调用主函数，启动自由落体仿真。
    main()
