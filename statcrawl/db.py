
from statcrawl.conf import connstring
from statcrawl.mainparser import TOP_DIMS, filter_by_dims
from statcrawl import parser
from sqlalchemy.engine import create_engine

engine = create_engine(connstring)

def create_columns(dimensions):
    """Add column in `cube` table for each in dimensions"""

    conn = engine.connect()
    trans = conn.begin()

    for dim in dimensions:
        conn.execute("ALTER TABLE cube ADD COLUMN %s text;" % dim)
        conn.execute("CREATE INDEX i_%s ON cube (%s ASC NULLS LAST);" % (dim, dim))

    trans.commit()
    conn.close()


def parse_and_save(content):
    parsed = parser.parse(content)
    cols = [TOP_DIMS[ dim ] for dim, _ in parser.iter_dims(parsed)]

    conn = engine.connect()
    trans = conn.begin()

    conn.execute("insert into statinfo (statname) values (:statname) ",
                 statname=parsed['stat'])
    print conn.execute("select currval(statinfo_id_seq) ").fetchall()[0][0]
    return
    for entry in parser.iter_data(parsed):
        dim_vals = entry[:-1]
        val = entry[-1]

        for i, dim_val in enumerate(dim_vals):
            print cols[i], dim_val

        print val


        break


def main():
    for content in filter_by_dims(TOP_DIMS):
        parse_and_save(content)
        break

if __name__ == '__main__':
    main()

