from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from account.utils import check_auth
from transport import utils
from transport.services import *

router = APIRouter()


@router.get('/{id}', response_model=Transport)
async def get_transport(id: int):
    res = await Transport.get_transport(id)

    if res:
        return res

    utils.transport_exists(res)


@router.post('/', response_model=StatusOperationCar)
async def add_new_transport(transport: AddNewTransport, authorize: check_auth = Depends()):
    authorize: AuthJWT
    user_id = authorize.get_jwt_subject()
    ts_id = await transport.new_transport(int(user_id))
    return StatusOperationCar(status='success', id=ts_id)


@router.put('/{id}', response_model=StatusOperationCar)
async def update_transport(id: int, transport: UpdateTransportBody, authorize: check_auth = Depends()):
    authorize: AuthJWT
    user_id = authorize.get_jwt_subject()
    car = await Transport.get_transport(id)

    utils.transport_exists(car)
    utils.check_owner(car.owner_id, int(user_id))

    await transport.update_transport(id)

    return StatusOperationCar(status="success", id=id)


@router.delete('/{id}', response_model=StatusOperationCar)
async def delete_transport(id: int, authorize: check_auth = Depends()):
    authorize: AuthJWT
    user_id = authorize.get_jwt_subject()
    car = await Transport.get_transport(id)

    utils.transport_exists(car)
    utils.check_owner(car.owner_id, int(user_id))

    await car.delete_car()

    return StatusOperationCar(status='success', id=id)
