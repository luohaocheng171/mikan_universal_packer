#!/usr/bin/env python3
"""
🌸 Mikan Universal Packer v3.10
支持: Python · Java · Rust · Go · PHP · Node.js · C++
所有打包器新老版本自动适配
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

# ============================================================
# 0. 自动安装Python依赖
# ============================================================

def install_python_deps():
    required = {
        'PySide6': 'PySide6',
        'tomli': 'tomli',
        'tomli_w': 'tomli-w',
        'psutil': 'psutil',
        'requests': 'requests',
    }
    
    missing = []
    for module, package in required.items():
        if importlib.util.find_spec(module) is None:
            missing.append(package)
    
    if missing:
        print(f"🌸 安装依赖: {', '.join(missing)}")
        for package in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
    
    return True

install_python_deps()

# ============================================================
# 导入
# ============================================================

import shutil
import json
import threading
import time
import platform
import requests
import zipfile
import tarfile
import ctypes
import webbrowser
import tempfile
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox,
    QGroupBox, QTextEdit, QComboBox, QProgressBar, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog, QDialogButtonBox,
    QCheckBox, QTabWidget, QListWidget, QListWidgetItem, QMenu,
    QTreeWidget, QTreeWidgetItem, QSplitter, QFrame, QScrollArea,
    QToolButton
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QSettings, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QIcon, QAction, QPalette, QCursor


# ============================================================
# 工具函数
# ============================================================

def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def detect_language_by_extension(file_path: str) -> Optional[str]:
    ext = Path(file_path).suffix.lower()
    ext_map = {
        '.py': 'python', '.pyw': 'python',
        '.java': 'java',
        '.rs': 'rust',
        '.go': 'go',
        '.php': 'php', '.phtml': 'php',
        '.js': 'nodejs', '.mjs': 'nodejs', '.cjs': 'nodejs',
        '.ts': 'nodejs',
        '.cpp': 'msvc', '.cxx': 'msvc', '.cc': 'msvc', '.c': 'msvc',
        '.h': 'msvc', '.hpp': 'msvc',
    }
    return ext_map.get(ext)


def open_url(url: str):
    webbrowser.open(url)


# ============================================================
# 可爱风样式 - 纯白背景
# ============================================================

CUTE_STYLE = """
QMainWindow, QDialog, QWidget {
    background: #ffffff;
    font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif;
}
QWidget {
    font-size: 13px;
    color: #4a4a4a;
}
QGroupBox {
    background: #ffffff;
    border: 2px solid #f0e6d3;
    border-radius: 16px;
    margin-top: 14px;
    padding: 16px 14px 14px 14px;
    font-weight: 600;
    color: #5a5a5a;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 10px;
    background: #ffffff;
    color: #ff8a9b;
    font-size: 14px;
}
QPushButton {
    background: #ffe8eb;
    border: none;
    border-radius: 12px;
    padding: 8px 20px;
    color: #5a5a5a;
    font-weight: 500;
    min-height: 32px;
}
QPushButton:hover {
    background: #ffd4d9;
    color: #4a4a4a;
}
QPushButton:pressed {
    background: #f5c0c6;
}
QPushButton#primary-btn {
    background: #ff8a9b;
    color: white;
    font-size: 15px;
    font-weight: 600;
    padding: 12px 36px;
}
QPushButton#primary-btn:hover {
    background: #ff6f83;
}
QPushButton#primary-btn:disabled {
    background: #d4c5c8;
    color: #b0a0a3;
}
QPushButton#success-btn {
    background: #a8d8c8;
    color: white;
}
QPushButton#success-btn:hover {
    background: #8fceb8;
}
QPushButton#warning-btn {
    background: #f7d794;
    color: #5a5a5a;
}
QPushButton#warning-btn:hover {
    background: #f5ce7a;
}
QPushButton#link-btn {
    background: #e8f0fe;
    color: #4a7ec8;
    font-size: 12px;
    padding: 4px 12px;
}
QPushButton#link-btn:hover {
    background: #d4e4f8;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background: #fcf8f5;
    border: 2px solid #f0e6d3;
    border-radius: 10px;
    padding: 8px 14px;
    color: #4a4a4a;
    font-size: 13px;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border-color: #ffb3c1;
    background: #ffffff;
}
QTableWidget {
    background: #ffffff;
    border: 2px solid #f0e6d3;
    border-radius: 12px;
    gridline-color: #f5eee8;
    selection-background-color: #ffe8eb;
    selection-color: #4a4a4a;
}
QTableWidget::item {
    padding: 6px 10px;
}
QHeaderView::section {
    background: #fcf8f5;
    border: none;
    border-bottom: 2px solid #f0e6d3;
    padding: 8px 12px;
    font-weight: 600;
    color: #b8a9c9;
}
QProgressBar {
    border: none;
    border-radius: 8px;
    background: #f0e6d3;
    height: 8px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #ffb3c1, stop:1 #a8d8c8);
    border-radius: 8px;
}
QScrollBar:vertical {
    background: transparent;
    width: 4px;
    border-radius: 2px;
}
QScrollBar::handle:vertical {
    background: #f0e6d3;
    border-radius: 2px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #e0d0c0;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QCheckBox {
    color: #5a5a5a;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 6px;
    border: 2px solid #f0e6d3;
    background: #ffffff;
}
QCheckBox::indicator:checked {
    background: #ffb3c1;
    border-color: #ff8a9b;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #b8a9c9;
    margin-right: 6px;
}
QMenu {
    background: #ffffff;
    border: 2px solid #f0e6d3;
    border-radius: 12px;
    padding: 6px;
}
QMenu::item {
    padding: 6px 24px;
    border-radius: 8px;
    color: #4a4a4a;
}
QMenu::item:selected {
    background: #ffe8eb;
}
"""


# ============================================================
# 语言官网配置
# ============================================================

LANGUAGE_WEBSITES = {
    "python": {"name": "Python", "icon": "🐍", "url": "https://www.python.org/downloads/", "desc": "下载 Python 解释器"},
    "java": {"name": "Java", "icon": "☕", "url": "https://www.oracle.com/java/technologies/downloads/", "desc": "下载 JDK"},
    "rust": {"name": "Rust", "icon": "🦀", "url": "https://www.rust-lang.org/zh-CN/tools/install", "desc": "下载 Rust 编译器"},
    "go": {"name": "Go", "icon": "🦫", "url": "https://go.dev/dl/", "desc": "下载 Go 语言"},
    "php": {"name": "PHP", "icon": "🐘", "url": "https://www.php.net/downloads.php", "desc": "下载 PHP"},
    "nodejs": {"name": "Node.js", "icon": "🟢", "url": "https://nodejs.org/zh-cn/download/", "desc": "下载 Node.js"},
    "git": {"name": "Git", "icon": "📦", "url": "https://git-scm.com/downloads", "desc": "下载 Git"},
    "msvc": {"name": "MSVC", "icon": "⚙️", "url": "https://visualstudio.microsoft.com/zh-hans/downloads/", "desc": "下载 Visual Studio Build Tools"}
}


# ============================================================
# 完整语言配置 (含所有打包器)
# ============================================================

LANGUAGE_CONFIGS = {
    "python": {
        "name": "Python",
        "icon": "🐍",
        "website": "https://www.python.org/downloads/",
        "extensions": [".py", ".pyw"],
        "check_cmd": ["python", "--version"],
        "dep_files": ["requirements.txt", "pyproject.toml"],
        "main_files": ["main.py", "app.py", "__init__.py", "run.py"],
        "packers": [
            {"id": "pyinstaller", "name": "PyInstaller ⭐", "desc": "最流行，支持单文件exe", "cmd": ["pyinstaller", "--onefile", "--noconsole", "{main_file}"], "install": ["pip", "install", "pyinstaller"], "check": ["pyinstaller", "--version"], "output_pattern": ["dist/*.exe"], "recommended": True, "version_adapt": True},
            {"id": "nuitka", "name": "Nuitka", "desc": "Python→C++编译，性能好", "cmd": ["nuitka", "--standalone", "--onefile", "--windows-disable-console", "{main_file}"], "install": ["pip", "install", "nuitka"], "check": ["nuitka", "--version"], "output_pattern": ["*.exe"], "recommended": False, "version_adapt": True},
            {"id": "cx_freeze", "name": "cx_Freeze", "desc": "老牌工具，配置灵活", "cmd": ["python", "setup.py", "build"], "install": ["pip", "install", "cx-freeze"], "check": ["cxfreeze", "--version"], "output_pattern": ["build/exe.win*/*.exe"], "recommended": False, "version_adapt": False},
            {"id": "pyoxidizer", "name": "PyOxidizer", "desc": "Rust编写，启动快", "cmd": ["pyoxidizer", "build"], "install": ["pip", "install", "pyoxidizer"], "check": ["pyoxidizer", "--version"], "output_pattern": ["build/*/release/*.exe"], "recommended": False, "version_adapt": True},
        ]
    },
    "java": {
        "name": "Java",
        "icon": "☕",
        "website": "https://www.oracle.com/java/technologies/downloads/",
        "extensions": [".java"],
        "check_cmd": ["java", "--version"],
        "dep_files": ["pom.xml", "build.gradle"],
        "main_files": ["Main.java", "App.java", "Application.java"],
        "packers": [
            {"id": "jpackage", "name": "jpackage (官方) ⭐", "desc": "JDK官方打包工具", "cmd": ["jpackage", "--input", "target", "--main-jar", "{jar_file}", "--name", "{app_name}"], "install": None, "check": ["jpackage", "--version"], "output_pattern": ["*.exe", "*.msi"], "recommended": True, "version_adapt": True},
            {"id": "launch4j", "name": "launch4j", "desc": "轻量级，XML配置", "cmd": ["launch4j", "config.xml"], "install": ["download", "https://sourceforge.net/projects/launch4j/"], "check": ["launch4j", "--version"], "output_pattern": ["*.exe"], "recommended": False, "version_adapt": False},
        ]
    },
    "rust": {
        "name": "Rust",
        "icon": "🦀",
        "website": "https://www.rust-lang.org/zh-CN/tools/install",
        "extensions": [".rs"],
        "check_cmd": ["rustc", "--version"],
        "dep_files": ["Cargo.toml"],
        "main_files": ["main.rs"],
        "packers": [
            {"id": "cargo_build", "name": "cargo build (官方) ⭐", "desc": "Rust官方编译，性能最佳", "cmd": ["cargo", "build", "--release"], "install": ["download", "https://rustup.rs/"], "check": ["cargo", "--version"], "output_pattern": ["target/release/*.exe"], "recommended": True, "version_adapt": False},
            {"id": "cargo_xwin", "name": "cargo-xwin (交叉编译)", "desc": "从Linux/Mac编译Windows exe", "cmd": ["cargo", "xwin", "build", "--release", "--target", "x86_64-pc-windows-msvc"], "install": ["cargo", "install", "cargo-xwin"], "check": ["cargo", "xwin", "--version"], "output_pattern": ["target/x86_64-pc-windows-msvc/release/*.exe"], "recommended": False, "version_adapt": False},
        ]
    },
    "go": {
        "name": "Go",
        "icon": "🦫",
        "website": "https://go.dev/dl/",
        "extensions": [".go"],
        "check_cmd": ["go", "version"],
        "dep_files": ["go.mod"],
        "main_files": ["main.go"],
        "packers": [
            {"id": "go_build", "name": "go build (官方) ⭐", "desc": "Go官方编译，天生单exe", "cmd": ["go", "build", "-ldflags=\"-H windowsgui\"", "-o", "{app_name}.exe"], "install": ["download", "https://go.dev/dl/"], "check": ["go", "version"], "output_pattern": ["*.exe"], "recommended": True, "version_adapt": False},
            {"id": "go_build_console", "name": "go build (带控制台)", "desc": "带命令行窗口的exe", "cmd": ["go", "build", "-o", "{app_name}.exe"], "install": ["download", "https://go.dev/dl/"], "check": ["go", "version"], "output_pattern": ["*.exe"], "recommended": False, "version_adapt": False},
            {"id": "gox", "name": "gox (并行编译)", "desc": "并行编译多个平台", "cmd": ["gox", "-osarch=\"windows/amd64\"", "-output=\"{app_name}.exe\""], "install": ["go", "install", "github.com/mitchellh/gox@latest"], "check": ["gox", "--version"], "output_pattern": ["*.exe"], "recommended": False, "version_adapt": False},
        ]
    },
    "php": {
        "name": "PHP",
        "icon": "🐘",
        "website": "https://www.php.net/downloads.php",
        "extensions": [".php", ".phtml"],
        "check_cmd": ["php", "--version"],
        "dep_files": ["composer.json"],
        "main_files": ["index.php", "app.php", "main.php"],
        "packers": [
            {"id": "phpacker", "name": "PHPacker ⭐", "desc": "新兴打包工具，打包成单exe", "cmd": ["phpacker", "build", "{main_file}"], "install": ["download", "https://github.com/crazywhalecc/phpacker/releases"], "check": ["phpacker", "--version"], "output_pattern": ["*.exe"], "recommended": True, "version_adapt": True},
            {"id": "phar", "name": "PHAR (官方归档)", "desc": "PHP官方打包成phar", "cmd": ["php", "-d", "phar.readonly=0", "pack.php"], "install": None, "check": ["php", "-r", "echo 'PHAR OK';"], "output_pattern": ["*.phar"], "recommended": False, "version_adapt": False},
        ]
    },
    "nodejs": {
        "name": "Node.js",
        "icon": "🟢",
        "website": "https://nodejs.org/zh-cn/download/",
        "extensions": [".js", ".mjs", ".cjs", ".ts"],
        "check_cmd": ["node", "--version"],
        "dep_files": ["package.json"],
        "main_files": ["index.js", "main.js", "app.js", "server.js"],
        "packers": [
            {"id": "pkg", "name": "pkg ⭐", "desc": "最流行的Node.js打包工具", "cmd": ["pkg", "{main_file}", "--targets", "node18-win-x64", "--output", "{app_name}.exe"], "install": ["npm", "install", "-g", "pkg"], "check": ["pkg", "--version"], "output_pattern": ["*.exe"], "recommended": True, "version_adapt": True},
            {"id": "nexe", "name": "nexe", "desc": "将Node.js应用编译成单exe", "cmd": ["nexe", "{main_file}", "--target", "windows-x64-18.15.0", "--output", "{app_name}.exe"], "install": ["npm", "install", "-g", "nexe"], "check": ["nexe", "--version"], "output_pattern": ["*.exe"], "recommended": False, "version_adapt": True},
            {"id": "electron_builder", "name": "Electron Builder", "desc": "打包Electron应用", "cmd": ["npx", "electron-builder", "--win", "--x64"], "install": ["npm", "install", "-g", "electron-builder"], "check": ["electron-builder", "--version"], "output_pattern": ["dist/*.exe"], "recommended": False, "version_adapt": True},
        ]
    },
    "msvc": {
        "name": "MSVC (C++)",
        "icon": "⚙️",
        "website": "https://visualstudio.microsoft.com/zh-hans/downloads/",
        "extensions": [".cpp", ".cxx", ".cc", ".c", ".h", ".hpp"],
        "check_cmd": ["cl"],
        "dep_files": ["CMakeLists.txt"],
        "main_files": ["main.cpp", "main.c"],
        "packers": [
            {"id": "msvc_build", "name": "MSVC 编译 (官方) ⭐", "desc": "使用Visual Studio编译C++", "cmd": ["cl", "/EHsc", "{main_file}", "/Fe:{app_name}.exe"], "install": ["download", "https://visualstudio.microsoft.com/zh-hans/downloads/"], "check": ["cl"], "output_pattern": ["*.exe"], "recommended": True, "version_adapt": False},
            {"id": "cmake_build", "name": "CMake + MSVC", "desc": "使用CMake构建C++项目", "cmd": ["cmake", "--build", ".", "--config", "Release", "--target", "{app_name}"], "install": ["download", "https://cmake.org/download/"], "check": ["cmake", "--version"], "output_pattern": ["Release/*.exe"], "recommended": False, "version_adapt": False},
        ]
    },
    "git": {
        "name": "Git",
        "icon": "📦",
        "website": "https://git-scm.com/downloads",
        "extensions": [],
        "check_cmd": ["git", "--version"],
        "dep_files": [],
        "main_files": [],
        "packers": []
    }
}


# ============================================================
# 全自动路径管理器
# ============================================================

class PathManager:
    @staticmethod
    def get_system_path() -> str:
        import platform
        system = platform.system()
        if system == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
                path, _ = winreg.QueryValueEx(key, "Path")
                winreg.CloseKey(key)
                return path
            except:
                return os.environ.get("PATH", "")
        else:
            return os.environ.get("PATH", "")
    
    @staticmethod
    def find_executable(cmd: str) -> Optional[str]:
        import shutil
        if os.path.isabs(cmd) and os.path.exists(cmd):
            return cmd
        exe_path = shutil.which(cmd)
        if exe_path:
            return exe_path
        system = platform.system()
        if system == "Windows":
            system_path = PathManager.get_system_path()
            for path_dir in system_path.split(";"):
                if path_dir and os.path.exists(path_dir):
                    for ext in [".exe", ".cmd", ".bat", ""]:
                        full_path = os.path.join(path_dir, cmd + ext)
                        if os.path.exists(full_path):
                            return full_path
        username = os.getlogin()
        common_paths = {
            "python": [f"C:\\Python311\\python.exe", f"C:\\Python310\\python.exe", f"C:\\Program Files\\Python311\\python.exe", f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe", f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"],
            "java": [f"C:\\Program Files\\Java\\jdk-21\\bin\\java.exe", f"C:\\Program Files\\Java\\jdk-17\\bin\\java.exe"],
            "cargo": [f"C:\\Users\\{username}\\.cargo\\bin\\cargo.exe"],
            "rustc": [f"C:\\Users\\{username}\\.cargo\\bin\\rustc.exe"],
            "go": [f"C:\\Program Files\\Go\\bin\\go.exe"],
            "php": [f"C:\\php\\php.exe", f"C:\\Program Files\\php\\php.exe"],
            "node": [f"C:\\Program Files\\nodejs\\node.exe"],
            "npm": [f"C:\\Users\\{username}\\AppData\\Roaming\\npm\\npm.cmd"],
            "pkg": [f"C:\\Users\\{username}\\AppData\\Roaming\\npm\\pkg.cmd"],
            "nuitka": [f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python314\\Scripts\\nuitka.exe", f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\nuitka.exe", f"C:\\Python311\\Scripts\\nuitka.exe"],
            "pyinstaller": [f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\pyinstaller.exe", f"C:\\Python311\\Scripts\\pyinstaller.exe"],
            "cl": [f"C:\\Program Files\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Tools\\MSVC\\*\\bin\\Hostx64\\x64\\cl.exe"],
            "cmake": [f"C:\\Program Files\\CMake\\bin\\cmake.exe"],
            "git": [f"C:\\Program Files\\Git\\bin\\git.exe"],
            "cxfreeze": [f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\cxfreeze.exe", f"C:\\Python311\\Scripts\\cxfreeze.exe"],
            "pyoxidizer": [f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\pyoxidizer.exe", f"C:\\Python311\\Scripts\\pyoxidizer.exe"],
            "phpacker": [f"C:\\phpacker\\phpacker.exe", f"C:\\Users\\{username}\\Downloads\\phpacker.exe"],
            "nexe": [f"C:\\Users\\{username}\\AppData\\Roaming\\npm\\nexe.cmd", f"C:\\Program Files\\nodejs\\nexe.cmd"],
            "electron-builder": [f"C:\\Users\\{username}\\AppData\\Roaming\\npm\\electron-builder.cmd", f"C:\\Program Files\\nodejs\\electron-builder.cmd"],
            "gox": [f"C:\\Users\\{username}\\go\\bin\\gox.exe", f"C:\\Program Files\\Go\\bin\\gox.exe"],
            "launch4j": [f"C:\\Program Files\\launch4j\\launch4j.exe", f"C:\\Program Files (x86)\\launch4j\\launch4j.exe"],
            "jpackage": [f"C:\\Program Files\\Java\\jdk-21\\bin\\jpackage.exe", f"C:\\Program Files\\Java\\jdk-17\\bin\\jpackage.exe"],
        }
        for path in common_paths.get(cmd, []):
            if "*" in path:
                import glob
                for matched in glob.glob(path):
                    if os.path.exists(matched):
                        return matched
            elif os.path.exists(path):
                return path
        return None
    
    @staticmethod
    def load_vs_env() -> dict:
        env = os.environ.copy()
        system = platform.system()
        if system != "Windows":
            return env
        vcvars_paths = [
            r"C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat",
            r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
            r"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsall.bat",
            r"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat",
        ]
        for vcvars in vcvars_paths:
            if os.path.exists(vcvars):
                try:
                    cmd = f'"{vcvars}" x64 >nul 2>&1 && set'
                    result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=15)
                    for line in result.stdout.splitlines():
                        if '=' in line:
                            key, value = line.split('=', 1)
                            env[key] = value
                    return env
                except:
                    pass
        return env
    
    @staticmethod
    def build_env(language: str = None, packer_id: str = None) -> dict:
        env = os.environ.copy()
        system = platform.system()
        if system == "Windows":
            if packer_id and ('nuitka' in packer_id or 'msvc' in packer_id or 'cl' in packer_id):
                vs_env = PathManager.load_vs_env()
                env.update(vs_env)
            username = os.getlogin()
            extra_paths = []
            python_versions = ["Python314", "Python313", "Python312", "Python311", "Python310"]
            for ver in python_versions:
                paths = [f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\{ver}\\Scripts", f"C:\\{ver}\\Scripts"]
                extra_paths.extend([p for p in paths if os.path.exists(p)])
            node_paths = [f"C:\\Users\\{username}\\AppData\\Roaming\\npm", f"C:\\Program Files\\nodejs"]
            extra_paths.extend([p for p in node_paths if os.path.exists(p)])
            rust_path = f"C:\\Users\\{username}\\.cargo\\bin"
            if os.path.exists(rust_path):
                extra_paths.append(rust_path)
            go_path = f"C:\\Program Files\\Go\\bin"
            if os.path.exists(go_path):
                extra_paths.append(go_path)
            git_paths = [f"C:\\Program Files\\Git\\bin", f"C:\\Program Files\\Git\\cmd"]
            extra_paths.extend([p for p in git_paths if os.path.exists(p)])
            if extra_paths:
                env["PATH"] = ";".join(extra_paths) + ";" + env.get("PATH", "")
        return env


# ============================================================
# 版本适配器 - 所有打包器新老版本自动切换
# ============================================================

class VersionAdapter:
    """通用版本适配器 - 支持所有打包器"""
    
    _version_cache = {}
    
    @classmethod
    def get_version(cls, tool_name: str, check_cmd: List[str]) -> Optional[str]:
        """获取工具版本"""
        cache_key = tool_name
        if cache_key in cls._version_cache:
            return cls._version_cache[cache_key]
        
        if not check_cmd:
            return None
        
        exe = check_cmd[0]
        full_path = PathManager.find_executable(exe)
        if not full_path:
            return None
        
        try:
            args = check_cmd[1:] if len(check_cmd) > 1 else []
            result = subprocess.run([full_path, *args], capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
            
            # 提取版本号
            match = re.search(r'(\d+)\.(\d+)\.(\d+)', output)
            if match:
                version = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
                cls._version_cache[cache_key] = version
                return version
            match = re.search(r'(\d+)\.(\d+)', output)
            if match:
                version = f"{match.group(1)}.{match.group(2)}"
                cls._version_cache[cache_key] = version
                return version
            cls._version_cache[cache_key] = "unknown"
            return "unknown"
        except:
            cls._version_cache[cache_key] = None
            return None
    
    @classmethod
    def adapt_nuitka(cls, cmd: List[str]) -> List[str]:
        """Nuitka: 2.x 移除 --no-pgo 和 --no-lto"""
        version = cls.get_version("nuitka", ["nuitka", "--version"])
        if version:
            parts = version.split('.')
            major = int(parts[0]) if parts else 0
            if major >= 2:
                return [arg for arg in cmd if arg not in ['--no-pgo', '--no-lto']]
        return cmd
    
    @classmethod
    def adapt_pyinstaller(cls, cmd: List[str]) -> List[str]:
        """PyInstaller: 4.0+ 支持 --noconfirm"""
        version = cls.get_version("pyinstaller", ["pyinstaller", "--version"])
        if version:
            parts = version.split('.')
            major = int(parts[0]) if parts else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            
            # 4.0 以下移除 --noconfirm
            if major < 4:
                return [arg for arg in cmd if arg != '--noconfirm']
        return cmd
    
    @classmethod
    def adapt_pkg(cls, cmd: List[str]) -> List[str]:
        """pkg: 5.0 以下移除 --no-bytecode"""
        version = cls.get_version("pkg", ["pkg", "--version"])
        if version:
            parts = version.split('.')
            major = int(parts[0]) if parts else 0
            if major < 5:
                return [arg for arg in cmd if arg != '--no-bytecode']
        return cmd
    
    @classmethod
    def adapt_nexe(cls, cmd: List[str]) -> List[str]:
        """nexe: 4.0 改变目标格式"""
        version = cls.get_version("nexe", ["nexe", "--version"])
        if version:
            parts = version.split('.')
            major = int(parts[0]) if parts else 0
            if major >= 4:
                # 新版使用 windows-x64-18.15.0 格式
                # 检查是否有旧格式参数
                cmd_str = ' '.join(cmd)
                if '--platform' in cmd_str and '--arch' in cmd_str:
                    # 新旧格式转换
                    pass
        return cmd
    
    @classmethod
    def adapt_pyoxidizer(cls, cmd: List[str]) -> List[str]:
        """PyOxidizer: 0.20+ 配置文件格式变化"""
        version = cls.get_version("pyoxidizer", ["pyoxidizer", "--version"])
        if version:
            parts = version.split('.')
            major = int(parts[0]) if parts else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            if major >= 0 and minor >= 20:
                # 新版使用新配置格式，命令行基本不变
                pass
        return cmd
    
    @classmethod
    def adapt_phpacker(cls, cmd: List[str]) -> List[str]:
        """PHPacker: 0.5+ 命令变化"""
        version = cls.get_version("phpacker", ["phpacker", "--version"])
        if version:
            parts = version.split('.')
            major = int(parts[0]) if parts else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            if major == 0 and minor < 5:
                # 旧版: phpacker build app.php -o app.exe
                # 新版: phpacker build app.php
                # 检查是否有 -o 参数
                if '-o' in cmd:
                    # 移除 -o 参数（新版会自动生成）
                    new_cmd = []
                    skip_next = False
                    for i, arg in enumerate(cmd):
                        if skip_next:
                            skip_next = False
                            continue
                        if arg == '-o':
                            skip_next = True
                            continue
                        new_cmd.append(arg)
                    return new_cmd
        return cmd
    
    @classmethod
    def adapt_jpackage(cls, cmd: List[str]) -> List[str]:
        """jpackage: JDK 16+ 支持"""
        version = cls.get_version("jpackage", ["jpackage", "--version"])
        if version:
            parts = version.split('.')
            major = int(parts[0]) if parts else 0
            if major < 16:
                return []  # jpackage 不可用
        return cmd
    
    @classmethod
    def adapt_electron_builder(cls, cmd: List[str]) -> List[str]:
        """electron-builder: 23.0+ 配置变化"""
        version = cls.get_version("electron-builder", ["electron-builder", "--version"])
        if version:
            parts = version.split('.')
            major = int(parts[0]) if parts else 0
            if major >= 23:
                # 新版支持新配置
                pass
        return cmd
    
    @classmethod
    def adapt(cls, packer_id: str, cmd: List[str], log_callback=None) -> List[str]:
        """通用适配入口"""
        adapters = {
            "nuitka": cls.adapt_nuitka,
            "pyinstaller": cls.adapt_pyinstaller,
            "pkg": cls.adapt_pkg,
            "nexe": cls.adapt_nexe,
            "pyoxidizer": cls.adapt_pyoxidizer,
            "phpacker": cls.adapt_phpacker,
            "jpackage": cls.adapt_jpackage,
            "electron_builder": cls.adapt_electron_builder,
            "cargo_build": None,  # 稳定，无需适配
            "cargo_xwin": None,
            "go_build": None,
            "go_build_console": None,
            "gox": None,
            "msvc_build": None,
            "cmake_build": None,
            "cx_freeze": None,
            "phar": None,
            "launch4j": None,
        }
        
        if packer_id in adapters and adapters[packer_id] is not None:
            original = cmd.copy()
            adapted = adapters[packer_id](cmd)
            if adapted != original:
                removed = set(original) - set(adapted)
                if removed and log_callback:
                    log_callback(f"    🔄 版本适配: 移除 {removed}")
                return adapted
        return cmd


# ============================================================
# 全自动依赖安装器
# ============================================================

class DependencyInstaller:
    @classmethod
    def check_installed(cls, name: str) -> Tuple[bool, str]:
        check_map = {
            "python": ["python", "--version"],
            "java": ["java", "--version"],
            "rust": ["rustc", "--version"],
            "go": ["go", "version"],
            "php": ["php", "--version"],
            "nodejs": ["node", "--version"],
            "git": ["git", "--version"],
            "npm": ["npm", "--version"],
            "msvc": ["cl"],
        }
        if name not in check_map:
            return True, "内置"
        exe = check_map[name][0]
        full_path = PathManager.find_executable(exe)
        if full_path:
            try:
                result = subprocess.run([full_path, *check_map[name][1:]], capture_output=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.decode().strip().split('\n')[0][:50]
                    return True, version
            except:
                pass
        return False, "未安装"
    
    @classmethod
    def check_packer_installed(cls, packer_id: str, check_cmd: List[str]) -> Tuple[bool, str]:
        if not check_cmd:
            special_cases = {
                "jpackage": ["jpackage", "--version"],
                "phar": ["php", "-v"],
                "cargo_build": ["cargo", "--version"],
                "go_build": ["go", "version"],
                "go_build_console": ["go", "version"],
                "msvc_build": ["cl"],
                "cmake_build": ["cmake", "--version"],
                "nuitka": ["nuitka", "--version"],
                "pyinstaller": ["pyinstaller", "--version"],
                "cx_freeze": ["cxfreeze", "--version"],
                "pyoxidizer": ["pyoxidizer", "--version"],
                "pkg": ["pkg", "--version"],
                "nexe": ["nexe", "--version"],
                "electron_builder": ["electron-builder", "--version"],
            }
            if packer_id in special_cases:
                check_cmd = special_cases[packer_id]
            else:
                return False, "无法检测"
        exe = check_cmd[0]
        full_path = PathManager.find_executable(exe)
        if full_path:
            try:
                result = subprocess.run([full_path, *check_cmd[1:]], capture_output=True, timeout=10)
                if result.returncode == 0:
                    version = result.stdout.decode().strip().split('\n')[0][:50]
                    return True, version
                if packer_id == "msvc_build" and "Microsoft" in result.stderr.decode():
                    return True, "MSVC 已安装"
            except:
                pass
        return False, "未安装"
    
    @classmethod
    def install_all(cls, log_callback=None) -> bool:
        tools = ["python", "java", "rust", "go", "php", "nodejs", "git"]
        results = {}
        for tool in tools:
            installed, version = cls.check_installed(tool)
            if installed:
                if log_callback:
                    log_callback(f"✅ {tool}: {version}")
                results[tool] = True
            else:
                if log_callback:
                    log_callback(f"📦 安装 {tool}...")
                success = cls.install_tool(tool, log_callback)
                results[tool] = success
                if success and log_callback:
                    log_callback(f"  ✅ {tool} 安装完成")
                elif log_callback:
                    log_callback(f"  ❌ {tool} 安装失败")
        if log_callback:
            log_callback("\n📦 安装打包器...")
        packers = ["pyinstaller", "nuitka", "cx_freeze", "pyoxidizer", "gox", "cargo_xwin", "pkg", "nexe", "electron_builder"]
        for packer in packers:
            check_cmd = cls._get_packer_check(packer)
            installed, version = cls.check_packer_installed(packer, check_cmd)
            if installed:
                if log_callback:
                    log_callback(f"  ✅ {packer}: {version}")
                continue
            install_cmd = cls._get_packer_install(packer)
            if install_cmd:
                if log_callback:
                    log_callback(f"  📦 安装 {packer}...")
                try:
                    env = PathManager.build_env(None, packer)
                    subprocess.run(install_cmd, env=env, check=True, capture_output=True, timeout=300)
                    if log_callback:
                        log_callback(f"    ✅ {packer} 安装完成")
                except:
                    if log_callback:
                        log_callback(f"    ❌ {packer} 安装失败")
            else:
                if log_callback:
                    log_callback(f"  ℹ️ {packer} 无需安装")
        return all(results.values())
    
    @classmethod
    def install_tool(cls, name: str, log_callback=None) -> bool:
        system = platform.system()
        if name == "python":
            return cls._install_python(log_callback)
        elif name == "java":
            return cls._install_java(log_callback)
        elif name == "rust":
            return cls._install_rust(log_callback)
        elif name == "go":
            return cls._install_go(log_callback)
        elif name == "php":
            return cls._install_php(log_callback)
        elif name == "nodejs":
            return cls._install_nodejs(log_callback)
        elif name == "git":
            return cls._install_git(log_callback)
        return False
    
    @classmethod
    def _install_python(cls, log_callback=None) -> bool:
        system = platform.system()
        if system == "Windows":
            try:
                subprocess.run(["winget", "install", "Python.Python.3.11"], check=True, capture_output=True, timeout=300)
                return True
            except:
                url = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
                installer = Path.home() / "Downloads" / "python_installer.exe"
                if cls._download_file(url, installer, log_callback):
                    subprocess.run([str(installer), "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True, timeout=600)
                    return True
                return False
        elif system == "Linux":
            try:
                subprocess.run(["sudo", "apt", "install", "-y", "python3", "python3-pip"], check=True, timeout=300)
                return True
            except:
                return False
        elif system == "Darwin":
            try:
                subprocess.run(["brew", "install", "python@3.11"], check=True, timeout=300)
                return True
            except:
                return False
        return False
    
    @classmethod
    def _install_nodejs(cls, log_callback=None) -> bool:
        system = platform.system()
        if system == "Windows":
            try:
                subprocess.run(["winget", "install", "OpenJS.NodeJS"], check=True, capture_output=True, timeout=300)
                return True
            except:
                url = "https://nodejs.org/dist/v18.17.0/node-v18.17.0-x64.msi"
                installer = Path.home() / "Downloads" / "node_installer.msi"
                if cls._download_file(url, installer, log_callback):
                    subprocess.run(["msiexec", "/i", str(installer), "/quiet"], check=True, timeout=600)
                    return True
                return False
        elif system == "Linux":
            try:
                subprocess.run("curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -", shell=True, check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "nodejs"], check=True)
                return True
            except:
                return False
        elif system == "Darwin":
            try:
                subprocess.run(["brew", "install", "node@18"], check=True, timeout=300)
                return True
            except:
                return False
        return False
    
    @classmethod
    def _install_java(cls, log_callback=None) -> bool:
        system = platform.system()
        if system == "Windows":
            try:
                subprocess.run(["winget", "install", "Oracle.JDK.21"], check=True, capture_output=True, timeout=300)
                return True
            except:
                url = "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe"
                installer = Path.home() / "Downloads" / "jdk_installer.exe"
                if cls._download_file(url, installer, log_callback):
                    subprocess.run([str(installer), "/quiet"], check=True, timeout=600)
                    return True
                return False
        elif system == "Linux":
            try:
                subprocess.run(["sudo", "apt", "install", "-y", "openjdk-21-jdk"], check=True, timeout=300)
                return True
            except:
                return False
        elif system == "Darwin":
            try:
                subprocess.run(["brew", "install", "openjdk@21"], check=True, timeout=300)
                return True
            except:
                return False
        return False
    
    @classmethod
    def _install_rust(cls, log_callback=None) -> bool:
        system = platform.system()
        if system == "Windows":
            url = "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe"
            installer = Path.home() / "Downloads" / "rustup-init.exe"
            if cls._download_file(url, installer, log_callback):
                subprocess.run([str(installer), "-y", "--default-toolchain", "stable"], check=True, timeout=600)
                return True
            return False
        else:
            try:
                cmd = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
                subprocess.run(cmd, shell=True, check=True, timeout=300)
                return True
            except:
                return False
    
    @classmethod
    def _install_go(cls, log_callback=None) -> bool:
        system = platform.system()
        if system == "Windows":
            try:
                subprocess.run(["winget", "install", "GoLang.Go"], check=True, capture_output=True, timeout=300)
                return True
            except:
                url = "https://go.dev/dl/go1.21.0.windows-amd64.msi"
                installer = Path.home() / "Downloads" / "go_installer.msi"
                if cls._download_file(url, installer, log_callback):
                    subprocess.run(["msiexec", "/i", str(installer), "/quiet"], check=True, timeout=600)
                    return True
                return False
        elif system == "Linux":
            try:
                subprocess.run(["sudo", "apt", "install", "-y", "golang-go"], check=True, timeout=300)
                return True
            except:
                return False
        elif system == "Darwin":
            try:
                subprocess.run(["brew", "install", "go"], check=True, timeout=300)
                return True
            except:
                return False
        return False
    
    @classmethod
    def _install_php(cls, log_callback=None) -> bool:
        system = platform.system()
        if system == "Windows":
            try:
                subprocess.run(["winget", "install", "PHP.PHP"], check=True, capture_output=True, timeout=300)
                return True
            except:
                url = "https://windows.php.net/downloads/releases/php-8.2.0-nts-Win32-vs16-x64.zip"
                zip_path = Path.home() / "Downloads" / "php.zip"
                if cls._download_file(url, zip_path, log_callback):
                    extract_dir = Path("C:/php")
                    extract_dir.mkdir(exist_ok=True)
                    with zipfile.ZipFile(zip_path, 'r') as zf:
                        zf.extractall(extract_dir)
                    return True
                return False
        elif system == "Linux":
            try:
                subprocess.run(["sudo", "apt", "install", "-y", "php", "php-cli"], check=True, timeout=300)
                return True
            except:
                return False
        elif system == "Darwin":
            try:
                subprocess.run(["brew", "install", "php"], check=True, timeout=300)
                return True
            except:
                return False
        return False
    
    @classmethod
    def _install_git(cls, log_callback=None) -> bool:
        system = platform.system()
        if system == "Windows":
            try:
                subprocess.run(["winget", "install", "Git.Git"], check=True, capture_output=True, timeout=300)
                return True
            except:
                url = "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe"
                installer = Path.home() / "Downloads" / "git_installer.exe"
                if cls._download_file(url, installer, log_callback):
                    subprocess.run([str(installer), "/VERYSILENT", "/NORESTART"], check=True, timeout=600)
                    return True
                return False
        elif system == "Linux":
            try:
                subprocess.run(["sudo", "apt", "install", "-y", "git"], check=True, timeout=300)
                return True
            except:
                return False
        elif system == "Darwin":
            try:
                subprocess.run(["brew", "install", "git"], check=True, timeout=300)
                return True
            except:
                return False
        return False
    
    @classmethod
    def _get_packer_check(cls, packer: str) -> Optional[List[str]]:
        map = {
            "pyinstaller": ["pyinstaller", "--version"],
            "nuitka": ["nuitka", "--version"],
            "cx_freeze": ["cxfreeze", "--version"],
            "pyoxidizer": ["pyoxidizer", "--version"],
            "cargo_xwin": ["cargo", "xwin", "--version"],
            "gox": ["gox", "--version"],
            "pkg": ["pkg", "--version"],
            "nexe": ["nexe", "--version"],
            "electron_builder": ["electron-builder", "--version"],
        }
        return map.get(packer)
    
    @classmethod
    def _get_packer_install(cls, packer: str) -> Optional[List[str]]:
        map = {
            "pyinstaller": ["pip", "install", "pyinstaller"],
            "nuitka": ["pip", "install", "nuitka"],
            "cx_freeze": ["pip", "install", "cx-freeze"],
            "pyoxidizer": ["pip", "install", "pyoxidizer"],
            "cargo_xwin": ["cargo", "install", "cargo-xwin"],
            "gox": ["go", "install", "github.com/mitchellh/gox@latest"],
            "pkg": ["npm", "install", "-g", "pkg"],
            "nexe": ["npm", "install", "-g", "nexe"],
        }
        return map.get(packer)
    
    @classmethod
    def _download_file(cls, url: str, dest: Path, log_callback=None) -> bool:
        try:
            response = requests.get(url, stream=True)
            total = int(response.headers.get('content-length', 0))
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if log_callback and total > 0:
                            pct = downloaded / total * 100
                            log_callback(f"    下载: {pct:.0f}%")
            return True
        except:
            return False


# ============================================================
# 打包引擎 - 混合模式 + 版本适配
# ============================================================

class PackerEngine:
    def __init__(self, language: str, packer_id: str, files: List[str], output_dir: Path, 
                 log_callback=None, progress_callback=None, auto_input: str = "y"):
        self.language = language
        self.packer_id = packer_id
        self.files = [Path(f) for f in files]
        self.output_dir = output_dir
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.auto_input = auto_input
        self.lang_config = LANGUAGE_CONFIGS.get(language)
        self.packer_config = None
        if self.lang_config:
            for p in self.lang_config.get("packers", []):
                if p["id"] == packer_id:
                    self.packer_config = p
                    break
    
    def log(self, msg: str):
        if self.log_callback:
            self.log_callback(msg)
    
    def _build_command_with_path(self, cmd: List[str]) -> List[str]:
        if not cmd:
            return cmd
        exe = cmd[0]
        full_path = PathManager.find_executable(exe)
        if full_path:
            self.log(f"    🔍 使用: {full_path}")
            cmd[0] = full_path
        else:
            self.log(f"    ⚠️ 未找到: {exe}")
        return cmd
    
    def _adapt_command(self, cmd: List[str]) -> List[str]:
        """版本适配入口"""
        need_adapt = self.packer_config.get("version_adapt", False)
        if not need_adapt:
            return cmd
        
        adapted = VersionAdapter.adapt(self.packer_id, cmd, self.log)
        if adapted != cmd:
            self.log(f"    🔄 版本适配: 已优化参数")
        return adapted
    
    def _run_hybrid(self, cmd: List[str], cwd: Path, timeout: int = 600) -> Tuple[bool, str, str]:
        """混合模式执行 (日志窗口 + 独立终端)"""
        # 1. 构建命令路径
        cmd = self._build_command_with_path(cmd)
        
        # 2. 版本适配
        cmd = self._adapt_command(cmd)
        
        cmd_str = ' '.join(cmd)
        env = PathManager.build_env(self.language, self.packer_id)
        
        # 3. 创建批处理文件
        bat_content = f"""@echo off
chcp 65001 >nul
title 🌸 Mikan Packer - 编译中...
echo ============================================================
echo    🌸 Mikan Packer - 编译日志
echo    命令: {cmd_str}
echo    目录: {cwd}
echo    Packer: {self.packer_id}
echo ============================================================
echo.
{cmd_str}
echo.
echo ============================================================
if %errorlevel% equ 0 (
    echo ✅ 编译成功！
) else (
    echo ❌ 编译失败！错误码: %errorlevel%
)
echo ============================================================
echo.
echo 按任意键关闭此窗口...
pause >nul
"""
        bat_path = cwd / f"_compile_{datetime.now().strftime('%H%M%S')}.bat"
        bat_path.write_text(bat_content, encoding='utf-8')
        self.log(f"    📌 批处理: {bat_path}")
        
        # 4. 打开独立终端
        system = platform.system()
        if system == "Windows":
            subprocess.Popen(["start", "cmd", "/k", str(bat_path)], shell=True, cwd=cwd)
            self.log("    📌 已打开独立终端窗口")
        else:
            try:
                subprocess.Popen(["xterm", "-e", f"bash -c 'source {bat_path}; read'"], cwd=cwd)
                self.log("    📌 已打开独立终端窗口")
            except:
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"bash {bat_path}; read"], cwd=cwd)
                self.log("    📌 已打开独立终端窗口")
        
        # 5. 日志窗口实时输出
        self.log("    📌 日志窗口实时输出:")
        self.log("    " + "="*50)
        
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='ignore',
            shell=False,
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW if system == "Windows" else 0
        )
        
        output_lines = []
        for line in iter(process.stdout.readline, ''):
            if line:
                line = line.rstrip()
                output_lines.append(line)
                if line.strip():
                    self.log(f"    📊 {line}")
        
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            self.log("    ⏰ 超时")
            return False, "", "超时"
        
        stdout = '\n'.join(output_lines)
        self.log("    " + "="*50)
        
        if process.returncode == 0:
            self.log("    ✅ 编译成功")
        else:
            self.log(f"    ❌ 编译失败 (返回码: {process.returncode})")
        
        return process.returncode == 0, stdout, ""
    
    def run(self) -> Tuple[bool, List[str]]:
        if not self.lang_config or not self.packer_config:
            return False, [f"❌ 语言 {self.language} 配置不存在"]
        
        self.log(f"🌸 开始打包: {len(self.files)} 个文件")
        
        # 检测打包器版本
        if self.packer_config.get("check"):
            check_cmd = self.packer_config["check"]
            version = VersionAdapter.get_version(self.packer_id, check_cmd)
            if version:
                self.log(f"    📌 {self.packer_config['name']} 版本: {version}")
        
        if not self._check_environment():
            self.log("📦 环境缺失，正在自动安装...")
            if not self._install_environment():
                return False, ["环境安装失败"]
        
        if self.packer_config.get("install"):
            self.log("🔧 安装打包工具...")
            if not self._install_packer():
                return False, ["打包工具安装失败"]
        
        results = []
        for i, file_path in enumerate(self.files):
            self.log(f"\n📦 [{i+1}/{len(self.files)}] 打包: {file_path.name}")
            
            file_lang = detect_language_by_extension(str(file_path))
            if file_lang and file_lang != self.language:
                if file_lang in LANGUAGE_CONFIGS and LANGUAGE_CONFIGS[file_lang].get("packers"):
                    self.log(f"  🌸 检测到 {file_lang}，自动切换...")
                    new_engine = PackerEngine(file_lang, self.packer_id, [str(file_path)], 
                                             self.output_dir, self.log_callback, 
                                             self.progress_callback, self.auto_input)
                    success, msgs = new_engine.run()
                    results.extend([(file_path.name, s) for s in msgs])
                    continue
            
            self._install_dependencies(file_path.parent)
            success, msg = self._pack_single_file(file_path)
            results.append((file_path.name, "✅ 成功" if success else f"❌ {msg}"))
        
        self.log(f"\n🎉 打包完成! 成功 {sum(1 for r in results if '成功' in r[1])}/{len(results)}")
        return True, [f"{name}: {status}" for name, status in results]
    
    def _check_environment(self) -> bool:
        check_cmd = self.lang_config.get("check_cmd", [])
        if not check_cmd:
            return True
        exe = check_cmd[0]
        full_path = PathManager.find_executable(exe)
        if full_path:
            try:
                result = subprocess.run([full_path, *check_cmd[1:]], capture_output=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.decode().strip().split('\n')[0][:50]
                    self.log(f"  ✅ {self.lang_config['name']}: {version}")
                    return True
            except:
                pass
        return False
    
    def _install_environment(self) -> bool:
        self.log(f"  📦 自动安装 {self.lang_config['name']}...")
        return DependencyInstaller.install_tool(self.language, self.log)
    
    def _install_packer(self) -> bool:
        install_config = self.packer_config.get("install")
        if not install_config:
            return True
        if isinstance(install_config, list):
            if install_config[0] == "download":
                url = install_config[1]
                self.log(f"  下载: {url}")
                dest = Path.home() / "Downloads" / Path(url).name
                if DependencyInstaller._download_file(url, dest, self.log):
                    self.log("  ✅ 下载完成")
                    return True
                return False
            try:
                env = PathManager.build_env(self.language, self.packer_id)
                subprocess.run(install_config, env=env, check=True, capture_output=True, timeout=300)
                self.log("  ✅ 安装完成")
                return True
            except:
                return False
        return True
    
    def _install_dependencies(self, project_path: Path):
        lang = self.language
        if lang == "python" and (project_path / "requirements.txt").exists():
            try:
                env = PathManager.build_env(lang, self.packer_id)
                subprocess.run(["pip", "install", "-r", "requirements.txt"], 
                              cwd=project_path, env=env, check=True, capture_output=True, timeout=300)
                self.log("    ✅ pip依赖完成")
            except:
                pass
        elif lang == "nodejs" and (project_path / "package.json").exists():
            try:
                env = PathManager.build_env(lang, self.packer_id)
                subprocess.run(["npm", "install"], cwd=project_path, env=env, check=True, capture_output=True, timeout=300)
                self.log("    ✅ npm依赖完成")
            except:
                pass
    
    def _pack_single_file(self, file_path: Path) -> Tuple[bool, str]:
        project_path = file_path.parent
        main_file = file_path.name
        
        if not file_path.exists():
            main_files = self.lang_config.get("main_files", [])
            for f in main_files:
                if (project_path / f).exists():
                    main_file = f
                    break
        
        cmd_template = self.packer_config.get("cmd", [])
        if not cmd_template:
            return False, "没有打包命令"
        
        cmd = []
        for c in cmd_template:
            c = c.replace("{main_file}", main_file)
            c = c.replace("{app_name}", project_path.name)
            c = c.replace("{jar_file}", self._find_jar_file(project_path))
            cmd.append(c)
        
        # 自动添加静默参数 (版本适配器会处理不兼容的参数)
        cmd_str = ' '.join(cmd).lower()
        if 'nuitka' in cmd_str:
            if '--assume-yes-for-downloads' not in cmd_str:
                cmd.append('--assume-yes-for-downloads')
        if 'pyinstaller' in cmd_str and '--noconfirm' not in cmd_str:
            cmd.append('--noconfirm')
        if 'pkg' in cmd_str and '--no-bytecode' not in cmd_str:
            cmd.append('--no-bytecode')
        if 'cargo' in cmd_str and '--quiet' not in cmd_str:
            cmd.append('--quiet')
        
        # 使用混合模式执行 (包含版本适配)
        success, stdout, stderr = self._run_hybrid(cmd, project_path)
        
        if success:
            self._collect_output(project_path)
            return True, "成功"
        else:
            error_msg = stderr[:200] if stderr else stdout[:200] if stdout else "打包失败"
            return False, error_msg
    
    def _find_jar_file(self, project_path: Path) -> str:
        for jar in project_path.glob("target/*.jar"):
            return jar.name
        return "app.jar"
    
    def _collect_output(self, project_path: Path):
        patterns = self.packer_config.get("output_pattern", [])
        for pattern in patterns:
            for f in project_path.glob(pattern):
                if f.is_file():
                    dest = self.output_dir / f.name
                    if not dest.exists():
                        shutil.copy(f, dest)
                        self.log(f"    📁 输出: {f.name}")


# ============================================================
# 打包线程
# ============================================================

class PackThread(QThread):
    log = Signal(str)
    progress = Signal(int)
    finished = Signal(bool, list)
    
    def __init__(self, language: str, packer_id: str, files: List[str], output_dir: str, auto_input: str = "y"):
        super().__init__()
        self.language = language
        self.packer_id = packer_id
        self.files = files
        self.output_dir = Path(output_dir)
        self.auto_input = auto_input
    
    def run(self):
        engine = PackerEngine(self.language, self.packer_id, self.files, self.output_dir,
                             self.log.emit, self.progress.emit, self.auto_input)
        self.progress.emit(10)
        success, results = engine.run()
        self.progress.emit(100)
        self.finished.emit(success, results)


# ============================================================
# 语言下载对话框
# ============================================================

class LanguageDownloadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🌐 下载编程语言")
        self.setFixedSize(500, 420)
        self.setStyleSheet("background: #ffffff;")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 16, 20, 16)
        
        title = QLabel("🌐 下载编程语言")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #ff8a9b;")
        layout.addWidget(title)
        subtitle = QLabel("点击语言名称跳转官网下载页面 🍊")
        subtitle.setStyleSheet("color: #b8a9c9; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        for key, info in LANGUAGE_WEBSITES.items():
            frame = QFrame()
            frame.setStyleSheet(""" QFrame { background: #fcf8f5; border-radius: 12px; padding: 8px 12px; } QFrame:hover { background: #f5eee8; } """)
            frame_layout = QHBoxLayout(frame)
            frame_layout.setContentsMargins(12, 8, 12, 8)
            
            label = QLabel(f"{info['icon']} {info['name']}")
            label.setStyleSheet("font-weight: 600; color: #4a4a4a; font-size: 14px;")
            label.setFixedWidth(100)
            frame_layout.addWidget(label)
            
            desc = QLabel(info['desc'])
            desc.setStyleSheet("color: #888; font-size: 12px;")
            frame_layout.addWidget(desc)
            frame_layout.addStretch()
            
            btn = QPushButton("🔗 跳转下载")
            btn.setObjectName("link-btn")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(lambda checked, url=info['url']: open_url(url))
            frame_layout.addWidget(btn)
            
            scroll_layout.addWidget(frame)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


# ============================================================
# 独立设置窗口
# ============================================================

class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("🌸 设置")
        self.setMinimumSize(600, 620)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet("QMainWindow { background: #ffffff; } QWidget { background: #ffffff; }")
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(16)
        layout.setContentsMargins(25, 20, 25, 20)
        
        title = QLabel("🌸 设置")
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #ff8a9b;")
        layout.addWidget(title)
        subtitle = QLabel("选择默认打包器 · 📥 一键跳转官网下载语言 🍊")
        subtitle.setStyleSheet("color: #b8a9c9; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        download_group = QFrame()
        download_group.setStyleSheet(""" QFrame { background: #fcf8f5; border-radius: 14px; padding: 12px 16px; border: 2px solid #f0e6d3; } QPushButton { background: #ffd4d9; border: none; border-radius: 8px; padding: 6px 14px; font-size: 12px; color: #5a5a5a; } QPushButton:hover { background: #ffb3c1; } """)
        download_layout = QVBoxLayout(download_group)
        download_layout.setSpacing(8)
        
        dl_title_row = QHBoxLayout()
        dl_title = QLabel("📥 下载编程语言")
        dl_title.setStyleSheet("font-weight: 600; color: #ff8a9b; font-size: 14px;")
        dl_title_row.addWidget(dl_title)
        dl_title_row.addStretch()
        dl_more_btn = QPushButton("🌐 更多语言...")
        dl_more_btn.setObjectName("link-btn")
        dl_more_btn.clicked.connect(self.open_language_download_dialog)
        dl_title_row.addWidget(dl_more_btn)
        download_layout.addLayout(dl_title_row)
        
        lang_grid1 = QHBoxLayout()
        lang_grid1.setSpacing(8)
        for label, key in [("🐍 Python", "python"), ("☕ Java", "java"), ("🦀 Rust", "rust"), ("🦫 Go", "go")]:
            btn = QPushButton(label)
            btn.setFixedHeight(32)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            if key in LANGUAGE_WEBSITES:
                btn.clicked.connect(lambda checked, u=LANGUAGE_WEBSITES[key]["url"]: open_url(u))
            lang_grid1.addWidget(btn)
        download_layout.addLayout(lang_grid1)
        
        lang_grid2 = QHBoxLayout()
        lang_grid2.setSpacing(8)
        for label, key in [("🐘 PHP", "php"), ("🟢 Node.js", "nodejs"), ("📦 Git", "git"), ("⚙️ MSVC", "msvc")]:
            btn = QPushButton(label)
            btn.setFixedHeight(32)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            if key in LANGUAGE_WEBSITES:
                btn.clicked.connect(lambda checked, u=LANGUAGE_WEBSITES[key]["url"]: open_url(u))
            lang_grid2.addWidget(btn)
        download_layout.addLayout(lang_grid2)
        
        tip = QLabel("💡 点击按钮跳转官网下载，支持 Python/Java/Rust/Go/PHP/Node.js/Git/MSVC")
        tip.setStyleSheet("color: #b8a9c9; font-size: 11px;")
        download_layout.addWidget(tip)
        layout.addWidget(download_group)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background: #f0e6d3; max-height: 2px;")
        layout.addWidget(line)
        
        packer_label = QLabel("🎯 默认打包器")
        packer_label.setStyleSheet("font-weight: 600; color: #5a5a5a; font-size: 14px;")
        layout.addWidget(packer_label)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        self.packer_settings = {}
        for lang_key, config in LANGUAGE_CONFIGS.items():
            if not config.get("packers"):
                continue
            group = QFrame()
            group.setStyleSheet("QFrame { background: #fcf8f5; border-radius: 12px; padding: 10px 14px; }")
            group_layout = QHBoxLayout(group)
            group_layout.setContentsMargins(10, 6, 10, 6)
            label = QLabel(f"{config['icon']} {config['name']}")
            label.setFixedWidth(80)
            label.setStyleSheet("font-weight: 600; color: #5a5a5a;")
            combo = QComboBox()
            for p in config["packers"]:
                text = p["name"] + (" ⭐" if p.get("recommended") else "")
                combo.addItem(text, p["id"])
            group_layout.addWidget(label)
            group_layout.addWidget(combo)
            group_layout.addStretch()
            scroll_layout.addWidget(group)
            self.packer_settings[lang_key] = combo
        
        group = QFrame()
        group.setStyleSheet("QFrame { background: #fcf8f5; border-radius: 12px; padding: 10px 14px; }")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(8)
        self.auto_detect_cb = QCheckBox("✨ 自动检测语言")
        self.auto_detect_cb.setChecked(True)
        group_layout.addWidget(self.auto_detect_cb)
        self.auto_install_cb = QCheckBox("📦 自动安装缺失依赖")
        self.auto_install_cb.setChecked(True)
        group_layout.addWidget(self.auto_install_cb)
        scroll_layout.addWidget(group)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        btn_row = QHBoxLayout()
        btn_install = QPushButton("📦 一键安装所有依赖")
        btn_install.setObjectName("warning-btn")
        btn_install.clicked.connect(self.install_all_deps)
        btn_row.addWidget(btn_install)
        btn_row.addStretch()
        btn_save = QPushButton("💾 保存")
        btn_save.setObjectName("success-btn")
        btn_save.clicked.connect(self.save_settings)
        btn_row.addWidget(btn_save)
        btn_close = QPushButton("关闭")
        btn_close.clicked.connect(self.close)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)
    
    def load_settings(self):
        settings = QSettings("MikanSoft", "UniversalPacker")
        for lang_key, combo in self.packer_settings.items():
            saved_id = settings.value(f"packer_{lang_key}", "")
            if saved_id:
                for i in range(combo.count()):
                    if combo.itemData(i) == saved_id:
                        combo.setCurrentIndex(i)
                        break
        self.auto_detect_cb.setChecked(settings.value("auto_detect", True, type=bool))
        self.auto_install_cb.setChecked(settings.value("auto_install", True, type=bool))
    
    def save_settings(self):
        settings = QSettings("MikanSoft", "UniversalPacker")
        for lang_key, combo in self.packer_settings.items():
            settings.setValue(f"packer_{lang_key}", combo.currentData())
        settings.setValue("auto_detect", self.auto_detect_cb.isChecked())
        settings.setValue("auto_install", self.auto_install_cb.isChecked())
        if self.parent:
            self.parent.refresh_packer_list()
        QMessageBox.information(self, "🌸 保存成功", "设置已保存 🎉")
    
    def install_all_deps(self):
        reply = QMessageBox.question(self, "📦 安装依赖", 
            "将自动安装:\n• Python, Java, Rust, Go, PHP, Node.js 运行时\n• Git\n• 所有打包工具\n\n预计需要 5-20 分钟 ⏳",
            QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        
        progress_dialog = QDialog(self)
        progress_dialog.setWindowTitle("📦 安装中...")
        progress_dialog.setFixedSize(500, 300)
        progress_dialog.setWindowFlags(Qt.WindowCloseButtonHint)
        layout = QVBoxLayout(progress_dialog)
        layout.addWidget(QLabel("🌸 正在安装所有依赖..."))
        layout.addWidget(QLabel("请耐心等待，不要关闭窗口 ⏳"))
        log_text = QTextEdit()
        log_text.setReadOnly(True)
        log_text.setStyleSheet("QTextEdit { background: #1e1e1e; color: #d4d4d4; font-family: Consolas, monospace; font-size: 11px; border-radius: 8px; padding: 8px; }")
        layout.addWidget(log_text)
        progress_bar = QProgressBar()
        layout.addWidget(progress_bar)
        btn_close = QPushButton("关闭")
        btn_close.setEnabled(False)
        layout.addWidget(btn_close)
        
        def append_log(msg):
            log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
            scrollbar = log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        
        def install_thread():
            success = DependencyInstaller.install_all(append_log)
            progress_bar.setValue(100)
            btn_close.setEnabled(True)
            if success:
                append_log("\n🎉 所有依赖安装完成！")
            else:
                append_log("\n⚠️ 部分安装失败，请手动安装")
        
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()
        progress_dialog.exec()
    
    def open_language_download_dialog(self):
        dialog = LanguageDownloadDialog(self)
        dialog.exec()


# ============================================================
# 打包器管理器对话框
# ============================================================

class PackerManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📦 打包器管理器")
        self.setMinimumSize(750, 500)
        self.setStyleSheet("background: #ffffff;")
        self.setup_ui()
        self.refresh_status()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 16, 20, 16)
        
        title = QLabel("📦 打包器管理器")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #ff8a9b;")
        layout.addWidget(title)
        subtitle = QLabel("选择要安装的打包器 🌸")
        subtitle.setStyleSheet("color: #b8a9c9; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["安装", "语言", "打包器", "描述", "状态"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        btn_row = QHBoxLayout()
        select_all_btn = QPushButton("全选")
        select_all_btn.clicked.connect(self.select_all)
        btn_row.addWidget(select_all_btn)
        deselect_all_btn = QPushButton("取消全选")
        deselect_all_btn.clicked.connect(self.deselect_all)
        btn_row.addWidget(deselect_all_btn)
        btn_row.addStretch()
        install_btn = QPushButton("🚀 安装选中")
        install_btn.setObjectName("success-btn")
        install_btn.clicked.connect(self.install_selected)
        btn_row.addWidget(install_btn)
        refresh_btn = QPushButton("🔄 刷新状态")
        refresh_btn.clicked.connect(self.refresh_status)
        btn_row.addWidget(refresh_btn)
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setStyleSheet("QTextEdit { background: #1e1e1e; color: #d4d4d4; font-family: Consolas, monospace; font-size: 11px; border-radius: 8px; padding: 8px; }")
        self.log_text.setVisible(False)
        layout.addWidget(self.log_text)
    
    def refresh_status(self):
        self.table.setRowCount(0)
        for lang_key, config in LANGUAGE_CONFIGS.items():
            for packer in config.get("packers", []):
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                cb = QCheckBox()
                cb.setChecked(True)
                self.table.setCellWidget(row, 0, cb)
                self.table.setItem(row, 1, QTableWidgetItem(f"{config['icon']} {config['name']}"))
                name = packer["name"] + (" ⭐" if packer.get("recommended") else "")
                self.table.setItem(row, 2, QTableWidgetItem(name))
                self.table.setItem(row, 3, QTableWidgetItem(packer["desc"]))
                
                check_cmd = packer.get("check", [])
                installed, version = DependencyInstaller.check_packer_installed(packer["id"], check_cmd)
                status = f"✅ {version[:30]}" if installed else "❌ 未安装"
                status_item = QTableWidgetItem(status)
                status_item.setForeground(QColor(0, 150, 0) if installed else QColor(200, 50, 50))
                self.table.setItem(row, 4, status_item)
        
        self.table.resizeColumnsToContents()
    
    def select_all(self):
        for row in range(self.table.rowCount()):
            cb = self.table.cellWidget(row, 0)
            if cb:
                cb.setChecked(True)
    
    def deselect_all(self):
        for row in range(self.table.rowCount()):
            cb = self.table.cellWidget(row, 0)
            if cb:
                cb.setChecked(False)
    
    def install_selected(self):
        to_install = []
        for row in range(self.table.rowCount()):
            cb = self.table.cellWidget(row, 0)
            if cb and cb.isChecked():
                status_item = self.table.item(row, 4)
                if status_item and "已安装" in status_item.text():
                    continue
                lang_item = self.table.item(row, 1)
                name_item = self.table.item(row, 2)
                for lang_key, config in LANGUAGE_CONFIGS.items():
                    if lang_item and config["name"] in lang_item.text():
                        for packer in config.get("packers", []):
                            if packer["name"] in name_item.text():
                                to_install.append((lang_key, packer["id"], packer.get("install")))
                                break
                        break
        
        if not to_install:
            QMessageBox.information(self, "🌸", "没有需要安装的打包器 🎉")
            return
        
        msg = f"将安装 {len(to_install)} 个打包器:\n\n"
        for lang_key, packer_id, _ in to_install:
            msg += f"  • {LANGUAGE_CONFIGS[lang_key]['name']}: {packer_id}\n"
        
        reply = QMessageBox.question(self, "确认安装", msg + "\n继续?", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        
        self.log_text.setVisible(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        
        def append_log(msg):
            self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        
        def install_thread():
            total = len(to_install)
            for i, (lang_key, packer_id, install_config) in enumerate(to_install):
                self.progress_bar.setValue(int((i / total) * 100))
                append_log(f"📦 安装 {packer_id}...")
                if not install_config:
                    append_log(f"  ✅ {packer_id} 无需安装")
                    continue
                if isinstance(install_config, list) and install_config[0] == "download":
                    url = install_config[1]
                    dest = Path.home() / "Downloads" / Path(url).name
                    append_log(f"  下载: {url}")
                    if DependencyInstaller._download_file(url, dest, append_log):
                        append_log(f"  ✅ {packer_id} 下载完成")
                    else:
                        append_log(f"  ❌ {packer_id} 下载失败")
                elif isinstance(install_config, list):
                    try:
                        env = PathManager.build_env(lang_key, packer_id)
                        subprocess.run(install_config, env=env, check=True, capture_output=True, timeout=300)
                        append_log(f"  ✅ {packer_id} 安装完成")
                    except:
                        append_log(f"  ❌ {packer_id} 安装失败")
            
            self.progress_bar.setValue(100)
            append_log("\n🎉 安装完成！")
        
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()


# ============================================================
# 主窗口 (精简)
# ============================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌸 Mikan Packer")
        self.setMinimumSize(900, 700)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.file_list = []
        
        self.setup_ui()
        self.load_config()
        self.setup_menu()
        self.setStyleSheet(CUTE_STYLE + "QMainWindow { background: #ffffff; }")
    
    def setup_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("QMenuBar { background: transparent; color: #5a5a5a; padding: 4px 8px; } QMenuBar::item:selected { background: #ffe8eb; border-radius: 8px; }")
        
        tools_menu = menubar.addMenu("🌸 工具")
        packer_mgr_action = QAction("📦 打包器管理器", self)
        packer_mgr_action.triggered.connect(self.open_packer_manager)
        tools_menu.addAction(packer_mgr_action)
        install_deps_action = QAction("📦 一键安装所有依赖", self)
        install_deps_action.triggered.connect(self.install_all_deps)
        tools_menu.addAction(install_deps_action)
        tools_menu.addSeparator()
        lang_download_action = QAction("🌐 下载编程语言", self)
        lang_download_action.triggered.connect(self.open_language_download)
        tools_menu.addAction(lang_download_action)
        tools_menu.addSeparator()
        settings_action = QAction("⚙️ 设置", self)
        settings_action.triggered.connect(self.open_settings)
        tools_menu.addAction(settings_action)
        
        help_menu = menubar.addMenu("❓ 帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 18, 24, 18)
        
        title_layout = QHBoxLayout()
        title = QLabel("🌸 Mikan Packer")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: #ff8a9b; background: transparent;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        version = QLabel("v3.10")
        version.setStyleSheet("color: #b8a9c9; font-size: 13px; background: transparent;")
        title_layout.addWidget(version)
        layout.addLayout(title_layout)
        
        subtitle = QLabel("🌸 轻点一下，脚本变exe · 全打包器版本适配 · 混合模式(日志+终端)")
        subtitle.setStyleSheet("color: #b8a9c9; font-size: 13px; margin-bottom: 6px; background: transparent;")
        layout.addWidget(subtitle)
        
        group1 = QGroupBox("📁 待打包文件")
        g1_layout = QVBoxLayout(group1)
        toolbar = QHBoxLayout()
        add_files_btn = QPushButton("➕ 添加文件")
        add_files_btn.clicked.connect(self.add_files)
        add_folder_btn = QPushButton("📂 添加文件夹")
        add_folder_btn.clicked.connect(self.add_folder)
        clear_btn = QPushButton("🗑️ 清空列表")
        clear_btn.clicked.connect(self.clear_files)
        toolbar.addWidget(add_files_btn)
        toolbar.addWidget(add_folder_btn)
        toolbar.addWidget(clear_btn)
        toolbar.addStretch()
        self.file_count_label = QLabel("🌸 0 个文件")
        self.file_count_label.setStyleSheet("color: #b8a9c9;")
        toolbar.addWidget(self.file_count_label)
        g1_layout.addLayout(toolbar)
        
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(4)
        self.file_table.setHorizontalHeaderLabels(["📄 文件名", "📁 路径", "🌐 语言", "📊 状态"])
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.file_table.setAlternatingRowColors(True)
        self.file_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.file_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_table.customContextMenuRequested.connect(self.show_context_menu)
        g1_layout.addWidget(self.file_table)
        layout.addWidget(group1)
        
        group2 = QGroupBox("🎯 打包配置")
        g2_layout = QHBoxLayout(group2)
        g2_layout.setSpacing(10)
        g2_layout.addWidget(QLabel("🌐 语言:"))
        self.lang_combo = QComboBox()
        for key, config in LANGUAGE_CONFIGS.items():
            if config.get("packers"):
                self.lang_combo.addItem(f"{config['icon']} {config['name']}", key)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        g2_layout.addWidget(self.lang_combo)
        g2_layout.addWidget(QLabel("📦 打包器:"))
        self.packer_combo = QComboBox()
        g2_layout.addWidget(self.packer_combo)
        g2_layout.addWidget(QLabel("📂 输出:"))
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("默认: 文件所在目录/dist")
        self.output_edit.setFixedWidth(180)
        g2_layout.addWidget(self.output_edit)
        output_browse = QPushButton("📁")
        output_browse.setFixedWidth(40)
        output_browse.clicked.connect(lambda: self.browse_folder(self.output_edit))
        g2_layout.addWidget(output_browse)
        g2_layout.addWidget(QLabel("✏️ 自动输入:"))
        self.auto_input_edit = QLineEdit()
        self.auto_input_edit.setPlaceholderText("y/n")
        self.auto_input_edit.setText("y")
        self.auto_input_edit.setFixedWidth(50)
        g2_layout.addWidget(self.auto_input_edit)
        layout.addWidget(group2)
        
        group3 = QGroupBox("📋 打包日志")
        g3_layout = QVBoxLayout(group3)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(140)
        self.log_text.setStyleSheet("QTextEdit { background: #fcf8f5; border: 2px solid #f0e6d3; border-radius: 12px; padding: 10px; font-family: Consolas, monospace; font-size: 11px; color: #4a4a4a; }")
        g3_layout.addWidget(self.log_text)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        g3_layout.addWidget(self.progress_bar)
        layout.addWidget(group3)
        
        btn_row = QHBoxLayout()
        self.pack_btn = QPushButton("🚀 一键打包")
        self.pack_btn.setObjectName("primary-btn")
        self.pack_btn.clicked.connect(self.start_pack)
        self.status_label = QLabel("💡 添加文件后点击打包 ✨")
        self.status_label.setStyleSheet("color: #b8a9c9; padding: 5px;")
        btn_row.addWidget(self.pack_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.status_label)
        layout.addLayout(btn_row)
        
        self.on_language_changed(0)
    
    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            line_edit.setText(folder)
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择要打包的文件", "",
            "所有支持 (*.py *.pyw *.java *.rs *.go *.php *.js *.mjs *.ts *.cpp *.c);;Python (*.py);;Java (*.java);;Rust (*.rs);;Go (*.go);;PHP (*.php);;Node.js (*.js *.mjs *.ts);;C++ (*.cpp *.c)")
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
        self.update_file_list()
    
    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择项目文件夹")
        if not folder:
            return
        extensions = []
        for config in LANGUAGE_CONFIGS.values():
            extensions.extend(config.get("extensions", []))
        count = 0
        for ext in extensions:
            for f in Path(folder).rglob(f"*{ext}"):
                if str(f) not in self.file_list:
                    self.file_list.append(str(f))
                    count += 1
        self.update_file_list()
        self.log_text.append(f"🌸 从 {Path(folder).name} 添加了 {count} 个文件")
    
    def clear_files(self):
        self.file_list.clear()
        self.update_file_list()
        self.log_text.clear()
    
    def update_file_list(self):
        self.file_table.setRowCount(len(self.file_list))
        for i, file_path in enumerate(self.file_list):
            path = Path(file_path)
            self.file_table.setItem(i, 0, QTableWidgetItem(path.name))
            self.file_table.setItem(i, 1, QTableWidgetItem(str(path.parent)))
            lang = detect_language_by_extension(file_path)
            display = LANGUAGE_CONFIGS.get(lang, {}).get("name", "🤔")
            self.file_table.setItem(i, 2, QTableWidgetItem(display))
            self.file_table.setItem(i, 3, QTableWidgetItem("⏳ 待打包"))
        self.file_count_label.setText(f"🌸 {len(self.file_list)} 个文件")
        if self.file_list:
            self.auto_detect_language()
    
    def show_context_menu(self, pos):
        menu = QMenu()
        remove_action = QAction("🗑️ 移除选中", self)
        remove_action.triggered.connect(self.remove_selected)
        menu.addAction(remove_action)
        clear_action = QAction("🗑️ 清空全部", self)
        clear_action.triggered.connect(self.clear_files)
        menu.addAction(clear_action)
        menu.exec(self.file_table.viewport().mapToGlobal(pos))
    
    def remove_selected(self):
        selected_rows = set()
        for item in self.file_table.selectedItems():
            selected_rows.add(item.row())
        for row in sorted(selected_rows, reverse=True):
            if row < len(self.file_list):
                self.file_list.pop(row)
        self.update_file_list()
    
    def auto_detect_language(self):
        if not self.file_list:
            return
        lang_count = {}
        for f in self.file_list:
            lang = detect_language_by_extension(f)
            if lang and lang in LANGUAGE_CONFIGS:
                lang_count[lang] = lang_count.get(lang, 0) + 1
        if lang_count:
            most_common = max(lang_count, key=lang_count.get)
            for i in range(self.lang_combo.count()):
                if self.lang_combo.itemData(i) == most_common:
                    self.lang_combo.setCurrentIndex(i)
                    break
    
    def on_language_changed(self, index):
        lang_key = self.lang_combo.currentData()
        if not lang_key:
            return
        self.packer_combo.clear()
        packers = LANGUAGE_CONFIGS[lang_key].get("packers", [])
        settings = QSettings("MikanSoft", "UniversalPacker")
        default_id = settings.value(f"packer_{lang_key}", "")
        selected_index = 0
        for i, p in enumerate(packers):
            label = p["name"] + (" ⭐" if p.get("recommended") else "")
            self.packer_combo.addItem(label, p["id"])
            if p["id"] == default_id:
                selected_index = i
            elif p.get("recommended") and not default_id:
                selected_index = i
        self.packer_combo.setCurrentIndex(selected_index)
    
    def refresh_packer_list(self):
        self.on_language_changed(self.lang_combo.currentIndex())
    
    def open_packer_manager(self):
        dialog = PackerManagerDialog(self)
        dialog.exec()
    
    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
        self.settings_window.raise_()
    
    def open_language_download(self):
        dialog = LanguageDownloadDialog(self)
        dialog.exec()
    
    def install_all_deps(self):
        reply = QMessageBox.question(self, "📦 安装依赖",
            "🌸 将自动安装:\n• Python, Java, Rust, Go, PHP, Node.js 运行时\n• Git\n• 所有打包工具\n\n预计需要 5-20 分钟 ⏳",
            QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("📦 安装中...")
        dialog.setFixedSize(500, 350)
        dialog.setWindowFlags(Qt.WindowCloseButtonHint)
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("🌸 正在安装所有依赖..."))
        layout.addWidget(QLabel("请耐心等待 ~ 🍊"))
        log_text = QTextEdit()
        log_text.setReadOnly(True)
        log_text.setStyleSheet("QTextEdit { background: #1e1e1e; color: #d4d4d4; font-family: Consolas, monospace; font-size: 11px; border-radius: 8px; padding: 8px; }")
        layout.addWidget(log_text)
        progress_bar = QProgressBar()
        layout.addWidget(progress_bar)
        btn_close = QPushButton("关闭")
        btn_close.setEnabled(False)
        layout.addWidget(btn_close)
        
        def append_log(msg):
            log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
            scrollbar = log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        
        def install_thread():
            success = DependencyInstaller.install_all(append_log)
            progress_bar.setValue(100)
            btn_close.setEnabled(True)
            if success:
                append_log("\n🎉 所有依赖安装完成！")
            else:
                append_log("\n⚠️ 部分安装失败，请手动安装")
        
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()
        dialog.exec()
    
    def show_about(self):
        QMessageBox.about(self, "🌸 关于 Mikan Packer",
            "🌸 Mikan Packer v3.10\n\n轻轻一点，脚本变exe ✨\n\n"
            "支持: Python · Java · Rust · Go · PHP · Node.js · C++\n"
            "功能:\n"
            "  • 批量打包多个脚本\n"
            "  • 自动识别文件后缀\n"
            "  • 一键安装所有依赖\n"
            "  • 官网跳转下载编程语言\n"
            "  • 🆕 所有打包器新老版本自动适配\n"
            "  • 混合模式: 日志窗口 + 独立终端\n"
            "  • 纯白背景 · 可爱风\n\n© 2026 MikanSoft 🍊")
    
    def load_config(self):
        settings = QSettings("MikanSoft", "UniversalPacker")
        self.output_edit.setText(settings.value("output_path", ""))
        self.auto_input_edit.setText(settings.value("auto_input", "y"))
    
    def save_config(self):
        settings = QSettings("MikanSoft", "UniversalPacker")
        settings.setValue("output_path", self.output_edit.text())
        settings.setValue("auto_input", self.auto_input_edit.text())
    
    def start_pack(self):
        if not self.file_list:
            QMessageBox.warning(self, "🌸", "请先添加要打包的文件 📁")
            return
        
        lang_key = self.lang_combo.currentData()
        packer_id = self.packer_combo.currentData()
        if not packer_id:
            QMessageBox.warning(self, "🌸", "请选择打包器 📦")
            return        
        auto_input = self.auto_input_edit.text().strip() or "y"
        output_dir = self.output_edit.text().strip()
        if not output_dir:
            output_dir = str(Path(self.file_list[0]).parent / "dist")
            self.output_edit.setText(output_dir)
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        self.pack_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.status_label.setText("⏳ 正在打包...")
        
        for row in range(self.file_table.rowCount()):
            self.file_table.setItem(row, 3, QTableWidgetItem("⏳ 打包中..."))
        
        self.thread = PackThread(lang_key, packer_id, self.file_list, output_dir, auto_input)
        self.thread.log.connect(self.append_log)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.on_pack_finished)
        self.thread.start()
        self.save_config()
    
    def append_log(self, msg: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {msg}")
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        if "打包:" in msg and "[" in msg:
            import re
            match = re.search(r'打包:\s*([^\s]+)', msg)
            if match:
                filename = match.group(1)
                for row in range(self.file_table.rowCount()):
                    item = self.file_table.item(row, 0)
                    if item and item.text() == filename:
                        self.file_table.setItem(row, 3, QTableWidgetItem("⏳ 处理中..."))
        
        if "✅" in msg or "成功" in msg or "🎉" in msg:
            for row in range(self.file_table.rowCount()):
                item = self.file_table.item(row, 3)
                if item and item.text() == "⏳ 处理中...":
                    self.file_table.setItem(row, 3, QTableWidgetItem("✅ 成功"))
        
        if "❌" in msg or "失败" in msg:
            for row in range(self.file_table.rowCount()):
                item = self.file_table.item(row, 3)
                if item and item.text() == "⏳ 处理中...":
                    self.file_table.setItem(row, 3, QTableWidgetItem("❌ 失败"))
    
    def on_pack_finished(self, success: bool, results: list):
        self.pack_btn.setEnabled(True)
        self.progress_bar.setValue(100)
        
        if success:
            self.status_label.setText(f"🎉 打包完成！ {sum(1 for r in results if '成功' in r)}/{len(results)} 成功")
            self.log_text.append("\n🎉 打包完成！")
            for r in results:
                self.log_text.append(f"  {r}")
        else:
            self.status_label.setText("😢 打包失败，查看日志")
        
        for row in range(self.file_table.rowCount()):
            item = self.file_table.item(row, 3)
            if item and item.text() == "⏳ 处理中...":
                self.file_table.setItem(row, 3, QTableWidgetItem("⚠️ 未完成"))


# ============================================================
# 入口
# ============================================================

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Mikan Packer")
    app.setOrganizationName("MikanSoft")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()