# 每日学习记录

这里按日期保存每天的学习内容、实验结果和下一步任务。项目首页只展示当前目标与进度，历史学习记录统一保留在本文中。

## 2026-06-14

- 建立机器人学习仓库。
- 整理 Linker Hand + BODex 学习路线。
- 明确第一个项目目标：先生成并仿真验证简单物体的抓取姿态。

## 2026-06-15

今天学习：

- 开始学习 MuJoCo 自由落体示例。
- 了解 MJCF 与普通 XML 的区别。
- 学习 `mujoco`、`option`、`worldbody`、`body`、`geom` 和 `freejoint`。
- 理解 `MjModel`、`MjData`、`mj_step` 和 Viewer 的基本作用。

完成内容：

- 将小球初始高度从 1 米修改为 2 米。
- 将地球重力 `-9.81 m/s²` 修改为月球重力 `-1.62 m/s²`。
- 将小球质量从 0.1 千克修改为 1 千克。
- 为自由落体 Python 示例添加逐行中文注释。
- 整理 MJCF/XML 零基础速查文档。
- 添加 `.gitignore`，忽略 Python 缓存、编辑器配置和仿真输出。

实验结论：

- 重力减小后，小球下落得更慢。
- 初始高度增加后，小球接触地面的时间更晚。
- 在相同重力下，修改小球质量不会改变自由落体加速度。
- `body` 表示刚体和坐标系，`geom` 表示形状与碰撞体。
- 没有 `freejoint` 时，小球会固定在世界中。

下一步：

- [ ] 运行 `02_read_state.py`。
- [ ] 学习读取 `qpos`、物体位置和接触数量。

## 2026-06-16

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

## 2026-06-17

今天学习：

- 确认 `hinge`、`axis`、`range`、`actuator` 和 `data.ctrl` 的含义。
- 学习 `04_motion_control.py` 和 `05_close_gripper.py`。
- 理解目标关节值 `ctrl` 和实际关节值 `qpos` 的区别。
- 理解两指夹爪中的 `slide joint`、执行器顺序和夹爪闭合过程。
- 在 `05_close_gripper.py` 与 `gripper.xml` 中补充中文注释。

下一步：

- [ ] 开始周四任务：运行 `06_contact_detection.py`。
- [ ] 学习接触发生在 `geom` 之间。
- [ ] 输出接触双方名称和首次接触时间。

## 2026-06-19

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
- [x] 整理 `docs/notes/mujoco-summary.md`。
- [x] 总结 `body / geom / joint / actuator`。
- [x] 总结 `qpos / qvel / xpos / ctrl / contact`。
- [x] 总结保存视频和判断抓取成功的方法。

## 2026-06-20

今天学习：

- 复习 `body / geom / joint / actuator`。
- 复习 `qpos / qvel / xpos / ctrl / contact`。
- 总结无 UI 视频保存流程。
- 总结当前抓取成功判断及其不足。
- 理解 MuJoCo 在 BODex 项目中负责物理验证。

完成内容：

- 能用自己的话解释 MuJoCo 的核心模型与状态概念。
- 完成并提交 `docs/notes/mujoco-summary.md`。

实验结论：

- BODex 负责生成候选抓取姿态，MuJoCo 负责验证姿态是否真的能够抓住物体。
- 仅凭最终高度判断抓取成功可能产生误判，后续需要结合接触和保持时间。

## 2026-06-21

今天学习：

- 下载并查看 Linker Hand 官方 URDF 仓库。
- 选择 `L20 right` 作为第一个纯仿真模型。
- 理解 Linker Hand 是产品系列，L20 是具体型号。
- 确认 L20 右手模型包含 22 个 link 和 21 个 revolute joint。
- 找到手掌根节点 `base_link` 和五个指尖末端 link。
- 阅读 `parent / child / axis / limit`。
- 理解普通手指的四个关节以及拇指对掌结构。
- 理解 URDF 与 MuJoCo MJCF 的区别。
- 理解 `joint_map.yaml` 用于不同系统之间的关节名称和顺序映射。

完成内容：

- 新增 `docs/notes/linkerhand-model-notes.md`。
- 新增 `examples/linkerhand/joint_map.yaml`。
- 记录全部 21 个 URDF 关节及其上下限。
- 未确认的电机编号和耦合关系统一标记为 `TODO`。

实验结论：

- URDF 是机器人结构说明，MJCF 是可直接描述完整物理场景的 MuJoCo 模型格式。
- BODex 输出的数组不能直接猜测含义，必须按关节名称和顺序建立映射。
- 当前没有真机，因此只做模型、抓取生成和 MuJoCo 仿真验证。

下一步：

- [ ] 检查 BODex 所需的 Python、CUDA、PyTorch 和驱动环境。
- [ ] 建立独立 BODex 环境。
- [ ] 跑通官方 Shadow Hand 示例。

## 日志模板

```markdown
## YYYY-MM-DD

今天学习：

-

完成内容：

-

遇到的问题：

-

下一步：

- [ ]
```
