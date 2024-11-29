import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("data_load.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из файла .env
load_dotenv()

DB_SETTINGS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Функция для подключения к базе данных
def get_connection():
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return None

# Функция для получения существующих значений из таблицы
def get_existing_values(conn, table_name, column_name):
    with conn.cursor() as cursor:
        query = sql.SQL("SELECT DISTINCT {} FROM {}").format(
            sql.Identifier(column_name),
            sql.Identifier(table_name)
        )
        cursor.execute(query)
        results = cursor.fetchall()
    return set([row[0] for row in results])

# Функция для обрезки строковых полей до максимальной длины
def truncate_strings(df, column_lengths):
    for col, max_length in column_lengths.items():
        df[col] = df[col].apply(lambda x: x[:max_length] if isinstance(x, str) else x)
    return df

# Функция для очистки данных таблицы address
def clean_address_data(df):
    logger.info("Очистка данных для таблицы address")
    df.columns = [col.lower() for col in df.columns]
    required_columns = ['address', 'flats', 'entrances', 'floors']
    df = df[required_columns]

    # Удаляем дубликаты
    df.drop_duplicates(subset=['address'], inplace=True)

    # Заполняем пропущенные значения
    df['address'] = df['address'].fillna('')

    # Приводим типы данных и обрабатываем ошибки
    numeric_columns = ['flats', 'entrances', 'floors']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(0).astype(int)

    # Удаляем строки с пустым адресом
    df = df[df['address'] != '']

    # Обрезаем строки до допустимой длины, если необходимо
    df = truncate_strings(df, {'address': 255})

    logger.info(f"После очистки данных для address осталось {len(df)} записей")
    return df

# Функция для очистки данных таблицы client с валидацией внешних ключей
def clean_client_data(df, existing_addresses):
    logger.info("Очистка данных для таблицы client")
    df.columns = [col.lower() for col in df.columns]
    required_columns = ['client_id', 'address', 'gender', 'age_range']
    df = df[required_columns]

    # Удаляем дубликаты
    df.drop_duplicates(subset=['client_id'], inplace=True)

    # Заполняем пропущенные значения в строковых полях
    string_columns = ['client_id', 'address', 'gender', 'age_range']
    for col in string_columns:
        df[col] = df[col].fillna('').astype(str)

    # Удаляем строки с пустым client_id
    df = df[df['client_id'] != '']

    # Валидация внешнего ключа address
    df = df[df['address'].isin(existing_addresses)]

    # Обрезаем строки до допустимой длины
    df = truncate_strings(df, {'client_id': 50, 'address': 255, 'gender': 1, 'age_range': 50})

    logger.info(f"После очистки данных для client осталось {len(df)} записей")
    return df

# Функция для очистки данных таблицы package_channel
def clean_package_channel_data(df):
    logger.info("Очистка данных для таблицы package_channel")
    df.columns = [col.lower() for col in df.columns]
    required_columns = ['pack_name', 'ch_id']
    df = df[required_columns]

    # Удаляем дубликаты по ch_id
    df.drop_duplicates(subset=['ch_id'], inplace=True)

    # Заполняем пропущенные значения в строковых полях
    df['pack_name'] = df['pack_name'].fillna('').astype(str)

    # Приводим ch_id к числовому типу и обрабатываем ошибки
    df['ch_id'] = pd.to_numeric(df['ch_id'], errors='coerce').astype('Int64')

    # Удаляем строки с некорректным ch_id
    df = df[df['ch_id'].notnull()]

    # Обрезаем строки до допустимой длины
    df = truncate_strings(df, {'pack_name': 50})

    logger.info(f"После очистки данных для package_channel осталось {len(df)} записей")
    return df

# Функция для очистки данных таблицы epg_stat с валидацией внешних ключей
def clean_epg_stat_data(df, existing_client_ids, existing_ch_ids):
    logger.info("Очистка данных для таблицы epg_stat")
    df.columns = [col.lower() for col in df.columns]
    required_columns = ['client_id', 'device_id', 'time_ch', 'ch_id', 'epg_name',
                        'time_epg', 'time_to_epg', 'duration', 'category', 'subcategory']
    df = df[required_columns]

    # Заполняем пропущенные значения в строковых полях
    string_columns = ['client_id', 'device_id', 'epg_name', 'category', 'subcategory']
    for col in string_columns:
        df[col] = df[col].fillna('').astype(str)

    # Приводим ch_id и duration к числовому типу и обрабатываем ошибки
    df['ch_id'] = pd.to_numeric(df['ch_id'], errors='coerce').astype('Int64')
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce').astype('Int64')

    # Обрабатываем даты и время
    date_columns = ['time_ch', 'time_epg', 'time_to_epg']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Удаляем строки с некорректными значениями в обязательных полях
    required_fields = ['client_id', 'device_id', 'time_ch', 'ch_id']
    df.dropna(subset=required_fields, inplace=True)

    # Удаляем строки с некорректными датами
    df.dropna(subset=date_columns, inplace=True)

    # Удаляем дубликаты по первичному ключу
    df.drop_duplicates(subset=['client_id', 'device_id', 'time_ch'], inplace=True)

    # Удаляем строки с отрицательной продолжительностью
    df = df[df['duration'].notnull() & (df['duration'] >= 0)]

    # Валидация внешних ключей
    df = df[df['client_id'].isin(existing_client_ids)]
    df = df[df['ch_id'].isin(existing_ch_ids)]

    # Обрезаем строки до допустимой длины
    df = truncate_strings(df, {
        'client_id': 50,
        'device_id': 50,
        'epg_name': 255,
        'category': 50,
        'subcategory': 50
    })

    logger.info(f"После очистки данных для epg_stat осталось {len(df)} записей")
    return df

# Функция для загрузки данных в базу данных
def load_data_to_db(df, table_name, conn):
    logger.info(f"Начинаем загрузку данных в таблицу {table_name}")
    # Формируем список кортежей для вставки
    records = df.to_dict('records')

    if not records:
        logger.warning(f"Нет данных для загрузки в таблицу {table_name}.")
        return

    # Определяем столбцы для вставки
    columns = df.columns.tolist()
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES %s ON CONFLICT DO NOTHING").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, columns))
    )

    with conn.cursor() as cursor:
        try:
            execute_values(cursor, insert_query, [tuple(record[col] for col in columns) for record in records], page_size=1000)
            conn.commit()
            logger.info(f"Успешно загружено {len(records)} записей в таблицу {table_name}.")
        except Exception as e:
            conn.rollback()
            logger.error(f"Ошибка при загрузке данных в таблицу {table_name}: {e}")

# Основная функция
def main():
    # Подключение к базе данных
    conn = get_connection()
    if not conn:
        return

    try:
        # Обработка и загрузка данных для таблицы address
        try:
            df_address = pd.read_csv('csv/address.csv', delimiter=';', encoding='utf-8', encoding_errors='replace')
            df_address_cleaned = clean_address_data(df_address)
            load_data_to_db(df_address_cleaned, 'address', conn)
        except Exception as e:
            logger.error(f"Ошибка при обработке данных для таблицы address: {e}")

        # Получаем список существующих адресов после загрузки таблицы address
        existing_addresses = get_existing_values(conn, 'address', 'address')

        # Обработка и загрузка данных для таблицы client
        try:
            df_client = pd.read_csv('csv/client.csv', delimiter=';', encoding='utf-8', encoding_errors='replace')
            df_client_cleaned = clean_client_data(df_client, existing_addresses)
            load_data_to_db(df_client_cleaned, 'client', conn)
        except Exception as e:
            logger.error(f"Ошибка при обработке данных для таблицы client: {e}")

        # Получаем список существующих client_id после загрузки таблицы client
        existing_client_ids = get_existing_values(conn, 'client', 'client_id')

        # Обработка и загрузка данных для таблицы package_channel
        try:
            df_package_channel = pd.read_csv('csv/package_channel.csv', delimiter=';', encoding='utf-8', encoding_errors='replace')
            df_package_channel_cleaned = clean_package_channel_data(df_package_channel)
            load_data_to_db(df_package_channel_cleaned, 'package_channel', conn)
        except Exception as e:
            logger.error(f"Ошибка при обработке данных для таблицы package_channel: {e}")

        # Получаем список существующих ch_id после загрузки таблицы package_channel
        existing_ch_ids = get_existing_values(conn, 'package_channel', 'ch_id')

        # Обработка и загрузка данных для таблицы epg_stat
        try:
            df_epg_stat = pd.read_csv('csv/epg_stat_2024_10.csv', delimiter=';', encoding='utf-8', encoding_errors='replace')
            df_epg_stat_cleaned = clean_epg_stat_data(df_epg_stat, existing_client_ids, existing_ch_ids)
            load_data_to_db(df_epg_stat_cleaned, 'epg_stat', conn)
        except Exception as e:
            logger.error(f"Ошибка при обработке данных для таблицы epg_stat: {e}")

    finally:
        conn.close()
        logger.info("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    main()
