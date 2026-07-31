from app.models.vacancy import VacancyModel
from app.db.session import session_factory
from sqlalchemy import select
import asyncio


async def main():
    # async with session_factory.begin() as session:
    #     new_vacancy = VacancyModel(company="Yandex", title="backend developer",
    #                                url="https://yandex.com", description="lets try")
    #     session.add(new_vacancy)
    #     print("vacancy added")

    # async with session_factory.begin() as session:
        # r = select(VacancyModel).order_by(VacancyModel.id).limit(1)
        # result = await session.execute(r)
        # vacancy = result.scalars().one_or_none()
        # vacancy.description = "i tried and i got it lol"
        # await session.commit()
        # print(vacancy.description)

    async with session_factory.begin() as session:
        smth = select(VacancyModel).order_by(VacancyModel.id).limit(1)
        result = await session.execute(smth)
        vacancy = result.scalars().one_or_none()
        result = await session.delete(vacancy)


if __name__ == "__main__":
    asyncio.run(main())