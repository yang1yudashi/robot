# MuJoCo 示例代码

本目录是 [MuJoCo 零基础实战教程](../../docs/tutorials/mujoco.md) 的配套代码。

## 安装

```bash
conda create -n mujoco-study python=3.10
conda activate mujoco-study
cd examples/mujoco
python -m pip install -r requirements.txt
```

## 运行

示例应按编号依次运行：

```bash
python scripts/01_free_fall.py
python scripts/01_free_fall_record_video.py
python scripts/02_read_state.py
python scripts/03_single_joint.py
python scripts/04_motion_control.py
python scripts/05_close_gripper.py
python scripts/06_contact_detection.py
python scripts/07_grasp_and_lift.py
```

模型文件位于 `models/`，Python 程序位于 `scripts/`。

## 保存视频

没有UI界面时，可以运行无界面录制脚本：

```bash
python scripts/01_free_fall_record_video.py
```

输出文件：

```text
outputs/free_fall.mp4
```

`outputs/`目录已被`.gitignore`忽略，生成的视频不会进入Git提交。
