from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel
from database import session
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    return {"message": "Hello world"}


@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(pizza_size=order.pizza_size, quantity=order.quantity)
    new_order.user = user

    session.add(new_order)
    session.commit()
    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status,
    }
    return jsonable_encoder(response)


@order_router.get("/orders")
async def list_all_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        orders = session.query(Order).all()

        return jsonable_encoder(orders)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Access not allowed "
    )


@order_router.get("/order/{id}")
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(user == User.username).first()

    if current_user.is_staff:
        order = session.query(Order).filter(id == Order.id).first()

        return jsonable_encoder(order)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to carry out request",
    )


@order_router.get("/user/orders")
async def get_current_user_order(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )
    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username == user).first()

    orders = {"orders": current_user.orders}

    return jsonable_encoder(orders)


@order_router.get("/user/order/{order_id}")
async def get_by_order_id(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username == user).first()

    order = list(filter(lambda order: order.id == order_id, current_user.orders))

    return jsonable_encoder({"order": order})


@order_router.put("/user/update/order/{order_id}")
async def update_by_order_id(
    order_id: int, order: OrderModel, Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    user = Authorize.get_jwt_subject()
    current_order = (
        session.query(Order)
        .join(User)
        .filter(Order.id == order_id, User.username == user)
        .first()
    )

    for key, value in order.dict(exclude_unset=True).items():
        setattr(current_order, key, value)

    session.commit()

    return jsonable_encoder({"message": f"Updated order {order_id} successfully "})
