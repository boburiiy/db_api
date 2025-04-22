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
        """!!! I prefer to execute delete or drop commands seperately"""
        if 'DROP' in command.upper() or 'DELETE' in command.upper():
            raise ValueError('You added denied command')

        """passes parameter if it is given"""
        self.cur.execute(command, params or None)
        if commit:
            self.conn.commit()
            print(colorize("committed", "GREEN"))

    def create_table(self, table_name: str, **kwargs):
        """table_name give me name for new table"""
        if not kwargs or not table_name:
            raise ValueError('No table_name or kwargs given!!!')
        # creating table example start
        """
            kwargs are used to define column names and it`s types ! note enter psql type
            example create_table(table_name='users',userId="INT",username='VARCHAR(255)')
        """
        cols = ",\n".join(
            [f"{v_name} {d_type}" for v_name, d_type in kwargs.items()])
        """
            this line translates userId='INT',username='VARCHAR(255)' from the example into list with string items like
            ['userId INT','username VARCHAR(255)']
            and joing method translates this list into sql command like this:
            userId INT,
            username VARCHAR(255)

        """
        sql_ = f"CREATE TABLE IF NOT EXISTS {table_name} (\n{cols}\n);"
        """
        passing table name and translated columns with f string
        now its looks like
            CREATE TABLE IF NOT EXISTS users (
                userId INT,
                username VARCHAR(255)
            );
        """
        # example end
        self.exec(sql_, commit=True)
        """executing the final command and committing"""
        return "done"

    def insert(self, table_name: str, **kwargs):
        # insert example start
        """table name is where to insert
        insert(table_name='users',columns=['userId',username'],values=[[12,'john doe'],[13,'bon doe']])"""
        variables = kwargs.get("columns")
        """
            gets list of column names
            imagine we have table named user and columns userId and username
        """
        values = kwargs.get("values")
        """
            gets values for those columns but it should be list inside the list so you can insert multiple values
            order by order
            example the first item of values is [12,'john doe'] where 12 is inserts to userId and john doe to username
        """
        var_count = len(variables)
        """its for passing %s parameter argument"""
        values_list = []

        if not isinstance(variables, list) or not variables:
            raise ValueError(
                colorize('Are you checked your columns?'), 'red')
        # checking if columns argument is list

        values_list.extend(
            data for order, data in enumerate(values)
            if isinstance(data, list)
            or
            print(colorize(f"{data} in order {order} is not a list", "red"))
            # checking each element of values nor they are list nor will be passed away
        )

        variables = ','.join(variables)
        "translating ['userId','username'] into 'userId,username' now its not a list anymore"
        # passing table name, variables and adding parameter arguments * to length of columns count
        paramters = ','.join(['%s']*var_count)
        sql_ = f"INSERT INTO {table_name} ({variables}) VALUES ({paramters})"
        for param in values_list:
            self.exec(sql_, tuple(param), commit=True)
            # adding each item of values list one by one and ending the insert example

    def select(self, *args, **kwargs):
        # selecting example
        """args are column names eg:['userId','username']"""
        if not kwargs.get('table') or not args or not kwargs.get('fetch'):
            # i think it`s understandable by the condition
            raise ValueError('table name or keys or fetch is not given')

        reqs = f"WHERE {kwargs['requires']}" if kwargs.get(
            'requires') else ''  # giving condition if it`s required by the user as requires argument

        sql_ = f"SELECT {','.join(args)} from {kwargs['table']} {reqs}"
        """
            sql_ look like that
            SELECT userId,username from table_name reqs if it`s given else nothin
            # note userId and username are from example not standart values
        """

        F = kwargs['fetch']  # for defining fetch type one,many or all
        self.exec(sql_)
        return self.cur.fetchmany(F) if type(F) is int else self.cur.fetchall() if F == 'all' else self.cur.fetchone()
        # return fetchmany(F) if F is integer return fetchall() if F is 'all' else fetchone

    @try_it
    def delete(self, table_name: str, condition: str, params: tuple, commit: bool):
        if not condition or not table_name or not params:
            raise ValueError(
                'this function requires table name, condition, column names and parameters check for it')  # do you understand?

        self.cur.execute(f"DELETE FROM {table_name} WHERE {condition}", params)
        """it will delete a row with the suitable condition from table with same as tale_name argument"""
        # note condition should contain parameter argument %s to avoid sql injection
        if commit:
            self.conn.commit()

    @try_it
    def _drop_table(self, table_name: str):
        self.cur.execute(f"DROP TABLE {table_name}")  # just drop a table
        self.conn.commit()
