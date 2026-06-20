---
name: win-gui-test
title: Windows GUI Test Skill
description: 从 WSL 内部通过 Python（pywinauto + OpenCV）操控 Windows 原生 GUI 程序，进行自动化测试、视觉分析和竞品对比。
version: 1.0.0
source:
  type: github
  url: https://github.com/<your-username>/win-gui-test-skill
triggers:
  - 截图
  - GUI 测试
  - 自动点击
  - 控件探测
  - 视觉分析
  - 竞品对比
tools:
  - python
  - opencv
  - pywinauto
  - PIL
  - mss
requirements:
  - python >= 3.8
  - pywinauto
  - opencv-python
  - pillow
  - mss
  - numpy
  - pyyaml
---

# Windows GUI Test Skill

从 Hermes（WSL 内部）通过 `pywinauto` + `OpenCV` 操控 Windows 原生 GUI 程序。

## 命令列表

| 命令 | 参数 | 说明 |
|------|------|------|
| `list-all` | — | 列出所有可见窗口 |
| `list-elements` | `<窗口标题>` | 列出窗口内所有控件（类型、名称、位置、尺寸） |
| `screenshot` | `<窗口标题>` | 截图到配置目录（mss → PIL 降级） |
| `click` | `<窗口标题> <控件名>` | 按控件名点击 |
| `click-coords` | `<窗口标题> <x> <y>` | 按屏幕坐标点击 |
| `sendkeys` | `<窗口标题> <按键>` | 发送键盘按键 |
| `scroll` | `<窗口标题> --target <控件> --dy <数量>` | 滚动控件或窗口 |
| `get-rect` | `<窗口标题> <控件名>` | 获取控件精确矩形 |
| `launch` | `<程序路径>` | 启动程序 |
| `analyze` | `<窗口标题> --out-dir <目录>` | 全量分析（尺寸+颜色+样式） |

## 典型工作流

### 场景 1：验证 Partner GUI 按钮

```bash
python scripts/cli.py screenshot "Partner"
python scripts/cli.py list-elements "Partner"
python scripts/cli.py get-rect "Partner" "发送"
```

### 场景 2：竞品分析（微信气泡）

```bash
python scripts/cli.py screenshot "微信"
python scripts/cli.py analyze "微信" --out-dir ./reports
# 分析报告在 ./reports/analysis_微信.json
```

### 场景 3：自动导航 + 操作

```bash
python scripts/cli.py click "Partner" "实例管理"
python scripts/cli.py click "Partner" "05"
python scripts/cli.py screenshot "Partner"
```

## 已知限制与解决

| 限制 | 解决 |
|------|------|
| pywinauto 报告尺寸包含布局间距 | 用 `setFixedHeight` 替代 `setMinimumHeight` |
| QComboBox 在 UIA 不可检测 | 通过控件间空隙位置推断 |
| 锁屏时 mss 截图失败 | 自动降级到 PIL.ImageGrab（已内置） |
| 大 JSON 管道输出截断 | 用 `> /tmp/file.json` 先存文件再解析 |

## 配置

参见 `config.example.yaml`。所有项可通过环境变量 `WG_*` 覆盖。

## 错误处理

- 窗口查找：超时 10s，找不到返回清晰错误
- 控件点击：自动重试 3 次（间隔 1s），捕获 `ElementNotFoundError` / `TimeoutError`
- 截图：mss 失败 → PIL.ImageGrab 自动降级
