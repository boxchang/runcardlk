import pyodbc

from django.db import connections

class mes_database:
    def select_sql(self, sql):
        with connections['MES'].cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def select_sql_dict(self, sql):
        with connections['MES'].cursor() as cur:
            cur.execute(sql)
            desc = cur.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row))
                    for row in cur.fetchall()]
            return data

    def select_sql_dict_param(self, sql, param):
        with connections['MES'].cursor() as cur:
            cur.execute(sql, param)
            desc = cur.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row))
                    for row in cur.fetchall()]
            return data

    def execute_sql(self, sql):
        with connections['MES'].cursor() as cur:
            cur.execute(sql)


class scada_database:
    def select_sql(self, sql):
        self.conn = self.create_sgada_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_sql_dict(self, sql):
        self.conn = self.create_sgada_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)

        desc = self.cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))
                for row in self.cur.fetchall()]
        return data

    def execute_sql(self, sql):
        self.conn = self.create_sgada_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()

    def create_sgada_connection(self):
        try:
            conn = pyodbc.connect("DRIVER={{SQL Server}};SERVER={server}; database={database}; \
                                   trusted_connection=no;UID={uid};PWD={pwd}".format(server="10.14.102.11",
                                                                                     database="PMG_DEVICE",
                                                                                     uid="scadauser",
                                                                                     pwd="pmgscada+123"))
            return conn
        except Exception as e:
            print(e)

        return None


class vnedc_database:
    def select_sql(self, sql):
        with connections['default'].cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def select_sql_dict(self, sql):
        with connections['default'].cursor() as cur:
            cur.execute(sql)
            desc = cur.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row))
                    for row in cur.fetchall()]
            return data

    def select_sql_dict_param(self, sql, param):
        with connections['default'].cursor() as cur:
            cur.execute(sql, param)
            desc = cur.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row))
                    for row in cur.fetchall()]
            return data

    def execute_sql(self, sql):
        with connections['default'].cursor() as cur:
            cur.execute(sql)