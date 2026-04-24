print("Hello, World!")

from app.db.db import SessionLocal
from app.db import crud

def main():
    db = SessionLocal()
    try:
        categories = crud.get_categories(db)
        if not categories:
            print("В базе нет категорий. Сначала запустите app/init_db.py")
            return

        for cat in categories:
            print(f"\n📚 Категория: {cat.title}")
            books = crud.get_books(db, category_id=cat.id)
            if not books:
                print("   (нет книг)")
                continue
            for book in books:
                print(f"   • {book.title}")
                print(f"     Описание: {book.description}")
                print(f"     Цена: {book.price} руб.")
                print(f"     Ссылка: {book.url or '(пусто)'}")
    finally:
        db.close()

if __name__ == "__main__":
    main()