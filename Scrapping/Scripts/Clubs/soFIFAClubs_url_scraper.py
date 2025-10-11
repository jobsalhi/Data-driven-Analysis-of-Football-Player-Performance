import csv
import asyncio
from playwright.async_api import async_playwright
import os

class ClubURLScraper:
    def __init__(self, base_url="https://sofifa.com/teams?type=club&col=rating&sort=desc"):
        self.base_url = base_url
        self.all_club_urls = []
        self.offset = 0
        self.page_size = 60
        self.max_offset = 660  # Last valid page

    async def scrape_all_club_urls(self):
        """Scrape all club URLs from paginated team list"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ],
            )

            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
                timezone_id="America/New_York",
            )

            page = await context.new_page()

            # Block unnecessary resources
            await page.route(
                "**/*",
                lambda route: (
                    route.abort()
                    if route.request.resource_type
                    in ["image", "font", "stylesheet", "media"]
                    else route.continue_()
                ),
            )

            page_num = 1

            while self.offset <= self.max_offset:
                url = (
                    f"{self.base_url}&offset={self.offset}"
                    if self.offset > 0
                    else self.base_url
                )
                print(f"\n[Page {page_num}] Scraping: {url}")

                # Retry logic
                for attempt in range(2):
                    try:
                        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                        break
                    except Exception:
                        if attempt == 0:
                            print(f"⚠️ Timeout on {url}, retrying in 5s...")
                            await asyncio.sleep(5)
                        else:
                            print(f"❌ Skipping {url} after multiple timeouts.")
                            continue

                await page.wait_for_timeout(2000)

                # ✅ Extract only real team URLs inside the main table
                club_urls = await page.evaluate(
                    """
                    () => {
                        const urls = [];
                        const rows = document.querySelectorAll('table tbody tr');
                        rows.forEach(row => {
                            const link = row.querySelector('a[href^="/team/"]:not([href*="random"])');
                            if (link) {
                                const href = link.href;
                                if (!urls.includes(href)) {
                                    urls.push(href);
                                }
                            }
                        });
                        return urls;
                    }
                    """
                )

                print(f"  ✓ Extracted {len(club_urls)} clubs")
                self.all_club_urls.extend(club_urls)
                self.save_urls_to_csv()

                self.offset += self.page_size
                page_num += 1

            await browser.close()

        print(f"\n✅ Total unique clubs scraped: {len(set(self.all_club_urls))}")
        return self.all_club_urls



    def save_urls_to_csv(self, filename=None):
        """Save all club URLs to CSV inside Scrapping/Data/Clubs/"""
        # Root = project folder
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(root_dir, "Data", "Clubs")
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, "club_urls.csv")

        unique_urls = list(dict.fromkeys(self.all_club_urls))
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["club_url"])
            for url in unique_urls:
                writer.writerow([url])
        print(f"  💾 Saved {len(unique_urls)} unique club URLs to {filename}")





async def main():
    scraper = ClubURLScraper()
    print("=" * 60)
    print("SoFIFA Club URL Scraper (Clubs Only)")
    print("=" * 60)
    await scraper.scrape_all_club_urls()
    print("\n✅ Completed club URL scraping")


if __name__ == "__main__":
    asyncio.run(main())
