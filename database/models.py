from sqlalchemy.orm import Mapped, mapped_column

from database.db import db


class Deal(db.Model):
    """
    Deals Table
    """

    __tablename__ = "deals"
    id: Mapped[int] = mapped_column(primary_key=True)
    destination: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    platform: Mapped[str] = mapped_column()
    rating: Mapped[float] = mapped_column()
    travel_type: Mapped[str] = mapped_column()

    def to_dict(self):
        """
        Convert the model object to dictionary
        """

        return {
            "id": self.id,
            "destination": self.destination,
            "price": self.price,
            "platform": self.platform,
            "rating": self.rating,
            "travel_type": self.travel_type,
        }