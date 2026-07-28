# 图片转 PDF

一个简洁的 Streamlit 图片转换工具：批量上传 JPG/PNG，生成保持原文件名前缀的独立 PDF。

## 功能

- 拖拽或批量选择 JPG、JPEG、PNG
- 自动修正照片方向
- 透明 PNG 自动铺白底
- 单独下载 PDF 或批量下载 ZIP
- 本地运行时可直接保存到指定目录
- 使用 `uv` 管理 Python 和依赖

## 开始使用

安装 [uv](https://docs.astral.sh/uv/) 后，在项目目录运行：

```bash
uv sync
uv run streamlit run app.py
```

浏览器通常会自动打开 `http://localhost:8501`。

## 测试

```bash
uv run pytest
```
