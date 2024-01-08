from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import csv
from sqlalchemy import create_engine
from sqlalchemy import MetaData


db = SQLAlchemy()


def to_dict(res: list):
    return [{column.name: getattr(row[0], column.name) for column in row[0].__table__.columns} for row in res]


migrate = Migrate()


def dump_sqlalchemy():
    DATABASE_URI = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"
    engine = create_engine(DATABASE_URI)

    meta = MetaData()
    meta.reflect(bind=engine)
    result = {}

    for table in meta.sorted_tables:
        if table.name != "alembic_version":
            result[table.name] = [row._asdict() for row in db.session.execute(table.select()).all()]

    for key, values in result.items():
        try:
            filename = f"backend/database/dump/{key}.csv"

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=values[0].keys())

                writer.writeheader()

                for row in values:
                    writer.writerow(row)
        except Exception as e:
            pass
