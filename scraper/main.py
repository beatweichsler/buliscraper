import scraper

games = scraper.scrape_games()

standings = scraper.calculate_standings(games)

print(standings)