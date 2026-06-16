# MJCF/XML 零基础速查

> 这不是完整的官方手册，而是一份面向初学者的 MuJoCo 模型阅读指南。
>
> 学习目标：能够看懂自由落体、单关节和简单夹爪模型。遇到复杂参数时，再查官方文档。

## 1. 先记住一句话

MuJoCo 使用一种叫 **MJCF** 的 XML 格式描述物理世界。

```text
XML = 通用的文本书写格式
MJCF = MuJoCo 对标签、属性和物理含义的具体规定
```

例如：

```xml
<geom type="sphere" size="0.05"/>
```

XML只规定它是一个标签，而MJCF规定：

- `geom`表示几何体。
- `type="sphere"`表示球体。
- 球体的`size`表示半径。
- 长度单位默认是米。

因此，学习MuJoCo模型时应该查MJCF文档，而不是只看普通XML教程。

## 2. 最小心智模型

暂时只记住5个概念：

| 标签 | 可以理解为 | 例子 |
| --- | --- | --- |
| `worldbody` | 整个物理世界 | 地面、机器人、物体都放在这里 |
| `body` | 一个刚体和坐标系 | 掌心、指节、小球 |
| `geom` | 刚体的外形和碰撞体 | 球、盒子、手指外壳 |
| `joint` | 刚体怎样运动 | 转动、滑动、自由运动 |
| `actuator` | 怎样驱动关节 | 电机、位置控制器 |

它们的关系可以理解为：

```text
物理世界 worldbody
└── 刚体 body
    ├── 运动方式 joint
    └── 外形与碰撞 geom

执行器 actuator
└── 控制某个 joint
```

在当前自由落体模型中：

```text
世界
├── 地面 geom
└── 小球 body
    ├── 自由运动 freejoint
    └── 球形外壳 geom
```

## 3. XML最基础语法

### 3.1 成对标签

```xml
<body>
  子标签
</body>
```

`<body>`表示开始，`</body>`表示结束。

### 3.2 自闭合标签

没有子标签时可以写成：

```xml
<joint name="finger_joint"/>
```

末尾的`/>`同时表示开始和结束。

### 3.3 属性

```xml
<body name="ball" pos="0 0 2">
```

其中：

- `body`是标签名称。
- `name`和`pos`是属性。
- `"ball"`和`"0 0 2"`是属性值。

属性值必须放在引号中。

### 3.4 注释

```xml
<!-- 这是一段注释，不参与模型计算 -->
```

## 4. 常用单位

除非模型中进行了特殊设置，否则常用单位是：

| 物理量 | 单位 |
| --- | --- |
| 长度 | 米，`m` |
| 质量 | 千克，`kg` |
| 时间 | 秒，`s` |
| 速度 | 米每秒或弧度每秒 |
| 重力加速度 | 米每二次方秒，`m/s²` |
| 关节角 | 默认通常为角度或由`compiler`决定 |
| Python中的关节状态 | 弧度 |

最常见的错误是把毫米直接当成米：

```text
50毫米 = 0.05米
```

如果把`50`写成米，模型会放大1000倍。

建议在模型根节点显式指定：

```xml
<compiler angle="radian"/>
```

这样关节范围和姿态统一使用弧度，更容易和Python、BODex对接。

## 5. MJCF基本骨架

一个较完整的模型通常长这样：

```xml
<mujoco model="模型名称">
  <compiler/>
  <option/>
  <default/>
  <asset/>

  <worldbody>
    <body>
      <joint/>
      <geom/>
    </body>
  </worldbody>

  <contact/>
  <actuator/>
  <sensor/>
</mujoco>
```

这些部分不是全部必需。简单模型可以只使用：

```xml
<mujoco>
  <option/>
  <worldbody/>
</mujoco>
```

## 6. mujoco：整个模型

```xml
<mujoco model="free fall">
  ...
</mujoco>
```

它是MJCF文件的根标签，其他内容都要放在里面。

`model`只是模型名称：

```xml
model="free fall"
```

它方便识别模型，不直接控制物理行为。

## 7. compiler：模型编译设置

常见写法：

```xml
<compiler angle="radian" meshdir="meshes"/>
```

### angle

规定XML中角度相关属性使用什么单位：

```xml
angle="radian"
```

表示使用弧度。

```xml
angle="degree"
```

表示使用角度。

注意：编译完成后，MuJoCo的运行时数据和Python API仍然使用弧度。

### meshdir

```xml
meshdir="meshes"
```

表示mesh文件默认从`meshes/`目录查找。

以后加载Linker Hand的STL时会用到。

## 8. option：仿真全局参数

```xml
<option timestep="0.002" gravity="0 0 -9.81"/>
```

### timestep

```xml
timestep="0.002"
```

每次调用`mj_step`，仿真时间前进0.002秒。

```text
1秒 ÷ 0.002秒 = 500步
```

时间步越小：

- 通常更稳定。
- 接触仿真通常更准确。
- 需要更多计算。

时间步过大可能造成：

- 穿模。
- 抖动。
- 高速物体穿过薄物体。
- 控制器不稳定。

### gravity

```xml
gravity="0 0 -9.81"
```

三个数字分别是世界坐标系中X、Y、Z方向的重力：

```text
X = 0
Y = 0
Z = -9.81
```

Z轴负方向表示向下。

## 9. worldbody：物理世界

```xml
<worldbody>
  ...
</worldbody>
```

地面、灯光、物体和机器人都放在这里。

直接放在`worldbody`中的`geom`通常固定在世界中：

```xml
<worldbody>
  <geom name="floor" type="plane"/>
</worldbody>
```

把`geom`放进带关节的`body`后，它才能跟随body运动。

## 10. body：刚体与坐标系

```xml
<body name="ball" pos="0 0 2">
  ...
</body>
```

### name

```xml
name="ball"
```

给body一个唯一名称。Python和其他标签可以通过名称找到它。

### pos

```xml
pos="0 0 2"
```

表示相对于父body的位置：

```text
x = 0米
y = 0米
z = 2米
```

body可以嵌套：

```xml
<body name="palm">
  <body name="finger">
    <body name="fingertip"/>
  </body>
</body>
```

子body的位置和姿态默认相对于父body。

这正是机械手的结构：

```text
掌心
└── 第一指节
    └── 第二指节
        └── 指尖
```

### quat或euler

body还可以设置初始旋转：

```xml
<body quat="1 0 0 0"/>
```

或者：

```xml
<body euler="0 0 1.57"/>
```

初学阶段先理解`pos`，旋转部分等学习坐标系后再深入。

## 11. geom：外形与碰撞体

```xml
<geom name="ball_geom"
      type="sphere"
      size="0.05"
      mass="1"
      rgba="0.2 0.5 0.9 1"/>
```

`geom`主要负责：

1. 显示物体外形。
2. 参与碰撞检测。
3. 帮助计算质量和惯性。

### name

```xml
name="ball_geom"
```

接触检测时，可以通过名称判断哪些geom发生了接触。

### type

常见几何体：

| 类型 | 写法 | 用途 |
| --- | --- | --- |
| 平面 | `plane` | 地面 |
| 球体 | `sphere` | 球、简化碰撞体 |
| 盒子 | `box` | 方块、掌心 |
| 圆柱 | `cylinder` | 杯子、圆柱物体 |
| 胶囊体 | `capsule` | 连杆、手指 |
| 网格 | `mesh` | STL/OBJ复杂模型 |

### size

`size`的含义取决于`type`。

#### sphere

```xml
<geom type="sphere" size="0.05"/>
```

`0.05`是半径，因此直径是0.1米。

#### box

```xml
<geom type="box" size="0.1 0.2 0.3"/>
```

三个数字是X、Y、Z方向的**半尺寸**：

```text
实际尺寸 = 0.2 × 0.4 × 0.6米
```

#### cylinder

```xml
<geom type="cylinder" size="0.05 0.2"/>
```

表示：

```text
半径 = 0.05米
半长度 = 0.2米
实际总长度 = 0.4米
```

#### capsule

```xml
<geom type="capsule" fromto="0 0 0 0 0 0.3" size="0.03"/>
```

表示从一个点连接到另一个点，半径为0.03米。它很适合简化机器人手指和连杆。

#### plane

```xml
<geom type="plane" size="2 2 0.1"/>
```

平面的碰撞在物理上无限延伸。前两个数主要控制可视化尺寸，第三个数与网格显示有关，不是普通意义上的厚度。

### mass

```xml
mass="1"
```

表示质量为1千克。

质量会影响：

- 碰撞响应。
- 抓取需要的力。
- 加速度和惯性。

质量不会改变真空中的重力加速度，因此轻球和重球会以相同加速度下落。

### rgba

```xml
rgba="0.2 0.5 0.9 1"
```

四个数字分别表示：

```text
红、绿、蓝、透明度
```

取值通常为0到1。

它只影响显示，不改变物理行为。

### friction

```xml
friction="1.0 0.01 0.001"
```

三个数字分别和滑动、扭转、滚动摩擦有关。

初学阶段重点关注第一个滑动摩擦值：

- 数值过低，物体容易滑落。
- 数值较高，物体更不容易滑动。
- 不能只靠无限增大摩擦掩盖错误抓取姿态。

## 12. joint：规定body怎样运动

没有joint的body会固定在父body上。

常见joint类型：

| 类型 | 作用 | 灵巧手中的例子 |
| --- | --- | --- |
| `hinge` | 绕轴转动 | 手指弯曲关节 |
| `slide` | 沿轴滑动 | 简单平行夹爪 |
| `ball` | 三维旋转 | 球形关节 |
| `free` | 三维平移和旋转 | 自由物体 |

### hinge

```xml
<joint name="finger_joint"
       type="hinge"
       axis="0 1 0"
       range="0 1.57"/>
```

含义：

- 名称是`finger_joint`。
- 绕Y轴旋转。
- 允许范围是0到1.57弧度。

### axis

```xml
axis="0 1 0"
```

表示旋转或滑动方向：

```text
1 0 0 = X轴
0 1 0 = Y轴
0 0 1 = Z轴
```

如果机械手关节朝反方向运动，`axis`和模型坐标系是重点检查对象。

### range

```xml
range="0 1.57"
```

表示关节运动范围。

关节限制非常重要：

- 防止仿真姿态超出机械结构。
- 防止BODex输出真机无法到达的姿态。
- 真机控制仍需再次做安全限位，不能只依赖模型。

### damping

```xml
damping="0.2"
```

阻尼可以理解为运动阻力。适当阻尼能够减少持续摆动。

### freejoint

自由物体可以使用简写：

```xml
<freejoint/>
```

它允许body：

- 沿X、Y、Z平移。
- 绕X、Y、Z旋转。

如果从自由落体小球中删除`freejoint`，小球会固定在初始位置。

## 13. actuator：驱动关节

定义joint后，body可以运动，但还需要actuator主动控制它。

位置执行器示例：

```xml
<actuator>
  <position name="finger_motor"
            joint="finger_joint"
            kp="30"
            kv="3"
            ctrlrange="0 1.57"/>
</actuator>
```

### joint

```xml
joint="finger_joint"
```

表示这个执行器控制哪个关节。

### kp

`kp`表示位置控制强度。

- 太小：关节可能追不上目标。
- 太大：可能产生抖动或不稳定。

### kv

`kv`提供速度阻尼，有助于减少振荡。

### ctrlrange

```xml
ctrlrange="0 1.57"
```

表示执行器允许接收的控制目标范围。

Python中设置控制目标：

```python
data.ctrl[actuator_id] = 0.8
```

注意：

```text
joint顺序、qpos顺序、actuator顺序可能不同
```

复杂模型中应该通过名称查找ID，不要猜数组下标。

## 14. asset与mesh：加载STL

以后Linker Hand模型会使用STL或OBJ：

```xml
<asset>
  <mesh name="finger_mesh" file="finger.stl"/>
</asset>
```

然后在geom中引用：

```xml
<geom type="mesh" mesh="finger_mesh"/>
```

可以把它理解成两步：

```text
asset：先登记并加载STL
geom：把这个STL作为某个body的形状
```

需要特别检查：

- 文件路径。
- 米和毫米的单位。
- mesh原点。
- mesh坐标方向。
- 模型面数是否过高。

显示模型和碰撞模型可以不同：

```text
高精度STL：负责好看
简单球、盒子或胶囊：负责快速稳定的碰撞检测
```

## 15. default：批量设置默认参数

当很多geom使用相同参数时，可以写：

```xml
<default>
  <geom friction="1.0 0.01 0.001"/>
  <joint damping="0.5"/>
</default>
```

后面的geom和joint会继承这些设置，除非自己覆盖。

优点：

- 减少重复。
- 修改统一参数更方便。

缺点：

- 初学时可能不知道某个参数从哪里继承。

阅读复杂模型时，如果标签里没有写某个参数，记得检查`default`。

## 16. contact：控制碰撞关系

MuJoCo通常会自动检测geom之间的碰撞。

复杂机器人可能需要排除相邻指节之间不必要的碰撞：

```xml
<contact>
  <exclude body1="finger_1" body2="finger_2"/>
</contact>
```

这表示不检测两个body之间的碰撞。

不要随意排除碰撞，否则可能出现手指穿过掌心或物体的情况。

## 17. sensor：添加传感器

示例：

```xml
<sensor>
  <jointpos name="finger_position" joint="finger_joint"/>
</sensor>
```

传感器数据可以从：

```python
data.sensordata
```

中读取。

初学阶段可以直接读取`qpos`和接触数据，等需要模拟触觉或力传感器时再深入`sensor`。

## 18. 自由落体模型逐层阅读

当前模型：

```xml
<mujoco model="free fall">
  <option timestep="0.002" gravity="0 0 -1.62"/>

  <worldbody>
    <light pos="0 0 2"/>
    <geom name="floor"
          type="plane"
          size="2 2 0.1"
          rgba="0.8 0.8 0.8 1"/>

    <body name="ball" pos="0 0 2">
      <freejoint/>
      <geom name="ball_geom"
            type="sphere"
            size="0.05"
            mass="1"
            rgba="0.2 0.5 0.9 1"/>
    </body>
  </worldbody>
</mujoco>
```

不要一开始逐个字看，可以按下面顺序阅读：

### 第一步：这个世界里有什么？

查看`worldbody`：

```text
一个地面
一个小球
一盏灯
```

### 第二步：哪些物体能运动？

小球body中有：

```xml
<freejoint/>
```

所以小球可以运动。地面没有joint，所以固定。

### 第三步：物体是什么形状？

```text
地面 = plane
小球 = sphere
```

### 第四步：物理环境是什么？

```text
时间步长 = 0.002秒
重力 = 月球重力-1.62m/s²
```

### 第五步：初始状态是什么？

```text
小球中心初始高度 = 2米
小球半径 = 0.05米
小球质量 = 1千克
```

这种阅读方式比从第一行机械地背到最后一行更有效。

## 19. 常见错误

### 标签没有正确闭合

错误：

```xml
<body>
```

但没有：

```xml
</body>
```

### name重复

同一类对象通常应使用唯一名称，否则按名称查找时容易出问题。

### size理解错误

`size`不是永远表示完整长度：

```text
sphere：半径
box：三个方向半尺寸
cylinder：半径和半长度
```

### 毫米和米混用

STL本身通常不保存明确单位。CAD中使用毫米导出的模型，放进以米为单位的机器人环境时可能放大1000倍。

### body有形状但不能运动

检查它是否定义了joint。没有joint的body固定在父body上。

### joint存在但控制无效

检查：

- 是否定义actuator。
- actuator是否绑定正确joint。
- `data.ctrl`是否写入正确actuator ID。
- 目标是否超过`ctrlrange`或关节范围。

### 物体穿模

检查：

- geom是否参与碰撞。
- 初始状态是否已经重叠。
- timestep是否过大。
- 控制速度和增益是否过大。
- mesh尺寸是否错误。

## 20. 当前学习顺序

现在不需要学习全部MJCF标签。按这个顺序即可：

### 第一层：自由落体

- [ ] `mujoco`
- [ ] `option`
- [ ] `worldbody`
- [ ] `body`
- [ ] `geom`
- [ ] `freejoint`

### 第二层：单关节

- [ ] `joint`
- [ ] `hinge`
- [ ] `axis`
- [ ] `range`
- [ ] `damping`
- [ ] `actuator/position`

### 第三层：夹爪与抓取

- [ ] `slide`
- [ ] `friction`
- [ ] `contact`
- [ ] 接触geom名称
- [ ] 质量和控制增益

### 第四层：Linker Hand

- [ ] `asset`
- [ ] `mesh`
- [ ] body层级
- [ ] 关节顺序
- [ ] 自碰撞排除
- [ ] actuator映射

## 21. 查官方文档的方法

官方文档不适合从头背诵，应当作为字典使用。

例如看到：

```xml
<geom type="capsule" size="0.03"/>
```

但不知道`size`含义时：

1. 打开XML Reference。
2. 页面搜索`body/geom`。
3. 在geom属性中查`size`。
4. 只阅读与`capsule`相关的部分。

推荐资料：

- [MuJoCo XML Reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)
- [MuJoCo Modeling Guide](https://mujoco.readthedocs.io/en/stable/modeling.html)
- [MuJoCo Python API](https://mujoco.readthedocs.io/en/stable/python.html)
- [MuJoCo Menagerie模型库](https://github.com/google-deepmind/mujoco_menagerie)

## 22. 今日最低掌握标准

今天只要能够回答以下问题就够了：

1. `body`和`geom`有什么区别？
2. 为什么小球需要`freejoint`才能落下？
3. `pos="0 0 2"`表示什么？
4. 球形geom的`size="0.05"`表示半径还是直径？
5. `timestep="0.002"`表示一次`mj_step`推进多久？
6. 为什么地面不需要joint？

不用背全部属性。能看懂当前示例，并知道遇到陌生属性去哪里查，就是合格。

