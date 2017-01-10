#!/bin/env python
from impala.dbapi import connect
from impala.util import as_pandas


def main():
    get_ingest_summary('flow',2016,10,7,2016,10,8)


def get_raw_data(pipeline, sy, sm, sd, ey, em, ed, limit = 500):
    
    qry = ("SELECT * from {0}.{1} WHERE y BETWEEN {2} AND {5} "
            " AND m BETWEEN {3} AND {6} AND d BETWEEN {4} AND {7} LIMIT {8}") 
    qry = qry.format('db_spot', pipeline, sy, sm, sd, ey, em, ed, limit)
 
    conn = connect(host='gmsonidw05', port=21050) 
    cur = conn.cursor()

    cur.execute(qry)
    df = as_pandas(cur)

    dic = df.to_dict('records')

    return dic



def get_ingest_summary(pipeline, sy, sm, sd, ey, em, ed, limit = 500):
    
    qry = ("SELECT tryear, trmonth, trday, trhour, trminute, COUNT(*) total"
                             " FROM {0}.{1} "
                             " WHERE y BETWEEN {2} AND {5} "
                             " AND m BETWEEN {3} AND {6} AND d BETWEEN {4} AND {7} "
                             " AND unix_tstamp IS NOT NULL "
                             " GROUP BY tryear, trmonth, trday, trhour, trminute limit {8};") 
    qry = qry.format('db_spot', pipeline, sy, sm, sd, ey, em, ed, limit)
 
    conn = connect(host='gmsonidw05', port=21050) 
    cur = conn.cursor()

    cur.execute(qry)
    df = as_pandas(cur)

    dic = df.to_dict('records')

    print dic
    return dic


if __name__=='__main__':
    main()

