# 机器人抓取学习记录

这个仓库记录从 MuJoCo 基础开始，逐步学习 Linker Hand、BODex 和灵巧手抓取仿真。

当前没有 Linker Hand 真机，项目只做纯仿真。现阶段不学习真机 SDK、电机控制、电流反馈和安全执行。

## 当前目标

第一阶段目标：

> 给定一个简单物体模型，为 Linker Hand L20 右手生成候选抓取姿态，并在 MuJoCo 中验证是否能够稳定抓取。

当前主线：

```text
MuJoCo 基础
    ↓
Linker Hand L20 URDF
    ↓
跑通 BODex 官方示例
    ↓
理解抓取结果和关节顺序
    ↓
适配 Linker Hand 模型
    ↓
MuJoCo 批量验证抓取
```

工具分工：

- Linker Hand URDF：描述手掌、手指、关节、外形和关节范围。
- BODex：生成手掌姿态和手指关节角等候选抓取结果。
- cuRobo：提供机器人运动学、碰撞检测和优化能力。
- MuJoCo：执行物理仿真，验证候选抓取是否会穿模、滑落或抓取失败。

## 当前进度

| 阶段 | 状态 | 已完成内容 |
| --- | --- | --- |
| MuJoCo 基础 | 已完成 | 状态读取、关节控制、接触检测、抓取抬升、无 UI 运行和 JSON 输出 |
| Linker Hand URDF 预习 | 已完成 | 选择 L20 右手，阅读 link、joint、axis、limit 和五指结构 |
| BODex 官方示例 | 下一步 | 准备环境，先跑通官方 Shadow Hand，不修改机器人模型 |
| Linker Hand 模型适配 | 未开始 | 机器人配置、碰撞模型和关节顺序映射 |
| MuJoCo 抓取验证 | 未开始 | 导入候选姿态，批量测试并统计成功率 |

## 当前模型

第一个练习模型选择 Linker Hand `L20 right`：

- 22 个 `link`
- 21 个 `revolute joint`
- 手掌根节点：`base_link`
- 五个指尖末端：`thumb_distal`、`index_distal`、`middle_distal`、`ring_distal`、`pinky_distal`

官方 URDF 仓库作为独立资源仓库存放在：

```text
D:\CodeStudy\robot\resource\linkerhand-urdf
```

学习仓库不复制官方 mesh 和 URDF，只保存自己的笔记、配置和实验代码。

## 下一步

1. 检查 NVIDIA 驱动、CUDA、Python 和 Conda 环境。
2. 建立独立的 BODex 环境。
3. 跑通官方 Shadow Hand 示例。
4. 找到输出中的 hand pose、joint positions、pre-grasp、grasp 和 squeeze。
5. 确认官方输出的关节顺序，再补充 Linker Hand `joint_map.yaml`。

硬规则：

> 官方示例没有跑通、输出格式没有看懂之前，不开始修改 Linker Hand 模型。

## 重要文档

### 当前学习

- [MuJoCo 学习总结](./docs/notes/mujoco-summary.md)
- [Linker Hand L20 模型笔记](./docs/notes/linkerhand-model-notes.md)
- [Linker Hand 初版关节表](./examples/linkerhand/joint_map.yaml)
- [当前加速学习计划](./docs/roadmaps/accelerated-plan.md)

### 教程与示例

- [MuJoCo 示例](./examples/mujoco/README.md)
- [MuJoCo 零基础实战教程](./examples/mujoco/tutorials/mujoco.md)
- [MJCF/XML 零基础速查](./examples/mujoco/tutorials/mujoco-mjcf-quick-reference.md)

### 项目背景

- [文档总目录](./docs/README.md)
- [学习路线入口](./docs/roadmaps/README.md)
- [Linker Hand + BODex 项目路线](./docs/roadmaps/reference/linkerhand-bodex.md)
- [具身智能长期路线](./docs/roadmaps/reference/embodied-ai-roadmap.md)
- [BODex 论文笔记](./docs/paper/bodex.md)

## 目录结构

```text
studynote/
├── docs/
│   ├── notes/          # 已完成阶段的学习总结
│   ├── paper/          # 论文笔记
│   └── roadmaps/       # 当前计划和长期路线
└── examples/
    ├── mujoco/         # MuJoCo 模型、脚本和教程
    └── linkerhand/     # Linker Hand 配置和后续适配代码
```

## 学习原则

1. 每个概念都通过一个可运行实验验证。
2. 先跑通官方示例，再修改机器人模型。
3. 每次只解决一个模型、配置或关节映射问题。
4. 不根据数组位置猜测关节含义，始终按名称建立映射。
5. 优化生成的抓取姿态必须经过物理仿真验证。
