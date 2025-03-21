import psycopg2
from decorator import try_it, colorize


class DB:
    def __init__(self, dbname: str = 'postgres', host: str = 'localhost', user: str = 'postgres', port='5432', passwd: str = "postgres"):
        self.conn = psycopg2.connect(
            dbname=dbname,
            host=host,
            user=user,
            password=passwd,
            port=port
        )
        self.cur = self.conn.cursor()

    @try_it
    def exec(self, command: str, params: tuple = None, commit=False):
        if 'DROP' in command.upper() or 'DELETE' in command.upper():
            raise ValueError('You added denied command')

        self.cur.execute(command, params or None)
        if commit:
            self.conn.commit()
            print(colorize("committed", "GREEN"))

    def create_table(self, table_name: str, **kwargs):
        if not kwargs or not table_name:
            raise ValueError('No table_name or kwargs given!!!')
        cols = ",\n".join(
            [f"{v_name} {d_type}" for v_name, d_type in kwargs.items()])
        sql_ = f'CREATE TABLE IF NOT EXISTS {table_name} (\n{cols}\n);'

        self.exec(sql_, commit=True)
        return "done"

    def insert(self, table_name: str, **kwargs):
        variables = kwargs.get("variables")
        values = kwargs.get("values")
        var_count = len(variables)
        values_list = []

        if not isinstance(variables, list) or not variables:
            raise ValueError(
                colorize('Are you checked your variables?'), 'red')

        values_list.extend(
            data for order, data in enumerate(values)
            if isinstance(data, list)
            or
            print(colorize(f'{data} in order {order} is not a list', 'red'))
        )
        variables = ','.join(variables)
        sql_ = f'INSERT INTO {table_name} ({variables}) VALUES ({','.join(['%s']*var_count)})'
        for param in values_list:
            self.exec(sql_, tuple(param), commit=True)

    def select(self, *args, **kwargs):
        if not kwargs.get('table') or not args or not kwargs.get('fetch'):
            raise ValueError('table name or keys or fetch is not given')

        reqs = f'WHERE {kwargs['requires']}' if kwargs.get(
            'requires') else ''
        sql_ = f"SELECT {','.join(args)} from {kwargs['table']} {reqs}"
        F = kwargs['fetch']
        self.exec(sql_)
        return self.cur.fetchmany(F) if type(F) is int else self.cur.fetchall() if F == 'all' else self.cur.fetchone()

    @try_it
    def delete(self, table_name: str, condition: str, params: tuple, commit: bool):
        if not condition or not table_name or not params:
            raise ValueError(
                'this function requires table name, condition, column names and parameters check for it')

        self.cur.execute(f'DELETE FROM {table_name} WHERE {condition}', params)
        if commit:
            self.conn.commit()

    def _drop_table(self, table_name: str):
        self.cur.execute(f'DROP TABLE {table_name}')
        self.conn.commit()


new_db = DB(passwd='batman', dbname="my_db")