import sqlite3
from sensors import gen_data

conn = sqlite3.connect('data_sensor.db:')
c = conn.cursor()

c.execute("""CREATE TABLE dataTable (
            moisture real,
            rainfall real,
            humidity real,
            temperature real,
            crop_yield real, 
            )""")


def insert_data(data):
    with conn:
        c.execute("INSERT INTO dataTable VALUES (:moisture, :rainfall, :humidity, :temperature, :crop_yield)",
                  {'moisture': data.moisture, 'rainfall': data.rainfall,
                   'humidity': data.humidity, 'temperature': data.temperature, 'crop_yield': data.crop_yield})


def get_data(moisture):
    c.execute("SELECT * FROM data_sensor WHERE moisture=:moisture", {'moisture': moisture})
    return c.fetchall()


def update_data(data, moisture):
    with conn:
        c.execute("""UPDATE data_sensor SET rainfall = :rainfall
                    WHERE moisture = :moisture AND humidity = :humidity""",
                  {'moisture': data.moisture, 'rainfall': data.rainfall, 'humidity': data.humidity,
                   'temperature': data.temperature, 'crop_yield': data.crop_yield})


def remove_data(data):
    with conn:
        c.execute("DELETE from data_sensor WHERE moisture = :moisture AND rainfall = :rainfall",
                  {'moisture': data.moisture, 'rainfall': data.rainfall, 'humidity': data.humidity,
                   'temperature': data.temperature, 'crop_yield': data.crop_yield})


data_1 = gen_data()
data_2 = gen_data()

insert_data(data_1)
insert_data(data_2)

data = get_data('moisture')
print(data)

update_data(data_2, 9.500)
remove_data(data_1)

data = get_data('crop_yield')
print(data)
conn.close()
