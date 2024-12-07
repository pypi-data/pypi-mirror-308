import os
import re
import asyncio
from pathlib import Path

# @hint: fnet-sitemapper (channel=pypi)
from fnet_sitemapper import default as fetch_sitemap

# @hint: pyppeteer (channel=pypi)
from pyppeteer import launch

# @hint: pypdf (channel=pypi)
from pypdf import PdfReader, PdfWriter


async def crawl_and_generate_pdfs(
    sitemap_url,
    output_directory,
    bundle=True,
    output_file="output",
    bundle_size=float("inf"),
    limit=float("inf"),
):
    print("Fetching sitemap URLs...")
    sitemap_data = fetch_sitemap(url=sitemap_url)
    urls = sitemap_data["sites"][: int(limit)]
    print(f"Found {len(urls)} URLs to process.")

    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({"width": 1920, "height": 1080})
    await page.emulateMedia("screen")

    temp_pdf_paths = []
    failed_urls = []

    try:
        for idx, url in enumerate(urls):
            sanitized_filename = re.sub(r"[^\w]", "_", url) + ".pdf"
            temp_pdf_path = output_dir / sanitized_filename

            if temp_pdf_path.exists():
                print(f"Skipping ({idx + 1}/{len(urls)}): {url} (already exists)")
                temp_pdf_paths.append(temp_pdf_path)
                continue

            try:
                print(f"Processing ({idx + 1}/{len(urls)}): {url}")
                await page.goto(url, {"waitUntil": "networkidle2"})
                await page.pdf({"path": str(temp_pdf_path), "format": "A4", "printBackground": True})
                temp_pdf_paths.append(temp_pdf_path)
                print(f"Saved PDF: {temp_pdf_path}")
            except Exception as e:
                print(f"Failed to process {url}: {e}")
                failed_urls.append(url)

        if bundle:
            print("Combining PDFs...")
            combine_pdfs_with_size_limit(temp_pdf_paths, output_dir, output_file, bundle_size)
    finally:
        await browser.close()

    if failed_urls:
        print("The following URLs failed to process:")
        print(failed_urls)


def combine_pdfs_with_size_limit(pdf_paths, output_directory, base_output_file_name, max_size_mb):
    current_writer = PdfWriter()
    current_bundle_size = 0
    bundle_index = 1

    def save_current_bundle():
        nonlocal current_writer, current_bundle_size, bundle_index
        if len(current_writer.pages) > 0:
            output_path = output_directory / f"{base_output_file_name}-{str(bundle_index).zfill(3)}.pdf"
            with open(output_path, "wb") as f:
                current_writer.write(f)
            print(f"Saved bundle: {output_path}")
            bundle_index += 1
            current_writer = PdfWriter()
            current_bundle_size = 0

    for pdf_path in pdf_paths:
        pdf_reader = PdfReader(str(pdf_path))
        for page in pdf_reader.pages:
            current_writer.add_page(page)

        pdf_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        current_bundle_size += pdf_size_mb

        if current_bundle_size >= max_size_mb:
            save_current_bundle()

    # Finalize the last bundle
    save_current_bundle()


if __name__ == "__main__":
    asyncio.run(
        crawl_and_generate_pdfs(
            sitemap_url="https://www.gry.pl/sitemap.xml",
            output_directory="./.temp/gry_pl",
            bundle=True,
            output_file="output",
            bundle_size=50,  # Maximum bundle size in MB
            limit=100,  # Limit the number of URLs processed
        )
    )