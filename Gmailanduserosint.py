import requests

username = input("Enter username: ")
results = []

sites = {

"GitHub":"https://github.com/{}",
"GitLab":"https://gitlab.com/{}",
"Bitbucket":"https://bitbucket.org/{}",
"Reddit":"https://www.reddit.com/user/{}",
"Pinterest":"https://www.pinterest.com/{}/",
"TikTok":"https://www.tiktok.com/@{}",
"Instagram":"https://www.instagram.com/{}/",
"Facebook":"https://www.facebook.com/{}",
"Twitter":"https://twitter.com/{}",
"Snapchat":"https://www.snapchat.com/add/{}",
"Twitch":"https://www.twitch.tv/{}",
"YouTube":"https://www.youtube.com/@{}",
"Spotify":"https://open.spotify.com/user/{}",
"SoundCloud":"https://soundcloud.com/{}",
"Medium":"https://medium.com/@{}",
"DevTo":"https://dev.to/{}",
"CodePen":"https://codepen.io/{}",
"Replit":"https://replit.com/@{}",
"Kaggle":"https://www.kaggle.com/{}",
"Steam":"https://steamcommunity.com/id/{}",
"Vimeo":"https://vimeo.com/{}",
"AboutMe":"https://about.me/{}",
"Disqus":"https://disqus.com/by/{}/",
"Imgur":"https://imgur.com/user/{}",
"TripAdvisor":"https://www.tripadvisor.com/members/{}",
"ProductHunt":"https://www.producthunt.com/@{}",
"Dribbble":"https://dribbble.com/{}",
"Behance":"https://www.behance.net/{}",
"Flickr":"https://www.flickr.com/people/{}",
"Patreon":"https://www.patreon.com/{}",
"Goodreads":"https://www.goodreads.com/{}",
"Keybase":"https://keybase.io/{}",
"HackerRank":"https://www.hackerrank.com/{}",
"LeetCode":"https://leetcode.com/{}",
"StackOverflow":"https://stackoverflow.com/users/{}",
"AngelList":"https://angel.co/u/{}",
"Crunchbase":"https://www.crunchbase.com/person/{}",
"500px":"https://500px.com/{}",
"Bandcamp":"https://bandcamp.com/{}",
"Codecademy":"https://www.codecademy.com/profiles/{}",
"Gravatar":"https://en.gravatar.com/{}",
"Gumroad":"https://gumroad.com/{}",
"IFTTT":"https://ifttt.com/p/{}",
"Instructables":"https://www.instructables.com/member/{}",
"LastFM":"https://www.last.fm/user/{}",
"Pastebin":"https://pastebin.com/u/{}",
"Slideshare":"https://www.slideshare.net/{}",
"Wattpad":"https://www.wattpad.com/user/{}",
"WordPress":"https://{}.wordpress.com",
"LiveJournal":"https://{}.livejournal.com",
"VK":"https://vk.com/{}",
"WeHeartIt":"https://weheartit.com/{}",
"TradingView":"https://www.tradingview.com/u/{}",
"Scratch":"https://scratch.mit.edu/users/{}",
"Chess":"https://www.chess.com/member/{}",
"DeviantArt":"https://www.deviantart.com/{}",
"Archive":"https://archive.org/details/@{}",
"Thingiverse":"https://www.thingiverse.com/{}",
"Unsplash":"https://unsplash.com/@{}",
"Linktree":"https://linktr.ee/{}",
"Carrd":"https://{}.carrd.co",
"Hashnode":"https://hashnode.com/@{}",
"Polywork":"https://www.polywork.com/{}",
"ResearchGate":"https://www.researchgate.net/profile/{}",
"Academia":"https://independent.academia.edu/{}",
"Codewars":"https://www.codewars.com/users/{}",
"PyPI":"https://pypi.org/user/{}",
"NPM":"https://www.npmjs.com/~{}",
"DockerHub":"https://hub.docker.com/u/{}",
"Freelancer":"https://www.freelancer.com/u/{}",
"Fiverr":"https://www.fiverr.com/{}",
"Upwork":"https://www.upwork.com/freelancers/~{}",

# extra community sites
"OpenSea":"https://opensea.io/{}",
"Trakt":"https://trakt.tv/users/{}",
"Letterboxd":"https://letterboxd.com/{}",
"BuyMeACoffee":"https://www.buymeacoffee.com/{}",
"KoFi":"https://ko-fi.com/{}",
"Substack":"https://{}.substack.com",
"Mix":"https://mix.com/{}",
"Rumble":"https://rumble.com/user/{}",
"Odysee":"https://odysee.com/@{}",
"PeerTube":"https://peertube.social/accounts/{}",
"Roblox":"https://www.roblox.com/user.aspx?username={}",
"Xbox":"https://xboxgamertag.com/search/{}",
"PlayStation":"https://psnprofiles.com/{}",
"Speedrun":"https://www.speedrun.com/user/{}",
"GameJolt":"https://gamejolt.com/@{}",
"Deezer":"https://www.deezer.com/profile/{}",
"Trello":"https://trello.com/{}",
"Canva":"https://www.canva.com/{}",
"Notion":"https://www.notion.so/{}",
"ProductHunt2":"https://www.producthunt.com/@{}",
"DailyMotion":"https://www.dailymotion.com/{}"
}

print("\nSearching username...\n")

for site,url in sites.items():

    link = url.format(username)

    try:
        r = requests.get(link,timeout=5)

        if r.status_code == 200:
            print("[FOUND]",site,link)
            results.append(link)

    except:
        pass


# EMAIL OSINT (Public Search)
email = input("\nEnter email for OSINT search: ")

email_links = [
"https://www.google.com/search?q=" + email,
"https://duckduckgo.com/?q=" + email,
"https://haveibeenpwned.com/account/" + email,
"https://hunter.io/search/" + email,
"https://intelx.io/?s=" + email
]

print("\nEmail OSINT Links:\n")

for l in email_links:
    print(l)
