from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import DBAPIError

from account.services import UserMeInfo, User
from account.utils import check_auth
from payments.services import SuccessCreatePayment, PaymentStatus, Payment
from payments import utils
from payments.utils import AllowedCurrencies

router = APIRouter()


@router.post('/Hesoyam/{account_id}', response_model=UserMeInfo)
async def add_balance(account_id: int, authorize: check_auth = Depends()):
    authorize: AuthJWT
    user_id = authorize.get_jwt_subject()
    user = await UserMeInfo.get_user_info(int(user_id))

    if user.is_admin or (int(user_id) == account_id):
        user.balance += 250_000
        await User.edit_balance(account_id, user.balance)
        return user

    raise HTTPException(status_code=403, detail='У вас нету прав изменять баланс другому пользователю.')


@router.post('/create_payment', response_model=SuccessCreatePayment)
async def create_crypto_payment(amount: float, currency: AllowedCurrencies, authorize: check_auth = Depends()):
    try:
        payment = await Payment.create_payment(int(authorize.get_jwt_subject()), amount)
        url = utils.create_payment(payment.uuid, amount, currency.value)['result']['url']
        return SuccessCreatePayment(
            uuid=payment.uuid,
            url_for_payment=url,
            status=payment.status
        )

    except KeyError:
        raise HTTPException(status_code=400, detail='Мы не смогли создать платёж')

    except DBAPIError:
        raise HTTPException(status_code=400, detail='Полегче с суммами, парень')


@router.post('/check_paid', response_model=UserMeInfo)
async def check_paid(data: dict):
    if data['status'] in ('paid', 'paid_over'):
        payment = await Payment.get_payment(data['order_id'])

        if payment.status != PaymentStatus.COMPLETED.value:
            user = await UserMeInfo.get_user_info(int(payment.user_id))
            user.balance += payment.amount
            await User.edit_balance(payment.user_id, user.balance)
            await payment.complete_payment()
            return user

        raise HTTPException(status_code=400, detail='Данный платёж уже был оплачен')

    raise HTTPException(status_code=400, detail='Вообще не ебут остальные запросы. Реально. Чисто похуй.')
