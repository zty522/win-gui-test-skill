# win-gui-test-skill

Windows GUI 自动化测试与视觉分析技能。从 WSL 内部通过 Python（pywinauto + OpenCV）操控 Windows 原生 GUI 程序，进行自动化测试、视觉分析和竞品对比。

## 功能

- 🖥️ **窗口/控件发现** — 列出所有窗口、枚举控件树
- 📸 **截图 + 自动降级** — mss 为主，PIL.ImageGrab 兜底（锁屏也能截）
- 🎯 **精准操作** — 按控件名或坐标点击、键盘输入、滚轮滚动
- 🔬 **视觉分析** — 尺寸一致性检测、颜色/边框提取、圆角估算
- 🏭 **竞品对比** — 截图分析微信/QQ/Edge 等应用的 CSS 参数
- 📋 **结构化 JSON 输出** — 所有命令返回 JSON，便于程序消费

## 安装

```bash
# Python 依赖
pip install -r requirements.txt

# 从源码安装（可选）
pip install -e .
```

### 前置条件

- Windows 10/11（Python 3.8+）
- WSL2（运行命令端）
- Windows Python 已安装 pywinauto、opencv-python、pillow、mss

## 配置

复制配置示例并修改：

```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml 中的路径
```

所有配置项可通过环境变量覆盖（前缀 `WG_`，点号转下划线）：

```bash
export WG_SCREENSHOT_DIR="D:/screenshots"
export WG_RETRY_COUNT=5
```

## 命令行用法

```bash
# 基本命令
python scripts/cli.py list-all
python scripts/cli.py list-elements "Partner"
python scripts/cli.py screenshot "Partner"
python scripts/cli.py click "Partner" "发送"
python scripts/cli.py click-coords "Partner" 500 300
python scripts/cli.py sendkeys "Partner" "hello world"
python scripts/cli.py scroll "Partner" --target "列表" --dy -3
python scripts/cli.py get-rect "Partner" "发送"
python scripts/cli.py launch "calc.exe"

# 全量分析
python scripts/cli.py analyze "Partner" --out-dir ./reports

# 使用配置文件
python scripts/cli.py --config my_config.yaml list-elements "微信"
```

## 示例

```bash
# 场景 1：测试 Partner GUI
python examples/example1_partner_gui.py

# 场景 2：分析微信气泡样式
python examples/example2_wechat_analysis.py

# 场景 3：滚动点击交互测试
python examples/example3_scroll_click.py
```

## 项目结构

```
win-gui-test-skill/
├── README.md
├── SKILL.md
├── config.example.yaml
├── requirements.txt
├── setup.py
├── .gitignore
├── LICENSE
├── scripts/
│   ├── core.py              # 核心操作（窗口发现、控件交互）
│   ├── cli.py               # 命令行入口
│   ├── analyzers/
│   │   ├── size_analyzer.py      # 尺寸一致性检测
│   │   ├── color_analyzer.py     # 颜色分析
│   │   └── style_extractor.py    # CSS 属性推断
│   └── utils/
│       ├── config.py             # 配置加载（YAML/JSON/环境变量）
│       ├── logger.py             # 文件+控制台日志（每日轮转）
│       └── screenshot.py         # 截图（mss + PIL 降级）
├── examples/
│   ├── example1_partner_gui.py
│   ├── example2_wechat_analysis.py
│   └── example3_scroll_click.py
├── tests/
│   └── test_core.py
├── logs/                    # 运行时日志（自动创建）
└── screenshots/             # 默认截图目录
```

## 开发

```bash
# 运行单元测试
python -m pytest tests/ -v

# 或
python tests/test_core.py -v
```

### 添加新的分析器

在 `scripts/analyzers/` 下创建模块，实现接收 `(elements: list[dict]) -> dict` 的函数即可。CLI 的 `analyze` 命令会自动收集所有分析器的输出。

## 许可证

Apache 2.0
