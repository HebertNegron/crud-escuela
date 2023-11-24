from sqlalchemy import Column, String, text, engine

def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    with engine.connect() as conn:
        conn.execute(text('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type)))

column = Column('fotoPerfilUrl', String(50))
add_column(engine, 'alumnos', column)