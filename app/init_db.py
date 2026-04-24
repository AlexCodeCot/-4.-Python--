from app.db.db import SessionLocal, create_tables
from app.db import crud

def init_database():
    # Убедимся, что таблицы существуют
    create_tables()
    db = SessionLocal()
    try:
        # Проверим, есть ли уже категории (чтобы избежать дублирования)
        existing_categories = crud.get_categories(db)
        if existing_categories:
            print("База уже содержит категории. Инициализация пропущена.")
            return

        # Создаём две категории
        cat1 = crud.create_category(db, title="Фантастика")
        cat2 = crud.create_category(db, title="Детективы")

        # Книги для категории "Фантастика"
        crud.create_book(
            db, title="Дюна", description="Пустынная планета Арракис",
            price=750.0, url="", category_id=cat1.id
        )
        crud.create_book(
            db, title="1984", description="Антиутопия Оруэлла",
            price=450.0, url="", category_id=cat1.id
        )
        crud.create_book(
            db, title="Солярис", description="Загадочный океан",
            price=500.0, url="", category_id=cat1.id
        )

        # Книги для категории "Детективы"
        crud.create_book(
            db, title="Шерлок Холмс", description="Приключения сыщика",
            price=600.0, url="", category_id=cat2.id
        )
        crud.create_book(
            db, title="Убийство в Восточном экспрессе",
            description="Эркюль Пуаро расследует убийство",
            price=550.0, url="", category_id=cat2.id
        )
        crud.create_book(
            db, title="Десять негритят", description="Классический детектив",
            price=500.0, url="", category_id=cat2.id
        )

        db.commit()
        print("✅ База данных успешно инициализирована.")
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при инициализации: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()