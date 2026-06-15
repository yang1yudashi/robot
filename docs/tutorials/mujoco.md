# MuJoCo 零基础实战教程

这套教程面向机器人初学者，目标不是一次学完 MuJoCo 的所有功能，而是掌握 Linker Hand + BODex 项目真正需要的部分：

```text
加载模型
  ↓
读取关节状态
  ↓
控制关节
  ↓
检测碰撞与接触
  ↓
闭合夹爪并抬起物体
  ↓
替换为 Linker Hand 和 BODex 抓取姿态
```

教程包含 7 个可以直接运行的小实验。建议按顺序完成，不要只看代码。

## 1. 学完后能做什么

完成教程后，你应该能够：

- 看懂基础 MJCF/XML 模型。
- 理解 `MjModel` 和 `MjData` 的区别。
- 读取 `qpos`、`qvel`、物体位置和接触信息。
- 使用 `data.ctrl` 控制位置执行器。
- 设置关节、质量、摩擦和时间步长。
- 编写一个简单的抓取成功判断。
- 理解如何把 BODex 输出的关节角送入 MuJoCo。

## 2. MuJoCo 中最重要的概念

第一次接触MJCF/XML时，可以配合阅读：

- [MJCF/XML 零基础速查](../references/mjcf-quick-reference.md)

| 概念 | 含义 | Linker Hand 中的用途 |
| --- | --- | --- |
| body | 刚体和坐标系 | 掌心、指节、物体 |
| geom | 碰撞和显示形状 | 手指表面、物体表面 |
| joint | body 之间的运动自由度 | 手指转动关节 |
| actuator | 对 joint 施加控制 | 电机的位置或力矩控制 |
| sensor | 仿真测量数据 | 关节、力和接触信息 |
| `qpos` | 广义位置 | 关节角和自由物体位姿 |
| `qvel` | 广义速度 | 关节速度和物体速度 |
| `ctrl` | 执行器控制输入 | 目标角度或力矩 |
| contact | 当前接触点 | 判断手指是否接触物体 |

需要特别注意：

> `qpos` 的顺序不一定等于 actuator 的顺序，也不一定等于 BODex 输出或真机电机的顺序。

以后适配 Linker Hand 时，必须按照名称建立明确映射。

## 3. 安装环境

MuJoCo 官方 Python 包可以通过 `pip` 安装。当前教程约束在 MuJoCo 3.x。

### 3.1 创建虚拟环境

推荐使用 Conda：

```bash
conda create -n mujoco-study python=3.10
conda activate mujoco-study
```

进入配套示例目录并安装依赖：

```bash
cd examples/mujoco
python -m pip install -r requirements.txt
```

检查版本：

```bash
python -c "import mujoco; print(mujoco.__version__)"
```

官方 `mujoco` Python 包已经包含 MuJoCo 运行库，不需要像旧教程那样单独下载 `mujoco-py`。不要安装已经停止作为主线使用的 `mujoco-py`。

### 3.2 图形窗口问题

示例使用官方交互式 viewer。运行时会打开一个窗口：

- 鼠标左键拖动：旋转视角。
- 鼠标右键拖动：平移视角。
- 滚轮：缩放。
- 双击物体：聚焦物体。

如果窗口没有出现：

1. 确认当前环境可以正常显示桌面窗口。
2. 确认安装的是 `mujoco`，不是 `mujoco-py`。
3. 在 Linux 远程服务器上运行时，需要配置图形转发或使用无头渲染。
4. 先运行不需要窗口的 `02_read_state.py`，区分模型问题和图形问题。

## 4. 目录结构

```text
examples/mujoco/
├── README.md
├── requirements.txt
├── scripts/
│   ├── 01_free_fall.py
│   ├── 02_read_state.py
│   ├── 03_single_joint.py
│   ├── 04_motion_control.py
│   ├── 05_close_gripper.py
│   ├── 06_contact_detection.py
│   └── 07_grasp_and_lift.py
└── models/
    ├── free_fall.xml
    ├── hinge.xml
    └── gripper.xml
```

所有命令均在 `examples/mujoco` 目录中运行。

## 5. 实验一：自由落体

运行：

```bash
python scripts/01_free_fall.py
```

你会看到一个小球从 1 米高度落下，与地面发生碰撞。

模型中的核心内容：

```xml
<body name="ball" pos="0 0 1">
  <freejoint/>
  <geom type="sphere" size="0.05" mass="0.1"/>
</body>
```

这里：

- `body` 创建小球刚体。
- `pos="0 0 1"` 表示初始位置在 1 米高处。
- `freejoint` 让物体具有自由平移和旋转能力。
- `geom` 创建半径为 0.05 米的碰撞球。
- `mass` 设置质量，单位为千克。

### 动手练习

- [ ] 将小球高度改为 2 米。
- [ ] 将重力改成月球重力 `0 0 -1.62`。
- [ ] 将球替换成 box。
- [ ] 修改地面和小球颜色。

### 验收

能够指出 XML 中哪一行控制高度、重力、形状和质量。

## 6. 实验二：读取仿真状态

运行：

```bash
python scripts/02_read_state.py
```

这个实验不打开窗口，而是输出：

```text
nq=7, nv=6, nu=0
time=...
qpos_z=...
xpos_z=...
contacts=...
```

核心对象：

```python
model = mujoco.MjModel.from_xml_path(...)
data = mujoco.MjData(model)
mujoco.mj_step(model, data)
```

- `MjModel` 保存基本不变的模型信息，例如关节、质量和时间步长。
- `MjData` 保存不断变化的状态，例如关节位置、速度和接触。
- `mj_step` 让物理世界前进一步。

为什么自由物体的 `nq=7`、`nv=6`？

- 位置使用 `x, y, z` 加四元数，共 7 个数。
- 速度使用 3 个线速度加 3 个角速度，共 6 个数。

### 动手练习

- [ ] 将输出间隔从 100 步改成 50 步。
- [ ] 输出小球的 z 方向速度。
- [ ] 记录首次出现接触的时间。
- [ ] 比较 `qpos` 和 `xpos` 中的小球高度。

### 验收

能够解释为什么不能把整个 `data.qpos` 都理解成“关节角”。

## 7. 实验三：单关节位置控制

运行：

```bash
python scripts/03_single_joint.py
```

模型包含一个转动关节：

```xml
<joint name="arm_joint"
       type="hinge"
       axis="0 1 0"
       range="-90 90"/>
```

以及一个位置执行器：

```xml
<position name="arm_position"
          joint="arm_joint"
          kp="30"
          kv="3"
          ctrlrange="-1.57 1.57"/>
```

Python 中使用：

```python
data.ctrl[0] = 0.8
```

给执行器设置目标位置。这里使用弧度，因此 `0.8 rad` 大约是 `45.8°`。

`kp` 越大，执行器通常越努力追踪目标，但设置过大可能导致振荡或不稳定。`kv` 提供速度阻尼。

### 动手练习

- [ ] 将目标改成 `-0.5 rad`。
- [ ] 分别尝试较小和较大的 `kp`。
- [ ] 修改 `axis`，观察旋转方向变化。
- [ ] 缩小关节 `range` 并观察限制效果。

### 验收

能够解释 `joint`、`actuator` 和 `data.ctrl` 三者的关系。

## 8. 实验四：连续轨迹控制

运行：

```bash
python scripts/04_motion_control.py
```

程序每一步都更新目标：

```python
target = 0.8 * math.sin(2 * math.pi * 0.25 * data.time)
data.ctrl[0] = target
```

这说明控制不是“发送一次命令就结束”，而是随时间连续更新目标。

未来执行 BODex 抓取姿态时，也不应该让手指从张开姿态瞬间跳到抓取姿态。应该进行插值：

```python
q_target = (1.0 - ratio) * q_open + ratio * q_grasp
```

### 动手练习

- [ ] 改变振幅。
- [ ] 改变运动频率。
- [ ] 将正弦运动改成两个目标之间的线性插值。
- [ ] 每隔 0.5 秒输出目标角和实际角。

### 验收

能够区分目标关节角和实际关节角。

## 9. 实验五：两指夹爪闭合

运行：

```bash
python scripts/05_close_gripper.py
```

这个模型包含：

- 一个自由运动的绿色方块。
- 一个可以上下运动的手掌。
- 两个滑动手指。
- 三个位置执行器。

控制数组：

```text
data.ctrl[0] = 手掌抬升目标
data.ctrl[1] = 左手指闭合目标
data.ctrl[2] = 右手指闭合目标
```

注意，`ctrl` 的顺序来自 `<actuator>` 中执行器的定义顺序，而不是 joint 在 XML 中出现的顺序。

### 动手练习

- [ ] 让左右手指以不同速度闭合。
- [ ] 改变方块尺寸。
- [ ] 减小手指摩擦系数。
- [ ] 输出每个关节的实际 `qpos`。

### 验收

两个手指能够接近方块，且最终关节状态不会超过关节范围。

## 10. 实验六：检测接触

运行：

```bash
python scripts/06_contact_detection.py
```

程序通过以下数据读取接触：

```python
data.ncon
data.contact[index].geom1
data.contact[index].geom2
```

接触发生在 `geom` 之间，而不是抽象的 joint 之间。程序将 geom ID 转换为名称，输出新出现的接触组合。

在灵巧手抓取中，仅有接触数量还不能证明抓取成功。例如：

- 手指可能只从单侧碰到物体。
- 物体可能同时接触地面。
- 接触可能伴随严重穿透。
- 抬升后物体仍可能滑落。

### 动手练习

- [ ] 找出方块和左手指首次接触的时间。
- [ ] 找出方块和右手指首次接触的时间。
- [ ] 判断闭合结束时物体是否还接触地面。
- [ ] 阅读 MuJoCo API，尝试取得接触力。

### 验收

能够输出“哪个手指在什么时间接触了哪个物体”。

## 11. 实验七：抓取并抬升

运行：

```bash
python scripts/07_grasp_and_lift.py
```

控制过程分成三个阶段：

```text
0.0～0.5 秒：等待模型稳定
0.5～2.0 秒：闭合手指
2.5～4.5 秒：抬高手掌
4.5～6.0 秒：保持并观察
```

程序使用一个非常简单的成功标准：

```python
success = object_height > 0.08
```

真实抓取评估至少还应该检查：

- 物体是否离开地面。
- 物体是否保持一定时间。
- 物体是否距离手掌过远。
- 关节是否超过限制。
- 是否发生不合理穿透。
- 抓取过程中是否出现异常大力。

### 动手练习

- [ ] 让手掌抬得更高。
- [ ] 将保持时间增加到 10 秒。
- [ ] 把摩擦系数降低一半，观察是否滑落。
- [ ] 改变物体质量。
- [ ] 将成功条件改成“离地且保持 3 秒”。

### 验收

能够解释为什么“优化得到抓取姿态”和“物理仿真抓取成功”不是同一件事。

## 12. 从两指夹爪迁移到 Linker Hand

完成 7 个实验后，再开始适配 Linker Hand。

### 12.1 第一步：整理模型

需要确认：

- 掌心 body 名称。
- 所有可控 joint 名称。
- 五个指尖 geom/body 名称。
- 每个关节的范围和轴方向。
- URDF 关节、BODex 关节和真机电机之间的对应关系。
- 是否存在耦合关节。

### 12.2 第二步：建立名称映射

不要使用固定数组下标猜测关节顺序。使用名称查找 ID：

```python
joint_id = mujoco.mj_name2id(
    model,
    mujoco.mjtObj.mjOBJ_JOINT,
    "joint_name",
)
```

进一步读取 joint 对应的 `qpos` 地址：

```python
qpos_address = model.jnt_qposadr[joint_id]
```

执行器也应按名称取得 ID：

```python
actuator_id = mujoco.mj_name2id(
    model,
    mujoco.mjtObj.mjOBJ_ACTUATOR,
    "actuator_name",
)
data.ctrl[actuator_id] = target
```

### 12.3 第三步：输入 BODex 姿态

BODex 可能输出：

```text
pre-grasp qpos
grasp qpos
squeeze qpos
```

推荐执行方式：

```text
张开姿态
  ↓ 插值
pre-grasp
  ↓ 手掌接近物体
grasp
  ↓ 缓慢闭合
squeeze
  ↓
抬升并保持
```

每个阶段都要：

1. 按名称转换关节顺序。
2. 检查上下限。
3. 使用插值控制。
4. 记录接触与物体位置。
5. 判断是否抓取成功。

### 12.4 第四步：批量评估

单个抓取成功后，再编写批量测试：

```text
读取一个 BODex 抓取
→ 重置仿真
→ 执行抓取
→ 抬升
→ 记录成功或失败
→ 测试下一个抓取
```

建议保存：

```json
{
  "grasp_id": 1,
  "success": true,
  "max_object_height": 0.15,
  "hold_time": 3.0,
  "final_contacts": 4
}
```

## 13. 常见问题

### 模型一加载就爆炸

常见原因：

- 初始状态存在严重穿透。
- 质量或惯性不合理。
- 控制增益过大。
- 时间步长过大。
- mesh 单位错误。

处理顺序：

1. 暂时关闭执行器。
2. 检查初始碰撞。
3. 使用简单 geom 替代复杂 mesh。
4. 降低 `kp`。
5. 缩小 timestep。

### 关节朝反方向运动

检查：

- joint 的 `axis`。
- 模型零姿态。
- BODex 到 MuJoCo 的正负号。
- 左手和右手模型是否混用。

### 手指穿过物体

检查：

- 是否定义 collision geom。
- mesh 是否正常加载。
- `contype` 和 `conaffinity` 是否禁用了碰撞。
- 时间步长和控制速度是否过大。
- 接触模型参数是否合理。

### 夹住后仍然滑落

不要只增大摩擦。还要检查：

- 接触位置是否形成稳定抓取。
- 手指闭合力是否足够。
- 物体质量是否合理。
- 指尖碰撞模型是否准确。
- 抓取姿态是否只在几何上接近，而没有力闭合能力。

## 14. 推荐学习节奏

| 天数 | 内容 | 结果 |
| ---: | --- | --- |
| 1 | 安装环境、实验 1 | 看见自由落体 |
| 2 | 实验 2 | 会读取状态 |
| 3 | 实验 3 | 会控制单关节 |
| 4 | 实验 4 | 会生成连续轨迹 |
| 5 | 阅读夹爪 XML | 看懂 joint 和 actuator |
| 6 | 实验 5、6 | 会闭合和检测接触 |
| 7 | 实验 7 | 完成抓取抬升 |
| 8～10 | 修改物体、摩擦和质量 | 形成实验记录 |
| 11～14 | 阅读 Linker Hand 模型 | 建立关节映射 |

每天学习结束后，在仓库根目录的 README 学习日志中记录：

- 今天运行了哪个实验。
- 修改了什么参数。
- 观察到了什么。
- 遇到了什么错误。
- 明天准备做什么。

## 15. 官方资料

- [MuJoCo 官方文档](https://mujoco.readthedocs.io/en/stable/)
- [Python Bindings](https://mujoco.readthedocs.io/en/stable/python.html)
- [MJCF XML Reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)
- [MuJoCo GitHub](https://github.com/google-deepmind/mujoco)
- [MuJoCo Menagerie 模型库](https://github.com/google-deepmind/mujoco_menagerie)
- [DexGraspBench](https://github.com/JYChen18/DexGraspBench)

## 16. 完成检查

- [ ] 7 个示例全部运行。
- [ ] 理解 `MjModel`、`MjData` 和 `mj_step`。
- [ ] 会读取 `qpos`、`qvel` 和 body 位置。
- [ ] 会通过 actuator 控制 joint。
- [ ] 会使用名称查找 body、joint、geom 和 actuator ID。
- [ ] 会检测物体和手指接触。
- [ ] 会编写抓取成功条件。
- [ ] 修改过质量、摩擦、控制增益和时间步长。
- [ ] 能说明如何将 BODex 关节姿态映射到 MuJoCo。
