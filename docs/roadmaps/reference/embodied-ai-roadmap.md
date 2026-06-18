# 具身智能长期学习路线

> 本文只用于了解长期方向，不作为每日学习任务入口。每天的具体作业以[加速学习计划](../accelerated-plan.md)为准。
>
> 目标：从机器人零基础，逐步学习到能做具身智能项目：让智能体在真实或仿真环境中感知、理解、决策并执行动作。
>
> 建议周期：6～12 个月。每天 1～2 小时，持续做项目，不靠纯看课。

## 1. 先搞清楚具身智能是什么

具身智能不是单纯的大模型，也不是单纯的机器人控制。它关心的是：

```text
智能体拥有身体
    ↓
通过传感器感知世界
    ↓
理解任务和环境
    ↓
规划下一步动作
    ↓
通过身体执行动作
    ↓
根据结果继续反馈和学习
```

机器人只是具身智能最常见的载体之一。

你现在做的 **MuJoCo + Linker Hand + BODex**，属于具身智能中的：

```text
机器人操作 Manipulation
灵巧手 Dexterous Manipulation
仿真验证 Simulation
抓取规划 Grasp Planning
动作执行 Control
```

## 2. 总体路线

```text
阶段 0：编程和数学基础
    ↓
阶段 1：机器人基础
    ↓
阶段 2：仿真与物理世界
    ↓
阶段 3：控制、运动学和规划
    ↓
阶段 4：感知与三维视觉
    ↓
阶段 5：机器学习和深度学习
    ↓
阶段 6：模仿学习和强化学习
    ↓
阶段 7：视觉-语言-动作模型 VLA
    ↓
阶段 8：真实机器人与 sim-to-real
    ↓
阶段 9：完整具身智能项目
```

不要把它理解成“学完一阶段才能碰下一阶段”。更好的方式是：

```text
项目牵引学习
哪里卡住，补哪里
每个月交付一个能运行的小系统
```

## 3. 阶段 0：编程和数学基础

时间：2～4 周，后续持续补。

### 必学内容

- Python
- NumPy
- Git
- Linux/Conda
- 基础线性代数
- 三角函数
- 坐标系
- 矩阵乘法
- 概率和统计基础

### 暂时不用深挖

- 高等数学证明
- 复杂优化理论
- C++底层模板
- 机器人动力学完整推导

### 项目练习

- [ ] 用 Python 模拟一个二维小车移动
- [ ] 用 NumPy 写二维旋转矩阵
- [ ] 用 Git 记录每天学习
- [ ] 写一个关节角限位检查程序

### 通过标准

- [ ] 能看懂普通 Python 项目结构
- [ ] 能用 NumPy 处理向量和矩阵
- [ ] 能解释世界坐标系和局部坐标系
- [ ] 能用 Git 提交学习记录

## 4. 阶段 1：机器人基础

时间：4～6 周。

### 必学内容

- ROS 2 基础
- URDF
- STL/OBJ
- RViz
- TF 坐标系
- 关节、连杆和机器人模型
- 传感器消息
- 机器人执行器

### 你要理解的核心问题

```text
机器人长什么样？
每个关节怎么动？
机器人身体坐标系在哪里？
传感器数据如何进入系统？
控制指令如何发给执行器？
```

### 项目练习

- [ ] 显示一个两轮小车 URDF
- [ ] 显示一个两关节机械臂 URDF
- [ ] 在 RViz 中显示 TF
- [ ] 读取 `/joint_states`
- [ ] 用键盘控制一个简单机器人

### 通过标准

- [ ] 能看懂 `link` 和 `joint`
- [ ] 能解释 TF 树
- [ ] 能知道一个机器人模型的掌心、末端、传感器坐标系在哪里
- [ ] 能把一个简单 URDF 在 RViz 中显示出来

## 5. 阶段 2：仿真与物理世界

时间：3～5 周。

你当前就在这个阶段。

### 主要工具

- MuJoCo：接触、抓取、控制、快速物理验证
- Gazebo：ROS系统集成、导航、传感器
- Isaac Sim/Isaac Lab：高保真视觉、大规模训练、机器人学习

### 当前优先级

```text
MuJoCo > Gazebo > Isaac Sim/Isaac Lab
```

因为你现在的目标是灵巧手抓取验证，MuJoCo最直接。

### 必学内容

- MJCF/XML
- `body / geom / joint / actuator`
- `qpos / qvel / ctrl / contact`
- 无 UI 仿真
- 保存视频
- 接触检测
- 简单抓取成功判断

### 项目练习

- [ ] 自由落体
- [ ] 状态读取
- [ ] 单关节控制
- [ ] 两指夹爪
- [ ] 接触检测
- [ ] 抓取并抬升
- [ ] 无 UI 批量测试

### 通过标准

- [ ] 能不打开 UI 跑仿真
- [ ] 能保存 MP4
- [ ] 能读取物体位置和接触
- [ ] 能判断抓取成功或失败

## 6. 阶段 3：控制、运动学和规划

时间：6～8 周，和项目并行学习。

### 必学内容

- 正运动学 FK
- 逆运动学 IK
- 雅可比矩阵的直观意义
- 轨迹插值
- 关节空间控制
- 笛卡尔空间控制
- PID 基础
- 碰撞检测
- 运动规划
- MoveIt 2 基础

### 项目练习

- [ ] 二关节机械臂正运动学
- [ ] 给机械臂末端设定目标点
- [ ] 关节从 A 姿态平滑运动到 B 姿态
- [ ] 给灵巧手做张开、半握、闭合轨迹
- [ ] 使用 MoveIt 2 控制机械臂到指定位置

### 通过标准

- [ ] 能解释关节空间和笛卡尔空间
- [ ] 能做简单插值轨迹
- [ ] 能理解“目标姿态”和“执行轨迹”不是一回事
- [ ] 能把规划结果安全地转换成执行指令

## 7. 阶段 4：感知与三维视觉

时间：6～10 周。

### 必学内容

- 相机模型
- RGB-D 相机
- 点云
- 相机内参和外参
- 手眼标定
- 物体检测
- 位姿估计
- 语义分割
- 深度图
- 3D重建基础

### 常用工具

- OpenCV
- Open3D
- RealSense SDK
- Segment Anything 相关工具
- FoundationPose、MegaPose 等位姿估计方向

### 项目练习

- [ ] 读取 RGB 图片
- [ ] 读取深度图
- [ ] 将深度图转点云
- [ ] 从点云中分割桌面
- [ ] 估计一个杯子的粗略位置
- [ ] 将物体坐标转换到机器人坐标系

### 通过标准

- [ ] 能解释像素坐标、相机坐标、机器人坐标
- [ ] 能把 RGB-D 数据转成点云
- [ ] 能得到一个物体的大致位姿
- [ ] 能理解为什么抓取需要物体位姿

## 8. 阶段 5：机器学习和深度学习

时间：8～12 周，长期持续。

### 必学内容

- PyTorch
- 数据集和 DataLoader
- MLP
- CNN
- Transformer
- 损失函数
- 优化器
- 训练、验证、测试
- 过拟合
- checkpoint
- GPU训练

### 项目练习

- [ ] 用 PyTorch 训练 MNIST
- [ ] 训练一个简单图像分类器
- [ ] 训练一个小模型预测机器人动作
- [ ] 读取机器人轨迹数据
- [ ] 将 observation 映射到 action

### 通过标准

- [ ] 能写一个 PyTorch 训练循环
- [ ] 能保存和加载模型
- [ ] 能看懂 loss 曲线
- [ ] 能理解机器人学习中的 observation/action/dataset

## 9. 阶段 6：模仿学习和强化学习

时间：8～12 周。

### 模仿学习 Imitation Learning

核心思想：

```text
人或专家演示
    ↓
收集 observation-action 数据
    ↓
训练策略模型
    ↓
机器人模仿执行
```

重点方法：

- Behavior Cloning
- ACT
- Diffusion Policy
- Data augmentation
- Dataset replay

推荐工具：

- LeRobot
- robomimic
- ManiSkill

Hugging Face 的 LeRobot 目前提供真实机器人数据、模型和训练工具，重点覆盖模仿学习、强化学习和视觉-语言-动作模型。

### 强化学习 Reinforcement Learning

核心思想：

```text
机器人尝试动作
    ↓
环境给奖励
    ↓
策略逐渐学会更好的动作
```

重点方法：

- PPO
- SAC
- DDPG/TD3
- Reward design
- Domain randomization
- Sim-to-real

推荐工具：

- Isaac Lab
- MuJoCo
- Stable-Baselines3
- RL Games

NVIDIA Isaac Lab 是面向机器人学习的GPU加速框架，适合大规模强化学习、模仿学习和sim-to-real研究。

### 项目练习

- [ ] 用行为克隆学习一个简单夹爪策略
- [ ] 用RL训练一个小车到达目标点
- [ ] 用RL训练一个机械臂到达目标位置
- [ ] 用模仿学习复现简单抓取动作

### 通过标准

- [ ] 能解释模仿学习和强化学习的区别
- [ ] 能训练一个简单策略
- [ ] 能理解为什么真实机器人数据很贵
- [ ] 能理解为什么仿真到现实会有差距

## 10. 阶段 7：视觉-语言-动作模型 VLA

时间：长期方向，建议在有机器人和深度学习基础后进入。

### VLA是什么

VLA 是 Vision-Language-Action：

```text
视觉输入
    +
语言指令
    ↓
模型输出机器人动作
```

代表性方向：

- RT-1
- RT-2
- Open X-Embodiment / RT-X
- Octo
- OpenVLA
- LeRobot 中的 VLA 实践方向

RT-2 这类模型把视觉语言模型和机器人动作结合，让模型能够把视觉、语言和动作统一到同一个策略中。

Open X-Embodiment 提供了跨机器人形态的大规模真实机器人轨迹数据，用于训练更通用的机器人策略。

### 必学内容

- Transformer基础
- Vision Transformer
- VLM
- Tokenization
- Action representation
- Robot trajectory datasets
- Multi-task learning
- Cross-embodiment learning

### 项目练习

- [ ] 阅读一个VLA模型的输入输出格式
- [ ] 下载一个小型机器人数据集
- [ ] 使用预训练策略做离线推理
- [ ] 理解语言指令如何映射到动作

### 通过标准

- [ ] 能解释VLM和VLA的区别
- [ ] 能说出机器人动作如何被模型表示
- [ ] 能理解为什么跨机器人数据很难统一

## 11. 阶段 8：真实机器人与 sim-to-real

时间：长期贯穿。

### 必学内容

- 真实机器人安全
- 限位
- 限速
- 急停
- 标定
- 延迟
- 噪声
- 摩擦差异
- 传感器误差
- Domain randomization
- System identification

### 项目练习

- [ ] 在仿真中加入质量扰动
- [ ] 在仿真中加入摩擦扰动
- [ ] 在仿真中加入观测噪声
- [ ] 将仿真轨迹低速发送到真机
- [ ] 记录仿真成功但真机失败的案例

### 通过标准

- [ ] 能解释为什么仿真成功不等于真机成功
- [ ] 能安全执行低速动作
- [ ] 能记录和分析失败案例
- [ ] 能逐步缩小仿真与真实差距

## 12. 阶段 9：完整具身智能项目

时间：第 6 个月以后开始形成作品。

建议做三个层级的项目。

### 项目A：灵巧手抓取验证

与你当前路线一致：

```text
BODex生成抓取
→ Linker Hand关节映射
→ MuJoCo验证
→ 真机低速执行
```

成果：

- 抓取成功率报告
- 成功/失败视频
- 关节映射文档
- 仿真与真机差异分析

### 项目B：视觉引导抓取

加入相机：

```text
RGB-D相机
→ 物体检测
→ 位姿估计
→ 抓取生成
→ 机械手执行
```

成果：

- 能抓取桌面上的已知物体
- 能处理物体位置变化
- 能保存感知和抓取日志

### 项目C：语言指令抓取

加入语言：

```text
用户指令：“拿起红色杯子”
→ 语言理解
→ 视觉定位目标
→ 抓取规划
→ 执行动作
```

成果：

- 简单语言指令到机器人动作
- 多物体场景中的目标选择
- 成功率和失败分析

## 13. 推荐学习节奏

### 前2周

跟随当前加速计划：

- MuJoCo基础闭环
- BODex官方示例
- Linker Hand资料整理

### 第1～2个月

主线：

- 机器人基础
- MuJoCo
- BODex
- Linker Hand最小适配

目标：

- 完成一个灵巧手抓取仿真闭环

### 第3～4个月

主线：

- ROS 2
- 运动学
- 感知
- 点云
- 相机标定

目标：

- 让机器人基于物体位姿执行抓取

### 第5～6个月

主线：

- PyTorch
- 模仿学习
- 强化学习
- LeRobot

目标：

- 训练或复现一个简单策略

### 第6个月以后

主线：

- VLA
- Open X-Embodiment
- sim-to-real
- 多任务机器人策略

目标：

- 做一个能展示的具身智能项目

## 14. 每个阶段的学习比例

建议比例：

```text
20% 理论
60% 动手
20% 复盘和记录
```

不要变成：

```text
90% 看视频
10% 复制代码
```

具身智能最大的问题不是概念不够多，而是系统太长。你必须不断做小闭环。

## 15. 你当前最适合的主线

结合你现在的项目，我建议当前主线是：

```text
MuJoCo
→ BODex
→ Linker Hand
→ 抓取仿真验证
→ ROS 2
→ 相机/点云
→ 模仿学习
→ VLA
```

暂时不要同时铺开：

- SLAM
- 自动驾驶
- 多足机器人
- Isaac Sim 大规模训练
- 全套大模型训练

这些都属于具身智能，但现在会分散你的主线。

## 16. 推荐资料

基础和机器人：

- [ROS 2 文档](https://docs.ros.org/)
- [MoveIt 2 文档](https://moveit.picknik.ai/)
- [MuJoCo 文档](https://mujoco.readthedocs.io/en/stable/)

机器人学习：

- [LeRobot 文档](https://huggingface.co/docs/lerobot/en/index)
- [Isaac Lab](https://developer.nvidia.com/isaac/lab)
- [Isaac Lab 文档](https://isaac-sim.github.io/IsaacLab/)

大规模机器人数据和VLA：

- [Open X-Embodiment](https://robotics-transformer-x.github.io/)
- [Open X-Embodiment GitHub](https://github.com/google-deepmind/open_x_embodiment)
- [RT-2论文](https://arxiv.org/abs/2307.15818)
- [RT-2项目页](https://robotics-transformer2.github.io/)

当前项目相关：

- [BODex 论文笔记](../../paper/bodex.md)
- [BODex](https://github.com/JYChen18/BODex)
- [Linker Hand URDF](https://github.com/linker-bot/linkerhand-urdf)
- [DexGraspBench](https://github.com/JYChen18/DexGraspBench)
