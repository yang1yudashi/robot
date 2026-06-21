# MuJoCo 学习总结

日期：2026-06-21

## 1. MuJoCo 是什么

MuJoCo 是一个机器人物理仿真环境，可以模拟物体运动、关节控制、碰撞、摩擦和接触。

在当前 Linker Hand + BODex 项目中：

```text
BODex：生成灵巧手的候选抓取姿态
MuJoCo：模拟抓取过程，验证候选姿态能否真的抓住物体
```

MuJoCo 可以检查手指是否接触物体、是否发生穿模、物体能否被抬起，以及抓住后是否会滑落。

## 2. 模型结构

### body

`body` 可以理解为一个带有位置和姿态的整体，也是模型的结构容器。一个 `body` 可以包含多个 `geom`，这些 `geom` 会跟随该 `body` 一起运动。

### geom

`geom` 描述仿真环境中的具体形状，例如 `box`、`sphere` 和 `plane`。它主要负责显示和碰撞检测。

地面通常是一个 `type="plane"` 的 `geom`。灯光 `light` 不属于 `geom`。

### joint

`joint` 定义一个 `body` 相对于父 `body` 能够怎样运动，例如旋转、滑动或者自由运动。

`joint` 规定“能怎么动”，但不会主动驱动模型运动。

### actuator

`actuator` 是驱动器，通过 `data.ctrl` 接收控制输入，驱动对应的 `joint`。

在当前示例的 `position actuator` 中，`ctrl` 表示目标关节位置。

```text
joint：规定能怎么动
actuator：负责让 joint 动起来
```

## 3. 仿真状态

### qpos

`qpos` 表示关节当前的实际位置或姿态。

### qvel

`qvel` 表示关节当前的实际运动速度。它和 `qpos` 配套：

```text
qpos：现在在哪里
qvel：现在动得多快
```

### xpos

`xpos` 表示 `body` 在世界坐标系中的位置。

例如：

```python
object_height = data.xpos[object_id, 2]
```

这里读取的是物体 `body` 的 z 轴高度。

### ctrl

`ctrl` 是发送给执行器的控制输入。在位置执行器中，它是目标关节位置，不是关节的实际位置。

即使设置：

```python
data.ctrl[1] = 0.045
```

实际 `qpos` 也可能只有 `0.0304`。这是因为关节可能受到摩擦、碰撞、质量、执行器力度和运动时间的影响。

### contact

`contact` 保存 `geom` 之间的接触信息：

```python
data.ncon
data.contact[i].geom1
data.contact[i].geom2
```

`data.ncon` 是当前仿真步的接触点数量，不是接触物体的数量。两个 `geom` 之间可能同时产生多个接触点。

## 4. 控制和状态之间的关系

```text
actuator 使用 ctrl 驱动 joint
joint 的实际状态通过 qpos 和 qvel 读取
body 的世界位置通过 xpos 读取
geom 之间的碰撞通过 contact 读取
```

例如夹爪模型中：

```python
data.ctrl[0]    # 控制夹爪整体升降
data.ctrl[1]    # 控制左手指
data.ctrl[2]    # 控制右手指
data.ctrl[1:3]  # 同时控制左右手指
```

`data.ctrl[1:3]` 包含索引 1 和 2，不包含索引 3。

## 5. 如何保存视频

保存无界面仿真视频的基本流程是：

```text
mj_step 推进物理仿真
→ Renderer 渲染当前画面
→ 按目标帧率抽取图像帧
→ imageio 将图像帧编码成 MP4
```

主要组件：

- `mujoco.mj_step()`：推进物理仿真。
- `mujoco.Renderer`：将当前仿真状态渲染成图像。
- 抽帧逻辑：按视频帧率保存画面，不必保存每一个物理仿真步。
- `imageio`：将所有图像帧写入视频文件。

例如仿真步长为 `0.002s` 时，每秒有 500 个物理步；如果视频为 30 FPS，每秒只需要保存约 30 张画面。

## 6. 如何判断抓取成功

当前示例通过物体最终高度判断抓取是否成功：

```python
object_height = data.xpos[object_id, 2]
success = object_height > 0.08
```

如果物体最终高度超过 `0.08m`，就认为抓取成功。

这个判断比较简单，存在以下不足：

- 物体被撞飞也可能超过高度阈值。
- 物体可能只是短暂被抬起。
- 物体到达高度后可能马上滑落。
- 只检查最终高度，不能确认左右手指是否都接触物体。

更可靠的判断可以组合以下条件：

- 左右手指都接触物体。
- 物体确实离开地面。
- 物体在一定时间内保持目标高度。
- 物体没有被撞飞或明显滑落。

## 7. 无 UI 仿真

Viewer 只负责把仿真画面显示给人看，`time.sleep()` 用于限制显示速度。

真正推进物理仿真的是：

```python
mujoco.mj_step(model, data)
```

因此删除 Viewer 和等待逻辑后，物理仿真仍然可以运行，而且通常运行得更快。无 UI 仿真适合后续批量验证大量 BODex 候选抓取。

## 8. 当前学习结论

我已经能够：

- 解释 `body / geom / joint / actuator` 的基本作用。
- 区分 `qpos / qvel / xpos / ctrl / contact`。
- 控制单关节和两指夹爪。
- 读取物体高度和接触信息。
- 运行抓取抬升实验。
- 在无 UI 环境中运行仿真并输出 JSON 结果。
- 说明 BODex 和 MuJoCo 在项目中的分工。

下一阶段将预习 Linker Hand URDF，并学习 BODex 官方示例的输入、输出和机器人配置。
