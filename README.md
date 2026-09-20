# Mikan Universal Packer

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://www.qt.io/qt-for-python)

> 全语言通用脚本打包器 — 支持 Python / Java / Rust / Go / PHP / Node.js / C++，所有打包器新老版本自动适配

Mikan Universal Packer 是一款基于 Python 和 PySide6 开发的全语言通用脚本打包器桌面应用程序，提供图形化界面来管理多语言项目的打包编译流程。支持 Python、Java、Rust、Go、PHP、Node.js、C++ 七大编程语言，内置 15+ 种打包器（PyInstaller、Nuitka、jpackage、cargo、go build、pkg、nexe、MSVC 等），并具备打包器版本自动适配、环境自动检测与依赖一键安装等智能功能。旨在为开发者提供一个免费、开源、全能的跨语言打包工具。

---

## 功能特性

### 多语言支持

- **Python**：支持 .py / .pyw 文件，推荐 PyInstaller / Nuitka / cx_Freeze / PyOxidizer
- **Java**：支持 .java 文件，推荐 jpackage (JDK 官方) / launch4j
- **Rust**：支持 .rs 文件，推荐 cargo build / cargo-xwin (交叉编译)
- **Go**：支持 .go 文件，推荐 go build / go build (带控制台) / gox (并行编译)
- **PHP**：支持 .php / .phtml 文件，推荐 PHPacker / PHAR (官方归档)
- **Node.js**：支持 .js / .mjs / .cjs / .ts 文件，推荐 pkg / nexe / Electron Builder
- **C++**：支持 .cpp / .cxx / .cc / .c / .h / .hpp 文件，推荐 MSVC 编译 / CMake + MSVC

### 打包器版本自动适配

- 自动检测打包器版本并适配命令行参数变化
- 支持 PyInstaller (4.0+ / 旧版)、Nuitka (2.x / 旧版)、pkg (5.0 / 旧版)、nexe (4.0+)、PyOxidizer、PHPacker、jpackage、Electron Builder 等全版本适配
- 智能移除不兼容参数，确保新老版本均可正常运行

### 全自动依赖管理

- **语言运行时自动安装**：支持 Python、Java、Rust、Go、PHP、Node.js、Git 的自动检测与安装
- **打包工具自动安装**：自动检测并安装 PyInstaller、Nuitka、cx_Freeze、PyOxidizer、gox、cargo-xwin、pkg、nexe、electron-builder 等打包器
- **跨平台支持**：Windows (winget / 下载安装)、Linux (apt)、macOS (brew) 三种平台全覆盖
- **一键安装所有依赖**：内置打包器管理器，可批量安装/卸载任意打包器

### 混合模式执行引擎

- **日志窗口实时输出**：后台 subprocess 实时捕获 stdout/stderr 并在 UI 日志窗口显示
- **独立终端窗口**：同时打开独立 cmd/terminal 窗口运行编译命令，方便用户直接观察完整输出
- **超时保护**：内置 600 秒超时机制，超时自动终止进程
- **环境变量智能构建**：自动检测并注入 Python/Node.js/Rust/Go/MSVC 等工具的 PATH 路径

### 智能环境检测

- 自动检测编程语言运行时是否安装（Python、Java、Rust、Go、PHP、Node.js、Git、MSVC）
- 自动检测打包器是否安装并显示版本信息
- 环境缺失时自动触发安装流程
- MSVC 环境自动加载 Visual Studio vcvarsall.bat 环境变量

### 文件管理与打包

- 批量添加单个文件或整个文件夹（自动递归扫描支持的文件扩展名）
- 自动根据文件扩展名识别编程语言
- 支持多文件批量打包，实时显示每个文件的打包状态
- 自定义输出目录，默认输出到文件所在目录的 dist 文件夹
- 打包完成后自动收集输出文件到指定目录

### 设置与配置

- 为每种语言单独设置默认打包器
- 自动检测语言开关
- 自动安装缺失依赖开关
- QSettings 持久化配置，重启后自动加载
- 打包器管理器对话框：可视化查看/安装/刷新所有打包器状态

### UI 特性

- 纯白背景可爱风 UI 设计
- 粉色系按钮配色（主按钮、成功按钮、警告按钮、链接按钮）
- 渐变色进度条（粉色到绿色渐变）
- 表格交替行颜色
- 右键菜单（移除选中/清空全部）
- 菜单栏（工具菜单 + 帮助菜单）

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.8+ |
| GUI 框架 | PySide6 (Qt for Python) |
| 系统交互 | subprocess (跨平台命令执行) |
| 路径管理 | pathlib + os + winreg (Windows) |
| 依赖安装 | pip / npm / cargo / winget / apt / brew |
| 配置存储 | QSettings (原生配置管理) |
| 并发模型 | QThread + threading.Thread |
| UI 样式 | 自定义 QSS 纯白可爱风主题 |

---

## 安装与运行

### 环境要求

- Windows / macOS / Linux
- Python 3.8 或更高版本
- pip 包管理器

### 安装依赖

```bash
pip install PySide6 tomli tomli-w psutil requests
```

### 运行程序

```bash
python mikan_universal_packer.py
```

首次运行时，程序会自动检测并安装缺失的 Python 依赖包（PySide6、tomli、tomli-w、psutil、requests）。

---

## 项目结构

```
mikan_universal_packer.py    # 主程序入口（单文件应用）
├── config/                   # 配置目录（QSettings 自动生成）
└── dist/                     # 打包输出目录（默认）
```

> 注：本项目采用单文件架构，所有模块、引擎、对话框和主窗口均集成在 `mikan_universal_packer.py` 中，便于分发和部署。

---

## 模块说明

| 模块 | 说明 |
|------|------|
| `PathManager` | 路径管理器（系统 PATH 读取、可执行文件查找、VS 环境变量加载） |
| `VersionAdapter` | 版本适配器（所有打包器新老版本自动参数适配） |
| `DependencyInstaller` | 依赖安装器（全语言运行时 + 全打包器自动安装，跨平台） |
| `PackerEngine` | 打包引擎（混合模式执行：日志窗口 + 独立终端，版本适配，依赖安装） |
| `PackThread` | 打包线程（QThread 异步执行，信号回调更新 UI） |
| `LanguageDownloadDialog` | 语言下载对话框（跳转官网下载各编程语言） |
| `SettingsWindow` | 设置窗口（默认打包器选择、自动检测/安装开关、一键安装依赖） |
| `PackerManagerDialog` | 打包器管理器（可视化安装/刷新/管理所有打包器状态） |
| `MainWindow` | 主窗口（文件管理、语言/打包器选择、打包执行、日志显示） |

---

## 注意事项

1. **管理员权限**：部分语言（如 Java jpackage、MSVC）可能需要管理员权限才能安装到系统路径。
2. **杀毒软件**：程序涉及进程创建和系统路径操作，可能被杀毒软件误报，请将程序加入白名单。
3. **依赖安装时间**：首次一键安装所有依赖可能需要 5~20 分钟，请耐心等待，不要关闭窗口。
4. **网络要求**：自动安装依赖需要稳定的网络连接；部分语言运行时需要从官网下载较大安装包。
5. **MSVC 环境**：C++ 打包需要 Visual Studio Build Tools，可通过设置面板中的官网链接下载安装。
6. **输出文件**：打包完成后，生成的可执行文件位于指定的输出目录中，请根据打包器不同注意文件扩展名（.exe / .app 等）。

---

## 开发

### 代码风格

- 遵循 PEP 8 编码规范
- 使用类型注解（typing）
- 异步操作通过 QThread + Signal/Slot 机制实现
- UI 样式统一使用 QSS 管理

### 添加新语言支持

1. 在 `LANGUAGE_CONFIGS` 字典中添加新的语言配置（包含名称、图标、扩展名、检测命令、依赖文件、主文件列表、打包器列表）
2. 在 `LANGUAGE_WEBSITES` 中添加官网下载链接
3. 在 `DependencyInstaller` 中添加对应的自动安装方法
4. 在 `PathManager.build_env()` 中添加该语言的 PATH 路径

### 添加新打包器

1. 在目标语言的 `LANGUAGE_CONFIGS` 配置中添加新的打包器条目
2. 配置打包器 ID、名称、描述、构建命令模板、安装命令、版本检测命令、输出文件模式
3. 如需版本适配，在 `VersionAdapter` 中添加对应的适配方法并在 `adapt()` 注册表中注册
4. 设置 `version_adapt: True` 启用版本适配

---

## 许可证

本项目采用 **GNU General Public License v3.0** 许可。你可以自由地复制、修改和再分发本软件，但必须保留版权声明和许可声明。衍生作品也必须以相同的许可证开源。

详见 [LICENSE](LICENSE) 文件。

---

## 致谢

- [PySide6](https://www.qt.io/qt-for-python) - Qt for Python 绑定
- [PyInstaller](https://www.pyinstaller.org/) - Python 打包工具
- [Nuitka](https://nuitka.net/) - Python 到 C++ 编译器
- [cargo](https://doc.rust-lang.org/cargo/) - Rust 包管理器与构建工具
- [go build](https://go.dev/doc/build) - Go 官方编译命令
- [pkg](https://github.com/vercel/pkg) - Node.js 打包工具
- [MSVC](https://visualstudio.microsoft.com/) - Microsoft Visual C++ 编译器
- [DeepSeek](https://www.deepseek.com/) - AI 辅助开发

---

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

*Made with care by Mikan Team · AI assisted by DeepSeek*
