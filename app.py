import os, re
from datetime import date, datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set")

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    "dev-secret-change-me"
)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

db = SQLAlchemy(app)
jwt = JWTManager(app)

CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    tagline = db.Column(db.String(160))
    description = db.Column(db.Text)
    best_time = db.Column(db.String(80))
    currency = db.Column(db.String(40))
    language = db.Column(db.String(60))
    price = db.Column(db.Integer, nullable=False)  # per person, USD
    highlights = db.Column(db.JSON, default=list)
    image = db.Column(db.String(300))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    travelers = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="confirmed")  # confirmed | cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.relationship("Country")

    def to_dict(self):
        return {"id": self.id, "travel_date": self.travel_date.isoformat(), "travelers": self.travelers,
                "total_price": self.total_price, "status": self.status,
                "created_at": self.created_at.isoformat(), "country": self.country.to_dict()}


SEED = [
 ("Japan", "japan", "Where ancient temples meet neon skylines", "Cherry blossoms, bullet trains, world-class food and serene temples. From Tokyo's electric energy to Kyoto's quiet geisha lanes and Mount Fuji's views.", "Mar–May, Oct–Nov", "Yen (JPY)", "Japanese", 1450, ["Fushimi Inari Shrine, Kyoto", "Shibuya Crossing, Tokyo", "Mount Fuji day trip", "Nara deer park"], "japan,temple"),
 ("France", "france", "Romance, art and unforgettable cuisine", "Stroll along the Seine, explore the Louvre, taste Provence lavender fields and Champagne cellars, and unwind on the French Riviera.", "Apr–Jun, Sep–Oct", "Euro (EUR)", "French", 1600, ["Eiffel Tower, Paris", "Louvre Museum", "Loire Valley châteaux", "French Riviera"], "paris,france"),
 ("Italy", "italy", "History on every corner, pasta on every table", "Walk through Rome's ruins, ride gondolas in Venice, admire Florence's art and explore Amalfi's dramatic coastline.", "Apr–Jun, Sep–Oct", "Euro (EUR)", "Italian", 1500, ["Colosseum, Rome", "Venice canals", "Florence Duomo", "Amalfi Coast"], "italy,rome"),
 ("India", "india", "A kaleidoscope of colour, culture and flavour", "From the Taj Mahal to Kerala's backwaters, Rajasthan's palaces and the Himalayas, India is a journey for every sense.", "Oct–Mar", "Rupee (INR)", "Hindi, English", 900, ["Taj Mahal, Agra", "Jaipur palaces", "Kerala backwaters", "Varanasi ghats"], "india,taj"),
 ("Thailand", "thailand", "Golden temples and turquoise beaches", "Island hopping in Phuket and Krabi, vibrant Bangkok street food, jungle treks and elephant sanctuaries in Chiang Mai.", "Nov–Feb", "Baht (THB)", "Thai", 1000, ["Grand Palace, Bangkok", "Phi Phi Islands", "Chiang Mai old city", "Railay Beach"], "thailand,beach"),
 ("Egypt", "egypt", "Walk in the footsteps of pharaohs", "Marvel at the Pyramids of Giza, cruise the Nile to Luxor and Aswan, and snorkel the Red Sea's coral reefs.", "Oct–Apr", "Egyptian Pound (EGP)", "Arabic", 1100, ["Pyramids of Giza", "Valley of the Kings", "Nile cruise", "Red Sea diving"], "egypt,pyramids"),
 ("Australia", "australia", "Big skies, wild coasts and laid-back cities", "See the Sydney Opera House, dive the Great Barrier Reef, drive the Great Ocean Road and meet kangaroos in the outback.", "Sep–Nov, Mar–May", "Australian Dollar (AUD)", "English", 2100, ["Sydney Opera House", "Great Barrier Reef", "Great Ocean Road", "Uluru"], "australia,sydney"),
 ("Brazil", "brazil", "Rhythm, rainforest and golden beaches", "Samba in Rio, Christ the Redeemer, the mighty Iguazu Falls and the Amazon rainforest — Brazil is pure energy.", "Dec–Mar, Jun–Aug", "Real (BRL)", "Portuguese", 1300, ["Christ the Redeemer, Rio", "Iguazu Falls", "Amazon rainforest", "Copacabana Beach"], "brazil,rio"),
]

def seed():
    if Country.query.count():
        return
    for i, (n, s, t, d, b, c, l, p, h, k) in enumerate(SEED, 1):
        db.session.add(Country(name=n, slug=s, tagline=t, description=d, best_time=b, currency=c,
                               language=l, price=p, highlights=h,
                               image=f"/static/images/{k}.jpg?lock={i}"))
    db.session.commit()


def err(msg, code=400):
    return jsonify({"error": msg}), code


def parse_booking(data):
    try:
        d = date.fromisoformat(data.get("travel_date", ""))
        n = int(data.get("travelers", 0))
    except (ValueError, TypeError):
        return None, None, "Invalid date or number of travelers"
    if d <= date.today():
        return None, None, "Travel date must be in the future"
    if not 1 <= n <= 20:
        return None, None, "Travelers must be between 1 and 20"
    return d, n, None


# ---------- Pages ----------
def page(name):
    return send_from_directory(os.path.join(app.root_path, "templates"), name)

@app.route("/")
@app.route("/login")
def login_page(): return page("login.html")
@app.route("/signup")
def signup_page(): return page("signup.html")
@app.route("/home")
def home_page(): return page("home.html")
@app.route("/country/<slug>")
def country_page(slug): return page("country.html")
@app.route("/bookings")
def bookings_page(): return page("bookings.html")


# ---------- Auth API ----------
@app.post("/api/signup")
def signup():
    d = request.get_json(silent=True) or {}
    name, email, pw = d.get("name", "").strip(), d.get("email", "").strip().lower(), d.get("password", "")
    if not name or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return err("Enter a valid name and email")
    if len(pw) < 6:
        return err("Password must be at least 6 characters")
    if User.query.filter_by(email=email).first():
        return err("Email already registered", 409)
    db.session.add(User(name=name, email=email, password_hash=generate_password_hash(pw)))
    db.session.commit()
    return jsonify({"message": "Account created. Please log in."}), 201


@app.post("/api/login")
def login():
    d = request.get_json(silent=True) or {}
    u = User.query.filter_by(email=d.get("email", "").strip().lower()).first()
    if not u or not check_password_hash(u.password_hash, d.get("password", "")):
        return err("Invalid email or password", 401)
    return jsonify({"token": create_access_token(identity=str(u.id)), "user": {"id": u.id, "name": u.name, "email": u.email}})


@app.get("/api/me")
@jwt_required()
def me():
    u = db.session.get(User, int(get_jwt_identity()))
    return jsonify({"id": u.id, "name": u.name, "email": u.email})


# ---------- Countries ----------
@app.get("/api/countries")
def countries():
    return jsonify([c.to_dict() for c in Country.query.order_by(Country.name)])


@app.get("/api/countries/<slug>")
def country(slug):
    c = Country.query.filter_by(slug=slug).first()
    return jsonify(c.to_dict()) if c else err("Country not found", 404)


# ---------- Bookings ----------
@app.post("/api/bookings")
@jwt_required()
def create_booking():
    d = request.get_json(silent=True) or {}
    c = db.session.get(Country, d.get("country_id"))
    if not c:
        return err("Country not found", 404)
    dt, n, e = parse_booking(d)
    if e:
        return err(e)
    b = Booking(user_id=int(get_jwt_identity()), country_id=c.id, travel_date=dt, travelers=n, total_price=c.price * n)
    db.session.add(b)
    db.session.commit()
    return jsonify(b.to_dict()), 201


@app.get("/api/bookings")
@jwt_required()
def list_bookings():
    bs = Booking.query.filter_by(user_id=int(get_jwt_identity())).order_by(Booking.created_at.desc()).all()
    return jsonify([b.to_dict() for b in bs])


def own_booking(bid):
    return Booking.query.filter_by(id=bid, user_id=int(get_jwt_identity())).first()


@app.put("/api/bookings/<int:bid>")
@jwt_required()
def edit_booking(bid):
    b = own_booking(bid)
    if not b:
        return err("Booking not found", 404)
    if b.status == "cancelled":
        return err("Cancelled bookings cannot be edited", 409)
    dt, n, e = parse_booking(request.get_json(silent=True) or {})
    if e:
        return err(e)
    b.travel_date, b.travelers, b.total_price = dt, n, b.country.price * n
    db.session.commit()
    return jsonify(b.to_dict())


@app.delete("/api/bookings/<int:bid>")
@jwt_required()
def cancel_booking(bid):
    b = own_booking(bid)
    if not b:
        return err("Booking not found", 404)
    b.status = "cancelled"
    db.session.commit()
    return jsonify(b.to_dict())


with app.app_context():
    db.create_all()
    seed()

if __name__ == "__main__":
    app.run(debug=True)

