def drop_if_exists(engine, tablename):
    sql = 'DROP TABLE IF EXISTS ' + tablename
    return engine.execute(sql)
