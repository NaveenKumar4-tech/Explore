"""Seeds countries + places and generates a placeholder SVG image per country.
Replace the files in static/img/ with real photos any time (keep the same file names,
or change the `image` value below)."""
import os
from models import Country, Place, db

IMG_DIR = os.path.join(os.path.dirname(__file__), "static", "img")

COUNTRIES = [
    {"slug": "japan", "name": "Japan", "flag": "🇯🇵", "continent": "Asia", "colors": ("#1d3557", "#e63946"),
     "tagline": "Ancient temples, neon cities, bullet trains.",
     "description": "Japan blends centuries-old tradition with cutting-edge modern life. Walk through lantern-lit Kyoto streets in the morning, ride a bullet train to Tokyo by lunch, and end the day with ramen in a tiny alley bar.",
     "best_time": "March–May, Oct–Nov", "currency": "Japanese Yen (JPY)", "language": "Japanese",
     "highlights": ["Cherry blossom season", "Mount Fuji views", "Onsen hot springs", "World-class food"],
     "places": [("Tokyo City Break", "Shibuya, Asakusa, teamLab and day trips to Nikko.", 5, 1150),
                ("Kyoto Temples & Tea", "Fushimi Inari, Arashiyama bamboo grove and a tea ceremony.", 4, 890),
                ("Mount Fuji & Hakone", "Lake Ashi cruise, ropeway rides and a ryokan stay.", 3, 720)]},
    {"slug": "france", "name": "France", "flag": "🇫🇷", "continent": "Europe", "colors": ("#1b3a6b", "#8ecae6"),
     "tagline": "Art, wine and cafés on every corner.",
     "description": "From the Eiffel Tower to lavender fields in Provence, France rewards slow travel. Spend mornings in museums, afternoons at sidewalk cafés and evenings tasting regional wine.",
     "best_time": "April–June, Sep–Oct", "currency": "Euro (EUR)", "language": "French",
     "highlights": ["Louvre & Musée d'Orsay", "Provence lavender", "Loire châteaux", "Riviera beaches"],
     "places": [("Paris Classic", "Eiffel Tower, Louvre, Montmartre and a Seine cruise.", 4, 980),
                ("Provence Countryside", "Lavender villages, markets and vineyard tastings.", 5, 1050),
                ("French Riviera", "Nice, Cannes and the Monaco coastline.", 4, 1200)]},
    {"slug": "italy", "name": "Italy", "flag": "🇮🇹", "continent": "Europe", "colors": ("#2d6a4f", "#d9ed92"),
     "tagline": "Roman ruins, Tuscan hills, endless pasta.",
     "description": "Italy packs more history per square mile than almost anywhere. Explore the Colosseum, float through Venice's canals and drive the rolling hills of Tuscany.",
     "best_time": "April–June, Sep–Oct", "currency": "Euro (EUR)", "language": "Italian",
     "highlights": ["Colosseum & Vatican", "Venice canals", "Tuscan wine country", "Amalfi Coast"],
     "places": [("Rome & Vatican", "Colosseum, Roman Forum, Vatican Museums and Trastevere dinners.", 4, 900),
                ("Venice & Florence", "Gondola rides, Uffizi Gallery and Duomo climb.", 5, 1100),
                ("Amalfi Coast", "Positano, Ravello and boat trips to Capri.", 4, 1350)]},
    {"slug": "thailand", "name": "Thailand", "flag": "🇹🇭", "continent": "Asia", "colors": ("#0b6e4f", "#f2a900"),
     "tagline": "Island beaches, street food, golden temples.",
     "description": "Thailand is easy to love: friendly people, incredible food and beaches that look edited. Mix Bangkok's temples and markets with island time in the south.",
     "best_time": "November–February", "currency": "Thai Baht (THB)", "language": "Thai",
     "highlights": ["Phi Phi islands", "Bangkok street food", "Elephant sanctuaries", "Chiang Mai temples"],
     "places": [("Bangkok Explorer", "Grand Palace, Wat Pho, floating markets and food tours.", 4, 520),
                ("Phuket & Phi Phi", "Island hopping, snorkeling and beach resorts.", 6, 780),
                ("Chiang Mai Culture", "Mountain temples, cooking class and ethical elephant visit.", 4, 560)]},
    {"slug": "india", "name": "India", "flag": "🇮🇳", "continent": "Asia", "colors": ("#7b2d26", "#f4a261"),
     "tagline": "Colour, spice and a thousand stories.",
     "description": "India overwhelms in the best way: palaces in Rajasthan, backwaters in Kerala, the Taj Mahal at sunrise and food that changes every hundred kilometres.",
     "best_time": "October–March", "currency": "Indian Rupee (INR)", "language": "Hindi, English",
     "highlights": ["Taj Mahal at sunrise", "Rajasthan palaces", "Kerala backwaters", "Himalayan foothills"],
     "places": [("Golden Triangle", "Delhi, Agra and Jaipur with the Taj Mahal.", 6, 640),
                ("Kerala Backwaters", "Houseboat stay in Alleppey, tea hills of Munnar.", 5, 590),
                ("Rajasthan Royal Trail", "Udaipur lakes, Jodhpur fort and desert camp in Jaisalmer.", 7, 850)]},
    {"slug": "egypt", "name": "Egypt", "flag": "🇪🇬", "continent": "Africa", "colors": ("#6b4226", "#e9c46a"),
     "tagline": "Pyramids, the Nile and 5,000 years of history.",
     "description": "Stand before the Great Pyramid, cruise the Nile past temples and dive the Red Sea's coral reefs, all in one trip.",
     "best_time": "October–April", "currency": "Egyptian Pound (EGP)", "language": "Arabic",
     "highlights": ["Pyramids of Giza", "Nile cruise", "Valley of the Kings", "Red Sea diving"],
     "places": [("Cairo & Giza", "Pyramids, Sphinx and the Egyptian Museum.", 3, 480),
                ("Nile Cruise", "Luxor to Aswan with temple visits on board.", 5, 950),
                ("Red Sea Diving", "Hurghada reef trips and beach resort stay.", 5, 700)]},
    {"slug": "australia", "name": "Australia", "flag": "🇦🇺", "continent": "Oceania", "colors": ("#0077b6", "#ffb703"),
     "tagline": "Reefs, red deserts and harbour views.",
     "description": "Australia is big, sunny and full of wildlife. Snorkel the Great Barrier Reef, watch the sun set on Uluru and climb the Sydney Harbour Bridge.",
     "best_time": "September–November", "currency": "Australian Dollar (AUD)", "language": "English",
     "highlights": ["Great Barrier Reef", "Sydney Opera House", "Uluru at sunset", "Great Ocean Road"],
     "places": [("Sydney Highlights", "Opera House, Bondi to Coogee walk, Blue Mountains.", 4, 1000),
                ("Great Barrier Reef", "Cairns base with reef snorkeling and rainforest tour.", 5, 1300),
                ("Uluru & Red Centre", "Sunrise at Uluru, Kings Canyon and stargazing dinner.", 4, 1250)]},
    {"slug": "brazil", "name": "Brazil", "flag": "🇧🇷", "continent": "South America", "colors": ("#006d32", "#ffd60a"),
     "tagline": "Samba, rainforest and Rio's beaches.",
     "description": "Brazil is rhythm and nature. See Christ the Redeemer above Rio, walk beneath the thundering Iguaçu Falls and float into the Amazon rainforest.",
     "best_time": "May–October", "currency": "Brazilian Real (BRL)", "language": "Portuguese",
     "highlights": ["Christ the Redeemer", "Iguaçu Falls", "Amazon rainforest", "Copacabana beach"],
     "places": [("Rio de Janeiro", "Sugarloaf, Christ the Redeemer and Ipanema beach days.", 5, 870),
                ("Iguaçu Falls", "Both sides of the falls plus a boat ride to the base.", 3, 640),
                ("Amazon Adventure", "Manaus river lodge, jungle walks and night canoeing.", 5, 990)]},
]


def make_svg(c):
    a, b = c["colors"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" preserveAspectRatio="xMidYMid slice">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>
<rect width="800" height="560" fill="url(#g)"/>
<circle cx="640" cy="130" r="150" fill="#fff" opacity=".08"/><circle cx="120" cy="470" r="220" fill="#000" opacity=".10"/>
<text x="400" y="290" font-size="190" text-anchor="middle" dominant-baseline="middle">{c["flag"]}</text>
</svg>'''


def seed_data():
    os.makedirs(IMG_DIR, exist_ok=True)
    for c in COUNTRIES:
        fname = f'{c["slug"]}.svg'
        with open(os.path.join(IMG_DIR, fname), "w", encoding="utf-8") as f:
            f.write(make_svg(c))
        country = Country(slug=c["slug"], name=c["name"], continent=c["continent"], tagline=c["tagline"],
                          description=c["description"], image=fname, best_time=c["best_time"],
                          currency=c["currency"], language=c["language"], highlights=c["highlights"])
        db.session.add(country)
        db.session.flush()
        for name, desc, days, price in c["places"]:
            db.session.add(Place(country_id=country.id, name=name, description=desc,
                                 duration_days=days, price_per_person=price))
    db.session.commit()
    print(f"Seeded {len(COUNTRIES)} countries.")


if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()
        if Country.query.count() == 0:
            seed_data()
        else:
            print("Database already has countries; nothing to seed.")
