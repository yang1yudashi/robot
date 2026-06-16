"""不打开 Viewer，直接读取 MuJoCo 仿真状态。"""

# 导入 Path，用于拼接模型 XML 文件路径。
from pathlib import Path

# 导入 MuJoCo Python API，用于加载模型和推进仿真。
import mujoco


# 当前文件在 scripts/ 目录中，parents[1] 返回 examples/mujoco/。
# 然后拼接到 models/free_fall.xml，得到自由落体模型路径。
MODEL_PATH = Path(__file__).parents[1] / "models" / "free_fall.xml"


# 定义主函数；这个示例不会打开窗口，只在终端打印数据。
def main() -> None:
    # 加载 XML，得到静态模型对象。
    # model 中保存关节数量、body 数量、时间步长、重力等不随仿真变化的信息。
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))

    # 根据 model 创建动态状态对象。
    # data 中保存时间、位置、速度、接触等会随着 mj_step 改变的信息。
    data = mujoco.MjData(model)

    # 通过名字 "ball" 查找小球 body 的整数 ID。
    # 后面读取 data.xpos 时，需要使用这个 ID 作为数组索引。
    ball_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "ball")

    # nq 是广义位置 qpos 的长度。
    # nv 是广义速度 qvel 的长度。
    # nu 是控制输入 ctrl 的长度；自由落体模型没有电机，所以 nu=0。
    print(f"nq={model.nq}, nv={model.nv}, nu={model.nu}")

    # 打印小球 body 的 ID，方便理解“名称查找 ID，再用 ID 读数组”的流程。
    print(f"ball body id={ball_id}")

    # 循环推进 1001 步。
    # 当前模型 timestep=0.002 秒，所以总仿真时间大约是 1001*0.002=2 秒。
    # 记录第一次接触发生的时间，观察小球落地的时刻。
    first_contact_time = None
    for step in range(1501):
        # 推进一次物理仿真。
        # 每调用一次，data.time、data.qpos、data.qvel、data.xpos 等状态都会更新。
        mujoco.mj_step(model, data)

        # 每 100 步打印一次，避免终端输出太多。
        # 100 步对应 100*0.002=0.2 秒。
        if step % 100 == 0:
            # data.xpos 保存每个 body 在世界坐标系中的位置。
            # [ball_id, 2] 表示读取小球 body 的 z 坐标，也就是高度。
            ball_z = data.xpos[ball_id, 2]

            # 打印当前仿真时间、小球高度和接触数量。
            print(
                # data.time 是 MuJoCo 内部的仿真时间，单位是秒。
                f"time={data.time:5.2f}s "
                # data.qpos 是广义位置。
                # 对 freejoint 来说，qpos[0:3] 是 x/y/z，qpos[3:7] 是四元数姿态。
                f"qpos_z={data.qpos[2]:.3f} "
                # xpos_z 是根据 body ID 读取到的世界坐标高度。
                # 在这个简单模型中，它和 qpos_z 会非常接近。
                f"xpos_z={ball_z:.3f} "
                # data.ncon 是当前仿真步检测到的接触数量。
                # 小球落到地面后，这个值通常会大于 0。
                f"contacts={data.ncon}"
                # 输出z方向的速度
                f" qvel_z={data.qvel[2]:.3f}"
            )
            if first_contact_time is None and data.ncon > 0:
                first_contact_time = data.time
                print(f"First contact at time={first_contact_time:.2f}s")


# 只有直接运行本文件时才会执行 main()。
if __name__ == "__main__":
    # 启动无 Viewer 的状态读取示例。
    main()
