from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship("Booking", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(60), unique=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    continent = db.Column(db.String(40))
    tagline = db.Column(db.String(160))
    description = db.Column(db.Text)
    image = db.Column(db.String(120))
    best_time = db.Column(db.String(80))
    currency = db.Column(db.String(40))
    language = db.Column(db.String(60))
    highlights = db.Column(db.JSON, default=list)
    places = db.relationship("Place", backref="country", lazy=True, order_by="Place.id")

    def to_dict(self, with_places=False):
        data = {
            "id": self.id, "slug": self.slug, "name": self.name,
            "continent": self.continent, "tagline": self.tagline,
            "description": self.description, "image": f"/static/img/{self.image}",
            "best_time": self.best_time, "currency": self.currency,
            "language": self.language, "highlights": self.highlights or [],
            "starting_price": min((p.price_per_person for p in self.places), default=0),
        }
        if with_places:
            data["places"] = [p.to_dict() for p in self.places]
        return data


class Place(db.Model):
    """A bookable destination / package inside a country."""
    __tablename__ = "places"
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration_days = db.Column(db.Integer, default=3)
    price_per_person = db.Column(db.Integer, nullable=False)  # USD

    def to_dict(self):
        return {
            "id": self.id, "country_id": self.country_id, "name": self.name,
            "description": self.description, "duration_days": self.duration_days,
            "price_per_person": self.price_per_person,
        }


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    travelers = db.Column(db.Integer, nullable=False, default=1)
    notes = db.Column(db.String(300))
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="confirmed")  # confirmed | cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    place = db.relationship("Place")

    def to_dict(self):
        return {
            "id": self.id,
            "reference": f"TRV-{self.id:05d}",
            "place": self.place.to_dict(),
            "country": {"name": self.place.country.name, "slug": self.place.country.slug,
                        "image": f"/static/img/{self.place.country.image}"},
            "travel_date": self.travel_date.isoformat(),
            "travelers": self.travelers,
            "notes": self.notes or "",
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
