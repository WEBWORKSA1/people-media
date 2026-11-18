/* People.Media site configuration — edit these values, no other code changes needed. */
window.PM_CONFIG = {
  siteName: "People.Media",
  // Google AdSense publisher (auto ads are loaded in every page <head>)
  adsenseClient: "ca-pub-6620975821265271",

  // Optional payment handles. Leave "" to hide a button; the pledge form always works.
  // Example: paypalMe: "peoplemedia"  -> https://paypal.me/peoplemedia
  payments: {
    paypalMe: "",
    buyMeACoffee: "",
    kofi: "",
    upiId: "",        // e.g. "name@bank" — shows a UPI deep link for Indian supporters
    stripeLink: ""    // full https://buy.stripe.com/... payment link
  },

  // Public fundraising goal shown on the Support page (edit as pledges arrive)
  fundraising: { goal: 25000, raised: 0, currency: "$", supporters: 0, campaign: "Founding Supporters 2026–27" },

  // Monthly story contest — the countdown targets this date (ISO, local time)
  contest: { theme: "The Day Everything Changed", closes: "2026-12-31T23:59:00", prizePool: "$1,000+" },

  // YouTube channels the auto-refresh workflow pulls from (see scripts/refresh.py)
  youtubeFallback: [
    { title: "TED", url: "https://www.youtube.com/@TED" },
    { title: "TEDx Talks", url: "https://www.youtube.com/@TEDx" },
    { title: "People.Media on YouTube (search)", url: "https://www.youtube.com/results?search_query=inspiring+human+stories" }
  ]
};
