# 长期学习与项目路线图

> 目标：从 MuJoCo 入门，逐步完成 Linker Hand + BODex 的最小复现，再扩展到仿真评估和真机执行。
>
> 预计周期：8～12 周。每天 1～2 小时，周末适当集中处理环境和模型问题。

## 1. 总路线

```text
第 1 阶段：MuJoCo 基础闭环
    ↓
第 2 阶段：BODex 官方示例跑通
    ↓
第 3 阶段：Linker Hand 模型资料整理
    ↓
第 4 阶段：Linker Hand 最小适配
    ↓
第 5 阶段：BODex 抓取结果进入 MuJoCo 验证
    ↓
第 6 阶段：真机控制准备与安全执行
```

阶段目标不是“学完所有机器人知识”，而是逐步把下面这条链路跑通：

```text
物体模型
→ BODex 生成抓取姿态
→ Linker Hand 关节映射
→ MuJoCo 验证抓取
→ 真机低速执行
```

## 2. 阶段 1：MuJoCo 基础闭环

时间：第 1 周

当前状态：进行中。

目标：

- 能看懂简单 MJCF。
- 能读取仿真状态。
- 能控制关节。
- 能检测接触。
- 能保存无 UI 视频。
- 能判断一次简单抓取是否成功。

任务：

- [ ] 完成 `01_free_fall.py`
- [ ] 完成 `01_free_fall_record_video.py`
- [ ] 完成 `02_read_state.py`
- [ ] 完成 `03_single_joint.py`
- [ ] 完成 `04_motion_control.py`
- [ ] 完成 `05_close_gripper.py`
- [ ] 完成 `06_contact_detection.py`
- [ ] 完成 `07_grasp_and_lift.py`
- [ ] 写 `docs/notes/mujoco-summary.md`

交付物：

- MuJoCo 学习总结。
- 一个无 UI 抓取验证脚本。
- 一个 MP4 仿真视频。
- 一个简单抓取结果 JSON。

通过标准：

- [ ] 能解释 `body / geom / joint / actuator`
- [ ] 能解释 `qpos / qvel / xpos / ctrl / contact`
- [ ] 能不打开 Viewer 跑仿真
- [ ] 能保存视频
- [ ] 能判断抓取成功或失败

## 3. 阶段 2：BODex 官方示例跑通

时间：第 2 周

目标：

- 安装 BODex 环境。
- 跑通官方示例。
- 理解 BODex 输出结构。
- 不修改机器人模型前先证明官方流程可运行。

任务：

- [ ] 记录电脑系统、显卡、CUDA、驱动版本
- [ ] 创建 BODex Conda 环境
- [ ] 安装 PyTorch、CUDA 相关依赖
- [ ] 安装 cuRobo
- [ ] 克隆 BODex
- [ ] 跑官方 Shadow Hand 示例
- [ ] 保存完整运行命令和输出
- [ ] 找到 pre-grasp、grasp、squeeze 输出
- [ ] 找到手掌位姿、物体位姿和关节向量

交付物：

- `docs/notes/bodex-install-notes.md`
- `docs/notes/bodex-output-notes.md`
- 官方示例运行截图或日志
- 官方示例输出文件位置说明

通过标准：

- [ ] 官方示例能重复运行
- [ ] 能找到 BODex 输出的关节角
- [ ] 能说清 pre-grasp、grasp、squeeze 的区别
- [ ] 能说清哪些数据要送入 MuJoCo 验证

风险点：

- CUDA/PyTorch版本冲突
- cuRobo安装失败
- 显存不足
- 官方数据集或mesh下载失败

硬规则：

> 官方示例没有跑通前，不进入 Linker Hand 适配。

## 4. 阶段 3：Linker Hand 模型资料整理

时间：第 3 周

目标：

- 找到对应型号的 Linker Hand URDF/STL。
- 整理 link、joint、掌心、指尖。
- 建立第一版关节映射表。

任务：

- [ ] 确认型号：L20、L25、O6、O7 或其他
- [ ] 确认左手还是右手
- [ ] 下载对应 URDF/STL
- [ ] 列出全部 link
- [ ] 列出全部 joint
- [ ] 找到 palm link
- [ ] 找到 fingertip links
- [ ] 找到每个 joint 的上下限
- [ ] 找到可控关节和固定关节
- [ ] 标记可能的 mimic 或机械耦合
- [ ] 建立 `examples/linkerhand/joint_map.yaml`

交付物：

- `docs/notes/linkerhand-model-notes.md`
- `examples/linkerhand/joint_map.yaml`
- `examples/linkerhand/link_list.txt`
- `examples/linkerhand/joint_list.txt`

通过标准：

- [ ] 能说出模型有多少个 link
- [ ] 能说出模型有多少个 joint
- [ ] 能说出哪些关节是可控的
- [ ] 能找到掌心和五个指尖 link
- [ ] 不依赖数组顺序猜关节映射

风险点：

- URDF中关节和真机电机数量不一致
- 左手和右手模型混用
- STL单位可能是毫米
- mesh路径不完整

## 5. 阶段 4：Linker Hand 最小适配

时间：第 4～5 周

目标：

- 让 Linker Hand 模型能被仿真或优化流程解析。
- 完成关节顺序和限位的最小映射。
- 不追求一开始抓取成功，先追求模型正确。

任务：

- [ ] 尝试将 URDF 转换或整理为 MuJoCo/MJCF 可用模型
- [ ] 检查 mesh 路径
- [ ] 检查模型单位
- [ ] 检查关节轴方向
- [ ] 检查关节上下限
- [ ] 建立 `urdf_to_mujoco_joint_order`
- [ ] 建立 `bodex_to_linkerhand_joint_order`
- [ ] 对每个关节做随机姿态限位测试
- [ ] 保存零姿态图或视频
- [ ] 保存一组张开/半握/闭合姿态图或视频

交付物：

- Linker Hand 最小仿真模型
- 关节映射脚本
- 限位检查脚本
- 3个基础姿态视频或截图

通过标准：

- [ ] 模型能加载
- [ ] 关节能按预期方向运动
- [ ] 姿态不会明显穿模
- [ ] 随机关节姿态不会越界
- [ ] 关节映射脚本有简单测试

风险点：

- mesh太复杂导致仿真慢
- collision模型不稳定
- 关节轴方向错误
- 关节耦合难处理

## 6. 阶段 5：BODex 抓取结果进入 MuJoCo 验证

时间：第 6～8 周

目标：

- 将 BODex 输出的抓取姿态转换为 Linker Hand 仿真关节值。
- 在 MuJoCo 中执行 pre-grasp、grasp、squeeze。
- 对简单物体做抓取成功率评估。

任务：

- [ ] 读取 BODex 输出文件
- [ ] 提取 pre-grasp、grasp、squeeze
- [ ] 转换到 Linker Hand 关节顺序
- [ ] 做关节限位检查
- [ ] 执行插值控制
- [ ] 在 MuJoCo 中闭合手指
- [ ] 抬升物体
- [ ] 判断成功/失败
- [ ] 批量评估多个候选抓取
- [ ] 为成功和失败案例保存视频

交付物：

- `scripts/evaluate_bodex_grasp_in_mujoco.py`
- 抓取评估 JSON/CSV
- 成功案例视频
- 失败案例视频
- 抓取失败原因记录

通过标准：

- [ ] 至少一个简单物体能在仿真中被抓起
- [ ] 能批量评估多个候选姿态
- [ ] 能自动保存结果
- [ ] 能区分“碰到物体”和“抓取成功”

风险点：

- BODex输出关节顺序和Linker Hand不一致
- 接触模型和真实手差距较大
- 碰撞模型过粗或过细
- 物体姿态和坐标系转换错误

## 7. 阶段 6：真机控制准备与安全执行

时间：第 9～12 周

目标：

- 在真机上低速、安全地执行已验证姿态。
- 先做固定手掌抓取，再考虑机械臂和视觉。

任务：

- [ ] 获取 Linker Hand SDK
- [ ] 能读取真机关节状态
- [ ] 能单独控制每个电机
- [ ] 标定零位和方向
- [ ] 实现 `sim_q_to_motor_command`
- [ ] 设置限位、限速和力/电流限制
- [ ] 实现急停
- [ ] 空手执行张开/闭合姿态
- [ ] 使用柔软物体做低速抓取
- [ ] 记录成功率和失败原因

交付物：

- 真机关节映射表
- 安全控制脚本
- 柔软物体抓取视频
- 真机实验记录

通过标准：

- [ ] 每个电机方向正确
- [ ] 每个目标指令都经过限位检查
- [ ] 能低速执行仿真姿态
- [ ] 能安全停止
- [ ] 完成至少一种柔软物体抓取

风险点：

- 真机关节范围和URDF不一致
- 电机方向和仿真相反
- 机械耦合导致姿态无法直接复现
- 力过大损坏手或物体

硬规则：

> 仿真没有通过的姿态，不直接上真机。  
> 没有限速、限位和急停，不做真机抓取。

## 8. 总里程碑

| 时间 | 里程碑 | 交付物 |
| --- | --- | --- |
| 第 1 周 | MuJoCo基础闭环 | 7个示例、视频、总结 |
| 第 2 周 | BODex官方示例跑通 | 安装记录、官方输出 |
| 第 3 周 | Linker Hand资料清楚 | link/joint清单、joint_map |
| 第 4～5 周 | Linker Hand最小模型适配 | 模型加载、关节映射 |
| 第 6～8 周 | BODex结果进入仿真验证 | 批量评估、成功/失败视频 |
| 第 9～12 周 | 真机安全执行 | 低速抓取、实验记录 |

## 9. 每周复盘模板

每周末在 `README.md` 或 `docs/notes/weekly-review.md` 中记录：

```markdown
## 第 N 周复盘

本周目标：

- 

完成内容：

- 

没有完成：

- 

遇到的问题：

- 

下周目标：

- 

是否需要调整计划：

- 
```

## 10. 判断是否该继续往下走

每个阶段都要有通过标准。如果没有通过，不要硬跳到下一阶段。

例如：

- BODex官方示例没跑通，就不适配Linker Hand。
- Linker Hand关节映射不清楚，就不做抓取优化。
- MuJoCo抓取不稳定，就不接真机。
- 真机没有急停和限位，就不抓硬物。

这样做不是拖慢速度，而是避免后面花更多时间排查混在一起的问题。

