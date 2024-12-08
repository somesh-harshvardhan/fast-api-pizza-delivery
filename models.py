from database import Base
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    Text,
    String,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship


class ORDER_STATUSES(Enum):
    PENDING = "pending"
    IN_TRANSIT = "in-transit"
    DELIVERED = "delivered"


class PIZZA_SIZES(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra-large"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(
        SQLAlchemyEnum(ORDER_STATUSES), default=ORDER_STATUSES.PENDING
    )
    pizza_size = Column(
        SQLAlchemyEnum(PIZZA_SIZES),
        default=PIZZA_SIZES.SMALL,
    )
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}>"
