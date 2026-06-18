# Linker Hand + BODex 灵巧手抓取学习与实现路线

> 本文是项目背景路线，不作为每日学习任务入口。每天的具体作业以[加速学习计划](../accelerated-plan.md)为准。
>
> 适用对象：机器人零基础，希望使用 Linker Hand 复现或借鉴 BODex，实现物体抓取姿态生成与真机抓取。
>
> 建议周期：16～24 周。每天 1～2 小时，每周至少完成一个可以展示的结果。
>
> 当前执行节奏已切换到加速版：本周完成 MuJoCo 基础闭环，下周进入 BODex 官方示例和 Linker Hand 适配准备。详见[加速学习计划](../accelerated-plan.md)。

## 1. 最终目标

完整系统不是只有 BODex，而是下面这条链路：

```text
物体三维模型
    ↓
BODex 生成预抓取、抓取和夹紧姿态
    ↓
Linker Hand 关节映射与限位检查
    ↓
仿真验证抓取稳定性
    ↓
机械臂或固定支架移动到预抓取位置
    ↓
Linker Hand 真机缓慢闭合
    ↓
电流、触觉或位置反馈判断是否抓稳
```

第一阶段的最终项目建议缩小为：

> 给定一个已知位置的简单物体，生成 Linker Hand 抓取姿态，在仿真中完成抓取。

不要一开始同时做相机识别、机械臂规划、灵巧手控制和 BODex 适配。

## 2. 先认识项目中的工具

| 工具 | 在项目中的作用 |
| --- | --- |
| STL/OBJ | 描述手和物体的三维表面 |
| URDF | 描述手的 link、joint、坐标系和关节限制 |
| RViz | 检查 URDF、关节运动和 TF 坐标系 |
| ROS 2 | 连接机械手、机械臂、相机和控制程序 |
| BODex | 优化手掌位姿和手指关节角，生成抓取姿态 |
| cuRobo | GPU 机器人运动学、碰撞检测和轨迹优化 |
| MuJoCo/其他物理仿真器 | 验证抓取后物体是否滑落、弹飞或穿模 |
| Linker Hand SDK | 将目标关节值发送给真实机械手 |

BODex 输出的主要是“应该摆成什么姿势”，不是完整的真机控制系统。

## 3. 开始前的硬件和软件准备

### 3.1 推荐电脑环境

- Ubuntu 22.04 或项目依赖明确支持的 Linux 版本
- NVIDIA 独立显卡
- 建议显存 12 GB 以上；显存不足时减少并行环境数量
- 32 GB 内存更舒适
- 至少预留 100 GB 磁盘空间

BODex 官方安装示例使用：

- Python 3.10
- PyTorch 2.2.2
- CUDA 12.1
- NumPy 1.26.4

先完全按照仓库版本安装，不要擅自升级 PyTorch、CUDA 或 NumPy。

### 3.2 开始前需要确认

- [ ] Linker Hand 的具体型号：L20、L25、O6、O7 或其他
- [ ] 左手还是右手
- [ ] 是否已经拿到真机
- [ ] 是否有官方 Python/ROS 2 SDK
- [ ] 每个电机的位置范围和控制单位
- [ ] 是否存在机械耦合关节
- [ ] NVIDIA 显卡型号、显存和驱动版本
- [ ] 后续是否连接机械臂

## 4. 总体阶段安排

| 阶段 | 建议时间 | 阶段成果 |
| --- | ---: | --- |
| A. Python、Linux、Git | 2 周 | 能运行和修改机器人项目 |
| B. 坐标系与运动学 | 2 周 | 能计算并解释手指末端位置 |
| C. ROS 2、URDF、RViz | 3 周 | Linker Hand 模型可正确运动 |
| D. 原版 BODex | 2～3 周 | 跑通官方 Shadow Hand 抓取示例 |
| E. Linker Hand 适配 | 4～6 周 | BODex 能输出 Linker Hand 抓取姿态 |
| F. 仿真验证 | 3～4 周 | 仿真中抓起简单物体 |
| G. 真机执行 | 3～6 周 | 低速、安全地复现抓取姿态 |

## 5. 阶段 A：Python、Linux 和 Git

### 学习内容

Python：

- 变量、列表、字典、循环和函数
- 类和对象的基本用法
- `numpy` 数组、矩阵乘法和文件保存
- YAML、JSON 和 NPY 文件读写
- 使用 `matplotlib` 画曲线

Linux：

- 文件与目录操作
- 软件安装和环境变量
- Conda 环境
- 查看 GPU：`nvidia-smi`
- 查看进程和日志

Git：

- `clone`、`status`、`diff`
- `add`、`commit`
- 分支的基本概念

### 练习

编写一个 Python 小程序：

1. 输入 5 个手指关节角。
2. 检查角度是否超过限制。
3. 将角度保存成 YAML。
4. 重新读取并画出关节角柱状图。

### 验收标准

- [ ] 能创建并激活 Conda 环境
- [ ] 能看懂普通 Python 报错的最后 10 行
- [ ] 能用 NumPy 创建和相乘 `4x4` 矩阵
- [ ] 能使用 Git 保存一次自己的代码修改

## 6. 阶段 B：坐标系和机器人运动学

### 学习内容

- 弧度和角度的转换
- 向量与矩阵
- 平移和旋转
- 旋转矩阵、欧拉角、四元数
- 齐次变换矩阵
- 父坐标系与子坐标系
- 正运动学
- 雅可比矩阵只需先理解用途
- 逆运动学先理解问题，不要求手算复杂公式

### 必做练习

用两个转动关节模拟一根手指：

```text
掌心 → 第一指节 → 第二指节 → 指尖
```

输入两个关节角，计算指尖二维坐标，并画出手指姿态。

### 验收标准

- [ ] 能解释 `xyz` 和 `rpy` 分别是什么
- [ ] 能解释 link 坐标系为什么会跟着 joint 运动
- [ ] 能判断关节轴方向错误时，模型会出现什么现象
- [ ] 能计算两段连杆的简单正运动学

## 7. 阶段 C：ROS 2、URDF 和 Linker Hand

### 7.1 ROS 2 最小知识集

重点掌握：

- workspace、package、node
- topic、message、service
- parameter 和 launch
- `/joint_states`
- TF 与 `robot_state_publisher`
- `colcon build`

暂时不必深入：

- Nav2
- SLAM
- ROS 2 底层 DDS
- 实时控制器源码

### 7.2 URDF 学习顺序

1. 用 box 创建一个手掌。
2. 添加一个 revolute joint 和一节手指。
3. 添加关节限制。
4. 在 RViz 中通过 GUI 调整关节。
5. 再阅读 Linker Hand 的完整 URDF。

需要理解的标签：

```xml
<link>
<joint>
<parent>
<child>
<origin>
<axis>
<limit>
<visual>
<collision>
<inertial>
<mimic>
```

### 7.3 Linker Hand 模型检查表

为具体型号建立一份 `joint_map.yaml`，至少记录：

```yaml
hand_model: linker_hand_unknown
side: left
palm_link: TODO

joints:
  - urdf_name: TODO
    motor_id: TODO
    finger: thumb
    lower_rad: TODO
    upper_rad: TODO
    direction: TODO
    offset: TODO
    coupled: false
```

逐项检查：

- [ ] URDF 可以加载，没有缺失 mesh
- [ ] 左右手模型没有选反
- [ ] 所有关节都能在 RViz 中运动
- [ ] 每个关节的旋转方向符合真机
- [ ] 关节范围符合机械限制
- [ ] 掌心 link 已确定
- [ ] 五个指尖 link 已确定
- [ ] mesh 单位正确，没有放大或缩小 1000 倍
- [ ] visual 和 collision 模型用途明确
- [ ] URDF 自由度与真机可控电机数量的关系明确

### 阶段成果

录制一个短视频：在 RViz 中依次移动 Linker Hand 的所有可控关节，并显示 TF。

## 8. 阶段 D：跑通原版 BODex

这一阶段不要修改机器人模型。先证明环境和官方代码正常。

### 8.1 阅读顺序

1. BODex README
2. `example_grasp/plan_batch_env.py`
3. `sim_shadow/fc.yml`
4. Shadow Hand 的机器人配置
5. 结果可视化脚本

第一次阅读源码只回答三个问题：

- 配置从哪里读入？
- 机器人模型在哪里加载？
- 最终关节姿态保存在哪里？

### 8.2 官方环境安装流程

安装命令应以 BODex 仓库最新 README 为准。建立单独环境：

```bash
conda create -n bodex python=3.10
conda activate bodex
```

克隆代码前安装 Git LFS：

```bash
sudo apt install git-lfs
git lfs install
```

安装完成后，先执行官方调试示例。初次运行将并行数设为 1：

```bash
CUDA_VISIBLE_DEVICES=0 python example_grasp/plan_batch_env.py \
  -c sim_shadow/fc.yml \
  -w 1 \
  -m usd \
  -debug \
  -d all \
  -i 0 1
```

### 8.3 需要理解的输出

- 手掌的平移与旋转
- 手指关节向量及其顺序
- pre-grasp、grasp、squeeze 三种姿态
- 接触点
- 碰撞与模型穿透
- 优化是否收敛

### 验收标准

- [ ] 原版代码在未修改机器人模型时成功运行
- [ ] 能生成至少一个抓取结果
- [ ] 能可视化抓取姿态
- [ ] 能找到保存的关节向量
- [ ] 能说清关节向量中每个元素对应哪个关节
- [ ] 保存完整的环境版本和运行命令

## 9. 阶段 E：适配 Linker Hand

这是整个项目的核心阶段。每次只改一个问题，不要同时更换机器人、物体和优化参数。

### 9.1 建立模型适配资料

从官方 URDF 提取：

- 根 link 和掌心 link
- 可控关节名称与顺序
- 固定关节
- 关节上下限
- 关节轴
- 指尖 link
- mesh 路径
- 自碰撞关系

建议生成以下文件：

```text
linkerhand_bodex/
├── README.md
├── config/
│   ├── robot.yml
│   ├── fc.yml
│   └── joint_map.yaml
├── urdf/
│   └── linker_hand.urdf
├── scripts/
│   ├── inspect_urdf.py
│   ├── convert_joint_order.py
│   └── validate_joint_limits.py
└── tests/
    └── test_joint_mapping.py
```

### 9.2 简化碰撞模型

高精度 STL 适合显示，但不一定适合快速碰撞检测。碰撞模型可以使用：

- 凸包
- 多个球体
- 胶囊体
- 简化后的低面数 mesh

原则：

- 指尖接触区域不能简化得过分粗糙。
- 掌心和指节优先保证碰撞检测稳定。
- visual 模型和 collision 模型可以不同。

### 9.3 关节映射

BODex 的关节顺序、URDF 顺序和真机电机顺序可能完全不同。必须显式映射，不能依赖“看起来顺序一样”。

```text
BODex q
    ↓ reorder
URDF q
    ↓ coupling + direction + offset
Motor command
```

映射函数至少完成：

1. 重新排列关节顺序。
2. 处理正负方向。
3. 加入零位偏移。
4. 将弧度转换为 SDK 使用的单位。
5. 处理耦合关节。
6. 限制在真机安全范围内。

### 9.4 分步验收

- [ ] BODex/cuRobo 能加载 Linker Hand 模型
- [ ] 零姿态显示正常
- [ ] 随机关节姿态不会越界
- [ ] 正运动学结果与 RViz 一致
- [ ] 自碰撞检测基本正确
- [ ] 能针对一个立方体开始优化
- [ ] 优化能输出无 NaN 的结果
- [ ] 抓取姿态没有明显穿模
- [ ] 能批量生成多个候选抓取

## 10. 阶段 F：仿真验证

BODex 优化成功不等于真实抓取一定成功。还需要物理仿真验证。

### 最小验证场景

- 固定手掌，不连接机械臂
- 物体使用立方体或圆柱体
- 使用重力
- 机械手从 pre-grasp 插值到 grasp
- 再从 grasp 插值到 squeeze
- 保持 3～5 秒
- 缓慢抬高手掌

### 记录指标

- 物体是否从手中掉落
- 是否发生明显模型穿透
- 接触力是否突然爆炸
- 关节是否超过限制
- 抓取过程中物体位移
- 抬起后保持成功的时间

### 推荐测试顺序

1. 小立方体
2. 圆柱体
3. 瓶子
4. 不规则物体
5. 不同摩擦系数
6. 物体位姿存在小误差的情况

### 验收标准

- [ ] 至少一个简单物体可被抓起
- [ ] 同一姿态重复测试 10 次并记录成功率
- [ ] 对摩擦系数变化进行测试
- [ ] 找到至少一个优化成功但仿真失败的案例并分析原因

## 11. 阶段 G：连接真实 Linker Hand

### 11.1 真机前必须完成

- [ ] 软件急停可用
- [ ] 物理断电方式明确
- [ ] 每个电机独立低速测试完成
- [ ] 读取关节状态正常
- [ ] 关节方向和零位已校准
- [ ] 电流、速度和位置限制已设置
- [ ] 指令插值已实现
- [ ] 仿真关节值能够转换为真机指令

### 11.2 第一次真机测试

第一次不要放物体：

1. 使用远离关节极限的张开姿态。
2. 以很低速度发送目标。
3. 每次只移动一个关节。
4. 对比实际方向和 URDF 方向。
5. 发现方向错误立即停止并修改映射。

第二次使用海绵等柔软物体：

1. 手掌固定。
2. 人工将物体放在掌心附近。
3. 移动到 pre-grasp。
4. 缓慢闭合到 grasp。
5. 使用低电流移动到 squeeze。
6. 根据电流、触觉或位置误差停止闭合。

不要把 BODex 的最终关节角一步发送给真机，应使用限速插值轨迹。

## 12. 16 周参考课表

| 周数 | 学习任务 | 本周产出 |
| ---: | --- | --- |
| 1 | Python 基础、NumPy | 关节限位检查脚本 |
| 2 | Linux、Conda、Git | 独立环境和代码仓库 |
| 3 | 坐标系、旋转矩阵 | 坐标变换练习 |
| 4 | 正运动学 | 二关节手指可视化 |
| 5 | ROS 2 topic、TF | 发布和读取关节状态 |
| 6 | URDF、RViz | 自制两关节手指模型 |
| 7 | 阅读 Linker Hand URDF | 关节与 link 表格 |
| 8 | 安装 BODex | 固定版本环境记录 |
| 9 | 跑官方示例 | Shadow Hand 抓取结果 |
| 10 | 阅读配置和输出 | 抓取数据说明文档 |
| 11 | 建立 Linker Hand 配置 | 模型成功加载 |
| 12 | 关节与碰撞适配 | 随机姿态检查通过 |
| 13 | 生成简单物体抓取 | 第一组候选姿态 |
| 14 | 仿真接触参数调整 | 固定手掌抓住物体 |
| 15 | 关节到电机映射 | 带测试的转换程序 |
| 16 | 低速真机实验 | 柔软物体抓取录像 |

如果第 9 周官方示例没有跑通，不要进入 Linker Hand 适配。

## 13. 学习笔记模板

每次实验都记录：

```markdown
## 实验名称

日期：
目标：
环境版本：
运行命令：
输入文件：
输出文件：

### 结果

成功或失败：
观察到的现象：

### 错误

完整报错：
我认为发生错误的位置：
已经尝试的方法：

### 下一步

- [ ] ...
```

遇到问题时，先保存：

- 完整命令
- 完整报错
- 配置文件
- `nvidia-smi`
- `conda list`
- 输入物体名称
- 是否修改过源码

## 14. 常见错误与处理顺序

### 模型尺寸异常

检查 STL 是以米还是毫米导出。URDF 默认使用米。

### 手指朝错误方向旋转

检查 joint 的 `axis`、父子 link、零姿态和真机方向映射。

### 优化结果穿过手掌或手指

检查 collision mesh、碰撞球、自碰撞忽略表和 mesh 坐标。

### 关节姿态看起来完全错误

优先检查关节顺序，不要先调优化参数。

### 出现 CUDA out of memory

减少并行 worker、对象数量和候选数量，关闭其他 GPU 程序。

### 真机动作和仿真相反

停止测试，检查方向、零点和电机映射，不要通过扩大关节范围来掩盖问题。

## 15. 项目完成标准

完成以下内容才算实现了一个可靠的最小系统：

- [ ] Linker Hand URDF 关节和真机关节对应明确
- [ ] 原版 BODex 示例可重复运行
- [ ] Linker Hand 能被 BODex/cuRobo 加载
- [ ] 能为简单物体生成多组候选抓取
- [ ] 关节角没有越界
- [ ] 仿真可以过滤明显失败的抓取
- [ ] 关节映射有自动化测试
- [ ] 真机执行包含限速、限位和急停
- [ ] 至少完成一种简单物体的重复抓取实验
- [ ] 保存成功率、失败案例和环境版本

## 16. 推荐资料

- [Linker Hand URDF](https://github.com/linker-bot/linkerhand-urdf)
- [BODex](https://github.com/JYChen18/BODex)
- [BODex 论文笔记](../../paper/bodex.md)
- [BODex 项目主页](https://pku-epic.github.io/BODex/)
- [cuRobo](https://github.com/NVlabs/curobo)
- [DexGraspBench](https://github.com/JYChen18/DexGraspBench)
- [Dexonomy](https://github.com/JYChen18/Dexonomy)
- [ROS 2 Jazzy 文档](https://docs.ros.org/en/jazzy/index.html)
- [ROS 2 URDF 教程](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html)

截至 2026 年 4 月，BODex 仓库作者推荐新用户关注后续项目 Dexonomy，因为它更便于适配新手型，并提供更好的抓取生成结果。学习 BODex 仍然很有价值，但在正式开发前应比较两者对 Linker Hand 的适配成本。

## 17. 现在立即开始

第一周只做下面五件事：

1. 确认 Linker Hand 型号、左右手和 SDK。
2. 记录电脑的 CPU、内存、NVIDIA 显卡和系统版本。
3. 学完 Python 的列表、函数、类和 NumPy 数组。
4. 下载对应型号的 URDF，列出全部 joint 和 link。
5. 建立 `joint_map.yaml`，先把未知项标记为 `TODO`。

第一周完成标志：

> 你能明确说出自己的机械手有多少个 URDF 关节、多少个真实执行器、掌心 link 是什么、五个指尖 link 是什么。
