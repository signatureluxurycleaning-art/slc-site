/**
 * Signature Luxury Cleaning — Multi-language Translations
 * Supported: English (en), Chinese Simplified (zh), Hindi (hi),
 *            Tagalog (tl), Vietnamese (vi), Korean (ko)
 */

const TRANSLATIONS = {

  en: {
    // Topbar
    topbar_discount: "✨ New clients save up to 15% on every visit with recurring service — weekly −15%, bi-weekly −10%",
    topbar_call:     "Call or text:",
    topbar_offer:    "New clients save up to 15% on every visit with recurring service — weekly −15%, bi-weekly −10%",
    topbar_phone:    "Call or text: <span class='accent'>(650) 619-3504</span>",
    topbar_products: "Professional-grade products & equipment",
    topbar_rating:   "<span class='accent'>5.0★</span> Perfect score on Google Reviews",
    topbar_insured:  "Background-checked & fully insured team",
    topbar_app:      "No download needed — open our app on any phone",

    // Navbar
    nav_services: "Services",
    nav_how:      "How It Works",
    nav_why:      "Why Us",
    nav_reviews:  "Reviews",
    nav_areas:    "Areas",
    nav_phone:    "📞 (650) 619-3504",
    nav_app:      "📱 Use Our App",

    // Hero
    hero_badge:       "⭐ #1 Rated Cleaning Service in Silicon Valley & Peninsula",
    hero_stat_families: "Cleanings Completed",
    hero_stat_rating:   "Google Rating",
    hero_stat_cities:   "Cities Served",
    hero_btn_small:     "No download needed — works on any phone",
    hero_btn_strong:    "Open Our App",
    hero_prefer_call:   "Prefer to call?",
    mockup_greeting:    "Good morning,",
    mockup_welcome:     "Welcome back!",
    mockup_services:    "Our Services",
    mockup_book:        "Book Now — Pay Securely in App",
    badge_rating:       "5.0 — Perfect Score",
    badge_booking:      "Booking Confirmed!",
    svc_regular:        "Regular",
    svc_deep:           "Deep Clean",
    svc_moveout:        "Move Out",
    hero_title:    "Reclaim Your Time.<br><em>Come Home to a Spotless House.</em>",
    hero_subtitle: "Silicon Valley & Peninsula's most trusted luxury cleaning service. We take care of your home so you can focus on what matters most.",
    hero_badge:    "📍 Serving Silicon Valley & Peninsula",
    hero_slots:    "⚡ Limited slots available this week",
    hero_btn_app:  "<small>Book in 60 seconds</small><strong>Open Our App</strong>",
    hero_btn_phone:"📞 (650) 619-3504",

    // Trust bar
    trust_licensed:   "Fully Licensed & Insured",
    trust_background: "Background-Checked Team",
    trust_eco:        "Eco-Friendly Products",
    trust_guarantee:  "100% Satisfaction Guarantee",
    trust_app:        "Book & Pay via App",
    trust_1: "✅ Background-Checked Team",
    trust_2: "🌿 Eco-Friendly Products",
    trust_3: "💯 100% Satisfaction Guarantee",
    trust_4: "📱 Book & Pay via App",
    trust_5: "⭐ 5.0★ Google Rating",
    trust_6: "🔒 Fully Insured",

    // Services section
    services_label:    "Our Services",
    services_title:    "What cleaning services<br><em>does SLC offer?</em>",
    services_subtitle: "Six professional cleaning services — luxury-level attention to detail on every single visit.",

    svc1_name:  "Regular Cleaning",
    svc1_desc:  "Weekly or bi-weekly maintenance cleaning. We handle kitchens, bathrooms, bedrooms, living areas and more.",
    svc1_price: "From $170",

    svc2_name:  "Deep Cleaning",
    svc2_desc:  "A thorough top-to-bottom deep clean. Perfect for first-time clients or seasonal refreshes.",
    svc2_price: "From $220",
    svc2_badge: "⭐ Most Popular",

    svc3_name:  "Move In / Move Out",
    svc3_desc:  "Moving in or out? We leave every inch spotless for the next chapter.",
    svc3_price: "From $220",

    svc4_name:  "Post-Construction",
    svc4_desc:  "Renovation dust and debris removed. We handle the mess so you can enjoy the result.",
    svc4_price: "Custom Quote",

    svc5_name:  "Airbnb Turnover",
    svc5_desc:  "Fast, reliable turnover cleaning for short-term rentals. Guest-ready every time.",
    svc5_price: "From $150",

    svc6_name:  "Spring Cleaning",
    svc6_desc:  "A complete seasonal refresh. Inside cabinets, behind appliances — nothing missed.",
    svc6_price: "From $270",

    svc_cta:       "Book via App →",
    badge_popular: "⭐ Most Popular",
    svc1_title: "Regular Cleaning",
    svc1_desc:  "Weekly, bi-weekly, or monthly maintenance. Your home, consistently spotless — on your schedule.",
    svc1_i1: "All rooms vacuumed & mopped",
    svc1_i2: "Kitchen & bathrooms sanitized",
    svc1_i3: "Surfaces dusted & wiped",
    svc1_i4: "Beds made & linens changed",
    svc2_title: "Deep Cleaning",
    svc2_desc:  "A thorough top-to-bottom clean — inside appliances, cabinets, baseboards and every corner.",
    svc2_i1: "Inside oven, fridge & microwave",
    svc2_i2: "Inside cabinets & drawers",
    svc2_i3: "Baseboards & window sills",
    svc2_i4: "Grout & tile scrubbing",
    svc3_title: "Move In / Move Out",
    svc3_desc:  "Get your full deposit back. Complete sanitization of every surface, cabinet and appliance.",
    svc3_i1: "Full deep clean of entire property",
    svc3_i2: "Inside all appliances",
    svc3_i3: "Walls spot-cleaned",
    svc3_i4: "Deposit-back guarantee",
    svc4_title: "Post-Construction",
    svc4_desc:  "Specialized dust removal and debris cleanup after renovation or construction work.",
    svc4_i1: "Construction dust removal",
    svc4_i2: "Debris & residue cleanup",
    svc4_i3: "Window & surface polishing",
    svc4_i4: "Final inspection walkthrough",
    svc5_title: "Airbnb Turnover",
    svc5_desc:  "Fast, thorough turnovers. Fresh linens, full clean — guest-ready every single time.",
    svc5_i1: "Full clean between guests",
    svc5_i2: "Fresh linens & towels",
    svc5_i3: "Restock essentials",
    svc5_i4: "Photo-ready presentation",
    svc6_title: "Spring Cleaning",
    svc6_desc:  "Annual deep refresh — decluttering assistance, deep cleaning all rooms, windows and more.",
    svc6_i1: "Full home deep clean",
    svc6_i2: "Window cleaning inside & out",
    svc6_i3: "Decluttering assistance",
    svc6_i4: "Garage & storage areas",

    // White Glove Deep Clean
    svc_whiteglove_title: "White Glove Deep Clean",
    svc_whiteglove_desc:  "The most thorough cleaning we offer. Our 2-cleaner team physically moves your refrigerator, stove, washer, dryer, sofas, and beds to clean every hidden surface. Includes before/after photo documentation.",

    svc_btn_book:  "Book via App →",
    svc_btn_quote: "Call for Quote →",

    // App section
    app_label:    "Our App",
    app_title:    "How does the<br><em>SLC booking app work?</em>",
    app_subtitle: "No phone calls. No waiting. Open our app and take full control of your cleaning schedule — anytime, anywhere.",
    app_btn:      "<small>Works on iPhone & Android</small><strong>Open Our App</strong>",
    pwa_small:       "No App Store needed",
    pwa_strong:      "Open Our App",
    pwa_steps_title: "How to add to your home screen:",
    pwa_s1_title: "Open the link",
    pwa_s1_desc:  "Tap the button above on your phone",
    pwa_s2_title: "Tap Share / Menu",
    pwa_s2_desc:  "iPhone: tap Share ↑ | Android: tap ⋮ Menu",
    pwa_s3_title: "Add to Home Screen",
    pwa_s3_desc:  "Tap 'Add to Home Screen' — done! Works like an app.",
    pwa_step1_ios:   "iPhone: Tap Share → Add to Home Screen",
    pwa_step2_android: "Android: Tap Menu → Add to Home Screen",
    pwa_step3:       "Done! Access like a native app",

    // How it works
    how_s1_title: "Open Our App",
    how_s1_desc:  "No download needed. Open the link on your phone — works on iPhone and Android, instantly.",
    how_s2_title: "Choose Your Service",
    how_s2_desc:  "Browse services, see transparent pricing and pick the date and time that works for you.",
    how_s3_title: "We Clean",
    how_s3_desc:  "Our background-checked team arrives on time, fully equipped. You don't need to be home.",
    how_s4_title: "Enjoy Your Home",
    how_s4_desc:  "Come home to spotless, fresh-smelling spaces. Rate us in the app — guaranteed every time.",
    how_label:    "How It Works",
    how_title:    "How does our<br><em>booking process work?</em>",
    how_subtitle: "From booking to a clean home — the whole process takes less than 2 minutes.",
    how1_title:   "Open Our App",
    how1_desc:    "Works on iPhone and Android instantly — no download required.",
    how2_title:   "Choose Your Service",
    how2_desc:    "Regular, deep, move-out, Airbnb — pick what your home needs.",
    how3_title:   "Pick Your Time",
    how3_desc:    "Choose a date and time that works for you. Same-week availability.",
    how4_title:   "Relax & Enjoy",
    how4_desc:    "Our team arrives, cleans to perfection, and you inspect before we leave.",

    // Why us
    why_badge_title: "Satisfaction Guarantee",
    why_badge_desc:  "You inspect — we fix it before we leave",
    why_intro:       "We know how exhausting it is to work long hours and still come home to a messy house. That's why we exist — to give you back your evenings, your weekends, and your peace of mind.",
    why_p1_title: "Eco-Friendly Products",
    why_p1_desc:  "Non-toxic, plant-based, biodegradable products — safe for your kids, pets and the planet.",
    why_p2_title: "Detail-Obsessed Team",
    why_p2_desc:  "Every corner, every surface, every visit — cleaned to our highest standard. No shortcuts, ever.",
    why_p3_title: "Licensed, Bonded & Insured",
    why_p3_desc:  "Fully bonded and insured in California. Every team member is background-checked before hire.",
    why_p4_title: "100% Satisfaction Guarantee",
    why_p4_desc:  "When we finish, you walk through and inspect every area. If anything is not to your satisfaction, we fix it right then and there — before we leave. Your approval is our standard.",
    why_p5_title: "Full Control via App",
    why_p5_desc:  "Schedule, reschedule, pay and communicate with your team — all from the palm of your hand.",
    why_label:    "Why Choose Us",
    why_title:    "Why choose Signature Luxury Cleaning<br><em>over corporate maid services?</em>",
    why_subtitle: "We know how exhausting it is to work long hours and still come home to a messy house. That's why we exist — to give you back your evenings, your weekends, and your peace of mind.",
    why1_title:   "Background-Checked Team",
    why1_desc:    "Every cleaner is thoroughly vetted, insured, and trained to our luxury standard before entering your home.",
    why2_title:   "Eco-Friendly Products",
    why2_desc:    "Safe for your family, pets, and the environment. We use professional-grade, non-toxic cleaning solutions.",
    why3_title:   "100% Satisfaction Guarantee",
    why3_desc:    "When we finish, you walk through and inspect. If anything is not to your satisfaction, we fix it right then and there — before we leave.",
    why4_title:   "Book & Pay via App",
    why4_desc:    "No phone calls needed. Open our app, choose your service, pick a time, and pay securely — all in under 60 seconds.",

    // Gallery
    gallery_label:    "Our Work",
    gallery_title:    "What homes have we<br><em>cleaned in Silicon Valley?</em>",
    gallery_subtitle: "Real results from real homes across Silicon Valley.",

    // Reviews
    reviews_label:    "Reviews",
    reviews_title:    "What do Silicon Valley<br><em>residents say about us?</em>",
    reviews_count:    "Hundreds of happy families across Silicon Valley & Peninsula",

    // Areas
    areas_label:    "Service Areas",
    areas_title:    "Which Silicon Valley cities<br><em>do we serve?</em>",
    areas_subtitle: "We serve 20+ cities across Silicon Valley & Peninsula — from Burlingame to San Jose. Don't see your city? Call us — we may still be able to help.",

    // About / Trust
    trust_title:   "Why do families trust<br><em>Signature Luxury Cleaning?</em>",

    // CTA banner
    cta_title:     "Ready for a<br><em>Spotless Home?</em>",
    cta_subtitle:  "New clients save up to 15% on every visit with recurring service — weekly −15%, bi-weekly −10%. Open our app and book in under 60 seconds — no download required.",
    pwa_cta_small: "Works on iPhone & Android",
    cta_or_call:   "Or call us: <a href='tel:6506193504' style='color:var(--gold-light);'>(650) 619-3504</a>",
    cta_label:    "📱 Get Started",
    cta_title:    "Ready for a<br><em>Spotless Home?</em>",
    cta_subtitle: "New clients save up to 15% on every visit with recurring service — weekly −15%, bi-weekly −10%. Open our app and book in under 60 seconds — no download required.",
    cta_btn:      "<small>Works on iPhone & Android</small><strong>Open Our App</strong>",
    cta_or:       "Or call us:",

    // Footer
    footer_company:  "Company",
    footer_about:    "About Us",
    footer_faq:      "FAQ",
    footer_careers:  "Careers",
    footer_contact:  "Contact",
    footer_app:      "📱 Open Our App",
    footer_privacy:  "Privacy Policy",
    footer_love:     "Serving Silicon Valley with ❤️",
    rev1_text: "\"I've tried 4 different services in Palo Alto and Signature is BY FAR the best. They're thorough, professional, and the house smells amazing after every visit.\"",
    rev2_text: "\"Booked a move-out clean and got my full deposit back — $3,200! They cleaned things I didn't even think about. Worth every single penny.\"",
    rev3_text: "\"I have a 4-bedroom home and they finished in 3 hours perfectly. The team was polite, fast, and incredibly detailed. I've been a client for 8 months.\"",
    rev4_text: "\"Deep cleaning before my parents visited. My mom said it was the cleanest she'd ever seen my house. That says everything! Booking again next month.\"",
    rev5_text: "\"Best cleaning service in Silicon Valley, period. I've been a weekly client for over a year and the quality never drops. Highly recommend to everyone.\"",
    rev6_text: "\"Post-construction cleaning after our full remodel — they removed all the dust and debris perfectly. The house looked brand new. Incredible job by the whole team.\"",
    footer_desc:     "Silicon Valley & Peninsula's most trusted luxury residential cleaning service. Serving Burlingame, Palo Alto, Cupertino, Mountain View, Sunnyvale & 20+ cities.",
    footer_services: "Services",
    footer_contact:  "Contact",
    footer_areas:    "Service Areas",
    footer_copy:     "© 2025 Signature Luxury Cleaning. All rights reserved.",
    footer_love:     "Serving Silicon Valley & Peninsula with ❤️",
    gallery_subtitle: "Real results from real homes across Silicon Valley & Peninsula.",
    // AEO Snippets
    aeo_services: "Signature Luxury Cleaning offers seven services across Silicon Valley: Regular Cleaning, Deep Cleaning, Move In/Out, Post-Construction, Airbnb Turnover, Office Cleaning, and Spring Cleaning. All include eco-friendly products and a 100% satisfaction guarantee.",
    aeo_how: "Book through our web app in under 60 seconds: choose service, select frequency, pick date and time, confirm address. Pay via Stripe. Our team arrives, performs the service, and walks through with you to ensure satisfaction.",
    aeo_how2: "Book through our web app in under 60 seconds: choose service, select frequency, pick date and time, confirm address. Pay via Stripe. Our team arrives, performs the service, and walks through with you to ensure satisfaction.",
    aeo_why: "Signature Luxury Cleaning is owner-operated since 2023, not a franchise or call center. Every conversation reaches one of the owners directly. Every cleaner is background-checked, bonded, and personally trained. We carry full liability insurance.",
    aeo_reviews: "Signature Luxury Cleaning holds a 5.0★ rating on Google with reviews from clients across Palo Alto, Mountain View, Cupertino, Belmont, and Burlingame. Clients consistently cite consistency, professionalism, and respect for personal space.",
    aeo_areas: "We serve 18 cities across Silicon Valley and the Peninsula, from Belmont in the north to San Jose in the south. Most areas qualify for same-day cleaning availability. Service radius covers San Mateo County and Santa Clara County.",
  },

  // ─────────────────────────────────────────────
  zh: {
    topbar_offer:    "新客户享受定期服务每次最高15%折扣 — 每周−15%，每两周−10%",
    topbar_phone:    "电话或短信：<span class='accent'>(650) 619-3504</span>",
    topbar_products: "专业级清洁产品与设备",
    topbar_rating:   "<span class='accent'>5.0★</span> Google 评分满分",
    topbar_insured:  "背景调查通过，全额保险",
    topbar_app:      "无需下载 — 在任何手机上打开我们的应用",

    nav_services: "服务",
    nav_why:      "为什么选择我们",
    nav_reviews:  "客户评价",
    nav_areas:    "服务区域",
    nav_phone:    "📞 (650) 619-3504",
    nav_app:      "📱 打开应用",

    hero_title:    "找回您的时间。<br><em>回家享受一尘不染的家。</em>",
    hero_subtitle: "硅谷最值得信赖的豪华清洁服务。我们照顾您的家，让您专注于最重要的事情。",
    hero_badge:    "📍 圣何塞及硅谷地区",
    hero_slots:    "⚡ 本周预约名额有限",
    hero_btn_app:  "<small>60秒内完成预约</small><strong>打开应用</strong>",
    hero_btn_phone:"📞 (650) 619-3504",

    trust_1: "✅ 背景调查团队",
    trust_2: "🌿 环保清洁产品",
    trust_3: "💯 100% 满意保证",
    trust_4: "📱 通过应用预约和付款",
    trust_5: "⭐ Google 5.0★ 评分",
    trust_6: "🔒 全额保险",

    services_label:    "我们的服务",
    services_title:    "我们提供哪些<br><em>清洁服务？</em>",
    services_subtitle: "六项专业清洁服务 — 每次拜访都提供豪华级别的细心服务。",

    svc1_name:  "定期清洁",
    svc1_desc:  "每周或每两周的日常清洁。我们负责厨房、浴室、卧室、客厅等区域。",
    svc1_price: "起价 $170",
    svc2_name:  "深度清洁",
    svc2_desc:  "彻底的全面深度清洁。非常适合首次客户或季节性焕新。",
    svc2_price: "起价 $220",
    svc2_badge: "⭐ 最受欢迎",
    svc3_name:  "搬入/搬出清洁",
    svc3_desc:  "搬入或搬出？我们让每一寸空间都一尘不染。",
    svc3_price: "起价 $220",
    svc4_name:  "装修后清洁",
    svc4_desc:  "清除装修灰尘和碎屑。我们处理杂乱，让您享受成果。",
    svc4_price: "定制报价",
    svc5_name:  "Airbnb 翻台清洁",
    svc5_desc:  "快速可靠的短租房翻台清洁。每次都为客人做好准备。",
    svc5_price: "起价 $150",
    svc6_name:  "春季大扫除",
    svc6_desc:  "全面的季节性焕新。柜子内部、电器后面 — 一处不漏。",
    svc6_price: "起价 $270",

    svc_whiteglove_title: "White Glove 深度清洁",
    svc_whiteglove_desc:  "我们提供的最彻底清洁服务。2人团队会移动您的冰箱、炉灶、洗衣机、烘干机、沙发和床，清洁每一个隐藏表面。包含清洁前后对比照片。",

    svc_btn_book:  "通过应用预约 →",
    svc_btn_quote: "致电获取报价 →",

    app_label:    "我们的应用",
    app_title:    "SLC预约应用<br><em>如何使用？</em>",
    app_subtitle: "无需电话。无需等待。打开我们的应用，随时随地完全掌控您的清洁日程。",
    app_btn:      "<small>支持 iPhone 和 Android</small><strong>打开应用</strong>",
    pwa_steps_title: "如何添加到主屏幕：",
    pwa_step1_ios:   "iPhone：点击分享 → 添加到主屏幕",
    pwa_step2_android: "Android：点击菜单 → 添加到主屏幕",
    pwa_step3:       "完成！像原生应用一样使用",

    how_label:    "如何运作",
    how_title:    "我们的预约流程<br><em>如何运作？</em>",
    how_subtitle: "从预约到清洁完成 — 整个过程不到2分钟。",
    how1_title:   "打开应用",
    how1_desc:    "立即在 iPhone 和 Android 上使用 — 无需下载。",
    how2_title:   "选择服务",
    how2_desc:    "定期、深度、搬出、Airbnb — 选择您家所需的服务。",
    how3_title:   "选择时间",
    how3_desc:    "选择适合您的日期和时间。本周即可预约。",
    how4_title:   "放松享受",
    how4_desc:    "我们的团队到达，完美清洁，您在我们离开前检查验收。",

    why_label:    "为什么选择我们",
    why_title:    "为什么选择Signature Luxury Cleaning<br><em>而非大型清洁公司？</em>",
    why_subtitle: "我们深知长时间工作后回家面对凌乱房间有多令人疲惫。这就是我们存在的原因 — 还给您属于自己的夜晚、周末和内心的平静。",
    why1_title:   "背景调查团队",
    why1_desc:    "每位清洁员在进入您家之前都经过严格审查、投保并按我们的豪华标准培训。",
    why2_title:   "环保产品",
    why2_desc:    "对您的家人、宠物和环境安全。我们使用专业级无毒清洁溶液。",
    why3_title:   "100% 满意保证",
    why3_desc:    "完成后，您亲自检查每个区域。如有任何不满意之处，我们当场修正 — 在离开之前。",
    why4_title:   "通过应用预约和付款",
    why4_desc:    "无需电话。打开应用，选择服务，选择时间，安全付款 — 60秒内完成。",

    gallery_label:    "我们的工作",
    gallery_title:    "我们在硅谷<br><em>清洁过哪些家庭？</em>",
    gallery_subtitle: "来自硅谷真实家庭的真实效果。",

    reviews_label:    "客户评价",
    reviews_title:    "硅谷居民<br><em>如何评价我们？</em>",
    reviews_count:    "硅谷数百个次清洁完成",

    areas_label:    "服务区域",
    areas_title:    "我们服务硅谷<br><em>哪些城市？</em>",
    areas_subtitle: "我们服务湾区20多个城市。没看到您的城市？请致电 — 我们可能仍能为您服务。",

    trust_title:  "家庭为何信赖<br><em>Signature Luxury Cleaning？</em>",

    cta_label:    "📱 立即开始",
    cta_title:    "准备好迎接<br><em>一尘不染的家了吗？</em>",
    cta_subtitle: "新客户享受定期服务每次最高15%折扣 — 每周−15%，每两周−10%。打开我们的应用，60秒内预约 — 无需下载。",
    cta_btn:      "<small>支持 iPhone 和 Android</small><strong>打开应用</strong>",
    cta_or:       "或致电我们：",

    footer_desc:     "硅谷最值得信赖的豪华住宅清洁服务。服务圣何塞、帕洛阿尔托、山景城、桑尼维尔及20多个城市。",
    footer_services: "服务",
    footer_contact:  "联系我们",
    footer_areas:    "服务区域",
    footer_copy:     "© 2025 Signature Luxury Cleaning. 版权所有。",
    // AEO Snippets
    aeo_services: "Signature Luxury Cleaning在硅谷提供七项服务：日常清洁、深度清洁、搬入/搬出清洁、施工后清洁、Airbnb周转清洁、办公室清洁和春季大扫除。所有服务均使用环保产品，并提供100%满意保证。",
    aeo_how: "通过我们的网络应用60秒内完成预约：选择服务、选择频率、选择日期和时间、确认地址。通过Stripe支付。我们的团队到达后执行服务，并与您一起确认满意度。",
    aeo_how2: "通过我们的网络应用60秒内完成预约：选择服务、选择频率、选择日期和时间、确认地址。通过Stripe支付。我们的团队到达后执行服务，并与您一起确认满意度。",
    aeo_why: "Signature Luxury Cleaning自2023年起由业主经营，不是连锁店或呼叫中心。每次对话都直接联系到业主。每位清洁工都经过背景调查、担保和亲自培训。我们拥有全额责任保险。",
    aeo_reviews: "Signature Luxury Cleaning在Google上保持5.0★评分，客户来自Palo Alto、Mountain View、Cupertino、Belmont和Burlingame。客户一致赞扬服务的一致性、专业性和对个人空间的尊重。",
    aeo_areas: "我们服务硅谷和半岛的18个城市，从北部的Belmont到南部的San Jose。大多数地区可享受当天清洁服务。服务范围覆盖San Mateo县和Santa Clara县。",
  },

  // ─────────────────────────────────────────────
  hi: {
    topbar_offer:    "नए ग्राहक रिकरिंग सेवा के साथ हर बार 15% तक बचाएं — साप्ताहिक −15%, पाक्षिक −10%",
    topbar_phone:    "कॉल या टेक्स्ट: <span class='accent'>(650) 619-3504</span>",
    topbar_products: "पेशेवर-ग्रेड उत्पाद और उपकरण",
    topbar_rating:   "<span class='accent'>5.0★</span> Google पर परफेक्ट स्कोर",
    topbar_insured:  "बैकग्राउंड-चेक्ड और पूरी तरह बीमाकृत टीम",
    topbar_app:      "डाउनलोड की जरूरत नहीं — किसी भी फोन पर हमारा ऐप खोलें",

    nav_services: "सेवाएं",
    nav_why:      "हमें क्यों चुनें",
    nav_reviews:  "समीक्षाएं",
    nav_areas:    "सेवा क्षेत्र",
    nav_phone:    "📞 (650) 619-3504",
    nav_app:      "📱 हमारा ऐप खोलें",

    hero_title:    "अपना समय वापस पाएं।<br><em>एक बेदाग घर में घर आएं।</em>",
    hero_subtitle: "सिलिकॉन वैली की सबसे भरोसेमंद लक्जरी सफाई सेवा। हम आपके घर की देखभाल करते हैं ताकि आप सबसे महत्वपूर्ण चीजों पर ध्यान दे सकें।",
    hero_badge:    "📍 सैन जोस और सिलिकॉन वैली",
    hero_slots:    "⚡ इस सप्ताह सीमित स्लॉट उपलब्ध",
    hero_btn_app:  "<small>60 सेकंड में बुक करें</small><strong>ऐप खोलें</strong>",
    hero_btn_phone:"📞 (650) 619-3504",

    trust_1: "✅ बैकग्राउंड-चेक्ड टीम",
    trust_2: "🌿 पर्यावरण-अनुकूल उत्पाद",
    trust_3: "💯 100% संतुष्टि गारंटी",
    trust_4: "📱 ऐप से बुक और भुगतान करें",
    trust_5: "⭐ Google 5.0★ रेटिंग",
    trust_6: "🔒 पूरी तरह बीमाकृत",

    services_label:    "हमारी सेवाएं",
    services_title:    "SLC कौन सी<br><em>सफाई सेवाएं प्रदान करता है？</em>",
    services_subtitle: "छह पेशेवर सफाई सेवाएं — हर विजिट पर लक्जरी-स्तर का ध्यान।",

    svc1_name:  "नियमित सफाई",
    svc1_desc:  "साप्ताहिक या द्वि-साप्ताहिक रखरखाव सफाई। हम रसोई, बाथरूम, बेडरूम, लिविंग एरिया और बहुत कुछ संभालते हैं।",
    svc1_price: "$170 से शुरू",
    svc2_name:  "डीप क्लीनिंग",
    svc2_desc:  "ऊपर से नीचे तक गहरी सफाई। पहली बार के ग्राहकों या मौसमी ताजगी के लिए बिल्कुल सही।",
    svc2_price: "$220 से शुरू",
    svc2_badge: "⭐ सबसे लोकप्रिय",
    svc3_name:  "मूव इन / मूव आउट",
    svc3_desc:  "शिफ्ट हो रहे हैं? हम हर इंच को बेदाग छोड़ते हैं।",
    svc3_price: "$220 से शुरू",
    svc4_name:  "निर्माण के बाद सफाई",
    svc4_desc:  "नवीनीकरण की धूल और मलबे को हटाना। हम गंदगी संभालते हैं ताकि आप परिणाम का आनंद ले सकें।",
    svc4_price: "कस्टम कोट",
    svc5_name:  "Airbnb टर्नओवर",
    svc5_desc:  "शॉर्ट-टर्म रेंटल के लिए तेज, विश्वसनीय टर्नओवर सफाई। हर बार मेहमानों के लिए तैयार।",
    svc5_price: "$150 से शुरू",
    svc6_name:  "स्प्रिंग क्लीनिंग",
    svc6_desc:  "पूर्ण मौसमी ताजगी। अलमारी के अंदर, उपकरणों के पीछे — कुछ भी नहीं छूटता।",
    svc6_price: "$270 से शुरू",

    svc_whiteglove_title: "White Glove डीप क्लीन",
    svc_whiteglove_desc:  "हमारी सबसे गहन सफाई। 2 क्लीनरों की टीम आपके फ्रिज, स्टोव, वॉशर, ड्रायर, सोफा और बेड को हटाकर हर छिपी सतह को साफ करती है। पहले/बाद की तस्वीरें शामिल।",

    svc_btn_book:  "ऐप से बुक करें →",
    svc_btn_quote: "कोट के लिए कॉल करें →",

    app_label:    "हमारा ऐप",
    app_title:    "SLC बुकिंग ऐप<br><em>कैसे काम करता है？</em>",
    app_subtitle: "कोई फोन कॉल नहीं। कोई इंतजार नहीं। हमारा ऐप खोलें और कभी भी, कहीं भी अपनी सफाई शेड्यूल पर पूरा नियंत्रण रखें।",
    app_btn:      "<small>iPhone और Android पर काम करता है</small><strong>ऐप खोलें</strong>",
    pwa_steps_title: "होम स्क्रीन पर कैसे जोड़ें:",
    pwa_step1_ios:   "iPhone: शेयर टैप करें → होम स्क्रीन पर जोड़ें",
    pwa_step2_android: "Android: मेनू टैप करें → होम स्क्रीन पर जोड़ें",
    pwa_step3:       "हो गया! नेटिव ऐप की तरह एक्सेस करें",

    how_label:    "यह कैसे काम करता है",
    how_title:    "हमारी बुकिंग प्रक्रिया<br><em>कैसे काम करती है？</em>",
    how_subtitle: "बुकिंग से साफ घर तक — पूरी प्रक्रिया 2 मिनट से कम लेती है।",
    how1_title:   "ऐप खोलें",
    how1_desc:    "iPhone और Android पर तुरंत काम करता है — डाउनलोड की जरूरत नहीं।",
    how2_title:   "सेवा चुनें",
    how2_desc:    "नियमित, डीप, मूव-आउट, Airbnb — अपने घर की जरूरत चुनें।",
    how3_title:   "समय चुनें",
    how3_desc:    "अपने लिए सुविधाजनक तारीख और समय चुनें। इसी सप्ताह उपलब्धता।",
    how4_title:   "आराम करें और आनंद लें",
    how4_desc:    "हमारी टीम आती है, परफेक्ट सफाई करती है, और जाने से पहले आप निरीक्षण करते हैं।",

    why_label:    "हमें क्यों चुनें",
    why_title:    "कॉर्पोरेट मेड सेवाओं की बजाय<br><em>Signature Luxury Cleaning क्यों चुनें？</em>",
    why_subtitle: "हम जानते हैं कि लंबे घंटे काम करने के बाद गंदे घर में आना कितना थका देने वाला होता है। इसीलिए हम मौजूद हैं — आपको आपकी शामें, आपके वीकेंड और मन की शांति वापस देने के लिए।",
    why1_title:   "बैकग्राउंड-चेक्ड टीम",
    why1_desc:    "हर सफाईकर्मी को आपके घर में प्रवेश करने से पहले पूरी तरह से जांचा, बीमाकृत और हमारे लक्जरी मानक के अनुसार प्रशिक्षित किया जाता है।",
    why2_title:   "पर्यावरण-अनुकूल उत्पाद",
    why2_desc:    "आपके परिवार, पालतू जानवरों और पर्यावरण के लिए सुरक्षित। हम पेशेवर-ग्रेड, गैर-विषाक्त सफाई समाधान उपयोग करते हैं।",
    why3_title:   "100% संतुष्टि गारंटी",
    why3_desc:    "जब हम खत्म करते हैं, आप हर क्षेत्र का निरीक्षण करते हैं। अगर कुछ भी संतोषजनक नहीं है, हम वहीं ठीक करते हैं — जाने से पहले।",
    why4_title:   "ऐप से बुक और भुगतान करें",
    why4_desc:    "कोई फोन कॉल नहीं। ऐप खोलें, सेवा चुनें, समय चुनें और सुरक्षित भुगतान करें — 60 सेकंड में।",

    gallery_label:    "हमारा काम",
    gallery_title:    "सिलिकॉन वैली में हमने<br><em>किन घरों की सफाई की है？</em>",
    gallery_subtitle: "सिलिकॉन वैली के असली घरों से असली परिणाम।",

    reviews_label:    "समीक्षाएं",
    reviews_title:    "सिलिकॉन वैली के निवासी<br><em>हमारे बारे में क्या कहते हैं？</em>",
    reviews_count:    "सिलिकॉन वैली में सैकड़ों खुशहाल परिवार",

    areas_label:    "सेवा क्षेत्र",
    areas_title:    "हम सिलिकॉन वैली के<br><em>किन शहरों में सेवा देते हैं？</em>",
    areas_subtitle: "हम बे एरिया के 20+ शहरों में सेवा देते हैं। अपना शहर नहीं दिखा? हमें कॉल करें।",

    trust_title:  "परिवार Signature Luxury Cleaning पर<br><em>क्यों भरोसा करते हैं？</em>",

    cta_label:    "📱 शुरू करें",
    cta_title:    "बेदाग घर के लिए<br><em>तैयार हैं?</em>",
    cta_subtitle: "नए ग्राहक रिकरिंग सेवा के साथ हर बार 15% तक बचाएं — साप्ताहिक −15%, पाक्षिक −10%। ऐप खोलें और 60 सेकंड में बुक करें — डाउनलोड की जरूरत नहीं।",
    cta_btn:      "<small>iPhone और Android पर काम करता है</small><strong>ऐप खोलें</strong>",
    cta_or:       "या हमें कॉल करें:",

    footer_desc:     "सिलिकॉन वैली की सबसे भरोसेमंद लक्जरी आवासीय सफाई सेवा। सैन जोस, पालो आल्टो, माउंटेन व्यू, सनीवेल और 20+ शहरों में सेवा।",
    footer_services: "सेवाएं",
    footer_contact:  "संपर्क",
    footer_areas:    "सेवा क्षेत्र",
    footer_copy:     "© 2025 Signature Luxury Cleaning. सर्वाधिकार सुरक्षित।",
    // AEO Snippets
    aeo_services: "Signature Luxury Cleaning सिलिकॉन वैली में सात सेवाएं प्रदान करता है: नियमित सफाई, गहरी सफाई, मूव इन/आउट, निर्माण के बाद, Airbnb टर्नओवर, कार्यालय सफाई, और वसंत सफाई। सभी में इको-फ्रेंडली उत्पाद और 100% संतुष्टि गारंटी शामिल है।",
    aeo_how: "हमारे वेब ऐप से 60 सेकंड में बुक करें: सेवा चुनें, आवृत्ति चुनें, तारीख और समय चुनें, पता पुष्टि करें। Stripe से भुगतान करें। हमारी टीम पहुंचती है, सेवा करती है, और संतुष्टि सुनिश्चित करने के लिए आपके साथ जांच करती है।",
    aeo_how2: "हमारे वेब ऐप से 60 सेकंड में बुक करें: सेवा चुनें, आवृत्ति चुनें, तारीख और समय चुनें, पता पुष्टि करें। Stripe से भुगतान करें। हमारी टीम पहुंचती है, सेवा करती है, और संतुष्टि सुनिश्चित करने के लिए आपके साथ जांच करती है।",
    aeo_why: "Signature Luxury Cleaning 2023 से मालिक-संचालित है, फ्रेंचाइज़ी या कॉल सेंटर नहीं। हर बातचीत सीधे मालिकों में से एक तक पहुंचती है। हर सफाईकर्मी की पृष्ठभूमि जांच, बॉन्ड और व्यक्तिगत प्रशिक्षण होता है। हमारे पास पूर्ण देयता बीमा है।",
    aeo_reviews: "Signature Luxury Cleaning Google पर 5.0★ रेटिंग रखता है, Palo Alto, Mountain View, Cupertino, Belmont और Burlingame के ग्राहकों की समीक्षाओं के साथ। ग्राहक लगातार निरंतरता, व्यावसायिकता और व्यक्तिगत स्थान के सम्मान का उल्लेख करते हैं।",
    aeo_areas: "हम सिलिकॉन वैली और प्रायद्वीप के 18 शहरों में सेवा देते हैं, उत्तर में Belmont से दक्षिण में San Jose तक। अधिकांश क्षेत्र उसी दिन सफाई के लिए योग्य हैं। सेवा क्षेत्र San Mateo काउंटी और Santa Clara काउंटी को कवर करता है।",
  },

  // ─────────────────────────────────────────────
  tl: {
    topbar_offer:    "Makatipid ng hanggang 15% sa bawat bisita sa recurring service — weekly −15%, bi-weekly −10%",
    topbar_phone:    "Tumawag o mag-text: <span class='accent'>(650) 619-3504</span>",
    topbar_products: "Mga propesyonal na produkto at kagamitan",
    topbar_rating:   "<span class='accent'>5.0★</span> Perpektong marka sa Google Reviews",
    topbar_insured:  "Background-checked at ganap na insured na koponan",
    topbar_app:      "Hindi kailangang mag-download — buksan ang aming app sa anumang telepono",

    nav_services: "Mga Serbisyo",
    nav_why:      "Bakit Kami",
    nav_reviews:  "Mga Review",
    nav_areas:    "Mga Lugar",
    nav_phone:    "📞 (650) 619-3504",
    nav_app:      "📱 Buksan ang App",

    hero_title:    "Ibalik ang Iyong Oras.<br><em>Umuwi sa Malinis na Tahanan.</em>",
    hero_subtitle: "Ang pinaka-mapagkakatiwalaang luxury cleaning service sa Silicon Valley. Inaalagaan namin ang iyong tahanan para makapag-focus ka sa pinakamahalagang bagay.",
    hero_badge:    "📍 San Jose at Silicon Valley",
    hero_slots:    "⚡ Limitadong slot ngayong linggo",
    hero_btn_app:  "<small>Mag-book sa loob ng 60 segundo</small><strong>Buksan ang App</strong>",
    hero_btn_phone:"📞 (650) 619-3504",

    trust_1: "✅ Background-Checked na Koponan",
    trust_2: "🌿 Eco-Friendly na Produkto",
    trust_3: "💯 100% Garantiya ng Kasiyahan",
    trust_4: "📱 Mag-book at Magbayad sa App",
    trust_5: "⭐ Google 5.0★ Rating",
    trust_6: "🔒 Ganap na Insured",

    services_label:    "Aming Mga Serbisyo",
    services_title:    "Anong mga serbisyo ng paglilinis<br><em>ang inaalok ng SLC?</em>",
    services_subtitle: "Anim na propesyonal na serbisyo ng paglilinis — luxury-level na atensyon sa bawat pagbisita.",

    svc1_name:  "Regular na Paglilinis",
    svc1_desc:  "Lingguhang o dalawang lingguhang maintenance cleaning. Inaalagaan namin ang kusina, banyo, kwarto, sala at iba pa.",
    svc1_price: "Mula $170",
    svc2_name:  "Deep Cleaning",
    svc2_desc:  "Masusing paglilinis mula itaas hanggang ibaba. Perpekto para sa mga bagong kliyente o seasonal refresh.",
    svc2_price: "Mula $220",
    svc2_badge: "⭐ Pinaka-popular",
    svc3_name:  "Move In / Move Out",
    svc3_desc:  "Lilipat ka ba? Iniiwan namin ang bawat sulok na malinis.",
    svc3_price: "Mula $220",
    svc4_name:  "Post-Construction",
    svc4_desc:  "Inaalis ang alikabok at basura mula sa renovasyon. Inaalagaan namin ang kalat para ma-enjoy mo ang resulta.",
    svc4_price: "Custom na Quote",
    svc5_name:  "Airbnb Turnover",
    svc5_desc:  "Mabilis at maaasahang turnover cleaning para sa mga short-term rental. Laging handa para sa mga bisita.",
    svc5_price: "Mula $150",
    svc6_name:  "Spring Cleaning",
    svc6_desc:  "Kumpletong seasonal refresh. Loob ng cabinet, likod ng appliance — walang maiiwan.",
    svc6_price: "Mula $270",

    svc_whiteglove_title: "White Glove Deep Clean",
    svc_whiteglove_desc:  "Ang pinaka-masusing paglilinis na inaalok namin. Ang 2-cleaner team ay pisikal na gumagalaw ng iyong refrigerator, stove, washer, dryer, sofa, at kama para linisin ang bawat nakatagong ibabaw. Kasama ang before/after na dokumentasyon.",

    svc_btn_book:  "Mag-book sa App →",
    svc_btn_quote: "Tumawag para sa Quote →",

    app_label:    "Aming App",
    app_title:    "Paano gumagana ang<br><em>SLC booking app?</em>",
    app_subtitle: "Walang tawag sa telepono. Walang paghihintay. Buksan ang aming app at kontrolin ang iyong cleaning schedule — kahit saan, kahit kailan.",
    app_btn:      "<small>Gumagana sa iPhone at Android</small><strong>Buksan ang App</strong>",
    pwa_steps_title: "Paano idagdag sa home screen:",
    pwa_step1_ios:   "iPhone: I-tap ang Share → Add to Home Screen",
    pwa_step2_android: "Android: I-tap ang Menu → Add to Home Screen",
    pwa_step3:       "Tapos na! I-access tulad ng native app",

    how_label:    "Paano Ito Gumagana",
    how_title:    "Paano gumagana ang aming<br><em>proseso ng pag-book?</em>",
    how_subtitle: "Mula sa pag-book hanggang sa malinis na tahanan — ang buong proseso ay tumatagal ng wala pang 2 minuto.",
    how1_title:   "Buksan ang App",
    how1_desc:    "Gumagana agad sa iPhone at Android — hindi kailangang mag-download.",
    how2_title:   "Piliin ang Serbisyo",
    how2_desc:    "Regular, deep, move-out, Airbnb — piliin ang kailangan ng iyong tahanan.",
    how3_title:   "Piliin ang Oras",
    how3_desc:    "Pumili ng petsa at oras na maginhawa para sa iyo. Available ngayong linggo.",
    how4_title:   "Mag-relax at Mag-enjoy",
    how4_desc:    "Darating ang aming koponan, maglilinis nang perpekto, at ikaw ang mag-iinspect bago kami umalis.",

    why_label:    "Bakit Piliin Kami",
    why_title:    "Bakit piliin ang Signature Luxury Cleaning<br><em>kaysa sa mga corporate maid service?</em>",
    why_subtitle: "Alam namin kung gaano kapagod ang magtrabaho nang matagal at umuwi pa rin sa makalat na bahay. Kaya naman kami nandito — para ibalik sa iyo ang iyong mga gabi, weekend, at kapayapaan ng isip.",
    why1_title:   "Background-Checked na Koponan",
    why1_desc:    "Bawat manglilinis ay masusing sinusuri, insured, at sinanay ayon sa aming luxury na pamantayan bago pumasok sa iyong tahanan.",
    why2_title:   "Eco-Friendly na Produkto",
    why2_desc:    "Ligtas para sa iyong pamilya, alagang hayop, at kalikasan. Gumagamit kami ng propesyonal na non-toxic na solusyon sa paglilinis.",
    why3_title:   "100% Garantiya ng Kasiyahan",
    why3_desc:    "Kapag tapos na kami, ikaw ang mag-iinspect sa bawat lugar. Kung may hindi ka nasisiyahan, aayusin namin agad — bago kami umalis.",
    why4_title:   "Mag-book at Magbayad sa App",
    why4_desc:    "Walang tawag sa telepono. Buksan ang app, piliin ang serbisyo, pumili ng oras, at magbayad nang ligtas — lahat sa loob ng 60 segundo.",

    gallery_label:    "Aming Gawa",
    gallery_title:    "Anong mga tahanan ang aming<br><em>nalinis sa Silicon Valley?</em>",
    gallery_subtitle: "Tunay na resulta mula sa tunay na mga tahanan sa buong Silicon Valley.",

    reviews_label:    "Mga Review",
    reviews_title:    "Ano ang sinasabi ng mga residente<br><em>ng Silicon Valley tungkol sa amin?</em>",
    reviews_count:    "Daan-daang masasayang pamilya sa buong Silicon Valley",

    areas_label:    "Mga Lugar na Pinaglilingkuran",
    areas_title:    "Aling mga lungsod ng Silicon Valley<br><em>ang aming pinaglilingkuran?</em>",
    areas_subtitle: "Naglilingkod kami sa 20+ lungsod sa Bay Area. Hindi mo nakita ang iyong lungsod? Tumawag sa amin.",

    trust_title:  "Bakit pinagkakatiwalaan ng mga pamilya<br><em>ang Signature Luxury Cleaning?</em>",

    cta_label:    "📱 Magsimula",
    cta_title:    "Handa na para sa<br><em>Malinis na Tahanan?</em>",
    cta_subtitle: "Makatipid ng hanggang 15% sa bawat bisita sa recurring service — weekly −15%, bi-weekly −10%. Buksan ang app at mag-book sa loob ng 60 segundo — hindi kailangang mag-download.",
    cta_btn:      "<small>Gumagana sa iPhone at Android</small><strong>Buksan ang App</strong>",
    cta_or:       "O tumawag sa amin:",

    footer_desc:     "Ang pinaka-mapagkakatiwalaang luxury residential cleaning service sa Silicon Valley. Naglilingkod sa San Jose, Palo Alto, Mountain View, Sunnyvale at 20+ lungsod.",
    footer_services: "Mga Serbisyo",
    footer_contact:  "Makipag-ugnayan",
    footer_areas:    "Mga Lugar",
    footer_copy:     "© 2025 Signature Luxury Cleaning. Lahat ng karapatan ay nakalaan.",
    // AEO Snippets
    aeo_services: "Nag-aalok ang Signature Luxury Cleaning ng pitong serbisyo sa Silicon Valley: Regular Cleaning, Deep Cleaning, Move In/Out, Post-Construction, Airbnb Turnover, Office Cleaning, at Spring Cleaning. Lahat ay may kasamang eco-friendly na produkto at 100% satisfaction guarantee.",
    aeo_how: "Mag-book sa pamamagitan ng aming web app sa loob ng 60 segundo: pumili ng serbisyo, piliin ang frequency, pumili ng petsa at oras, kumpirmahin ang address. Magbayad sa pamamagitan ng Stripe. Darating ang aming team, gagawin ang serbisyo, at susuriin kasama mo para matiyak ang kasiyahan.",
    aeo_how2: "Mag-book sa pamamagitan ng aming web app sa loob ng 60 segundo: pumili ng serbisyo, piliin ang frequency, pumili ng petsa at oras, kumpirmahin ang address. Magbayad sa pamamagitan ng Stripe. Darating ang aming team, gagawin ang serbisyo, at susuriin kasama mo para matiyak ang kasiyahan.",
    aeo_why: "Ang Signature Luxury Cleaning ay owner-operated mula 2023, hindi franchise o call center. Bawat pag-uusap ay direktang naabot ang isa sa mga may-ari. Bawat cleaner ay background-checked, bonded, at personal na sinanay. May full liability insurance kami.",
    aeo_reviews: "Ang Signature Luxury Cleaning ay may 5.0★ rating sa Google mula sa mga kliyente sa Palo Alto, Mountain View, Cupertino, Belmont, at Burlingame. Palaging binabanggit ng mga kliyente ang consistency, professionalism, at paggalang sa personal na espasyo.",
    aeo_areas: "Naglilingkod kami sa 18 lungsod sa Silicon Valley at Peninsula, mula Belmont sa hilaga hanggang San Jose sa timog. Karamihan ng lugar ay kwalipikado para sa same-day cleaning. Saklaw ng serbisyo ang San Mateo County at Santa Clara County.",
  },

  // ─────────────────────────────────────────────
  vi: {
    topbar_offer:    "Khách mới tiết kiệm đến 15% mỗi lần với dịch vụ định kỳ — hàng tuần −15%, hai tuần −10%",
    topbar_phone:    "Gọi hoặc nhắn tin: <span class='accent'>(650) 619-3504</span>",
    topbar_products: "Sản phẩm và thiết bị chuyên nghiệp",
    topbar_rating:   "<span class='accent'>5.0★</span> Điểm hoàn hảo trên Google Reviews",
    topbar_insured:  "Đội ngũ đã kiểm tra lý lịch và bảo hiểm đầy đủ",
    topbar_app:      "Không cần tải xuống — mở ứng dụng trên bất kỳ điện thoại nào",

    nav_services: "Dịch Vụ",
    nav_why:      "Tại Sao Chọn Chúng Tôi",
    nav_reviews:  "Đánh Giá",
    nav_areas:    "Khu Vực",
    nav_phone:    "📞 (650) 619-3504",
    nav_app:      "📱 Mở Ứng Dụng",

    hero_title:    "Lấy Lại Thời Gian Của Bạn.<br><em>Về Nhà Với Ngôi Nhà Sạch Bóng.</em>",
    hero_subtitle: "Dịch vụ dọn dẹp sang trọng đáng tin cậy nhất Silicon Valley. Chúng tôi chăm sóc ngôi nhà của bạn để bạn tập trung vào những điều quan trọng nhất.",
    hero_badge:    "📍 San Jose và Silicon Valley",
    hero_slots:    "⚡ Còn ít chỗ trống trong tuần này",
    hero_btn_app:  "<small>Đặt lịch trong 60 giây</small><strong>Mở Ứng Dụng</strong>",
    hero_btn_phone:"📞 (650) 619-3504",

    trust_1: "✅ Đội Ngũ Đã Kiểm Tra Lý Lịch",
    trust_2: "🌿 Sản Phẩm Thân Thiện Môi Trường",
    trust_3: "💯 Đảm Bảo 100% Hài Lòng",
    trust_4: "📱 Đặt Lịch & Thanh Toán Qua App",
    trust_5: "⭐ Google 5.0★",
    trust_6: "🔒 Bảo Hiểm Đầy Đủ",

    services_label:    "Dịch Vụ Của Chúng Tôi",
    services_title:    "SLC cung cấp<br><em>những dịch vụ dọn dẹp nào?</em>",
    services_subtitle: "Sáu dịch vụ dọn dẹp chuyên nghiệp — chú ý đến từng chi tiết ở mức độ sang trọng trong mỗi lần ghé thăm.",

    svc1_name:  "Dọn Dẹp Thường Xuyên",
    svc1_desc:  "Dọn dẹp bảo trì hàng tuần hoặc hai tuần một lần. Chúng tôi xử lý bếp, phòng tắm, phòng ngủ, phòng khách và nhiều hơn nữa.",
    svc1_price: "Từ $170",
    svc2_name:  "Dọn Dẹp Sâu",
    svc2_desc:  "Dọn dẹp sâu từ trên xuống dưới. Hoàn hảo cho khách hàng lần đầu hoặc làm mới theo mùa.",
    svc2_price: "Từ $220",
    svc2_badge: "⭐ Phổ Biến Nhất",
    svc3_name:  "Dọn Khi Chuyển Nhà",
    svc3_desc:  "Đang chuyển vào hay chuyển ra? Chúng tôi để lại từng góc nhà sạch bóng.",
    svc3_price: "Từ $220",
    svc4_name:  "Dọn Sau Xây Dựng",
    svc4_desc:  "Loại bỏ bụi và mảnh vụn sau cải tạo. Chúng tôi xử lý mớ hỗn độn để bạn tận hưởng kết quả.",
    svc4_price: "Báo Giá Tùy Chỉnh",
    svc5_name:  "Dọn Airbnb",
    svc5_desc:  "Dọn dẹp nhanh chóng, đáng tin cậy cho thuê ngắn hạn. Luôn sẵn sàng đón khách.",
    svc5_price: "Từ $150",
    svc6_name:  "Tổng Vệ Sinh",
    svc6_desc:  "Làm mới toàn diện theo mùa. Bên trong tủ, sau thiết bị — không bỏ sót gì.",
    svc6_price: "Từ $270",

    svc_whiteglove_title: "White Glove Vệ Sinh Sâu",
    svc_whiteglove_desc:  "Dịch vụ vệ sinh kỹ lưỡng nhất của chúng tôi. Đội 2 người sẽ di chuyển tủ lạnh, bếp, máy giặt, máy sấy, sofa và giường để làm sạch mọi bề mặt ẩn. Bao gồm ảnh trước/sau.",

    svc_btn_book:  "Đặt Qua App →",
    svc_btn_quote: "Gọi Để Báo Giá →",

    app_label:    "Ứng Dụng Của Chúng Tôi",
    app_title:    "Ứng dụng đặt lịch SLC<br><em>hoạt động như thế nào?</em>",
    app_subtitle: "Không cần gọi điện. Không cần chờ đợi. Mở ứng dụng và kiểm soát hoàn toàn lịch dọn dẹp của bạn — bất cứ lúc nào, bất cứ đâu.",
    app_btn:      "<small>Hoạt động trên iPhone và Android</small><strong>Mở Ứng Dụng</strong>",
    pwa_steps_title: "Cách thêm vào màn hình chính:",
    pwa_step1_ios:   "iPhone: Nhấn Chia sẻ → Thêm vào Màn hình Chính",
    pwa_step2_android: "Android: Nhấn Menu → Thêm vào Màn hình Chính",
    pwa_step3:       "Xong! Truy cập như ứng dụng gốc",

    how_label:    "Cách Thức Hoạt Động",
    how_title:    "Quy trình đặt lịch<br><em>của chúng tôi hoạt động thế nào?</em>",
    how_subtitle: "Từ đặt lịch đến ngôi nhà sạch — toàn bộ quá trình mất chưa đến 2 phút.",
    how1_title:   "Mở Ứng Dụng",
    how1_desc:    "Hoạt động ngay trên iPhone và Android — không cần tải xuống.",
    how2_title:   "Chọn Dịch Vụ",
    how2_desc:    "Thường xuyên, sâu, chuyển nhà, Airbnb — chọn những gì ngôi nhà bạn cần.",
    how3_title:   "Chọn Thời Gian",
    how3_desc:    "Chọn ngày và giờ phù hợp với bạn. Có thể đặt lịch trong tuần này.",
    how4_title:   "Thư Giãn & Tận Hưởng",
    how4_desc:    "Đội của chúng tôi đến, dọn dẹp hoàn hảo, và bạn kiểm tra trước khi chúng tôi rời đi.",

    why_label:    "Tại Sao Chọn Chúng Tôi",
    why_title:    "Tại sao chọn Signature Luxury Cleaning<br><em>thay vì dịch vụ dọn dẹp doanh nghiệp?</em>",
    why_subtitle: "Chúng tôi hiểu cảm giác mệt mỏi khi làm việc nhiều giờ và vẫn phải về nhà với mớ bừa bộn. Đó là lý do chúng tôi tồn tại — để trả lại cho bạn những buổi tối, cuối tuần và sự bình yên trong tâm hồn.",
    why1_title:   "Đội Ngũ Đã Kiểm Tra Lý Lịch",
    why1_desc:    "Mỗi nhân viên dọn dẹp đều được kiểm tra kỹ lưỡng, bảo hiểm và đào tạo theo tiêu chuẩn sang trọng của chúng tôi trước khi vào nhà bạn.",
    why2_title:   "Sản Phẩm Thân Thiện Môi Trường",
    why2_desc:    "An toàn cho gia đình, thú cưng và môi trường của bạn. Chúng tôi sử dụng dung dịch làm sạch chuyên nghiệp, không độc hại.",
    why3_title:   "Đảm Bảo 100% Hài Lòng",
    why3_desc:    "Khi chúng tôi hoàn thành, bạn kiểm tra từng khu vực. Nếu có gì không hài lòng, chúng tôi sửa ngay tại chỗ — trước khi rời đi.",
    why4_title:   "Đặt Lịch & Thanh Toán Qua App",
    why4_desc:    "Không cần gọi điện. Mở app, chọn dịch vụ, chọn thời gian và thanh toán an toàn — tất cả trong 60 giây.",

    gallery_label:    "Công Việc Của Chúng Tôi",
    gallery_title:    "Chúng tôi đã dọn dẹp<br><em>những ngôi nhà nào ở Silicon Valley?</em>",
    gallery_subtitle: "Kết quả thực tế từ những ngôi nhà thực tế trên khắp Silicon Valley.",

    reviews_label:    "Đánh Giá",
    reviews_title:    "Cư dân Silicon Valley<br><em>nói gì về chúng tôi?</em>",
    reviews_count:    "Hàng trăm gia đình hạnh phúc trên khắp Silicon Valley",

    areas_label:    "Khu Vực Phục Vụ",
    areas_title:    "Chúng tôi phục vụ<br><em>những thành phố nào ở Silicon Valley?</em>",
    areas_subtitle: "Chúng tôi phục vụ hơn 20 thành phố trên khắp Bay Area. Không thấy thành phố của bạn? Hãy gọi cho chúng tôi.",

    trust_title:  "Tại sao các gia đình tin tưởng<br><em>Signature Luxury Cleaning?</em>",

    cta_label:    "📱 Bắt Đầu",
    cta_title:    "Sẵn Sàng Cho<br><em>Ngôi Nhà Sạch Bóng?</em>",
    cta_subtitle: "Khách mới tiết kiệm đến 15% mỗi lần với dịch vụ định kỳ — hàng tuần −15%, hai tuần −10%. Mở ứng dụng và đặt lịch trong 60 giây — không cần tải xuống.",
    cta_btn:      "<small>Hoạt động trên iPhone và Android</small><strong>Mở Ứng Dụng</strong>",
    cta_or:       "Hoặc gọi cho chúng tôi:",

    footer_desc:     "Dịch vụ dọn dẹp nhà ở sang trọng đáng tin cậy nhất Silicon Valley. Phục vụ San Jose, Palo Alto, Mountain View, Sunnyvale và hơn 20 thành phố.",
    footer_services: "Dịch Vụ",
    footer_contact:  "Liên Hệ",
    footer_areas:    "Khu Vực",
    footer_copy:     "© 2025 Signature Luxury Cleaning. Bảo lưu mọi quyền.",
    // AEO Snippets
    aeo_services: "Signature Luxury Cleaning cung cấp bảy dịch vụ tại Silicon Valley: Dọn dẹp Thường xuyên, Dọn dẹp Sâu, Dọn nhà Vào/Ra, Sau Xây dựng, Airbnb Turnover, Dọn Văn phòng, và Dọn dẹp Mùa xuân. Tất cả đều sử dụng sản phẩm thân thiện môi trường và bảo đảm hài lòng 100%.",
    aeo_how: "Đặt lịch qua ứng dụng web trong vòng 60 giây: chọn dịch vụ, chọn tần suất, chọn ngày giờ, xác nhận địa chỉ. Thanh toán qua Stripe. Đội ngũ đến, thực hiện dịch vụ, và kiểm tra cùng bạn để đảm bảo hài lòng.",
    aeo_how2: "Đặt lịch qua ứng dụng web trong vòng 60 giây: chọn dịch vụ, chọn tần suất, chọn ngày giờ, xác nhận địa chỉ. Thanh toán qua Stripe. Đội ngũ đến, thực hiện dịch vụ, và kiểm tra cùng bạn để đảm bảo hài lòng.",
    aeo_why: "Signature Luxury Cleaning do chủ sở hữu điều hành từ 2023, không phải nhượng quyền hay tổng đài. Mọi cuộc trò chuyện đều đến trực tiếp chủ sở hữu. Mọi nhân viên đều được kiểm tra lý lịch, bảo lãnh và đào tạo cá nhân. Chúng tôi có bảo hiểm trách nhiệm đầy đủ.",
    aeo_reviews: "Signature Luxury Cleaning giữ đánh giá 5.0★ trên Google với nhận xét từ khách hàng ở Palo Alto, Mountain View, Cupertino, Belmont và Burlingame. Khách hàng luôn nhắc đến sự nhất quán, chuyên nghiệp và tôn trọng không gian cá nhân.",
    aeo_areas: "Chúng tôi phục vụ 18 thành phố ở Silicon Valley và Bán đảo, từ Belmont ở phía bắc đến San Jose ở phía nam. Hầu hết khu vực đều có dịch vụ dọn dẹp trong ngày. Phạm vi phục vụ bao gồm Quận San Mateo và Quận Santa Clara.",
  },

  // ─────────────────────────────────────────────
  ko: {
    topbar_offer:    "신규 고객 정기 서비스로 매회 최대 15% 절약 — 주간 −15%, 격주 −10%",
    topbar_phone:    "전화 또는 문자: <span class='accent'>(650) 619-3504</span>",
    topbar_products: "전문가급 제품 및 장비",
    topbar_rating:   "<span class='accent'>5.0★</span> Google 리뷰 만점",
    topbar_insured:  "신원 조회 완료, 완전 보험 가입 팀",
    topbar_app:      "다운로드 불필요 — 어떤 폰에서도 앱 바로 열기",

    nav_services: "서비스",
    nav_why:      "왜 우리를 선택하나요",
    nav_reviews:  "리뷰",
    nav_areas:    "서비스 지역",
    nav_phone:    "📞 (650) 619-3504",
    nav_app:      "📱 앱 열기",

    hero_title:    "당신의 시간을 되찾으세요.<br><em>깨끗한 집으로 귀가하세요.</em>",
    hero_subtitle: "실리콘밸리에서 가장 신뢰받는 럭셔리 청소 서비스. 저희가 집을 돌봐드리니 가장 중요한 일에 집중하세요.",
    hero_badge:    "📍 산호세 및 실리콘밸리",
    hero_slots:    "⚡ 이번 주 예약 자리 한정",
    hero_btn_app:  "<small>60초 안에 예약</small><strong>앱 열기</strong>",
    hero_btn_phone:"📞 (650) 619-3504",

    trust_1: "✅ 신원 조회 완료 팀",
    trust_2: "🌿 친환경 제품",
    trust_3: "💯 100% 만족 보장",
    trust_4: "📱 앱으로 예약 및 결제",
    trust_5: "⭐ Google 5.0★",
    trust_6: "🔒 완전 보험 가입",

    services_label:    "서비스",
    services_title:    "SLC는 어떤<br><em>청소 서비스를 제공하나요?</em>",
    services_subtitle: "6가지 전문 청소 서비스 — 매 방문마다 럭셔리 수준의 세심한 관리.",

    svc1_name:  "정기 청소",
    svc1_desc:  "주 1회 또는 격주 유지 청소. 주방, 욕실, 침실, 거실 등을 담당합니다.",
    svc1_price: "$170부터",
    svc2_name:  "딥 클리닝",
    svc2_desc:  "위에서 아래까지 철저한 심층 청소. 첫 고객이나 계절별 리프레시에 완벽합니다.",
    svc2_price: "$220부터",
    svc2_badge: "⭐ 가장 인기",
    svc3_name:  "이사 청소",
    svc3_desc:  "이사하시나요? 새 출발을 위해 구석구석 깨끗하게 청소해 드립니다.",
    svc3_price: "$220부터",
    svc4_name:  "공사 후 청소",
    svc4_desc:  "리모델링 먼지와 잔해 제거. 저희가 정리하니 결과를 즐기세요.",
    svc4_price: "맞춤 견적",
    svc5_name:  "에어비앤비 청소",
    svc5_desc:  "단기 임대를 위한 빠르고 신뢰할 수 있는 청소. 항상 게스트 맞이 준비 완료.",
    svc5_price: "$150부터",
    svc6_name:  "대청소",
    svc6_desc:  "완전한 계절별 리프레시. 수납장 안, 가전제품 뒤 — 빠짐없이.",
    svc6_price: "$270부터",

    svc_whiteglove_title: "White Glove 딥 클리닝",
    svc_whiteglove_desc:  "저희가 제공하는 가장 철저한 청소입니다. 2인 팀이 냉장고, 가스렌인지, 세탁기, 건조기, 소파, 침대를 이동하여 모든 숨겨진 표면을 청소합니다. 전후 사진 문서 포함.",

    svc_btn_book:  "앱으로 예약 →",
    svc_btn_quote: "견적 문의 전화 →",

    app_label:    "앱",
    app_title:    "SLC 예약 앱은<br><em>어떻게 작동하나요?</em>",
    app_subtitle: "전화 불필요. 대기 불필요. 앱을 열고 언제 어디서나 청소 일정을 완전히 관리하세요.",
    app_btn:      "<small>iPhone과 Android에서 작동</small><strong>앱 열기</strong>",
    pwa_steps_title: "홈 화면에 추가하는 방법:",
    pwa_step1_ios:   "iPhone: 공유 탭 → 홈 화면에 추가",
    pwa_step2_android: "Android: 메뉴 탭 → 홈 화면에 추가",
    pwa_step3:       "완료! 네이티브 앱처럼 접근",

    how_label:    "이용 방법",
    how_title:    "예약 과정은<br><em>어떻게 진행되나요?</em>",
    how_subtitle: "예약부터 깨끗한 집까지 — 전체 과정이 2분도 안 걸립니다.",
    how1_title:   "앱 열기",
    how1_desc:    "iPhone과 Android에서 즉시 작동 — 다운로드 불필요.",
    how2_title:   "서비스 선택",
    how2_desc:    "정기, 딥, 이사, 에어비앤비 — 집에 필요한 것을 선택하세요.",
    how3_title:   "시간 선택",
    how3_desc:    "편한 날짜와 시간을 선택하세요. 이번 주 예약 가능.",
    how4_title:   "편히 쉬며 즐기세요",
    how4_desc:    "팀이 도착해 완벽하게 청소하고, 떠나기 전에 고객님이 직접 확인합니다.",

    why_label:    "왜 우리를 선택하나요",
    why_title:    "대형 청소 업체 대신<br><em>Signature Luxury Cleaning을 선택해야 하는 이유는?</em>",
    why_subtitle: "긴 시간 일하고 돌아온 집이 지저분할 때 얼마나 지치는지 압니다. 그래서 저희가 있습니다 — 당신의 저녁, 주말, 그리고 마음의 평화를 되돌려 드리기 위해.",
    why1_title:   "신원 조회 완료 팀",
    why1_desc:    "모든 청소 직원은 고객님의 집에 들어오기 전에 철저히 심사되고, 보험에 가입되며, 럭셔리 기준에 따라 교육받습니다.",
    why2_title:   "친환경 제품",
    why2_desc:    "가족, 반려동물, 환경에 안전합니다. 전문가급 무독성 청소 솔루션을 사용합니다.",
    why3_title:   "100% 만족 보장",
    why3_desc:    "청소가 끝나면 고객님이 직접 모든 구역을 확인합니다. 마음에 들지 않는 부분이 있으면 떠나기 전에 바로 수정합니다.",
    why4_title:   "앱으로 예약 및 결제",
    why4_desc:    "전화 불필요. 앱을 열고 서비스를 선택하고 시간을 정하고 안전하게 결제 — 60초 안에 모두 완료.",

    gallery_label:    "작업 사례",
    gallery_title:    "실리콘밸리에서 어떤<br><em>집들을 청소했나요?</em>",
    gallery_subtitle: "실리콘밸리 실제 가정의 실제 결과.",

    reviews_label:    "리뷰",
    reviews_title:    "실리콘밸리 주민들은<br><em>저희에 대해 뭐라고 하나요?</em>",
    reviews_count:    "실리콘밸리 전역의 수백 개 행복한 가정",

    areas_label:    "서비스 지역",
    areas_title:    "실리콘밸리의 어떤 도시에서<br><em>서비스를 제공하나요?</em>",
    areas_subtitle: "베이 에어리어 20개 이상의 도시에서 서비스합니다. 도시가 없나요? 전화주세요.",

    trust_title:  "가족들이 Signature Luxury Cleaning을<br><em>신뢰하는 이유는?</em>",

    cta_label:    "📱 시작하기",
    cta_title:    "깨끗한 집을 위해<br><em>준비되셨나요?</em>",
    cta_subtitle: "신규 고객 정기 서비스로 매회 최대 15% 절약 — 주간 −15%, 격주 −10%. 앱을 열고 60초 안에 예약하세요 — 다운로드 불필요.",
    cta_btn:      "<small>iPhone과 Android에서 작동</small><strong>앱 열기</strong>",
    cta_or:       "또는 전화하세요:",

    footer_desc:     "실리콘밸리에서 가장 신뢰받는 럭셔리 주거 청소 서비스. 산호세, 팔로알토, 마운틴뷰, 서니베일 및 20개 이상의 도시 서비스.",
    footer_services: "서비스",
    footer_contact:  "연락처",
    footer_areas:    "서비스 지역",
    footer_copy:     "© 2025 Signature Luxury Cleaning. 모든 권리 보유.",
    // AEO Snippets
    aeo_services: "Signature Luxury Cleaning은 실리콘밸리에서 7가지 서비스를 제공합니다: 정기 청소, 정밀 청소, 입주/퇴거 청소, 공사 후 청소, Airbnb 턴오버, 사무실 청소, 봄맞이 청소. 모든 서비스에 친환경 제품과 100% 만족 보장이 포함됩니다.",
    aeo_how: "웹 앱으로 60초 안에 예약하세요: 서비스 선택, 빈도 선택, 날짜와 시간 선택, 주소 확인. Stripe로 결제. 팀이 도착하여 서비스를 수행하고, 만족을 확인하기 위해 함께 점검합니다.",
    aeo_how2: "웹 앱으로 60초 안에 예약하세요: 서비스 선택, 빈도 선택, 날짜와 시간 선택, 주소 확인. Stripe로 결제. 팀이 도착하여 서비스를 수행하고, 만족을 확인하기 위해 함께 점검합니다.",
    aeo_why: "Signature Luxury Cleaning은 2023년부터 오너가 직접 운영하며, 프랜차이즈나 콜센터가 아닙니다. 모든 대화는 오너에게 직접 전달됩니다. 모든 청소원은 신원 조회, 보증, 개인 교육을 받습니다. 전액 배상 보험에 가입되어 있습니다.",
    aeo_reviews: "Signature Luxury Cleaning은 Google에서 5.0★ 평점을 유지하며, Palo Alto, Mountain View, Cupertino, Belmont, Burlingame 고객들의 리뷰가 있습니다. 고객들은 일관성, 전문성, 개인 공간 존중을 꾸준히 언급합니다.",
    aeo_areas: "실리콘밸리와 반도 전역 18개 도시에 서비스를 제공합니다. 북쪽 Belmont부터 남쪽 San Jose까지. 대부분 지역에서 당일 청소가 가능합니다. 서비스 범위는 San Mateo 카운티와 Santa Clara 카운티를 포함합니다.",
  }

};

// ─────────────────────────────────────────────
// Language detection and application
// ─────────────────────────────────────────────

const SUPPORTED_LANGS = ['en', 'zh', 'hi', 'tl', 'vi', 'ko'];

function detectLanguage() {
  // 1. Check URL param (?lang=zh)
  const urlParam = new URLSearchParams(window.location.search).get('lang');
  if (urlParam && SUPPORTED_LANGS.includes(urlParam)) return urlParam;

  // 2. Check localStorage (user manually selected before)
  const saved = localStorage.getItem('slc_lang');
  if (saved && SUPPORTED_LANGS.includes(saved)) return saved;

  // 3. Detect from browser/device language
  const browserLangs = navigator.languages || [navigator.language || 'en'];
  for (const lang of browserLangs) {
    const code = lang.split('-')[0].toLowerCase();
    if (SUPPORTED_LANGS.includes(code)) return code;
  }

  return 'en'; // default
}

function applyTranslations(lang) {
  const t = TRANSLATIONS[lang] || TRANSLATIONS['en'];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key] !== undefined) {
      el.innerHTML = t[key];
    }
  });

  // Update html lang attribute
  document.documentElement.lang = lang;

  // Update active state on language switcher
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
  });

  // Save to localStorage
  localStorage.setItem('slc_lang', lang);
}

function initLanguage() {
  const lang = detectLanguage();
  applyTranslations(lang);

  // Wire up language switcher buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const selectedLang = btn.getAttribute('data-lang');
      applyTranslations(selectedLang);
    });
  });
}

// Run on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initLanguage);
} else {
  initLanguage();
}
