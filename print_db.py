from sqlalchemy import create_engine 
from app import db


def dump(sql, *multiparams, **params):
    print(sql.compile(dialect=engine.dialect))

if __name__ == '__main__':
    engine = create_engine('postgresql://', strategy='mock', executor=dump)
    db.metadata.create_all(engine)
