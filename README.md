# 图片转 PDF

一个简洁的 Streamlit 图片转换工具：批量上传 JPG/PNG，生成保持原文件名前缀的独立 PDF。

## 功能

- 拖拽或批量选择 JPG、JPEG、PNG
- 自动修正照片方向
- 透明 PNG 自动铺白底
- 单独下载 PDF 或批量下载 ZIP
- 使用 `uv` 管理 Python 和依赖

## 开始使用

安装 [uv](https://docs.astral.sh/uv/) 后，在项目目录运行：

```bash
uv sync
uv run streamlit run app.py
```

浏览器通常会自动打开 `http://localhost:8501`。

## Windows 桌面启动

双击项目中的 `start-windows.cmd` 即可启动，浏览器会自动打开。优先使用已有的 `.venv`；环境未准备好时会通过 `uv sync --locked` 安装依赖，因此首次使用需要安装 uv 并联网。

要添加桌面快捷方式，在项目目录执行一次：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-desktop-shortcut.ps1
```

以后直接双击桌面的 **图片转 PDF** 即可，无需进入项目目录。启动窗口默认最小化到任务栏，使用期间请保留；关闭该窗口即可停止服务。仅关闭浏览器不会停止服务。若启动失败，窗口会保留错误信息，可从任务栏打开查看。

快捷方式依赖此项目目录；移动项目后，重新运行安装脚本即可更新。

## 测试

```bash
uv run pytest
```
