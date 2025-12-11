import sqlite3

import psycopg2
import config as cfg

conn = psycopg2.connect(dbname=cfg.database_name, host=cfg.database_url, user=cfg.database_user,
                        password=cfg.database_password, port='5432')
cur = conn.cursor()


class Services:
    class select:
        def servises_list(self):
            cur.execute(f"SELECT service_name, price FROM {cfg.database_name}.services")
            records = cur.fetchall()
            answer = ""
            for name, price in records:
                answer += f"Услуга: {name}, Стоимость: {price} \n"
            return answer

        def service(name):
            cur.execute(f"SELECT service_name, price FROM {cfg.database_name}.services WHERE service_name = '{name}'")
            records = cur.fetchall()
            answer = ""
            for name, price in records:
                answer += f"Услуга: {name}, Стоимость: {price}"
            return answer

    class add:
        def add_service(name, price, type="buh"):
            # Вставить проверки значений
            try:
                cur.execute(f"INSERT INTO {cfg.database_name}.services(service_name, price, type) VALUES (%s,%s,%s)",
                            (name, price, type))
            except psycopg2.DatabaseError as err:
                print("Error: ", err)
                return False
            else:
                conn.commit()
                return True

    class edit:
        def edit_service(name, type, new_value):
            t = "service_name" if type == "name" else "price"
            try:
                cur.execute(f"UPDATE {cfg.database_name}.services SET {t}=%s WHERE service_name=%s", (new_value, name))
            except psycopg2.DatabaseError as err:
                print("Error: ", err)
                return False
            else:
                conn.commit()
                return True

    class delete:
        def delete_service(name):
            try:
                cur.execute(f"DELETE FROM {cfg.database_name}.services WHERE service_name='{name}'")
            except psycopg2.DatabaseError as err:
                print("Error: ", err)
                return False
            else:
                conn.commit()
                return True


if __name__ == '__main__':
    print(Services.select.service("Тестовая"))
