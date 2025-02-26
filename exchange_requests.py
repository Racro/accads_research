import json
import sys
import os 
import numpy as np
import tldextract

# known_domains = [
#     # 1–50
#     "doubleclick.net",              # Google Ad Manager (AdX / DoubleClick)
#     "googlesyndication.com",        # Google Open Bidding / Open Auction (approx.)
#     "xandr.com",                    # Xandr (AppNexus)
#     "appnexus.com",                 # Legacy AppNexus domain
#     "openx.net",                    # OpenX
#     "indexexchange.com",            # Index Exchange
#     "magnite.com",                  # Magnite (Rubicon/Telaria/SpotX)
#     "rubiconproject.com",           # Legacy Rubicon domain
#     "pubmatic.com",                 # PubMatic
#     "amazon-adsystem.com",          # Amazon Publisher Services / Amazon DSP
#     "sovrn.com",                    # Sovrn
#     "triplelift.com",               # TripleLift
#     "sharethrough.com",             # Sharethrough
#     "inmobi.com",                   # InMobi
#     "verizonmedia.com",             # Verizon Media (Oath / AOL / Yahoo)
#     "bidswitch.com",                # BidSwitch (IPONWEB)
#     "adform.com",                   # Adform
#     "mopub.com",                    # MoPub (AppLovin)
#     "applovin.com",                 # AppLovin
#     "fyber.com",                    # Fyber
#     "smartadserver.com",            # Smart AdServer (Smart)
#     "teads.tv",                     # Teads
#     "unruly.co",                    # Unruly
#     "33across.com",                 # 33Across
#     "smaato.com",                   # Smaato
#     "spotx.tv",                     # SpotX (part of Magnite)
#     "epom.com",                     # Epom Market
#     "smartyads.com",                # SmartyAds
#     "visto.com",                    # Visto
#     "avocet.io",                    # Avocet
#     "beachfront.com",               # Beachfront
#     "velismedia.com",               # Velis Media
#     "revcontent.com",               # Revcontent (native)
#     "taboola.com",                  # Taboola (native)
#     "outbrain.com",                 # Outbrain (native)
#     "platform161.com",              # Platform161
#     "improvedigital.com",           # Improve Digital (Azerion)
#     "yieldlab.net",                 # Yieldlab
#     "themediagrid.com",             # The MediaGrid (IPONWEB)
#     "districtm.net",                # district m (merged with Sharethrough)
#     "brealtime.com",                # bRealTime
#     "e-planning.net",               # ePlanning
#     "media.net",                    # Media.net
#     "criteo.com",                   # Criteo
#     "onetag.com",                   # OneTag
#     "a4advertising.com",            # a4 (Altice)
#     "ironsrc.com",                  # ironSource
#     "adcolony.com",                 # AdColony
#     "vungle.com",                   # Vungle
#     "chartboost.com",               # Chartboost
#     "mintegral.com",                # Mintegral
#     "tapjoy.com",                   # Tapjoy

#     # 51–100
#     "loopme.com",                   # LoopMe
#     "smartrtb.com",                 # SmartRTB
#     "liquidm.com",                  # LiquidM
#     "axonix.com",                   # Axonix
#     "engagebdr.com",                # Engage:BDR
#     "adyoulike.com",                # AdYouLike
#     "kargo.com",                    # Kargo
#     "rtbhouse.com",                 # RTB House
#     "sublime.xyz",                  # Sublime (Sublime Skinz)
#     "clearpier.com",                # ClearPier
#     "buysellads.com",               # BuySellAds
#     "bidsopt.com",                  # Bidsopt
#     "taptica.com",                  # Taptica
#     "adtelligent.com",              # Adtelligent (VertaMedia)
#     "underdogmedia.com",            # Underdog Media
#     "mobfox.com",                   # MobFox
#     "aerserv.com",                  # AerServ (InMobi)
#     "digilant.com",                 # Digilant
#     "burtintelligence.com",         # Burt Intelligence
#     "aol.com",                      # One by AOL (legacy, now Yahoo)
#     "coxdigitalsolutions.com",      # Cox Digital Solutions
#     "pantheranetwork.com",          # Panthera Network
#     "adxpansion.com",               # AdXpansion (adult-focused)
#     "spearad.com",                  # SpearAd
#     "admixer.net",                  # AdMixer
#     "bidfluence.com",               # Bidfluence
#     "mobair.com",                   # MobAir
#     "a4g.com",                      # A4G
#     "collective.com",               # Collective (Visto)
#     "adtradr.com",                  # AdTradr
#     "rhythmone.com",                # RhythmOne (Blinkx)
#     "stickyads.tv",                 # StickyAds.tv (FreeWheel/Comcast)
#     "freewheel.tv",                 # FreeWheel (Comcast)
#     "oneplanetonly.com",            # OnePlanetOnly
#     "smartrade.net",                # Smartrade (APAC)
#     "madhouse.cn",                  # Madhouse (China/India)
#     "baidu.com",                    # Baidu Exchange Services
#     "tencent.com",                  # Tencent Advertising Exchange
#     "tiktokforbusiness.com",        # TikTok For Business
#     "pangle.cn",                    # Pangle (ByteDance)
#     "youappi.com",                  # YouAppi
#     "aarki.com",                    # Aarki
#     "planetroll.com",               # Planetroll
#     "audiomob.com",                 # AudioMob
#     "shemedia.com",                 # SHE Media Partner Network
#     "cpex.com",                     # CPEx
#     "nexage.com",                   # Nexage (Verizon)
#     "brightroll.com",               # BrightRoll (Yahoo)
#     "conversantmedia.com",          # Conversant (formerly ValueClick)

#     # 101–150
#     "exponential.com",              # Exponential (Tribal Fusion)
#     "mediamath.com",                # MediaMath
#     "google.com",                   # (AdMeld integrated into Google; placeholder)
#     "liveramp.com",                 # LiveRamp (data marketplace)
#     "adgear.com",                   # AdGear (Samsung Ads)
#     "groundtruth.com",              # GroundTruth (xAd)
#     "adswizz.com",                  # AdsWizz (audio)
#     "doubleverify.com",             # DoubleVerify (verification + marketplace)
#     "pixalate.com",                 # Pixalate (fraud prevention, marketplace intelligence)
#     "openweb.com",                  # Spot.IM rebrand to OpenWeb
#     "brave.com",                    # Brave Ads
#     "revx.io",                      # RevX (Affle)
#     "optimatic.com",                # Optimatic (video, acquired by Matomy)
#     "matomy.com",                   # Matomy
#     "adknowledge.com",              # Adknowledge (parts sold to Viant)
#     "viantinc.com",                 # Viant (Adelphic DSP)
#     "specificmedia.com",            # Specific Media (Viant)
#     "adobe.com",                    # Adobe Advertising Cloud (TubeMogul)
#     "quantcast.com",                # Quantcast
#     "amobee.com",                   # Amobee (SingTel)
#     "videologygroup.com",           # Videology (acquired by Amobee)
#     "crossinstall.com",             # CrossInstall (acquired by Twitter)
#     "adblade.com",                  # AdBlade (native)
#     "distroscale.com",              # DistroScale / DistroTV
#     "roku.com",                     # Roku Advertising (OneView)
#     "ctvmedia.com",                 # CTV Media
#     "infolinks.com",                # Infolinks (in-text ads)
#     "powerinbox.com",               # PowerInbox (Jeeng)
#     "tapnative.com",                # TapNative
#     "zedo.com",                     # Zedo
#     "brid.tv",                      # Brid.TV
#     "vidazoo.com",                  # Vidazoo (Perion)
#     "aniview.com",                  # Aniview
#     "tremorinternational.com",      # Tremor Video DSP (parent site)
#     "samba.tv",                     # Samba TV
#     "cadent.tv",                    # Cadent
#     "synacor.com",                  # Synacor (Zimbra Ads)
#     "brightcom.com",                # Brightcom (YBrant)
#     "yeahmobi.com",                 # Yeahmobi
#     "mobvista.com",                 # Mobvista (Nativex)
#     "appier.com",                   # Appier (AI-based marketing)
#     "moloco.com",                   # Moloco
#     "remerge.io",                   # Remerge
#     "start.io",                     # StartApp rebrand
#     "personally.com",               # Persona.ly
#     "bidease.com",                  # Bidease
#     "gamoshi.com",                  # Gamoshi (merged w/ NexDSP)
#     "nexdsp.com",                   # NexDSP

#     # 151–200
#     "runads.com",                   # RUN (IgnitionOne) - partial
#     "ignitionone.com",              # IgnitionOne
#     "splicky.com",                  # Splicky
#     "placeiq.com",                  # Sevig/SeventhDecimal or PlaceIQ
#     "placeexchange.com",            # PlaceExchange (DOOH)
#     "vistarmedia.com",              # Vistar Media (DOOH)
#     "broadsign.com",                # Broadsign (DOOH)
#     "hivestack.com",                # Hivestack (DOOH)
#     "adstanding.com",               # AdStanding (DOOH aggregator)
#     "epom.com",                     # Epom White Label DSP (repeat of #28)
#     "bidvertiser.com",              # BidVertiser
#     "propellerads.com",             # PropellerAds
#     "popcash.net",                  # PopCash
#     "popads.net",                   # PopAds
#     "exoclick.com",                 # ExoClick
#     "trafficjunky.com",             # TrafficJunky (adult)
#     "adnium.com",                   # Adnium (adult)
#     "juicyads.com",                 # JuicyAds (adult)
#     "eroadvertising.com",           # EroAdvertising
#     "adsterra.com",                 # Adsterra
#     "hilltopads.com",               # HilltopAds
#     "clickadu.com",                 # ClickAdu
#     "activerevenue.com",            # ActiveRevenue
#     "megapu.sh",                    # MegaPush
#     "pushground.com",               # Pushground
#     "richads.com",                  # RichAds (RichPush)
#     "dable.io",                     # Dable (Korea native)
#     "mobisummer.com",               # MobiSummer
#     "yandex.ru",                    # Yandex Advertising Network
#     "mail.ru",                      # myTarget (Mail.ru / VK)
#     "vk.com",                       # VK Ads
#     "bing.com",                     # Bing Ads / Microsoft Ads
#     "linkedin.com",                 # LinkedIn Marketing Solutions
#     "reddit.com",                   # Reddit Advertising
#     "twitter.com",                  # Twitter Ads / MoPub (legacy)
#     "snapchat.com",                 # Snap Ads
#     "facebook.com",                 # Facebook Audience Network
#     "instagram.com",                # Instagram Ads (Meta)
#     "plista.com",                   # Plista (native)
#     "ligatus.com",                  # Ligatus (Outbrain)
#     "plugrush.com",                 # PlugRush
#     "voodooads.com",                # VoodooAds
#     "databerries.com",              # Databerries (Herow)
#     "herow.io",                     # Herow
#     "zemanta.com",                  # Zemanta (Outbrain DSP)
#     "storygize.com",                # Storygize

#     # 201–250
#     "yieldmo.com",                  # Yieldmo
#     "polar.me",                     # Polar (native, possibly acquired)
#     "stackadapt.com",               # StackAdapt
#     "bankrate.com",                 # Bankrate Exchange
#     "mediago.com",                  # MediaGo (Baidu int'l)
#     "alibaba.com",                  # UC Ads (Alibaba)
#     "youku.com",                    # Youku Ads (Alibaba)
#     "fluct.jp",                     # Fluct (Japan)
#     "fout.co.jp",                   # FreakOut (Japan) (sometimes freakout.net)
#     "geniee.co.jp",                 # Geniee (Japan)
#     "ad-generation.jp",             # Ad Generation (Supership)
#     "voyagegroup.com",              # VOYAGE GROUP (Japan)
#     "cyberagent.co.jp",             # CyberAgent DSP (Japan)
#     "line.me",                      # LINE Ads Platform
#     "kakao.com",                    # Kakao Ads (Korea)
#     "rakuten.com",                  # Rakuten Marketing / Ad Exchange
#     "yieldone.jp",                  # YIELD ONE (Cartaholdings, Japan)
#     "ad-stir.com",                  # ADSTIR (Japan)
#     "i-mobile.co.jp",               # i-mobile (Japan)
#     "daum.net",                     # Daum Kakao Exchange
#     "bidsxchange.com",              # BidsXchange (lesser-known)
#     "adprime.com",                  # AdPrime (health)
#     "pulsepoint.com",               # PulsePoint (health, integrated w/ WebMD)
#     "conversantmedia.com",          # Conversant Health (repeat domain, Epsilon)
#     "quadrantone.com",              # QuadrantOne (defunct local news JV)
#     "localiq.com",                  # LocalIQ (Gannett)
#     "reachlocal.com",               # ReachLocal (Gannett)
#     "basis.net",                    # Centro rebrand to Basis Technologies
#     "audiencex.com",                # AUDIENCEX
#     "automatad.com",                # Automatad
#     "bridgesad.com",                # Bridges Advertising (MENA)
#     "choueirigroup.com",            # DMS (Digital Media Services, MENA)
#     "dianomi.com",                  # Dianomi (finance native)
#     "nanigans.com",                 # Nanigans (performance)
#     "bidtellect.com",               # Bidtellect (native)
#     "targetspot.com",               # TargetSpot (audio)
#     "dynadmic.com",                 # DynAdmic (acquired by Smart)
#     "sizmek.com",                   # Sizmek (acquired by Amazon)
#     "adswerve.com",                 # Adswerve (Google reseller)
#     "beeswax.com",                  # Beeswax (bidding-as-a-service, now FreeWheel)
#     "bidstack.com",                 # Bidstack (in-game)
#     "anzu.io",                      # Anzu.io (in-game)
#     "adverty.com",                  # Adverty (in-game/VR)
#     "gadsme.com",                   # GADSME (in-game)
#     "frameplay.gg",                 # Frameplay (in-game)
#     "playwire.com",                 # Playwire (gaming/e-sports)
#     "tappx.com",                    # Tappx (mobile/CTV)
#     "sunmedia.tv",                  # SunMedia (Spain/LatAm)
#     "imoxi.com",                    # Imoxi (LatAm?), sometimes "imoox" or "imooxi"

#     # 251–300
#     "prebid.org",                   # Head Bidding Wrapper (not an exchange, but listing)
#     "bluebillywig.com",             # Blue Billywig (video)
#     "vidstart.com",                 # VidStart (mobile video)
#     "zoomd.com",                    # Zoomd
#     "adzmath.com",                  # AdzMath (APAC)
#     "gumgum.com",                   # GumGum (contextual)
#     "fiksu.com",                    # BidMind by Fiksu (acquired? brand may vary)
#     "spoteffects.com",              # Spoteffects (TV)
#     "tvty.tv",                      # TVTY (Nielsen)
#     "blis.com",                     # Blis (location)
#     "zilliadx.com",                 # Zilliadx
#     "hubvisor.io",                  # Hubvisor
#     "adsiduous.com",                # Adsiduous
#     "runative.com",                 # Runative (adult/native)
#     "adoperator.com",               # AdOperator
#     "affle.com",                    # Affle (owns RevX)
#     "adpone.com",                   # Adpone
#     "globalwidemedia.com",          # GlobalWide Media
#     "orbitsoft.com",                # OrbitSoft
#     "powerlink.ai",                 # Powerlink (Israel)
#     "invibes.com",                  # Invibes (Europe)
#     "yieldbird.com",                # YieldBird (Agora)
#     "ismartnetwork.com",            # iSmartNetwork (smaller aggregator)
#     # OneTag repeated below (#274) but we’ve listed it at #43
#     "seeding-alliance.de",          # SeedingAlliance (Ströer, Germany)
#     "videobase.com",                # VideoBase (less known)
#     "scripps.com",                  # Scripps Octane
#     "premionmedia.com",             # Premion (Tegna)
#     "hulu.com",                     # Hulu Ad Manager
#     "disneyadsales.com",            # Disney Ad Server
#     "nbcuniversal.com",             # NBCUniversal One Platform
#     "fox.com",                      # Fox Now Ads
#     "pluto.tv",                     # Pluto TV Ads
#     "tubi.tv",                      # Tubi Ads
#     "peacocktv.com",                # Peacock Ad Manager (NBCU)
#     "samsung.com",                  # Samsung Ads
#     "lgads.tv",                     # LG Ads
#     "vizioads.com",                 # Vizio Ads (Inscape)
#     "crimtan.com",                  # Crimtan
#     "ringier.com",                  # Ringier (Programmatic Marketplaces)
#     "admiralcloud.com",             # AdmiralCloud (some aggregator solutions)
#     "premiumaudience.com",          # PremiumAudience (Germany)
#     "carambola.com",                # Carambola (interactive video)
#     "vidoomy.com",                  # Vidoomy (video)
#     "mixpo.com",                    # Mixpo (video)
#     "aol.com",                      # AOL One Video (repeat domain)
#     "oneview.roku.com",             # OneView by Roku (subdomain, main = roku.com)
#     "enginemailer.com",             # Enginemailer Ads (email-based)

#     # 301–350
#     "dailymail.co.uk",              # MailOnline / DMG Media
#     "newscorp.com",                 # News Corp Global Exchange
#     "theguardian.com",              # Guardian News & Media Exchange
#     "relx.com",                     # RELX AdTech (Reed Exhibitions)
#     "cafemedia.com",                # CafeMedia
#     "monumetric.com",               # Monumetric
#     "mediavine.com",                # Mediavine
#     "sortable.com",                 # Sortable
#     "ezoic.com",                    # Ezoic
#     "snigel.com",                   # Snigel
#     "marfeel.com",                  # Marfeel
#     "jeeng.com",                    # PowerInbox rebrand
#     "sekindo.com",                  # Sekindo (Universal McCann)
#     "primis.tech",                  # Primis (Sekindo)
#     "truvid.com",                   # Truvid
#     "vi.ai",                        # Video Intelligence (Outbrain)
#     "prodigyads.com",               # ProdigyAds
#     "digitalturbine.com",           # Digital Turbine Exchange
#     "fyber.com",                    # Fyber FairBid (repeat domain)
#     "adfalcon.com",                 # AdFalcon (MENA)
#     "extend.tv",                    # ExtendTV
#     "shakeads.com",                 # ShakeAds
#     "dailymotion.com",              # Dailymotion Advertising
#     "vevo.com",                     # Vevo Ads
#     "spotify.com",                  # Spotify Ad Studio
#     "pandora.com",                  # Pandora for Brands (AdsWizz)
#     "iheart.com",                   # iHeartMedia AdBuilder
#     "tunein.com",                   # TuneIn Ads
#     "adinmo.com",                   # AdInMo (in-game)
#     "appgrowth.com",                # AppGrowth (China?)
#     "ucxprogrammatic.com",          # UCX Programmatic (Portugal)
#     "adglare.com",                  # AdGlare
#     "airpush.com",                  # Airpush
#     "mobidea.com",                  # Mobidea
#     "clickdealer.com",              # ClickDealer
#     "gunggo.com",                   # Gunggo
#     "runboadnetwork.com",           # RunboadNetwork
#     # aerserv.com repeated (#67)
#     "mobilefuse.com",               # MobileFuse
#     "simplifi.com",                 # Simpli.fi
#     # zedo.com repeated (#132)
#     # yieldone.jp repeated (#218)
#     "escoadvertising.com",          # Esco Advertising
#     "smarthub.dev",                 # SmartHub (by SmartyAds)
#     "fraudlogix.com",               # Fraudlogix
#     "traffichaus.com",              # TrafficHaus
#     "adperium.com",                 # AdPerium
#     "ccbill.com",                   # CCBill Ad Network

#     # 351–400
#     "clickky.biz",                  # RTB Exchange by Clickky
#     "bidderplace.com",              # Bidderplace
#     "leadbolt.com",                 # LeadBolt
#     "adscapital.com",               # AdsCapital
#     "mobipium.com",                 # Mobipium
#     "activeagent.de",               # ActiveAgent (ProSiebenSat.1)
#     "sevenonemedia.de",             # SevenOne Media
#     # "adaudience.de" possibly defunct JV in Germany
#     "medyanet.com",                 # MedyaNet (Turkey)
#     "adhood.com",                   # AdHood (Turkey)
#     "reklamstore.com",              # ReklamStore (Turkey)
#     "digitalks.co",                 # Digitalks Ads (Turkey)
#     "clickattack.com",              # Clickattack (SE Europe)
#     "httpool.com",                  # Httpool (Aleph Group)
#     "alephholding.com",             # Aleph Group
#     "adsnative.com",                # AdsNative (Polymorph → Walmart)
#     "walmart.com",                  # Walmart DSP / Walmart Exchange
#     "roundel.com",                  # Roundel (Target)
#     "thekrogerco.com",              # Kroger (KPM)
#     "criteo.com",                   # Criteo Retail Media (repeat domain)
#     "promatica.com",                # Promatica (retail aggregator?)
#     "albertsons.com",               # Albertsons Media Collective
#     "carrefour.com",                # Carrefour Links
#     "rakkan.co.jp",                 # Rakkan (Japan retail, limited info)
#     "pubgalaxy.com",                # PubGalaxy
#     # runative.com repeated (#264, #376)
#     "adzbuzz.com",                  # AdzBuzz
#     "10bumps.com",                  # 10Bumps
#     "ntent.com",                    # NTENT
#     "adlemons.com",                 # AdLemons
#     "tapgerine.com",                # Tapgerine
#     "acquire.io",                   # Acquire.io
#     "rtbbetter.com",                # RtbBetter
#     "bidmotion.com",                # BidMotion (France)
#     "roq.ad",                       # Roq.ad
#     "partnerize.com",               # Partnerize (Performance Horizon)
#     "avantlink.com",                # AvantLink
#     "cj.com",                       # CJ Affiliate
#     "rakutenadvertising.com",       # Rakuten Advertising
#     "skimlinks.com",                # Skimlinks
#     "sovrn.com",                    # Sovrn Commerce (repeat domain)
#     "monetizer101.com",             # Monetizer101
#     "adsempire.com",                # AdsEmpire
#     "appsamurai.com",               # App Samurai
#     "bid4bids.com",                 # Bid4Bids
#     # primis.tech repeated (#315)
#     "onefastad.com",                # OneFastAd
#     "ucweb.com",                    # UC Union (Alibaba)
#     "mammothmediainc.com",          # Mammoth Media
#     "mobiproks.com",                # Mobiproks

#     # 401–450
#     "mindtake.com",                 # MindTake Ad Marketplace
#     "projectagora.com",             # Project Agora (Tailwind/TDG)
#     "thinkdigitalgroup.com",        # Thinkdigital (TDG)
#     "njuice.com",                   # Njuice (native aggregator)
#     "zoominfo.com",                 # Clickagy -> Zoominfo MarketingOS
#     "6sense.com",                   # 6sense (ABM)
#     "demandbase.com",               # Demandbase (ABM)
#     "terminus.com",                 # Terminus (ABM)
#     "madisonlogic.com",             # Madison Logic
#     "rollworks.com",                # RollWorks (NextRoll)
#     "nextroll.com",                 # NextRoll (AdRoll)
#     "choozle.com",                  # Choozle
#     "zetaglobal.com",               # Zeta Global
#     "ampersand.tv",                 # Ampersand (Linear + Addressable TV)
#     "xumo.tv",                      # Xumo Ads (Comcast)
#     "showheroes.com",               # ShowHeroes (EU video)
#     # gadsme.com repeated (#245, #417)
#     "scibids.com",                  # Scibids (AI optimization)
#     "octopusadx.com",               # Octopus Ad Exchange
#     "whitemob.com",                 # Whitemob
#     "admachine.co",                 # AdMachine (white-label DSP)
#     "adsigo.com",                   # Adsigo
#     "adux.com",                     # ADUX (HiMedia Group, France)
#     "dotandmedia.com",              # DotAndMedia (Spain)
#     "spolecznosci.pl",              # Spolecznosci (Poland aggregator)
#     "adplayer.pro",                 # AdPlayer.Pro
#     "vidrtb.com",                   # VidRTB
#     # bidmotion.com repeated (#384, #428)
#     "yax.com",                      # YAX (native aggregator)
#     # adyoulike.com repeated (#56, #430)
#     "admanmedia.com",               # ADman Media (Spanish video, part of Entravision)
#     "entravision.com",              # Entravision (MediaDonuts)
#     # prebid.org repeated (#251, #433)
#     # magnite.com repeated (#7, #434 for DV+)
#     "nativo.com",                   # Nativo (native)
#     "roxot.com",                    # Roxot
#     "trafficstars.com",             # TrafficStars (adult)
#     "adspyglass.com",               # AdSpyglass
#     "djaxtech.com",                 # dJAX Adserver
#     "oximobi.com",                  # Oximobi
#     "adwool.com",                   # Adwool
#     # zoomd.com repeated (#254, #442)
#     "trioninteractive.com",         # Trion Interactive
#     "hawk.tech",                    # Hawk by TrackinStore
#     "spreaker.com",                 # Spreaker (iHeart)
#     "global.com",                   # Global (DAX - Digital Audio Exchange)
#     "admiraldsp.com",               # Admiral DSP (not Admiral consent)
#     "kiosked.com",                  # Kiosked
#     "smartclip.tv",                 # Smartclip (RTL)
#     "rtl-adconnect.com",            # RTL AdConnect

#     # 451–500
#     "rmedia.ru",                    # RMedia (Russia aggregator)
#     "mail.ru",                      # Mail.ru (myTarget) - repeat
#     "voxnest.com",                  # Voxnest (iHeart)
#     "adtone.com",                   # AdTone (telco-based)
#     "avocx.com",                    # AVOCX (CTV aggregator)
#     # conversantmedia.com repeated (#100, #456)
#     "mediaq.com",                   # MediaQ (APAC aggregator) - approximate
#     "tim.it",                       # TIM Media (Italy)
#     "optidigital.com",              # Opti Digital (EU)
#     "polar.me",                     # Polar Fish (repeat #203)
#     "aplus.net",                    # Aplus (older network, uncertain)
#     "adskate.com",                  # AdSkate (contextual)
#     "konduit.com",                  # Konduit (video)
#     "anyclip.com",                  # AnyClip (video AI)
#     "galaksion.com",                # Galaksion (pop/push)
#     # clickdealer.com repeated (#337, #466)
#     "trafficfactory.com",           # TrafficFactory (adult)
#     "adxxx.com",                    # AdXXX (adult)
#     "onetraffic.co",                # OneTraffic
#     "offertoro.com",                # OfferToro
#     "iron.media",                   # IronMedia (small aggregator)
#     # trafficstars.com repeated (#437, #472)
#     "ad-maven.com",                 # AdMaven
#     "adcombo.com",                  # AdCombo (CPA)
#     "offervault.com",               # OfferVault (aggregator)
#     "leadzu.com",                   # Leadzu
#     "profitsocial.com",             # ProfitSocial
#     "coinis.com",                   # Coinis (push/pop)
#     "addragon.com",                 # AdDragon (crypto-based)
#     "madgicx.com",                  # Madgicx
#     # mediago.com repeated (#206, #481)
#     "vertoz.com",                   # Vertoz
#     "yieldvision.com",              # Yieldivision (Nordic)
#     "deltaprojects.com",            # Delta Projects (Nordics)
#     "zitomedia.net",                # Zito Media
#     "mntn.com",                     # MNTN (SteelHouse)
#     # partnerize.com repeated (#386, #487)
#     "adcaff.com",                   # AdCaff
#     "airnowmedia.com",             # AirNow Media
#     "voluum.com",                   # Voluum DSP (affiliate-friendly)
#     "sprinklr.com",                 # Sprinklr
#     "kochava.com",                  # Kochava (Traffic Index)
#     "appnext.com",                  # Appnext
#     "wappier.com",                  # Wappier
#     # alephholding.com repeated (#365, #495)
#     "tokopedia.com",                # Tokopedia Marketing Services
#     "bukalapak.com",                # Bukalapak Ads
#     "shopee.com",                   # Shopee Ads
#     "carousell.com",                # Carousell Media Group
#     "gumtree.com",                  # Gumtree Ads
# ]

# This list is approximate and may contain duplicates or legacy domains.
# Always verify current/official ad-serving domains for each platform.

def belongs_to_known_exchange(url):

    known_domains = [
    # 1–50
        "doubleclick.net",              # Google Ad Manager (AdX / DoubleClick)
        "googlesyndication.com",        # Google Open Bidding / Open Auction (approx.)
        "xandr.com",                    # Xandr (AppNexus)
        "appnexus.com",                 # Legacy AppNexus domain
        "openx.net",                    # OpenX
        "indexexchange.com",            # Index Exchange
        "magnite.com",                  # Magnite (Rubicon/Telaria/SpotX)
        "rubiconproject.com",           # Legacy Rubicon domain
        "pubmatic.com",                 # PubMatic
        "amazon-adsystem.com",          # Amazon Publisher Services / Amazon DSP
        "sovrn.com",                    # Sovrn
        "triplelift.com",               # TripleLift
        "sharethrough.com",             # Sharethrough
        "inmobi.com",                   # InMobi
        "verizonmedia.com",             # Verizon Media (Oath / AOL / Yahoo)
        "bidswitch.com",                # BidSwitch (IPONWEB)
        "adform.com",                   # Adform
        "mopub.com",                    # MoPub (AppLovin)
        "applovin.com",                 # AppLovin
        "fyber.com",                    # Fyber
        "smartadserver.com",            # Smart AdServer (Smart)
        "teads.tv",                     # Teads
        "unruly.co",                    # Unruly
        "33across.com",                 # 33Across
        "smaato.com",                   # Smaato
        "spotx.tv",                     # SpotX (part of Magnite)
        "epom.com",                     # Epom Market
        "smartyads.com",                # SmartyAds
        "visto.com",                    # Visto
        "avocet.io",                    # Avocet
        "beachfront.com",               # Beachfront
        "velismedia.com",               # Velis Media
        "revcontent.com",               # Revcontent (native)
        "taboola.com",                  # Taboola (native)
        "outbrain.com",                 # Outbrain (native)
        "platform161.com",              # Platform161
        "improvedigital.com",           # Improve Digital (Azerion)
        "yieldlab.net",                 # Yieldlab
        "themediagrid.com",             # The MediaGrid (IPONWEB)
        "districtm.net",                # district m (merged with Sharethrough)
        "brealtime.com",                # bRealTime
        "e-planning.net",               # ePlanning
        "media.net",                    # Media.net
        "criteo.com",                   # Criteo
        "onetag.com",                   # OneTag
        "a4advertising.com",            # a4 (Altice)
        "ironsrc.com",                  # ironSource
        "adcolony.com",                 # AdColony
        "vungle.com",                   # Vungle
        "chartboost.com",               # Chartboost
        "mintegral.com",                # Mintegral
        "tapjoy.com",                   # Tapjoy

        # 51–100
        "loopme.com",                   # LoopMe
        "smartrtb.com",                 # SmartRTB
        "liquidm.com",                  # LiquidM
        "axonix.com",                   # Axonix
        "engagebdr.com",                # Engage:BDR
        "adyoulike.com",                # AdYouLike
        "kargo.com",                    # Kargo
        "rtbhouse.com",                 # RTB House
        "sublime.xyz",                  # Sublime (Sublime Skinz)
        "clearpier.com",                # ClearPier
        "buysellads.com",               # BuySellAds
        "bidsopt.com",                  # Bidsopt
        "taptica.com",                  # Taptica
        "adtelligent.com",              # Adtelligent (VertaMedia)
        "underdogmedia.com",            # Underdog Media
        "mobfox.com",                   # MobFox
        "aerserv.com",                  # AerServ (InMobi)
        "digilant.com",                 # Digilant
        "burtintelligence.com",         # Burt Intelligence
        "aol.com",                      # One by AOL (legacy, now Yahoo)
        "coxdigitalsolutions.com",      # Cox Digital Solutions
        "pantheranetwork.com",          # Panthera Network
        "adxpansion.com",               # AdXpansion (adult-focused)
        "spearad.com",                  # SpearAd
        "admixer.net",                  # AdMixer
        "bidfluence.com",               # Bidfluence
        "mobair.com",                   # MobAir
        "a4g.com",                      # A4G
        "collective.com",               # Collective (Visto)
        "adtradr.com",                  # AdTradr
        "rhythmone.com",                # RhythmOne (Blinkx)
        "stickyads.tv",                 # StickyAds.tv (FreeWheel/Comcast)
        "freewheel.tv",                 # FreeWheel (Comcast)
        "oneplanetonly.com",            # OnePlanetOnly
        "smartrade.net",                # Smartrade (APAC)
        "madhouse.cn",                  # Madhouse (China/India)
        "baidu.com",                    # Baidu Exchange Services
        "tencent.com",                  # Tencent Advertising Exchange
        "tiktokforbusiness.com",        # TikTok For Business
        "pangle.cn",                    # Pangle (ByteDance)
        "youappi.com",                  # YouAppi
        "aarki.com",                    # Aarki
        "planetroll.com",               # Planetroll
        "audiomob.com",                 # AudioMob
        "shemedia.com",                 # SHE Media Partner Network
        "cpex.com",                     # CPEx
        "nexage.com",                   # Nexage (Verizon)
        "brightroll.com",               # BrightRoll (Yahoo)
        "conversantmedia.com",          # Conversant (formerly ValueClick)

        # 101–150
        "exponential.com",              # Exponential (Tribal Fusion)
        "mediamath.com",                # MediaMath
        "google.com",                   # (AdMeld integrated into Google; placeholder)
        "liveramp.com",                 # LiveRamp (data marketplace)
        "adgear.com",                   # AdGear (Samsung Ads)
        "groundtruth.com",              # GroundTruth (xAd)
        "adswizz.com",                  # AdsWizz (audio)
        "doubleverify.com",             # DoubleVerify (verification + marketplace)
        "pixalate.com",                 # Pixalate (fraud prevention, marketplace intelligence)
        "openweb.com",                  # Spot.IM rebrand to OpenWeb
        "brave.com",                    # Brave Ads
        "revx.io",                      # RevX (Affle)
        "optimatic.com",                # Optimatic (video, acquired by Matomy)
        "matomy.com",                   # Matomy
        "adknowledge.com",              # Adknowledge (parts sold to Viant)
        "viantinc.com",                 # Viant (Adelphic DSP)
        "specificmedia.com",            # Specific Media (Viant)
        "adobe.com",                    # Adobe Advertising Cloud (TubeMogul)
        "quantcast.com",                # Quantcast
        "amobee.com",                   # Amobee (SingTel)
        "videologygroup.com",           # Videology (acquired by Amobee)
        "crossinstall.com",             # CrossInstall (acquired by Twitter)
        "adblade.com",                  # AdBlade (native)
        "distroscale.com",              # DistroScale / DistroTV
        "roku.com",                     # Roku Advertising (OneView)
        "ctvmedia.com",                 # CTV Media
        "infolinks.com",                # Infolinks (in-text ads)
        "powerinbox.com",               # PowerInbox (Jeeng)
        "tapnative.com",                # TapNative
        "zedo.com",                     # Zedo
        "brid.tv",                      # Brid.TV
        "vidazoo.com",                  # Vidazoo (Perion)
        "aniview.com",                  # Aniview
        "tremorinternational.com",      # Tremor Video DSP (parent site)
        "samba.tv",                     # Samba TV
        "cadent.tv",                    # Cadent
        "synacor.com",                  # Synacor (Zimbra Ads)
        "brightcom.com",                # Brightcom (YBrant)
        "yeahmobi.com",                 # Yeahmobi
        "mobvista.com",                 # Mobvista (Nativex)
        "appier.com",                   # Appier (AI-based marketing)
        "moloco.com",                   # Moloco
        "remerge.io",                   # Remerge
        "start.io",                     # StartApp rebrand
        "personally.com",               # Persona.ly
        "bidease.com",                  # Bidease
        "gamoshi.com",                  # Gamoshi (merged w/ NexDSP)
        "nexdsp.com",                   # NexDSP

        # 151–200
        "runads.com",                   # RUN (IgnitionOne) - partial
        "ignitionone.com",              # IgnitionOne
        "splicky.com",                  # Splicky
        "placeiq.com",                  # Sevig/SeventhDecimal or PlaceIQ
        "placeexchange.com",            # PlaceExchange (DOOH)
        "vistarmedia.com",              # Vistar Media (DOOH)
        "broadsign.com",                # Broadsign (DOOH)
        "hivestack.com",                # Hivestack (DOOH)
        "adstanding.com",               # AdStanding (DOOH aggregator)
        "epom.com",                     # Epom White Label DSP (repeat of #28)
        "bidvertiser.com",              # BidVertiser
        "propellerads.com",             # PropellerAds
        "popcash.net",                  # PopCash
        "popads.net",                   # PopAds
        "exoclick.com",                 # ExoClick
        "trafficjunky.com",             # TrafficJunky (adult)
        "adnium.com",                   # Adnium (adult)
        "juicyads.com",                 # JuicyAds (adult)
        "eroadvertising.com",           # EroAdvertising
        "adsterra.com",                 # Adsterra
        "hilltopads.com",               # HilltopAds
        "clickadu.com",                 # ClickAdu
        "activerevenue.com",            # ActiveRevenue
        "megapu.sh",                    # MegaPush
        "pushground.com",               # Pushground
        "richads.com",                  # RichAds (RichPush)
        "dable.io",                     # Dable (Korea native)
        "mobisummer.com",               # MobiSummer
        "yandex.ru",                    # Yandex Advertising Network
        "mail.ru",                      # myTarget (Mail.ru / VK)
        "vk.com",                       # VK Ads
        "bing.com",                     # Bing Ads / Microsoft Ads
        "linkedin.com",                 # LinkedIn Marketing Solutions
        "reddit.com",                   # Reddit Advertising
        "twitter.com",                  # Twitter Ads / MoPub (legacy)
        "snapchat.com",                 # Snap Ads
        "facebook.com",                 # Facebook Audience Network
        "instagram.com",                # Instagram Ads (Meta)
        "plista.com",                   # Plista (native)
        "ligatus.com",                  # Ligatus (Outbrain)
        "plugrush.com",                 # PlugRush
        "voodooads.com",                # VoodooAds
        "databerries.com",              # Databerries (Herow)
        "herow.io",                     # Herow
        "zemanta.com",                  # Zemanta (Outbrain DSP)
        "storygize.com",                # Storygize

        # 201–250
        "yieldmo.com",                  # Yieldmo
        "polar.me",                     # Polar (native, possibly acquired)
        "stackadapt.com",               # StackAdapt
        "bankrate.com",                 # Bankrate Exchange
        "mediago.com",                  # MediaGo (Baidu int'l)
        "alibaba.com",                  # UC Ads (Alibaba)
        "youku.com",                    # Youku Ads (Alibaba)
        "fluct.jp",                     # Fluct (Japan)
        "fout.co.jp",                   # FreakOut (Japan) (sometimes freakout.net)
        "geniee.co.jp",                 # Geniee (Japan)
        "ad-generation.jp",             # Ad Generation (Supership)
        "voyagegroup.com",              # VOYAGE GROUP (Japan)
        "cyberagent.co.jp",             # CyberAgent DSP (Japan)
        "line.me",                      # LINE Ads Platform
        "kakao.com",                    # Kakao Ads (Korea)
        "rakuten.com",                  # Rakuten Marketing / Ad Exchange
        "yieldone.jp",                  # YIELD ONE (Cartaholdings, Japan)
        "ad-stir.com",                  # ADSTIR (Japan)
        "i-mobile.co.jp",               # i-mobile (Japan)
        "daum.net",                     # Daum Kakao Exchange
        "bidsxchange.com",              # BidsXchange (lesser-known)
        "adprime.com",                  # AdPrime (health)
        "pulsepoint.com",               # PulsePoint (health, integrated w/ WebMD)
        "conversantmedia.com",          # Conversant Health (repeat domain, Epsilon)
        "quadrantone.com",              # QuadrantOne (defunct local news JV)
        "localiq.com",                  # LocalIQ (Gannett)
        "reachlocal.com",               # ReachLocal (Gannett)
        "basis.net",                    # Centro rebrand to Basis Technologies
        "audiencex.com",                # AUDIENCEX
        "automatad.com",                # Automatad
        "bridgesad.com",                # Bridges Advertising (MENA)
        "choueirigroup.com",            # DMS (Digital Media Services, MENA)
        "dianomi.com",                  # Dianomi (finance native)
        "nanigans.com",                 # Nanigans (performance)
        "bidtellect.com",               # Bidtellect (native)
        "targetspot.com",               # TargetSpot (audio)
        "dynadmic.com",                 # DynAdmic (acquired by Smart)
        "sizmek.com",                   # Sizmek (acquired by Amazon)
        "adswerve.com",                 # Adswerve (Google reseller)
        "beeswax.com",                  # Beeswax (bidding-as-a-service, now FreeWheel)
        "bidstack.com",                 # Bidstack (in-game)
        "anzu.io",                      # Anzu.io (in-game)
        "adverty.com",                  # Adverty (in-game/VR)
        "gadsme.com",                   # GADSME (in-game)
        "frameplay.gg",                 # Frameplay (in-game)
        "playwire.com",                 # Playwire (gaming/e-sports)
        "tappx.com",                    # Tappx (mobile/CTV)
        "sunmedia.tv",                  # SunMedia (Spain/LatAm)
        "imoxi.com",                    # Imoxi (LatAm?), sometimes "imoox" or "imooxi"

        # 251–300
        "prebid.org",                   # Head Bidding Wrapper (not an exchange, but listing)
        "bluebillywig.com",             # Blue Billywig (video)
        "vidstart.com",                 # VidStart (mobile video)
        "zoomd.com",                    # Zoomd
        "adzmath.com",                  # AdzMath (APAC)
        "gumgum.com",                   # GumGum (contextual)
        "fiksu.com",                    # BidMind by Fiksu (acquired? brand may vary)
        "spoteffects.com",              # Spoteffects (TV)
        "tvty.tv",                      # TVTY (Nielsen)
        "blis.com",                     # Blis (location)
        "zilliadx.com",                 # Zilliadx
        "hubvisor.io",                  # Hubvisor
        "adsiduous.com",                # Adsiduous
        "runative.com",                 # Runative (adult/native)
        "adoperator.com",               # AdOperator
        "affle.com",                    # Affle (owns RevX)
        "adpone.com",                   # Adpone
        "globalwidemedia.com",          # GlobalWide Media
        "orbitsoft.com",                # OrbitSoft
        "powerlink.ai",                 # Powerlink (Israel)
        "invibes.com",                  # Invibes (Europe)
        "yieldbird.com",                # YieldBird (Agora)
        "ismartnetwork.com",            # iSmartNetwork (smaller aggregator)
        # OneTag repeated below (#274) but we’ve listed it at #43
        "seeding-alliance.de",          # SeedingAlliance (Ströer, Germany)
        "videobase.com",                # VideoBase (less known)
        "scripps.com",                  # Scripps Octane
        "premionmedia.com",             # Premion (Tegna)
        "hulu.com",                     # Hulu Ad Manager
        "disneyadsales.com",            # Disney Ad Server
        "nbcuniversal.com",             # NBCUniversal One Platform
        "fox.com",                      # Fox Now Ads
        "pluto.tv",                     # Pluto TV Ads
        "tubi.tv",                      # Tubi Ads
        "peacocktv.com",                # Peacock Ad Manager (NBCU)
        "samsung.com",                  # Samsung Ads
        "lgads.tv",                     # LG Ads
        "vizioads.com",                 # Vizio Ads (Inscape)
        "crimtan.com",                  # Crimtan
        "ringier.com",                  # Ringier (Programmatic Marketplaces)
        "admiralcloud.com",             # AdmiralCloud (some aggregator solutions)
        "premiumaudience.com",          # PremiumAudience (Germany)
        "carambola.com",                # Carambola (interactive video)
        "vidoomy.com",                  # Vidoomy (video)
        "mixpo.com",                    # Mixpo (video)
        "aol.com",                      # AOL One Video (repeat domain)
        "oneview.roku.com",             # OneView by Roku (subdomain, main = roku.com)
        "enginemailer.com",             # Enginemailer Ads (email-based)

        # 301–350
        "dailymail.co.uk",              # MailOnline / DMG Media
        "newscorp.com",                 # News Corp Global Exchange
        "theguardian.com",              # Guardian News & Media Exchange
        "relx.com",                     # RELX AdTech (Reed Exhibitions)
        "cafemedia.com",                # CafeMedia
        "monumetric.com",               # Monumetric
        "mediavine.com",                # Mediavine
        "sortable.com",                 # Sortable
        "ezoic.com",                    # Ezoic
        "snigel.com",                   # Snigel
        "marfeel.com",                  # Marfeel
        "jeeng.com",                    # PowerInbox rebrand
        "sekindo.com",                  # Sekindo (Universal McCann)
        "primis.tech",                  # Primis (Sekindo)
        "truvid.com",                   # Truvid
        "vi.ai",                        # Video Intelligence (Outbrain)
        "prodigyads.com",               # ProdigyAds
        "digitalturbine.com",           # Digital Turbine Exchange
        "fyber.com",                    # Fyber FairBid (repeat domain)
        "adfalcon.com",                 # AdFalcon (MENA)
        "extend.tv",                    # ExtendTV
        "shakeads.com",                 # ShakeAds
        "dailymotion.com",              # Dailymotion Advertising
        "vevo.com",                     # Vevo Ads
        "spotify.com",                  # Spotify Ad Studio
        "pandora.com",                  # Pandora for Brands (AdsWizz)
        "iheart.com",                   # iHeartMedia AdBuilder
        "tunein.com",                   # TuneIn Ads
        "adinmo.com",                   # AdInMo (in-game)
        "appgrowth.com",                # AppGrowth (China?)
        "ucxprogrammatic.com",          # UCX Programmatic (Portugal)
        "adglare.com",                  # AdGlare
        "airpush.com",                  # Airpush
        "mobidea.com",                  # Mobidea
        "clickdealer.com",              # ClickDealer
        "gunggo.com",                   # Gunggo
        "runboadnetwork.com",           # RunboadNetwork
        # aerserv.com repeated (#67)
        "mobilefuse.com",               # MobileFuse
        "simplifi.com",                 # Simpli.fi
        # zedo.com repeated (#132)
        # yieldone.jp repeated (#218)
        "escoadvertising.com",          # Esco Advertising
        "smarthub.dev",                 # SmartHub (by SmartyAds)
        "fraudlogix.com",               # Fraudlogix
        "traffichaus.com",              # TrafficHaus
        "adperium.com",                 # AdPerium
        "ccbill.com",                   # CCBill Ad Network

        # 351–400
        "clickky.biz",                  # RTB Exchange by Clickky
        "bidderplace.com",              # Bidderplace
        "leadbolt.com",                 # LeadBolt
        "adscapital.com",               # AdsCapital
        "mobipium.com",                 # Mobipium
        "activeagent.de",               # ActiveAgent (ProSiebenSat.1)
        "sevenonemedia.de",             # SevenOne Media
        # "adaudience.de" possibly defunct JV in Germany
        "medyanet.com",                 # MedyaNet (Turkey)
        "adhood.com",                   # AdHood (Turkey)
        "reklamstore.com",              # ReklamStore (Turkey)
        "digitalks.co",                 # Digitalks Ads (Turkey)
        "clickattack.com",              # Clickattack (SE Europe)
        "httpool.com",                  # Httpool (Aleph Group)
        "alephholding.com",             # Aleph Group
        "adsnative.com",                # AdsNative (Polymorph → Walmart)
        "walmart.com",                  # Walmart DSP / Walmart Exchange
        "roundel.com",                  # Roundel (Target)
        "thekrogerco.com",              # Kroger (KPM)
        "criteo.com",                   # Criteo Retail Media (repeat domain)
        "promatica.com",                # Promatica (retail aggregator?)
        "albertsons.com",               # Albertsons Media Collective
        "carrefour.com",                # Carrefour Links
        "rakkan.co.jp",                 # Rakkan (Japan retail, limited info)
        "pubgalaxy.com",                # PubGalaxy
        # runative.com repeated (#264, #376)
        "adzbuzz.com",                  # AdzBuzz
        "10bumps.com",                  # 10Bumps
        "ntent.com",                    # NTENT
        "adlemons.com",                 # AdLemons
        "tapgerine.com",                # Tapgerine
        "acquire.io",                   # Acquire.io
        "rtbbetter.com",                # RtbBetter
        "bidmotion.com",                # BidMotion (France)
        "roq.ad",                       # Roq.ad
        "partnerize.com",               # Partnerize (Performance Horizon)
        "avantlink.com",                # AvantLink
        "cj.com",                       # CJ Affiliate
        "rakutenadvertising.com",       # Rakuten Advertising
        "skimlinks.com",                # Skimlinks
        "sovrn.com",                    # Sovrn Commerce (repeat domain)
        "monetizer101.com",             # Monetizer101
        "adsempire.com",                # AdsEmpire
        "appsamurai.com",               # App Samurai
        "bid4bids.com",                 # Bid4Bids
        # primis.tech repeated (#315)
        "onefastad.com",                # OneFastAd
        "ucweb.com",                    # UC Union (Alibaba)
        "mammothmediainc.com",          # Mammoth Media
        "mobiproks.com",                # Mobiproks

        # 401–450
        "mindtake.com",                 # MindTake Ad Marketplace
        "projectagora.com",             # Project Agora (Tailwind/TDG)
        "thinkdigitalgroup.com",        # Thinkdigital (TDG)
        "njuice.com",                   # Njuice (native aggregator)
        "zoominfo.com",                 # Clickagy -> Zoominfo MarketingOS
        "6sense.com",                   # 6sense (ABM)
        "demandbase.com",               # Demandbase (ABM)
        "terminus.com",                 # Terminus (ABM)
        "madisonlogic.com",             # Madison Logic
        "rollworks.com",                # RollWorks (NextRoll)
        "nextroll.com",                 # NextRoll (AdRoll)
        "choozle.com",                  # Choozle
        "zetaglobal.com",               # Zeta Global
        "ampersand.tv",                 # Ampersand (Linear + Addressable TV)
        "xumo.tv",                      # Xumo Ads (Comcast)
        "showheroes.com",               # ShowHeroes (EU video)
        # gadsme.com repeated (#245, #417)
        "scibids.com",                  # Scibids (AI optimization)
        "octopusadx.com",               # Octopus Ad Exchange
        "whitemob.com",                 # Whitemob
        "admachine.co",                 # AdMachine (white-label DSP)
        "adsigo.com",                   # Adsigo
        "adux.com",                     # ADUX (HiMedia Group, France)
        "dotandmedia.com",              # DotAndMedia (Spain)
        "spolecznosci.pl",              # Spolecznosci (Poland aggregator)
        "adplayer.pro",                 # AdPlayer.Pro
        "vidrtb.com",                   # VidRTB
        # bidmotion.com repeated (#384, #428)
        "yax.com",                      # YAX (native aggregator)
        # adyoulike.com repeated (#56, #430)
        "admanmedia.com",               # ADman Media (Spanish video, part of Entravision)
        "entravision.com",              # Entravision (MediaDonuts)
        # prebid.org repeated (#251, #433)
        # magnite.com repeated (#7, #434 for DV+)
        "nativo.com",                   # Nativo (native)
        "roxot.com",                    # Roxot
        "trafficstars.com",             # TrafficStars (adult)
        "adspyglass.com",               # AdSpyglass
        "djaxtech.com",                 # dJAX Adserver
        "oximobi.com",                  # Oximobi
        "adwool.com",                   # Adwool
        # zoomd.com repeated (#254, #442)
        "trioninteractive.com",         # Trion Interactive
        "hawk.tech",                    # Hawk by TrackinStore
        "spreaker.com",                 # Spreaker (iHeart)
        "global.com",                   # Global (DAX - Digital Audio Exchange)
        "admiraldsp.com",               # Admiral DSP (not Admiral consent)
        "kiosked.com",                  # Kiosked
        "smartclip.tv",                 # Smartclip (RTL)
        "rtl-adconnect.com",            # RTL AdConnect

        # 451–500
        "rmedia.ru",                    # RMedia (Russia aggregator)
        "mail.ru",                      # Mail.ru (myTarget) - repeat
        "voxnest.com",                  # Voxnest (iHeart)
        "adtone.com",                   # AdTone (telco-based)
        "avocx.com",                    # AVOCX (CTV aggregator)
        # conversantmedia.com repeated (#100, #456)
        "mediaq.com",                   # MediaQ (APAC aggregator) - approximate
        "tim.it",                       # TIM Media (Italy)
        "optidigital.com",              # Opti Digital (EU)
        "polar.me",                     # Polar Fish (repeat #203)
        "aplus.net",                    # Aplus (older network, uncertain)
        "adskate.com",                  # AdSkate (contextual)
        "konduit.com",                  # Konduit (video)
        "anyclip.com",                  # AnyClip (video AI)
        "galaksion.com",                # Galaksion (pop/push)
        # clickdealer.com repeated (#337, #466)
        "trafficfactory.com",           # TrafficFactory (adult)
        "adxxx.com",                    # AdXXX (adult)
        "onetraffic.co",                # OneTraffic
        "offertoro.com",                # OfferToro
        "iron.media",                   # IronMedia (small aggregator)
        # trafficstars.com repeated (#437, #472)
        "ad-maven.com",                 # AdMaven
        "adcombo.com",                  # AdCombo (CPA)
        "offervault.com",               # OfferVault (aggregator)
        "leadzu.com",                   # Leadzu
        "profitsocial.com",             # ProfitSocial
        "coinis.com",                   # Coinis (push/pop)
        "addragon.com",                 # AdDragon (crypto-based)
        "madgicx.com",                  # Madgicx
        # mediago.com repeated (#206, #481)
        "vertoz.com",                   # Vertoz
        "yieldvision.com",              # Yieldivision (Nordic)
        "deltaprojects.com",            # Delta Projects (Nordics)
        "zitomedia.net",                # Zito Media
        "mntn.com",                     # MNTN (SteelHouse)
        # partnerize.com repeated (#386, #487)
        "adcaff.com",                   # AdCaff
        "airnowmedia.com",             # AirNow Media
        "voluum.com",                   # Voluum DSP (affiliate-friendly)
        "sprinklr.com",                 # Sprinklr
        "kochava.com",                  # Kochava (Traffic Index)
        "appnext.com",                  # Appnext
        "wappier.com",                  # Wappier
        # alephholding.com repeated (#365, #495)
        "tokopedia.com",                # Tokopedia Marketing Services
        "bukalapak.com",                # Bukalapak Ads
        "shopee.com",                   # Shopee Ads
        "carousell.com",                # Carousell Media Group
        "gumtree.com",                  # Gumtree Ads
    ]
    """
    Returns True if the URL's registered domain (e.g., 'doubleclick.net')
    is in the known_domains list.
    """
    extracted = tldextract.extract(url)
    # tldextract gives you subdomain, domain, suffix separately.
    # Reconstruct the registered domain:
    registered_domain = f"{extracted.domain}.{extracted.suffix}"
    
    return registered_domain in known_domains

def extract_tld(input):
    if 'about:' in input or 'safeframe' in input:
        return ''
    return input.split('://')[-1].split('/')[0]

# Read .json file in /run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/data_backup/data_US/control and extract urls
def extract_urls(file_path, condition):
    # Requests
    if condition == 'reqs':
        if not os.path.exists(file_path):
            return []
        reqs = []
        reqs_all = []
        if_exchange = []
        try:
            with open(file_path) as f:
                data = json.load(f)["data"]["requests"]
        
                for ii in data:
                    tld = extract_tld(ii["url"])
                    if tld in file_path:
                        continue

                    if 'googlesyndication' in ii['url']:
                        continue
                    if ii["type"] == "Fetch" and ii["method"] == "POST":# and ii['responseBodyHash'] != None:
                        if 'responseBodyHash' in ii.keys() and ii['responseBodyHash'] == None:
                            continue
                        reqs.append(tld)
                
                    reqs_all.append(tld)
                    
                    if belongs_to_known_exchange(ii['url']):
                        if_exchange.append(tld)

        except Exception as e:
            print(e)
            print(file_path)
            sys.exit(0)
        return reqs, reqs_all, if_exchange

    # Ads
    if condition == 'ads':
        if not os.path.exists(file_path):
            return [], [], []
        with open(file_path) as f:
            data = json.load(f)
            imgs = []
            links = []
            frameurl = []
        try:
            num_ads = data['data']['ads']['scrapeResults']['nAdsScraped']
            data = data['data']['ads']['adAttrs']
        except Exception as e:
            return [], [], []
        
        for ii in range(num_ads):  
            for jj in range(len(data[ii]['adLinksAndImages'])):
                try:
                    if data[ii]['adLinksAndImages'][jj]['containsImgsOrLinks'] == True:
                        # imgs
                        for el in data[ii]['adLinksAndImages'][jj]['imgs']:
                            if el['width'] == 0 and el['height'] == 0:
                                continue
                            imgs.append(extract_tld(el['src']))
                        # links
                        for el in data[ii]['adLinksAndImages'][jj]['links']:
                            for el2 in el:
                                links.append(extract_tld(el2['href']))
                        
                        #frameURL
                        frameurl.append(extract_tld(data[ii]['adLinksAndImages'][jj]['frameUrl']))
                except KeyboardInterrupt: 
                    sys.exit() 
                except Exception as e: 
                    print(e)
                    continue    
        return imgs, links, frameurl


def analyse_ads_dict(src):
    fpath = 'exchange_ads_02_23.json'
    data = json.load(open(fpath, 'r'))[src]
    a_lst = np.array([])
    a_unique = set()

    for key in data:
        # if 'giallozafferano' in key:
        ctrl_set = set(list(data[key]['control'].keys()))
        # print(data[key]['control'])
        adb_set = set(list(data[key]['adblock'].keys()))
        # print(data[key]['adblock'])
        # if adb_set.issubset(ctrl_set):
        #     continue

        diff = adb_set - ctrl_set
        # if len(diff) > 0:
        a_lst = np.append(a_lst, len(diff))
        a_unique.update(diff)
        # else:
        #     # pass
        #     print(key, adb_set-ctrl_set)
    print(src, np.mean(a_lst), np.mean(a_lst), np.std(a_lst))

def analyse_reqs_dict(fp):
    fpath = f'exchange_requests_{fp}.json'
    data = json.load(open(fpath, 'r'))['reqs']

    for key in data:
        # if 'easycrochet' in key:
        ctrl_set = set(list(data[key]['control'].keys()))
        # print(data[key]['control'])
        adb_set = set(list(data[key]['adblock'].keys()))
        # print(data[key]['adblock'])
        if adb_set.issubset(ctrl_set):
            continue
        else:
            # pass
            print(key, adb_set-ctrl_set)

def generate_ads_dict():
    cases = ['control', 'adblock']

    # collect all jsons from the folder with filepath
    folder_path = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/data_02_23'

    url_dict = {'imgs': {}, 'links': {}, 'frameurl': {}}
    for file_name in [f for f in os.listdir(f'{folder_path}/control') if f.endswith('.json')]:
        url_dict['imgs'][file_name] = {'control': {}, 'adblock': {}}
        url_dict['links'][file_name] = {'control': {}, 'adblock': {}}
        url_dict['frameurl'][file_name] = {'control': {}, 'adblock': {}}
        for case in cases:
            imgs, links, frameurl = extract_urls(f'{folder_path}/{case}/{file_name}', 'ads')

            for url in imgs:
                if url not in url_dict['imgs'][file_name][case]:
                    url_dict['imgs'][file_name][case][url] = 1
                else:
                    url_dict['imgs'][file_name][case][url] += 1
            for url in links:
                if url not in url_dict['links'][file_name][case]:
                    url_dict['links'][file_name][case][url] = 1
                else:
                    url_dict['links'][file_name][case][url] += 1
            for url in frameurl:
                if url not in url_dict['frameurl'][file_name][case]:
                    url_dict['frameurl'][file_name][case][url] = 1
                else:
                    url_dict['frameurl'][file_name][case][url] += 1           
        
        json.dump(url_dict, open('exchange_ads_02_23.json', 'w'))

def generate_reqs_dict(fpath):
    cases = ['control', 'adblock']

    # collect all jsons from the folder with filepath
    # folder_path = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/{fpath}'
    folder_path = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/data_backup/{fpath}'

    url_dict = {'reqs': {}}
    for file_name in [f for f in os.listdir(f'{folder_path}/control') if f.endswith('.json')]:
        url_dict['reqs'][file_name] = {'control': {}, 'adblock': {}}
        for case in cases:
            reqs = extract_urls(f'{folder_path}/{case}/{file_name}', 'reqs')

            for url in reqs:
                if url not in url_dict['reqs'][file_name][case]:
                    url_dict['reqs'][file_name][case][url] = 1
                else:
                    url_dict['reqs'][file_name][case][url] += 1           
        
        json.dump(url_dict, open(f'exchange_requests_{fpath}.json', 'w'))

# generate_ads_dict()
# analyse_ads_dict('links')

# generate_reqs_dict('data_02_23')
# analyse_reqs_dict('data_02_23')

# generate_reqs_dict('data_US')
# analyse_reqs_dict('data_US')
