import asyncio
from soFIFAClubs_url_scraper import ClubURLScraper
from soFIFAClubs_scraper import SoFIFAClubScraper


async def main():
    print("=" * 60)
    print("⚽ SoFIFA Clubs Full Scraper")
    print("=" * 60)

    # Step 1: Scrape club URLs
    print("\nSTEP 1️⃣: Scraping all club URLs...")
    url_scraper = ClubURLScraper()
    await url_scraper.scrape_all_club_urls()
    print("✅ Club URLs scraping done.\n")

    # Step 2: Scrape club stats
    print("STEP 2️⃣: Scraping club statistics...")
    club_scraper = SoFIFAClubScraper()
    club_scraper.load_urls()
    await club_scraper.scrape_all_clubs()
    print("✅ Club stats scraping done.\n")

    print("=" * 60)
    print("🎉 ALL DONE — CSV files are ready!")
    print("=" * 60)
    print("➡ club_urls.csv and club_stats.csv saved in: Scrapping/Data/Clubs/")


if __name__ == "__main__":
    asyncio.run(main())
