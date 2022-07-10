from dataclasses import dataclass


@dataclass
class PlugSensor:
    time: str
    total: float
    yesterday: float
    power: float
    apparent_power: float
    reactive_power: float
    factor: float
    voltage: float
    current: float

    @staticmethod
    def from_json(data: dict) -> "PlugSensor":
        return PlugSensor(
            time = data["Time"],
            total = data["ENERGY"]["Total"],
            yesterday = data["ENERGY"]["Yesterday"],
            power = data["ENERGY"]["Power"],
            apparent_power = data["ENERGY"]["ApparentPower"],
            reactive_power = data["ENERGY"]["ReactivePower"],
            factor = data["ENERGY"]["Factor"],
            voltage = data["ENERGY"]["Voltage"],
            current = data["ENERGY"]["Current"]
        )

@dataclass
class PlugState:
    time: str
    uptime: int
    power: bool
    wifi_rssi: float
    wifi_signal: float

    @staticmethod
    def from_json(data: dict) -> "PlugState":
        return PlugState(
            time = data["Time"],
            uptime = data["UptimeSec"],
            power = data["POWER"],
            wifi_rssi = data["Wifi"]["RSSI"],
            wifi_signal = data["Wifi"]["Signal"]
        )