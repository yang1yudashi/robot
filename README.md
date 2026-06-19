# 我的机器人学习记录

这是我的机器人学习仓库，用来记录从零基础学习机器人、灵巧手和抓取算法的过程。

当前主要目标是学习 Linker Hand 的模型与控制，并尝试使用 BODex 为 Linker Hand 生成抓取姿态，最终在仿真和真机上完成简单物体抓取。

## 学习目标

完整的项目目标：

```text
理解机器人基础知识
    ↓
读懂 Linker Hand 的 URDF 模型
    ↓
跑通 BODex 官方抓取示例
    ↓
将 Linker Hand 适配到 BODex
    ↓
在仿真中验证抓取
    ↓
安全地控制真实 Linker Hand
```

第一阶段先完成一个小目标：

> 给定一个简单物体，由 BODex 生成 Linker Hand 的抓取姿态，并在仿真中完成抓取。

## 学习路线

学习文档请查看：

- [文档总目录](./docs/README.md)
- [学习路线入口](./docs/roadmaps/README.md)
- [加速学习计划](./docs/roadmaps/accelerated-plan.md)
- [Linker Hand + BODex 学习路线](./docs/roadmaps/reference/linkerhand-bodex.md)
- [具身智能长期学习路线](./docs/roadmaps/reference/embodied-ai-roadmap.md)
- [MuJoCo 零基础实战教程](examples/mujoco/tutorials/mujoco.md)
- [MJCF/XML 零基础速查](examples/mujoco/tutorials/mujoco-mjcf-quick-reference.md)
- [论文阅读目录](./docs/paper/README.md)
- [MuJoCo 配套示例](./examples/mujoco/README.md)

每天的学习任务只以[加速学习计划](./docs/roadmaps/accelerated-plan.md)为准。

整体分为以下阶段：

| 阶段 | 学习内容 | 当前状态 |
| --- | --- | --- |
| 1 | Python、NumPy、Linux、Git | 进行中 |
| 2 | 坐标系、矩阵与机器人运动学 | 未开始 |
| 3 | ROS 2、URDF、TF 和 RViz | 未开始 |
| 4 | MuJoCo 基础与抓取仿真 | 加速进行中 |
| 5 | 跑通 BODex 官方示例 | 下周开始 |
| 6 | 适配 Linker Hand 模型 | 未开始 |
| 7 | 物理仿真与抓取验证 | 未开始 |
| 8 | Linker Hand 真机控制 | 未开始 |

状态说明：`未开始`、`进行中`、`已完成`。

## 当前任务

当前每日任务见[加速学习计划](./docs/roadmaps/accelerated-plan.md)。

## 学习内容

### 机器人基础

- Python 与 NumPy
- Linux 与 Git
- 向量、矩阵和坐标变换
- 正运动学与逆运动学
- ROS 2 通信机制
- TF 坐标系

### 机器人模型

- STL、OBJ 与网格模型
- URDF 中的 link 和 joint
- visual、collision 与 inertial
- RViz 模型检查
- 关节限位和机械耦合

### 灵巧手抓取

- 抓取姿态与预抓取姿态
- 接触点和碰撞检测
- BODex 与 cuRobo
- MuJoCo 或其他物理仿真
- 仿真关节到真机电机的映射
- 位置、电流和触觉反馈

## 学习日志

### 2026-06-14

- 建立机器人学习仓库。
- 整理 Linker Hand + BODex 学习路线。
- 明确第一个项目目标：先生成并仿真验证简单物体的抓取姿态。

### 2026-06-15

今天学习：

- 开始学习 MuJoCo 自由落体示例。
- 了解 MJCF 与普通 XML 的区别。
- 学习 `mujoco`、`option`、`worldbody`、`body`、`geom` 和 `freejoint`。
- 理解 `MjModel`、`MjData`、`mj_step` 和 Viewer 的基本作用。

完成内容：

- 将小球初始高度从 1 米修改为 2 米。
- 将地球重力 `-9.81 m/s²`修改为月球重力 `-1.62 m/s²`。
- 将小球质量从 0.1 千克修改为 1 千克。
- 为自由落体 Python 示例添加逐行中文注释。
- 整理 MJCF/XML 零基础速查文档。
- 添加 `.gitignore`，忽略 Python 缓存、编辑器配置和仿真输出。

实验结论：

- 重力减小后，小球下落得更慢。
- 初始高度增加后，小球接触地面的时间更晚。
- 在相同重力下，修改小球质量不会改变自由落体加速度。
- `body`表示刚体和坐标系，`geom`表示形状与碰撞体。
- 没有`freejoint`时，小球会固定在世界中。

下一步：

- [ ] 运行`02_read_state.py`。
- [ ] 学习读取`qpos`、物体位置和接触数量。

### 2026-06-16

今天学习：

- 学习 MuJoCo 第二个示例：无 Viewer 读取仿真状态。
- 理解 `nq`、`nv`、`nu` 的基本含义。
- 学习通过 `mj_name2id` 用名称查找 body ID。
- 学习读取 `data.qpos`、`data.xpos` 和 `data.ncon`。
- 回顾第一天自由落体示例，并增加无界面视频保存能力。

完成内容：

- 为 `02_read_state.py` 添加逐行中文注释。
- 新增 `01_free_fall_record_video.py`，可将自由落体仿真保存为 MP4。
- 更新 MuJoCo 示例依赖，加入 `imageio` 和 `imageio-ffmpeg`。
- 更新 MuJoCo 示例说明和教程文档，补充无 UI 录制视频的运行方法。

实验结论：

- Viewer 负责让人看见仿真，`data` 负责让程序读取仿真状态。
- `qpos` 是广义位置，自由物体的 `qpos` 包含位置和四元数姿态。
- `xpos` 可以按 body ID 读取物体在世界坐标系中的位置。
- `ncon` 表示当前仿真步检测到的接触数量。
- 没有 UI 时，可以用离屏渲染保存视频，再下载到本地查看。

下一步：

- [ ] 修改 `02_read_state.py`，输出小球 z 方向速度。
- [ ] 记录小球第一次接触地面的时间。
- [ ] 学习第三个示例：单关节位置控制。

### 2026-06-16 收尾

今天额外整理：

- 更新具身智能长期学习路线，明确从机器人基础到 VLA、sim-to-real 的长期方向。
- 更新当前项目长期路线，把 Linker Hand + BODex 拆成阶段交付。
- 更新两周加速学习计划：本周收口 MuJoCo，下周进入 BODex 和 Linker Hand。
- 整理文档目录，将 MuJoCo 教程相关内容放入 MuJoCo 教程目录。
- 新增 `docs/paper/`，用于存放论文阅读笔记。
- 新增 BODex 论文笔记模板，后续阅读论文时继续补充。

下一步：

- [ ] 按加速计划继续完成 `03_single_joint.py`。
- [ ] 周末写 MuJoCo 学习总结。

### 2026-06-17

今天学习计划：

- 收尾周二内容：确认 `hinge`、`axis`、`range`、`actuator` 和 `data.ctrl` 的含义。
- 完成周三内容：学习 `04_motion_control.py` 和 `05_close_gripper.py`。
- 理解目标关节值 `ctrl` 和实际关节值 `qpos` 的区别。
- 理解两指夹爪中的 `slide joint`、执行器顺序和夹爪闭合过程。
- 在 `05_close_gripper.py` 与 `gripper.xml` 中补充中文注释。

下一步：

- [ ] 开始周四任务：运行 `06_contact_detection.py`。
- [ ] 学习接触发生在 `geom` 之间。
- [ ] 输出接触双方名称和首次接触时间。

### 2026-06-19

今天补完周四并完成周五的 MuJoCo 学习任务。

今天学习：

- 运行 `06_contact_detection.py`，观察夹爪、方块和地面之间的接触。
- 运行 `07_grasp_and_lift.py`，完成夹爪闭合、抬升和抓取成功判断。
- 理解 `body` 是物体的坐标系和结构容器，`geom` 是形状和碰撞外壳。
- 理解 `data.ncon` 记录当前仿真步的接触点数量，不等于接触物体数量。
- 理解 `data.ctrl[1:3]` 同时设置第 1、2 号执行器的控制目标。
- 学习在没有 Viewer 和 `time.sleep()` 的情况下运行 MuJoCo 仿真。

完成内容：

- 方块最终高度为 `0.088 m`，简单抓取判断结果为成功。
- 新增 `07_grasp_and_lift_headless.py`，通过 `mj_step()` 无 UI 运行仿真。
- 统计仿真过程中的最大接触点数量 `max_contacts`。
- 将 `object_height`、`grasp_success` 和 `max_contacts` 输出为 JSON。
- 理解 Viewer 只负责显示，物理仿真由 `mujoco.mj_step()` 推进。

实验结论：

- `ctrl` 是执行器目标值，`qpos` 是关节实际位置，两者不一定相同。
- 两个 `geom` 之间可以同时产生多个接触点。
- `max_contacts` 只能作为辅助统计，不能单独判断抓取是否成功。
- 当前示例通过物体最终高度是否超过 `0.08 m` 判断抓取成功。
- 无 UI 仿真更适合后续批量测试大量候选抓取。

下一步：

- [ ] 补充 JSON 结果中的 `hold_time`。
- [ ] 整理 `docs/notes/mujoco-summary.md`。
- [ ] 总结 `body / geom / joint / actuator`。
- [ ] 总结 `qpos / qvel / xpos / ctrl / contact`。
- [ ] 总结保存视频和判断抓取成功的方法。

后续日志按照下面的格式记录：

```markdown
### YYYY-MM-DD

今天学习：

- 

完成内容：

- 

遇到的问题：

- 

下一步：

- [ ] 
```

## 实验记录规范

每次运行实验时，尽量记录以下信息：

- 实验目标
- 系统、Python、CUDA 和依赖版本
- 完整运行命令
- 使用的机器人和物体配置
- 输出文件
- 成功或失败现象
- 完整报错
- 解决方法
- 下一步任务

不要只保存成功结果。失败案例通常更有助于理解模型、碰撞和关节映射问题。

## 参考项目

- [Linker Hand URDF](https://github.com/linker-bot/linkerhand-urdf)
- [BODex](https://github.com/JYChen18/BODex)
- [BODex 论文笔记](./docs/paper/bodex.md)
- [Dexonomy](https://github.com/JYChen18/Dexonomy)
- [DexGraspBench](https://github.com/JYChen18/DexGraspBench)
- [cuRobo](https://github.com/NVlabs/curobo)
- [ROS 2 文档](https://docs.ros.org/)

## 学习原则

1. 每学习一个概念，都完成一个可以运行的小实验。
2. 先跑通官方示例，再修改机器人模型。
3. 每次只修改一个问题，并记录修改前后的现象。
4. 仿真通过后再连接真机。
5. 真机实验始终使用限位、限速和急停保护。
