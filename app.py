"""Streamlit interface for JPG/PNG to PDF conversion."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import streamlit as st

from converter import ConversionError, image_bytes_to_pdf, pdf_filename, safe_output_path

st.set_page_config(
    page_title="图片转 PDF",
    page_icon="🖼️",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
          radial-gradient(circle at 15% 0%, rgba(112, 86, 255, .12), transparent 32rem),
          #f8f9fc;
    }
    .block-container { max-width: 780px; padding-top: 3rem; }
    .hero {
        padding: 1.8rem 2rem;
        border: 1px solid rgba(20, 24, 40, .08);
        border-radius: 24px;
        background: rgba(255, 255, 255, .9);
        box-shadow: 0 18px 55px rgba(35, 30, 90, .08);
        margin-bottom: 1.25rem;
    }
    .hero h1 { margin: 0; font-size: 2.1rem; letter-spacing: -.04em; }
    .hero p { color: #667085; margin: .6rem 0 0; }
    [data-testid="stFileUploader"] {
        padding: .8rem;
        border-radius: 18px;
        background: white;
        border: 1px solid rgba(20, 24, 40, .08);
    }
    .stDownloadButton button, .stButton button {
        border-radius: 12px;
        font-weight: 600;
    }
    </style>
    <div class="hero">
      <h1>图片转 PDF</h1>
      <p>上传 JPG 或 PNG，保留文件名前缀，一键转换和下载。</p>
    </div>
    """,
    unsafe_allow_html=True,
)

uploads = st.file_uploader(
    "拖拽图片到这里",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    help="支持同时选择多张图片；每张图片会生成一个独立 PDF。",
)

with st.expander("保存到本机指定目录（可选）"):
    st.caption("适用于在自己电脑上运行本工具。留空时可直接使用下方下载按钮。")
    output_directory = st.text_input(
        "输出目录",
        placeholder="例如：D:\\PDF 或 /Users/me/Documents/PDF",
    ).strip()

if uploads:
    converted: list[tuple[str, bytes]] = []
    failures: list[str] = []

    with st.spinner("正在转换…"):
        for upload in uploads:
            try:
                converted.append(
                    (pdf_filename(upload.name), image_bytes_to_pdf(upload.getvalue()))
                )
            except ConversionError as exc:
                failures.append(f"{upload.name}：{exc}")

    if failures:
        st.warning("以下文件未能转换：\n\n" + "\n\n".join(failures))

    if converted:
        st.success(f"已成功转换 {len(converted)} 个文件")

        if output_directory and st.button("保存全部到指定目录", type="primary"):
            target = Path(output_directory).expanduser()
            try:
                target.mkdir(parents=True, exist_ok=True)
                for name, pdf_data in converted:
                    safe_output_path(target, name).write_bytes(pdf_data)
                st.success(f"已保存到：{target.resolve()}")
            except OSError as exc:
                st.error(f"保存失败，请检查目录和权限：{exc}")

        st.markdown("#### 下载文件")
        for index, (name, pdf_data) in enumerate(converted):
            left, right = st.columns([3, 1])
            left.write(f"📄 {name}")
            right.download_button(
                "下载",
                data=pdf_data,
                file_name=name,
                mime="application/pdf",
                key=f"download-{index}-{name}",
                use_container_width=True,
            )

        if len(converted) > 1:
            archive = BytesIO()
            with ZipFile(archive, "w", ZIP_DEFLATED) as zip_file:
                for name, pdf_data in converted:
                    zip_file.writestr(name, pdf_data)
            st.download_button(
                "下载全部（ZIP）",
                data=archive.getvalue(),
                file_name="converted_pdfs.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True,
            )
else:
    st.info("选择图片后，转换会自动开始。")

st.caption("图片仅在当前运行环境中处理，不会由本工具主动上传到第三方服务。")
