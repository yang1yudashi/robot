"""无界面录制自由落体仿真视频。"""

# 导入 Path，用于拼接模型路径和输出视频路径。
from pathlib import Path

# 导入 imageio，用于把一帧帧图片保存成 mp4 视频。
import imageio.v2 as imageio

# 导入 MuJoCo Python API，用于加载模型、推进仿真和离屏渲染。
import mujoco


# 当前脚本位于 scripts/，parents[1] 返回 examples/mujoco/。
ROOT_DIR = Path(__file__).parents[1]

# 自由落体模型文件路径。
MODEL_PATH = ROOT_DIR / "models" / "free_fall.xml"

# 视频输出目录。outputs/ 已被 .gitignore 忽略，不会提交到仓库。
OUTPUT_DIR = ROOT_DIR / "outputs"

# 输出视频文件路径。
VIDEO_PATH = OUTPUT_DIR / "free_fall.mp4"


def main() -> None:
    # 确保输出目录存在；如果不存在就自动创建。
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 加载静态模型信息。
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))

    # 创建动态仿真状态。
    data = mujoco.MjData(model)

    # 创建离屏渲染器，不需要打开 Viewer 窗口。
    # width 和 height 控制输出视频分辨率。
    # 如果服务器上这里报 OpenGL/EGL 相关错误，可以先在终端设置：
    # Linux NVIDIA GPU: export MUJOCO_GL=egl
    # Linux 无GPU软件渲染: export MUJOCO_GL=osmesa
    renderer = mujoco.Renderer(model, width=640, height=480)

    # 保存每一帧图像的列表。
    frames = []

    # 目标视频帧率。30 fps 表示每秒保存 30 张图。
    # fps = 30
    fps = 60

    # 仿真总时长，单位为秒。
    # duration = 3.0
    duration = 10

    # 下一次应该保存视频帧的仿真时间。
    next_frame_time = 0.0

    # 只要仿真时间还没超过 duration，就继续推进物理仿真。
    while data.time < duration:
        # 推进一个物理时间步。
        mujoco.mj_step(model, data)

        # MuJoCo 物理步长通常比视频帧间隔小。
        # 这里每隔 1/fps 秒保存一帧，避免视频帧数过多。
        if data.time >= next_frame_time:
            # 根据当前 data 更新渲染场景。
            renderer.update_scene(data)

            # 渲染当前画面，返回一张 RGB 图片数组。
            frame = renderer.render()

            # 将当前帧加入列表。
            frames.append(frame)

            # 计算下一帧应该保存的仿真时间。
            next_frame_time += 1.0 / fps

    # 将所有帧写入 mp4 文件。
    imageio.mimsave(VIDEO_PATH, frames, fps=fps)

    # 在终端打印结果，方便确认视频保存位置。
    print(f"saved video: {VIDEO_PATH}")


# 只有直接运行本脚本时才执行 main()。
if __name__ == "__main__":
    # 启动无界面视频录制。
    main()
