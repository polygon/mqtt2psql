import psycopg2
from mqtt2psql.data import PlugSensor, PlugState

class PlugsSql:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str
    ):
        self.conn = psycopg2.connect(
            dbname = database,
            host = host,
            user = user,
            password = password
        )

    def insert_sensor_data(self, name: str, data: PlugSensor):
        plug_id = self._ensure_plug(name)
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO plugs_sensor_data
                  (time, plug_id, total, yesterday, power, apparent_power, reactive_power, factor, voltage, current)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (data.time, plug_id, data.total, data.yesterday, data.power, data.apparent_power, data.reactive_power,
                 data.factor, data.voltage, data.current)
            )
            self.conn.commit()
        
    def insert_state_data(self, name: str, data: PlugState):
        plug_id = self._ensure_plug(name)
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO plugs_status_data
                  (time, plug_id, uptime, power, wifi_rssi, wifi_signal)
                  VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                (data.time, plug_id, data.uptime, data.power, data.wifi_rssi, data.wifi_signal)
            )
            self.conn.commit()

    def _get_plug_id(self, name: str) -> int or None:
        with self.conn.cursor() as cur:
            cur.execute("SELECT plug_id FROM plugs_ids WHERE name = %s", (name, ))
            plug_id = cur.fetchone()

        return None if plug_id is None else plug_id[0]

    def _add_plug(self, name: str):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO plugs_ids (name) VALUES (%s)", (name, ))
            self.conn.commit()

    def _ensure_plug(self, name: str) -> int:
        plug_id = self._get_plug_id(name)
        if plug_id is None:
            self._add_plug(name)
            plug_id = self._get_plug_id(name)

        return plug_id
