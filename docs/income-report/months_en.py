"""月次記事の英語版（generate_articles.py の MONTHS と ym で対応させる）

- highlights は (name, desc) の並び。金額は日本語側の値をそのまま使う。
  日本語の金額に「弱」などの日本語が入るときだけ (name, amount, desc) で上書きする
- 数字・固有名詞・事実は日本語版と同じにする。足さない、削らない
- アプリ名は App Store の英語名（US ストア）を使う
"""

MONTHS_EN = {
    "2025-11": {
        "desc": "The first issue of a revenue report series by an indie developer aiming for ¥10M a month. November 2025 revenue was ¥38,050. I look at the AdMob and App Store breakdown and decide my next moves.",
        "highlights": [
            ("TravelMemoryMap", "¥12,415 from ads and ¥13,332 from the Supporter Plan. This one app earned 68% of all revenue. An eCPM of ¥728 isn't bad."),
            ("Floating Notepad", "¥5,013 from ads and ¥2,295 from subscriptions. My flagship app, with ¥1.46 million earned in total, is now running at about ¥5,000 a month."),
            ("Everything else", "Just under ¥5,000", "One one-time purchase of Fuchidori!, 12 weekly plans of Swipon, and small bits of ad revenue. Only a handful of my apps actually make money so far."),
        ],
        "analysis": """
<p>The number for the first issue: ¥38,050 for the month. That's after putting more than 50 apps on the App Store. This table is exactly why I call myself an indie developer at his limit.</p>
<p>In the breakdown, TravelMemoryMap accounts for 68% of revenue. Its ad eCPM of ¥728 isn't bad. The real problem is that only a few of my apps have any way to make money built in at all. And 1,253 downloads a month just isn't enough volume.</p>
<p>Flip that around and there's room to grow everywhere. From here on, I'll face the numbers every month and make my next move.</p>
""",
        "next_actions": [
            "Strengthen the path to TravelMemoryMap's Supporter Plan, pushing the 1-year plan",
            "Add ads or subscriptions, one app at a time, to the apps that have no monetization",
            "Rework TravelMemoryMap's ASO ahead of the year-end look-back season",
        ],
        "closing": "First, ¥100,000 a month. I'm starting by getting past 1% of the goal.",
    },
    "2025-12": {
        "desc": "December 2025 revenue was ¥81,754, more than double the previous month. TravelMemoryMap's downloads quadrupled with year-end demand, and subscriptions followed right along.",
        "highlights": [
            ("TravelMemoryMap", "Downloads rose 4.2x from last month to 3,826. The 1-year Supporter Plan sold 32 times, bringing subscriptions alone to ¥54,532. Ads made ¥13,284."),
            ("Floating Notepad", "¥3,003 in subscriptions and ¥4,471 in ads. It holds up the base every month without fail."),
            ("Swipon", "A photo cleanup app. Maybe more people want to free up storage at the end of the year, because the Premium plan started moving a little."),
        ],
        "analysis": """
<p>¥81,754. That's 2.1x last month, and the first time I've reached the ¥80,000 range.</p>
<p>The reason is clear. TravelMemoryMap downloads went from 903 to 3,826. The end of the year is when people want to look back on the year's trips, and that suits this app well. Subscriptions followed the extra downloads in step. The biggest piece was 32 sales of the 1-year Supporter Plan, a contract that pays a full year's revenue up front.</p>
<p>AdMob, on the other hand, was flat at ¥20,777. Ad revenue depends on whether an app gets opened every day, so for a utility app this is what happens even when downloads grow.</p>
""",
        "next_actions": [
            "New Year's should bring in new users too, so I won't let up in January",
            "Try one-time purchase plans in my English-market apps, for people who dislike subscriptions",
            "Prepare UNCHIKUN for overseas markets",
        ],
        "closing": "More downloads mean more subscriptions. Next is building the system that captures all of them.",
    },
    "2026-01": {
        "desc": "January 2026 revenue was ¥94,209. Google Play made its first sale, ¥102, and one-time purchase plans started selling in English-speaking markets.",
        "highlights": [
            ("TravelMemoryMap", "Downloads grew again, to 5,228. ¥44,488 from subscriptions and ¥15,624 from ads. And the Android version made its first Google Play sale: ¥102."),
            ("Medicine Reminder", "The English version of my medicine reminder. Its one-time purchase plan sold 3 times overseas. The price is high, so even a few sales count."),
            ("ShellLens and FocusDrive", "Annual plans in my English-market apps started selling here and there."),
        ],
        "analysis": """
<p>¥94,209, up 15.2% from last month. Almost at ¥100,000.</p>
<p>Two things happened this month. One was Google Play's first sale, ¥102. Small as it is, my revenue had been standing on iOS alone, and now it has a second leg in Android.</p>
<p>The other is that the one-time purchase plans I set up last month started moving in English-speaking markets. Medicine Reminder sold 3, for ¥13,272. There are definitely users who are tired of subscriptions, and abroad, a one-time purchase lands well. This lesson pays off later.</p>
<p>Revenue starting to spread across five apps is a good sign, too.</p>
""",
        "next_actions": [
            "Add a first-time-only one-time offer on the annual plan to UNCHIKUN",
            "Move forward with monetizing UNCHIKUN for Android",
            "Expand one-time purchase plans to my other English-market apps",
        ],
        "closing": "That ¥102 from the Play Store is probably a sale I'll never forget.",
    },
    "2026-02": {
        "desc": "February 2026 revenue was ¥215,002, 2.3x the previous month. UNCHIKUN jumped to nearly 20,000 downloads a month, and its annual one-time offer converted 54 times.",
        "highlights": [
            ("UNCHIKUN", "Downloads jumped to 19,504 for the month. The annual one-time offer sold 54 times for ¥44,982, and ads brought in ¥43,932. It became the mainstay overnight."),
            ("TravelMemoryMap", "Subscriptions hit an all-time high of ¥68,016. Together with ads, it holds up one of the two main pillars."),
            ("Floating Notepad", "¥10,577 in ads and ¥6,929 in subscriptions. A quietly effective third pillar."),
        ],
        "analysis": """
<p>¥215,002. That's 2.3x last month, and the first time over ¥200,000. Goal progress passed 2% as well.</p>
<p>The star is UNCHIKUN, no question. Downloads jumped overseas to nearly 20,000 a month. On top of that, the annual one-time offer I built from last month's NextAction converted 54 times. It's an app people log in every day, so ad revenue grows at the same time. Exploding downloads, a first-time-only offer, an app opened daily. When all three line up, this is what you get.</p>
<p>What's interesting is UNCHIKUN's high eCPM of ¥504. That's because most of its users were still in Japan at this point. As the global share rises after this, eCPM goes down. The total still grows.</p>
""",
        "next_actions": [
            "Add more ad placements to UNCHIKUN. The screen after a log is saved is a candidate",
            "Optimize the AdMob setup for UNCHIKUN on Android",
            "Set up a new app aimed at going viral",
        ],
        "closing": "The things I set up come back as numbers. That's what makes this series worth doing.",
    },
    "2026-03": {
        "desc": "In March 2026 my monthly revenue passed ¥1 million. The breakdown of ¥1,050,092, and how Oshi Island's one-time purchase plan sold 217 copies.",
        "highlights": [
            ("Oshi Island", "A huge viral hit with 36,700 downloads. The one-time purchase plan at about ¥3,000 sold 217 copies for ¥547,103. The weekly plan moved 1,281 times as well. Over ¥600,000 in a single month."),
            ("UNCHIKUN", "¥61,633 from the App Store, ¥134,126 from ads and ¥3,332 from Play. 20,145 downloads, and still growing."),
            ("Posture Reminder: Cat Coach", "32 one-time purchases for ¥81,056. Oshi Island's buzz spilled over to its sister app."),
            ("TravelMemoryMap", "¥69,786 in subscriptions. Even in a month where nothing happens, it now brings in ¥80,000."),
        ],
        "analysis": """
<p>¥1,050,092. My monthly revenue went over ¥1 million. For a moment, I reached a tenth of the way to ¥10 million.</p>
<p>The hero was Oshi Island. It went viral on social media, downloads jumped to 36,700, and the one-time purchase plan at about ¥3,000 sold 217 copies. The strength of a one-time purchase is that it turns the heat of a viral moment into cash on the spot. With a subscription, only the first month of that excitement would come in. Here it comes in all at once.</p>
<p>AdMob also hit a record at ¥205,320. But looking at it calmly, ¥550,000 of this month is a firework called a viral hit. Fireworks always fade. Next month's numbers will tell me what's left after this one does.</p>
""",
        "next_actions": [
            "To brace for the drop, keep giving Oshi Island's weekly plan a reason to stay subscribed",
            "Keep growing UNCHIKUN as stock revenue that doesn't rely on going viral",
            "Ad volume has grown, so review AdMob eCPM by format",
        ],
        "closing": "¥1 million is just a stop along the way. But I want to remember this view.",
    },
    "2026-04": {
        "desc": "April 2026 revenue was ¥359,991. It fell after the viral spike, but UNCHIKUN grew into a ¥170,000-a-month pillar. A month that made the difference between fireworks and stock obvious.",
        "highlights": [
            ("UNCHIKUN", "¥86,099 from the App Store, ¥86,231 from ads and ¥1,785 from Play. 31,645 downloads. The regular annual plan also sold ¥32,805, making it a ¥170,000-a-month pillar on its own."),
            ("TravelMemoryMap", "¥63,802 in subscriptions plus ads and Play. Rock solid."),
            ("Oshi Island", "One-time purchases fell to 3, but 299 weekly plans remained. What the viral hit left behind."),
        ],
        "analysis": """
<p>¥359,991. Down 65.7% from March's ¥1 million, but I had already priced in that drop. Compared with February, before the viral hit, it's up 67%, so the baseline has definitely risen.</p>
<p>What became clear this month is the difference between fireworks and stock. Oshi Island's one-time purchases went from 217 to 3. Meanwhile, 299 weekly plans stayed on as recurring revenue. The move I wrote about last month, keeping the value of the recurring plan, is working.</p>
<p>And UNCHIKUN grew into a ¥170,000-a-month pillar. It stacks up 30,000 downloads a month without relying on virality and earns from subscriptions and ads together. That's the ideal shape.</p>
""",
        "next_actions": [
            "Add AI features to UNCHIKUN to raise revenue per user and retention",
            "Add more paid plans to UNCHIKUN on Play",
            "Test whether I can lock in the ¥300,000 range as the floor",
        ],
        "closing": "Viral hits come and go. Stock is an asset. I'm going after both.",
    },
    "2026-05": {
        "desc": "May 2026 revenue was ¥338,294. UNCHIKUN evolved into an AI health log app, and Google Play passed ¥10,000 in a month for the first time.",
        "highlights": [
            ("UNCHIKUN, now UNCHIKUN: Poop Log &amp; AI Health", "It evolved into an AI health log app and got a new name. ¥62,131 from the App Store, ¥106,284 from ads and ¥9,391 from Play. 33,652 downloads."),
            ("TravelMemoryMap", "¥64,841 in subscriptions plus ads and Play. The Golden Week travel season helped too."),
            ("Google Play overall", "A monthly record. UNCHIKUN's special annual plan sold 14 times. Android is becoming a place where things sell."),
        ],
        "analysis": """
<p>¥338,294. Down 6% from last month, but it held the ¥300,000 range.</p>
<p>As I said last month, I added AI features to UNCHIKUN and turned it into UNCHIKUN: Poop Log &amp; AI Health. Putting AI in the name changed how it shows up in the store, and downloads reached 33,652. On its own it earned ¥178,000 this month, cementing its place as the main pillar.</p>
<p>The other topic is Google Play crossing ¥10,000 a month. It was ¥102 in January, so it has grown 100x in five months. The special annual offer sold 14 times. Android users are clearly willing to pay.</p>
<p>The worry is that UNCHIKUN's eCPM dropped to ¥143. It was ¥504 in February. That comes from the overseas share going up, so it's a sign of growth, but there's room to rethink the ad formats.</p>
""",
        "next_actions": [
            "Raise the share of higher-paying formats such as rewarded ads",
            "Raise Premium Monthly conversion with paywall A/B tests",
            "Improve the 32% ad match rate on UNCHIKUN for Android",
        ],
        "closing": "Nothing flashy, but months like this are what build the floor.",
    },
    "2026-06": {
        "desc": "June 2026 revenue was ¥341,961. UNCHIKUN passed 30,000 downloads a month. I also look back on the first half of the year, which totaled ¥2.4 million.",
        "highlights": [
            ("UNCHIKUN", "32,412 downloads for the month. ¥47,129 from the App Store, ¥105,988 from iOS ads, ¥15,909 from Android ads and ¥3,710 from Play."),
            ("TravelMemoryMap", "Subscriptions recovered to ¥73,086. The Supporter Plan's steadiness stands out."),
            ("Jelly Same Puzzle", "A consumable item called the Hammer Ticket sold. In-game purchases, a new kind of revenue for me."),
        ],
        "analysis": """
<p>¥341,961. Three months in a row in the ¥300,000 range, so the floor is more or less set.</p>
<p>UNCHIKUN downloads hit 32,412 for the month. Money comes in from four wallets: iOS ads, Android ads, iOS purchases and Android purchases. It has become an ideal multiplatform app.</p>
<p>Here's a summary of the first half of 2026. January through June totaled ¥2,399,549, an average of ¥399,925 a month. From ¥38,000 a month last November, I've reached an average of ¥400,000 a month in a little over half a year. I'm still at only 3.4% of the ¥10 million goal, but in terms of growth rate it's not a bad pace.</p>
<p>The next wall is clear: ¥500,000 a month without a viral hit. The keys are turning UNCHIKUN's 50,000 downloads into revenue more efficiently, and adding new pillars.</p>
""",
        "next_actions": [
            "Release several new apps in July. CarKeep and others are in the works",
            "Use ASO and localization to take UNCHIKUN from 50,000 to 100,000 downloads a month",
            "Expand placements of rewarded interstitials, which have already shown a ¥2,609 eCPM",
        ],
        "closing": "¥2.4 million in the first half. In the second half I'm going to build a ¥500,000-a-month floor.",
    },
    "2026-07": {
        "desc": "July 2026 revenue was ¥372,319. New downloads stayed flat and only ads grew, while the 5 apps I released this month made ¥0.",
        "highlights": [
            ("UNCHIKUN", "New iOS downloads were 32,579, flat from last month. On top of ¥75,211 in App Store purchases came ¥128,666 from iOS ads, ¥20,385 from Android ads and ¥6,368 from Play. That works out to 62% of the month's revenue from one app."),
            ("TravelMemoryMap", "¥70,425 in purchases plus ¥7,878 in ads and ¥2,686 from Play. New downloads were 3,139, down a little from last month. Quiet, for the summer travel season."),
            ("The 5 new apps I released in July", "DiveKeep, Coin Game Collection, Himekuri, OshiLog and YOU Receipt. New downloads ranged from 4 to 29, 56 across all five. Not a single yen in sales."),
        ],
        "analysis": """
<p>¥372,319. Up 8.9% from last month, the fourth straight month in the ¥300,000 range.</p>
<p>Almost all of the increase is ads. AdMob was ¥167,118, and UNCHIKUN on iOS alone made ¥128,666. Impressions grew to 867,281. It's my third-highest ad month since I received my first 21 yen (about $0.19) in July 2019. The only two months above it are this March, when Oshi Island went viral, and March 2022.</p>
<p>The interesting part is that the number of new people installing didn't grow. UNCHIKUN's new downloads were 32,412 in June and 32,579 in July. Across the whole App Store, they went from 39,240 to 38,972, barely moving. Yet ad impressions grew 16%. What grew was redownloads, 2.5x from 21,681 to 54,873. People either changed phones or deleted the app and installed it again. Either way, it was a month when people who already knew the app came back and opened it more than before.</p>
<p>Purchases were flat at ¥195,845. Ads grow when existing users use the app more, but purchases don't work that way. That's what this month's shape shows.</p>
<p>One more thing bothers me: how concentrated it is. UNCHIKUN and TravelMemoryMap made 84% of the month's revenue between them. I released 5 new apps in July, every one of them made ¥0, and some didn't even reach double-digit downloads. I'm not going to stop shipping. But the numbers say plainly that shipping alone makes nothing happen.</p>
""",
        "next_actions": [
            "Review UNCHIKUN's ad formats. Raising the ¥148 eCPM by just 10% changes revenue by more than ¥10,000 a month",
            "Change where UNCHIKUN's paywall appears, to turn the extra downloads into purchases",
            "Of the 5 apps released in July, narrow it down to the ones whose downloads are moving and redo their ASO",
        ],
        "closing": "Not how many I shipped, but the one that reached people. That's what I'm working on in August.",
    },
    "2026-08": {
        "desc": "August 2026 revenue was ¥494,888. YOU Receipt, which made ¥0 in July, passed ¥90,000, while UNCHIKUN's new downloads fell 30%.",
        "highlights": [
            ("UNCHIKUN", "¥77,664 in App Store purchases, plus ¥116,051 from iOS ads, ¥16,096 from Android ads and ¥4,087 from Play. New downloads were 22,445, down 31% from July's 32,579, yet purchases rose from ¥75,211 to ¥77,664."),
            ("TravelMemoryMap", "Purchases of ¥98,475 were a single-month record, with the 1-year Supporter Plan making up ¥44,879. New downloads grew 50%, from 3,139 to 4,707, and with ads and Play the total passed ¥110,000."),
            ("YOU Receipt", "July: 8 new downloads and ¥0 in sales. August: 1,985 downloads on iOS, and the ¥3,000 one-time purchase plan made ¥72,327. The Android version brought in ¥16,709 too."),
        ],
        "analysis": """
<p>¥494,888. Up 32.9% from last month, and my second-highest month after March's ¥1.04 million.</p>
<p>March was one app, Oshi Island, spiking. August has a different shape: three pillars of around ¥100,000 each standing at the same time. UNCHIKUN at ¥213,898, TravelMemoryMap at ¥114,753 and YOU Receipt at ¥94,640. These three make up 85% of the month.</p>
<p>YOU Receipt was one of the five apps I said made ¥0 in the July issue. It had 8 new downloads in July. In August, iOS got 1,985, and the ¥3,000 one-time purchase plan made ¥72,327. Android added ¥16,709. Per download that's ¥47.7, while UNCHIKUN in the same month made ¥9.5. Letting people use an app free for a long time and showing them ads, or selling something for ¥3,000 to 2,000 people. That's how far apart the two are.</p>
<p>UNCHIKUN, meanwhile, lost 30% of its new downloads, from 32,579 to 22,445. Ad revenue dropped from ¥128,666 to ¥116,051. But eCPM rose from ¥148 to ¥154, and purchases increased from ¥75,211 to ¥77,664. Purchase revenue per download went from ¥2.31 to ¥3.46. In July's NextAction I wrote that I'd review the ads and move the paywall, and both numbers turned upward. I haven't been able to separate out what worked and by how much.</p>
<p>I released 7 new apps in August: nokki, Monivo, Yattayo, EyeMole, Matchbox, Pancake Shop and Music Snapshot. Together they got 711 new downloads and ¥557 in sales. Same picture as last month. But one of the five I said the same thing about in July brought in ¥90,000 the following month. The numbers from the month an app ships tell you nothing.</p>
""",
        "next_actions": [
            "Try the ¥3,000 one-time purchase that sold in YOU Receipt on the paywalls of my other apps",
            "Bring UNCHIKUN's downloads back. The ad rate went up, so now volume is what moves the number",
            "Rework the store copy and first screen of each of the 7 apps released in August, once each, during September",
        ],
        "closing": "The numbers from the month an app ships don't tell you whether it's a hit. In September I'll keep shipping while working on last month's seven.",
    },
    "2026-09": {
        "desc": "September 2026 revenue was ¥464,476, down 6.1% from the previous month. TravelMemoryMap's purchases set a personal record for the second month in a row, while ad revenue fell nearly 20%.",
        "highlights": [
            ("UNCHIKUN", "¥87,508 in App Store purchases, plus ¥96,992 from iOS ads, ¥12,151 from Android ads and ¥18,492 from Play. New downloads were 16,410, down another 27% from August, but the total is about the same as August's ¥213,898."),
            ("TravelMemoryMap", "Purchases of ¥108,094 beat August's ¥98,475 again. The 1-year Supporter Plan made ¥49,130. New downloads fell from 4,707 to 4,070."),
            ("YOU Receipt", "New downloads rose from 1,985 to 3,147, yet the one-time purchase plan nearly halved, from ¥72,327 to ¥39,531. The weekly plan grew from ¥4,925 to ¥8,739."),
        ],
        "analysis": """
<p>¥464,476. Down 6.1% from last month. Even so, it's my third-highest month after March and August.</p>
<p>Almost all of the drop is ads. AdMob fell from ¥155,880 to ¥128,577, down ¥27,303. The month as a whole fell by ¥30,412, so ads explain 90% of it. Specifically, it's UNCHIKUN on iOS, which went from ¥116,051 to ¥96,992. Impressions fell from 752,203 to 701,335, and eCPM dropped from ¥154 to ¥138. I had just written in the August issue that the rate went up, and now it has fallen below July's ¥148.</p>
<p>UNCHIKUN's new downloads went from 22,445 to 16,410. In August's NextAction I wrote that I'd bring the volume back, and I couldn't. It has halved in two months. Purchases, though, rose from ¥77,664 to ¥87,508, with the annual plan nearly doubling from ¥21,542 to ¥39,736. Play purchases went from ¥4,087 to ¥18,492. Ads, purchases and Play add up to ¥215,143, almost unchanged from August. Fewer and fewer people are coming in, but the ones who stay are paying. I don't know how long that will hold.</p>
<p>TravelMemoryMap's purchases were ¥108,094, a personal record for the second month running. New downloads fell, yet the 1-year Supporter Plan rose from ¥44,879 to ¥49,130.</p>
<p>YOU Receipt moved the other way. New downloads rose 60%, from 1,985 to 3,147, but sales fell from August's ¥94,640 to ¥58,238. The ¥3,000 one-time purchase dropped by nearly half, and the weekly plan grew instead. App Store sales per download went from ¥38.9 to ¥15.3.</p>
<p>One-time purchases sold in other apps too. HomeKeep, TankMinder and WatchKeep each sold one, all priced in the ¥2,500 range. The 7 apps released in August got 181 new downloads combined in September, and their sales were ¥949, from EyeMole and nokki.</p>
<p>Google Play has grown every month since July: ¥9,356, ¥22,282, then ¥30,070. In September UNCHIKUN's monthly plan made ¥18,492, so UNCHIKUN is now number one on Play as well.</p>
""",
        "next_actions": [
            "Start a TikTok for UNCHIKUN. New downloads halved in two months, so I'll use video to bring in people from outside store search",
            "Make TikTok posts for TravelMemoryMap and YOU Receipt too, and compare which app's videos take off more easily",
            "Put a tracking link on every post, and report in the October issue how many downloads came from the videos that took off",
        ],
        "closing": "A month where my two pillars grew purchases and lost ad revenue. In October I'm going to open more doors with TikTok.",
    },
}
