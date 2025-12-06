import psycopg2
import config as cfg

conn = psycopg2.connect(dbname=cfg.database_name, host=cfg.database_url, user=cfg.database_user,
                        password=cfg.database_password, port='5432')
cur = conn.cursor()


def get_servises_list():
    cur.execute(f"SELECT service_name, price FROM {cfg.database_name}.services")
    records = cur.fetchall()
    answer = ""
    for name, price in records:
        answer += f"Услуга: {name}, Стоимость: {price} \n"
    return answer


if __name__ == '__main__':
    print(get_servises_list())
