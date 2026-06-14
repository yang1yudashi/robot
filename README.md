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

详细路线请查看：

- [Linker Hand + BODex 学习路线](./LinkerHand_BODex_学习路线.md)

整体分为以下阶段：

| 阶段 | 学习内容 | 当前状态 |
| --- | --- | --- |
| 1 | Python、NumPy、Linux、Git | 进行中 |
| 2 | 坐标系、矩阵与机器人运动学 | 未开始 |
| 3 | ROS 2、URDF、TF 和 RViz | 未开始 |
| 4 | 跑通 BODex 官方示例 | 未开始 |
| 5 | 适配 Linker Hand 模型 | 未开始 |
| 6 | 物理仿真与抓取验证 | 未开始 |
| 7 | Linker Hand 真机控制 | 未开始 |

状态说明：`未开始`、`进行中`、`已完成`。

## 当前任务

- [ ] 确认 Linker Hand 的具体型号和左右手
- [ ] 确认机械手 SDK 和通信方式
- [ ] 记录电脑系统、显卡型号和 CUDA 环境
- [ ] 学习 Python 基础和 NumPy
- [ ] 下载并在 RViz 中显示 Linker Hand URDF
- [ ] 整理机械手的全部 link 和 joint
- [ ] 建立 URDF 关节到真机电机的映射表

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
- [BODex 论文](https://arxiv.org/abs/2412.16490)
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

