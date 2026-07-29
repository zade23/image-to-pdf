"""Streamlit interface for JPG/PNG to PDF conversion."""

from __future__ import annotations

from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import streamlit as st

from converter import ConversionError, image_bytes_to_pdf, pdf_filename

st.set_page_config(
    page_title="图片转 PDF",
    page_icon="🖼️",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        --accent: #6750e8;
        --text: #202334;
        --muted: #6b7280;
        --surface: rgba(255, 255, 255, .92);
        --border: rgba(32, 35, 52, .09);
    }
    .stApp {
        background:
          radial-gradient(circle at 50% -10%, rgba(103, 80, 232, .14), transparent 34rem),
          #f7f8fc;
        color: var(--text);
    }
    .block-container {
        width: min(100%, 720px);
        padding: 4rem 1.5rem 2.5rem;
        margin: 0 auto;
    }
    .hero {
        max-width: 620px;
        margin: 0 auto 1.5rem;
        text-align: center;
    }
    .hero-icon {
        display: grid;
        width: 3.25rem;
        height: 3.25rem;
        margin: 0 auto 1rem;
        place-items: center;
        border-radius: 16px;
        background: linear-gradient(145deg, #7965f1, #5942d4);
        box-shadow: 0 10px 24px rgba(89, 66, 212, .2);
        color: white;
        font-size: .78rem;
        font-weight: 750;
        letter-spacing: .02em;
    }
    .hero h1 {
        margin: 0;
        font-size: clamp(2rem, 5vw, 2.6rem);
        letter-spacing: -.045em;
        line-height: 1.15;
    }
    .hero p {
        max-width: 520px;
        margin: .75rem auto 0;
        color: var(--muted);
        line-height: 1.7;
    }
    [data-testid="stFileUploader"] {
        padding: .75rem;
        border-radius: 20px;
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: 0 16px 44px rgba(35, 30, 90, .07);
    }
    [data-testid="stFileUploader"] [data-testid="stWidgetLabel"] {
        justify-content: center;
        gap: .25rem;
        text-align: center;
    }
    [data-testid="stFileUploaderDropzone"] {
        min-height: 12rem;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: .75rem;
        border-radius: 14px;
        border-color: rgba(103, 80, 232, .24);
        background: rgba(103, 80, 232, .025);
    }
    [data-testid="stFileUploaderDropzone"] > div {
        text-align: center;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] {
        text-align: center;
    }
    [data-testid="stAlert"] {
        border-radius: 14px;
    }
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    .stDownloadButton button, .stButton button {
        border-radius: 12px;
        font-weight: 600;
    }
    .stDownloadButton button[kind="primary"] {
        min-height: 3rem;
    }
    .download-heading {
        margin: 1.75rem 0 .5rem;
        text-align: center;
        color: var(--text);
        font-size: 1rem;
        font-weight: 650;
    }
    .footer-note {
        margin-top: 2.25rem;
        text-align: center;
        color: var(--muted);
        font-size: .82rem;
    }
    @media (max-width: 640px) {
        .block-container { padding: 2.5rem 1rem 2rem; }
        [data-testid="stFileUploaderDropzone"] { min-height: 10rem; }
    }
    </style>
    <div class="hero">
      <div class="hero-icon">PDF</div>
      <h1>图片转 PDF</h1>
      <p>上传 JPG 或 PNG 图片，自动转换为独立 PDF。文件名保持不变，转换完成即可下载。</p>
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

        st.markdown('<div class="download-heading">下载文件</div>', unsafe_allow_html=True)
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

st.markdown(
    '<div class="footer-note">图片仅在当前运行环境中处理，不会由本工具主动上传到第三方服务。</div>',
    unsafe_allow_html=True,
)
