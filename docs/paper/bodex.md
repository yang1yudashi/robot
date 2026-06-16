# BODex 论文笔记

## 基本信息

- 论文：[BODex: Scalable and Efficient Robotic Dexterous Grasp Synthesis Using Bilevel Optimization](https://arxiv.org/abs/2412.16490)
- 代码：[JYChen18/BODex](https://github.com/JYChen18/BODex)
- 项目页：[BODex Project](https://pku-epic.github.io/BODex/)
- 方向：灵巧手抓取生成、双层优化、仿真验证
- 阅读状态：准备阅读

## 这篇论文和当前项目的关系

当前项目希望使用 Linker Hand 实现类似 BODex 的抓取姿态生成流程。BODex 主要负责生成：

- 预抓取姿态
- 抓取姿态
- 夹紧姿态
- 可能的接近轨迹

它不是完整真机控制系统，因此后续还需要：

- Linker Hand 模型适配
- 关节顺序映射
- MuJoCo 抓取验证
- 真机限位、限速和安全执行

## 阅读时重点关注

- BODex 的输入是什么
- BODex 的输出是什么
- 使用了哪些手模型
- 如何表示手掌位姿和关节角
- 如何处理碰撞和接触
- 如何评估抓取是否成功
- 官方代码中配置文件和机器人模型如何组织

## 我需要复现的最小部分

- [ ] 跑通官方 Shadow Hand 示例
- [ ] 找到输出的 joint positions
- [ ] 找到 pre-grasp、grasp、squeeze
- [ ] 明确输出关节顺序
- [ ] 将输出姿态接入 MuJoCo 验证脚本
- [ ] 开始尝试 Linker Hand 模型适配

## 暂时不做

- 不直接上真机
- 不一开始改优化算法
- 不一开始加入视觉识别
- 不一开始追求完整论文指标

