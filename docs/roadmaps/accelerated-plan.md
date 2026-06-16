# 加速学习计划：MuJoCo 本周收口，下周进入 Linker Hand + BODex

> 当前目标：加快节奏，用一周完成 MuJoCo 基础闭环，下周开始 BODex 官方示例和 Linker Hand 适配准备。
>
> 重要提醒：下周的合理目标是“跑通 BODex 官方示例 + 完成 Linker Hand 前置资料 + 尝试最小模型适配”，不是直接完成完整论文复现。
>
> 本计划只覆盖最近两周。完整 8～12 周路线见[长期学习与项目路线图](./long-term-plan.md)。

## 1. 两周总目标

```text
本周
  MuJoCo 基础完结
  能读取状态、控制关节、检测接触、保存视频、判断抓取成功

下周
  跑通 BODex 官方示例
  整理 Linker Hand 关节和 link 信息
  建立 joint_map.yaml 初版
  尝试让 Linker Hand 模型进入 BODex/cuRobo 流程
```

完成这两周后，再进入：

```text
第三周
  Linker Hand 最小抓取姿态生成
  MuJoCo 中做简单物体抓取验证
```

## 2. 本周：MuJoCo 快速完结

每天建议 1～2 小时。不要追求看完所有文档，围绕“以后验证 BODex 抓取”学习。

### 周二：状态读取 + 单关节

学习文件：

- `examples/mujoco/scripts/02_read_state.py`
- `examples/mujoco/scripts/03_single_joint.py`
- `examples/mujoco/models/hinge.xml`

任务：

- [ ] 运行 `02_read_state.py`
- [ ] 输出小球 z 方向速度 `qvel_z`
- [ ] 记录小球第一次接触地面的时间
- [ ] 阅读 `03_single_joint.py`
- [ ] 为 `03_single_joint.py` 添加中文注释
- [ ] 运行单关节位置控制

必须理解：

- `qpos`
- `qvel`
- `xpos`
- `ncon`
- `hinge`
- `axis`
- `range`
- `actuator`
- `data.ctrl`

验收标准：

- [ ] 能说出 `qpos`、`qvel`、`xpos` 的区别
- [ ] 能解释 `data.ctrl[0] = 0.8` 的含义
- [ ] 能让单关节运动到指定角度

### 周三：轨迹控制 + 两指夹爪

学习文件：

- `examples/mujoco/scripts/04_motion_control.py`
- `examples/mujoco/scripts/05_close_gripper.py`
- `examples/mujoco/models/gripper.xml`

任务：

- [ ] 运行 `04_motion_control.py`
- [ ] 将正弦轨迹改成 A 点到 B 点的线性插值
- [ ] 运行 `05_close_gripper.py`
- [ ] 保存夹爪闭合视频
- [ ] 修改一次方块质量
- [ ] 修改一次手指摩擦

必须理解：

- 目标关节值和实际关节值不是同一个东西
- 控制应该连续插值，不能一步跳到目标
- `slide joint` 表示滑动关节
- `ctrl` 顺序来自 `<actuator>` 中执行器顺序

验收标准：

- [ ] 能让关节平滑运动
- [ ] 能让两指夹爪闭合
- [ ] 能说明质量和摩擦对抓取有什么影响

### 周四：接触检测 + 抓取抬升

学习文件：

- `examples/mujoco/scripts/06_contact_detection.py`
- `examples/mujoco/scripts/07_grasp_and_lift.py`

任务：

- [ ] 运行 `06_contact_detection.py`
- [ ] 输出左手指首次接触方块的时间
- [ ] 输出右手指首次接触方块的时间
- [ ] 运行 `07_grasp_and_lift.py`
- [ ] 输出最终物体高度
- [ ] 输出抓取成功或失败
- [ ] 保存抓取抬升视频

必须理解：

- 接触发生在 `geom` 之间
- `data.contact[i].geom1` 和 `data.contact[i].geom2` 是 geom ID
- 需要把 geom ID 转换成名字才好理解
- “碰到物体”不等于“抓住物体”

验收标准：

- [ ] 能打印接触双方名称
- [ ] 能判断物体是否离地
- [ ] 能写出一个最简单的抓取成功条件

### 周五：无 UI 批量测试框架

任务：

- [ ] 改造或新增一个 `07_grasp_and_lift_headless.py`
- [ ] 不打开 Viewer，只运行物理仿真
- [ ] 支持保存 MP4
- [ ] 输出 JSON 结果

建议输出：

```json
{
  "success": true,
  "object_height": 0.12,
  "max_contacts": 4,
  "hold_time": 2.0
}
```

必须理解：

- 批量评估时不可能每个抓取都手动看
- 大量候选抓取应该先用数据筛选
- 只为成功案例、失败案例和边界案例保存视频

验收标准：

- [ ] 可以在无 UI 环境运行
- [ ] 可以保存视频
- [ ] 可以输出结构化结果

### 周六：MuJoCo 总结

任务：

- [ ] 写一篇 `docs/notes/mujoco-summary.md`
- [ ] 总结 `body / geom / joint / actuator`
- [ ] 总结 `qpos / qvel / xpos / ctrl / contact`
- [ ] 总结如何保存视频
- [ ] 总结如何判断抓取成功
- [ ] 提交代码

验收标准：

- [ ] 能用自己的话解释 MuJoCo 在 BODex 项目中负责什么
- [ ] 能从零运行一个简单抓取测试

### 周日：Linker Hand 预习

任务：

- [ ] 下载或克隆 `linkerhand-urdf`
- [ ] 确认自己的 Linker Hand 型号
- [ ] 确认左手还是右手
- [ ] 找到对应 URDF/STL
- [ ] 列出全部 link
- [ ] 列出全部 joint
- [ ] 找到掌心 link
- [ ] 找到五个指尖 link

产出文件建议：

```text
docs/notes/linkerhand-model-notes.md
examples/linkerhand/joint_map.yaml
```

验收标准：

- [ ] 知道模型有多少个关节
- [ ] 知道模型有多少个可控自由度
- [ ] 知道 URDF 关节名和真机电机名可能不同

## 3. 下周：BODex + Linker Hand 前置适配

### 周一：BODex 环境准备

任务：

- [ ] 创建单独 Conda 环境
- [ ] 记录 Python、CUDA、PyTorch、驱动版本
- [ ] 安装 BODex 依赖
- [ ] 保存完整安装命令

风险：

- CUDA 版本不匹配
- PyTorch 版本不匹配
- cuRobo 安装失败
- 显存不足

验收标准：

- [ ] Python 能 import 项目核心依赖
- [ ] 环境版本记录完整

### 周二：跑通 BODex 官方示例

任务：

- [ ] 跑通官方 Shadow Hand 示例
- [ ] 保存运行命令
- [ ] 保存输出结果
- [ ] 如果失败，记录完整报错

硬规则：

> 官方示例没有跑通前，不进入 Linker Hand 适配。

验收标准：

- [ ] 能生成至少一个官方示例抓取结果
- [ ] 能找到结果文件位置

### 周三：理解 BODex 输出

任务：

- [ ] 找到 hand pose
- [ ] 找到 object pose
- [ ] 找到 joint positions
- [ ] 找到 pre-grasp、grasp、squeeze
- [ ] 搞清官方示例的关节顺序

验收标准：

- [ ] 能说明 BODex 输出哪些数据
- [ ] 能说明哪些数据要送进 MuJoCo 验证

### 周四：Linker Hand 关节映射

任务：

- [ ] 建立 `joint_map.yaml`
- [ ] 写入 URDF joint 名称
- [ ] 写入关节范围
- [ ] 写入手指归属
- [ ] 标记未知的 motor_id
- [ ] 标记是否存在耦合

模板：

```yaml
hand_model: TODO
side: TODO
palm_link: TODO

joints:
  - urdf_name: TODO
    motor_id: TODO
    finger: thumb
    lower_rad: TODO
    upper_rad: TODO
    direction: 1
    offset: 0
    coupled: false
```

验收标准：

- [ ] 所有 URDF 可动关节都在表中
- [ ] 未知项统一写为 `TODO`
- [ ] 不靠猜测数组顺序

### 周五：Linker Hand 模型加载尝试

任务：

- [ ] 尝试让 BODex/cuRobo 加载 Linker Hand 模型
- [ ] 如果失败，记录失败原因
- [ ] 检查 mesh 路径
- [ ] 检查关节上下限
- [ ] 检查掌心 link

验收标准：

- [ ] 成功加载模型，或者获得明确的失败清单
- [ ] 不修改多个问题后才测试

### 周末：最小适配评估

目标：

- [ ] Linker Hand 模型能显示或被解析
- [ ] 关节顺序基本明确
- [ ] 至少能生成或接收一个候选姿态
- [ ] 明确下一周需要解决的模型、碰撞或关节映射问题

## 4. 本周最终通过标准

本周结束时，MuJoCo 阶段通过标准是：

- [ ] 不打开 Viewer 也能运行仿真
- [ ] 能保存 MP4 视频
- [ ] 能读取物体位置、速度和接触
- [ ] 能控制单关节和夹爪
- [ ] 能判断一次简单抓取成功或失败
- [ ] 能解释 `qpos` 和 `ctrl` 不是一回事
- [ ] 能按名称查找 body、joint、geom 和 actuator ID

达到这些，就停止纯 MuJoCo 学习，进入 Linker Hand + BODex。

## 5. 不做清单

本周不要深入：

- MuJoCo 高级接触求解参数
- 肌肉模型
- 软体仿真
- 强化学习环境封装
- Isaac Sim
- Gazebo
- 相机识别
- 真机控制

这些都等 Linker Hand 最小仿真闭环跑通后再说。
