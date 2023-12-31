from dataclasses import dataclass
from enum import Enum
from typing import Optional
from transport import db_query


class TransportType(Enum):
    CAR = 'Car'
    BIKE = 'Bike'
    SCOOTER = 'Scooter'


@dataclass
class Transport:
    id: Optional[int]
    canBeRented: bool
    transportType: TransportType
    model: str
    color: str
    identifier: str
    description: Optional[str]
    latitude: float
    longitude: float
    minutePrice: Optional[float]
    dayPrice: Optional[float]
    owner_id: int

    @staticmethod
    async def get_transport(id: int):
        res = await db_query.get_car(id)

        if res:
            return Transport(*res)

    async def delete_car(self):
        await db_query.delete_car(self.id)


@dataclass
class AddNewTransport:
    canBeRented: bool
    transportType: TransportType
    model: str
    color: str
    identifier: str
    description: Optional[str]
    latitude: float
    longitude: float
    minutePrice: Optional[float]
    dayPrice: Optional[float]

    async def new_transport(self, user_id):
        return await db_query.add_car(self, user_id)


@dataclass
class UpdateTransportBody:
    canBeRented: bool
    transportType: TransportType
    model: str
    color: str
    identifier: str
    description: Optional[str]
    latitude: float
    longitude: float
    minutePrice: Optional[float]
    dayPrice: Optional[float]

    async def update_transport(self, id: int):
        await db_query.update_car(id, self)


@dataclass
class StatusOperationCar:
    status: str
    id: Optional[int] = None
