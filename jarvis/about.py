"""Creator information shown in the CLI, web UI and API."""

CREATOR = {
    "name": "Sami Bajwa",
    "brand": "Samioutic",
    "role": "Full-Stack Developer, Technical Consultant, AI Educator and Content Creator",
    "location": "Lahore, Pakistan",
    "email": "samibajwa491@gmail.com",
    "website": "https://samioutic.com",
    "facebook": "https://www.facebook.com/samibajwaisking",
    "instagram": "https://www.instagram.com/samibajwaisking",
    "threads": "https://www.threads.net/@samibajwaisking",
    "tiktok": "https://www.tiktok.com/@samibajwaisking",
    "linkedin": "https://www.linkedin.com/in/samibajwa106",
}

TAGLINE = "Free for everyone. Built to teach. Made by Sami Bajwa."


def about_text() -> str:
    c = CREATOR
    return (
        f"Jarvis AI was created by {c['name']} ({c['brand']}), {c['role']} based in {c['location']}.\n"
        f"Email:     {c['email']}\n"
        f"Website:   {c['website']}\n"
        f"Facebook:  {c['facebook']}\n"
        f"Instagram: {c['instagram']}\n"
        f"Threads:   {c['threads']}\n"
        f"TikTok:    {c['tiktok']}\n"
        f"LinkedIn:  {c['linkedin']}\n"
        "\nJarvis is free and open source (MIT). If it helps you, star the repo on GitHub, "
        "and an optional $1 one-time donation helps keep it growing."
    )
