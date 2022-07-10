import os
from functools import partial
from mqtt2psql.plugs_mqtt import PlugsMqtt
from mqtt2psql.data import PlugSensor, PlugState
from mqtt2psql.plugs_sql import PlugsSql

def consumer(sql: PlugsSql, name: str, data: PlugSensor or PlugState):
    if isinstance(data, PlugSensor):
        sql.insert_sensor_data(name, data)
    elif isinstance(data, PlugState):
        sql.insert_state_data(name, data)
    else:
        raise RuntimeError("Unexpected data received by consumer")

def mqtt2psql():
    mqtt_host = os.environ['MQTT_HOST']
    mqtt_port = os.environ.get('MQTT_PORT', 1883)
    mqtt_user = os.environ['MQTT_USER']
    mqtt_pass = os.environ['MQTT_PASS']

    psql_host = os.environ['PSQL_HOST']
    psql_db = os.environ['PSQL_DB']
    psql_user = os.environ['PSQL_USER']
    psql_pass = os.environ['PSQL_PASS']

    plugssql = PlugsSql(psql_host, psql_user, psql_pass, psql_db)
    consumer_with_sql = partial(consumer, plugssql)
    plugsmqtt = PlugsMqtt(mqtt_host, mqtt_port, mqtt_user, mqtt_pass, consumer_with_sql)
    plugsmqtt.run()

if __name__ == "__main__":
    mqtt2psql()
