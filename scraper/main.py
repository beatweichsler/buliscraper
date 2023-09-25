import requests
from lxml import html, etree

response = requests.get('https://www.bundesliga.com/de/bundesliga/spieltag/2023-2024/1')

tree = html.fromstring(response.content)

home_name = tree.xpath('//*[@id="fixtures"]/fixturescomponent/div/div[1]/a/match-fixture/match-team[1]/div/div')
home_score = tree.xpath('//*[@id="fixtures"]/fixturescomponent/div/div[1]/a/match-fixture/score-bug/div/div[1]/div[2]')

away_score = tree.xpath('//*[@id="fixtures"]/fixturescomponent/div/div[1]/a/match-fixture/score-bug/div/div[2]/div[2]')
away_name = tree.xpath('//*[@id="fixtures"]/fixturescomponent/div/div[1]/a/match-fixture/match-team[2]/div/div')

print(home_name[0].text_content(), home_score[0].text_content(), ":", away_score[0].text_content(), away_name[0].text_content())
