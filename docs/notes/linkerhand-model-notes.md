# Linker Hand L20 模型学习笔记

日期：2026-06-21

## 1. 当前学习对象

本次选择 Linker Hand `L20 right` 作为第一个纯仿真学习模型。

官方模型位于独立资源仓库：

```text
D:\CodeStudy\robot\resource\linkerhand-urdf\l20\right\linkerhand_l20_right.urdf
```

当前没有 Linker Hand 真机，因此本阶段只学习：

- URDF 模型结构
- 关节名称、连接关系和运动范围
- 后续 BODex/Dexonomy 模型适配
- MuJoCo 抓取仿真验证

暂时不学习真机 SDK、电机控制、电流反馈和安全控制。

## 2. L20 模型概况

L20 是 Linker Hand 系列中的五指灵巧手型号。

当前右手 URDF 包含：

- 22 个 `link`
- 21 个 `joint`
- 21 个关节均为 `revolute` 旋转关节
- 根 link（手掌）：`base_link`

22 个 link 只需要 21 个 joint，是因为 `base_link` 是整棵结构树的根节点，不需要关节连接到自己。其余 21 个子 link 各通过一个 joint 连接到父 link。

型号名称中的数字不一定等于 URDF 可动关节数。URDF 描述模型中能够运动的关节，真机独立电机数量还可能受到机械耦合影响。

## 3. URDF 和 MuJoCo MJCF 的区别

URDF 主要描述机器人本体：

- `link`
- `joint`
- `visual`
- `collision`
- 质量和惯性
- 关节轴与关节限位

MuJoCo MJCF 除了机器人结构，还可以直接描述完整仿真场景：

- 地面、灯光和被抓物体
- 关节和执行器
- 重力和仿真步长
- 接触、摩擦和传感器

常见概念对应：

| URDF | MuJoCo MJCF | 作用 |
| --- | --- | --- |
| `link` | `body` | 机器人部件与坐标系 |
| `visual` | 显示用 `geom` | 外观 |
| `collision` | 碰撞用 `geom` | 碰撞形状 |
| `revolute` joint | `hinge` joint | 旋转关节 |
| `prismatic` joint | `slide` joint | 滑动关节 |
| `limit` | `range` | 关节范围 |

URDF 通常不直接定义 MuJoCo 的执行器。后续将 Linker Hand 放入 MuJoCo 时，还需要转换或整理模型，并添加 actuator 和仿真场景。

## 4. 如何阅读一个 URDF joint

以 `pinky_mcp_roll` 为例，重点字段包括：

```xml
<joint name="pinky_mcp_roll" type="revolute">
  <origin xyz="..." rpy="..."/>
  <parent link="base_link"/>
  <child link="pinky_metacarpals"/>
  <axis xyz="1 0 0"/>
  <limit lower="-0.17" upper="0.17"/>
</joint>
```

含义：

- `origin`：关节在父 link 坐标系中的位置和朝向
- `parent`：父 link
- `child`：被该关节带动的子 link
- `axis`：关节局部坐标系中的旋转轴
- `lower / upper`：允许的最小和最大角度，单位为弧度
- `effort`：关节允许的力矩限制
- `velocity`：关节速度限制

## 5. 普通手指结构

食指、中指、无名指和小拇指均有 4 个关节：

```text
mcp_roll
→ mcp_pitch
→ pip
→ dip
```

作用：

- `mcp_roll`：手指根部左右侧摆
- `mcp_pitch`：手指根部弯曲
- `pip`：手指中段弯曲
- `dip`：靠近指尖的关节弯曲

以小拇指为例：

```text
base_link
  │ pinky_mcp_roll
  ↓
pinky_metacarpals
  │ pinky_mcp_pitch
  ↓
pinky_proximal
  │ pinky_pip
  ↓
pinky_middle
  │ pinky_dip
  ↓
pinky_distal
```

小拇指关节范围：

| joint | 范围（rad） | 主要动作 |
| --- | ---: | --- |
| `pinky_mcp_roll` | `-0.17` 到 `0.17` | 左右侧摆 |
| `pinky_mcp_pitch` | `0` 到 `1.4` | 根部弯曲 |
| `pinky_pip` | `0` 到 `1.57` | 中段弯曲 |
| `pinky_dip` | `0` 到 `1.4` | 指尖附近弯曲 |

## 6. 拇指结构

拇指包含 5 个关节：

```text
thumb_cmc_yaw
thumb_cmc_roll
thumb_cmc_pitch
thumb_mcp
thumb_dip
```

普通手指主要负责侧摆和弯曲，拇指根部的 CMC 关节组还需要调整多个旋转方向，使拇指能够朝向其他手指并完成对掌。

对掌能力使五指手能够捏住和包住物体，而不只是像平行夹板一样闭合。

## 7. 五个指尖 link

根据当前 URDF 的命名，五个指尖末端 link 为：

```text
thumb_distal
index_distal
middle_distal
ring_distal
pinky_distal
```

后续适配 BODex/cuRobo 时，需要确认这些 link 是否直接作为指尖 link 使用，还是需要额外定义具体接触点。

## 8. 当前结论

我已经能够：

- 区分 Linker Hand 产品系列和具体型号。
- 说明 L20 右手模型的 link、joint 和根节点数量。
- 理解 URDF 与 MuJoCo MJCF 的区别。
- 阅读 joint 的 `parent / child / axis / limit`。
- 理解普通手指的四个关节。
- 理解拇指多方向运动和对掌的作用。

下一阶段需要：

- 跑通 BODex 官方手型示例。
- 理解 BODex 机器人配置如何引用 URDF。
- 确认 Linker Hand 的关节顺序和耦合关系。
- 将 BODex 输出映射到 Linker Hand URDF/MuJoCo 关节顺序。
