from fastapi import HTTPException
from transport.services import Transport


def check_owner(owner_id, user_id):
    if owner_id != int(user_id):
        raise HTTPException(status_code=403, detail='Это не ваша машина :(')


def transport_exists(car: Transport):
    if not car:
        raise HTTPException(status_code=403, detail='Такой машины не существует ')
