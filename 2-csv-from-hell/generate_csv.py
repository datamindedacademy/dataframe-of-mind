from enum import Enum
from faker.providers import BaseProvider
from faker import Faker
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Measurement:
    id: int
    name: str
    timestamp: datetime
    blood_pressure: float
    heart_rate: float
    temperature: float
    blood_glucose: float


class LifeStage(Enum):
    CUB = "CUB"
    JUV = "JUV"
    ADULT = "ADULT"
    SENIOR = "SENIOR"


fake = Faker()

name_pool = [
    "Icy Ingrid",
    "Peter Panda",
    "Arctic Archie",
    "Chilly Willy",
    "Cubby Coldpaws",
    "Blizzard Bob",
]

polar_bear_birth_years = dict(
    zip(name_pool, [2024 - age for age in (4, 2, 30, 10, 0, 40)])
)
polar_bear_lifestage = {1: LifeStage.JUV, 4: LifeStage.ADULT, 15: LifeStage.SENIOR}


class VetHealthCheck(Enum):
    HEALTHY = "HEALTHY"
    SICK = "SICK"
    INJURED = "INJURED"


@dataclass
class BatchMeasurement:
    name: str
    age: int
    weight: float
    daily_steps: int
    timestamp: datetime
    vet_health_check: LifeStage
    life_stage: VetHealthCheck


class MeasurementProvider(BaseProvider):
    __provider__ = "transaction"

    def measurement(self) -> Measurement:
        return Measurement(
            id=fake.uuid4(),
            name=fake.random_element(name_pool),
            timestamp=fake.date_time_between(start_date="-3y", end_date="now"),
            blood_pressure=fake.random_int(60, 140),
            heart_rate=fake.random_int(60, 100),
            temperature=fake.random_int(36, 41),
            blood_glucose=fake.random_int(70, 140),
        )


class BatchMeasurementProvider(BaseProvider):
    __provider__ = "batch_measurement"

    def batch_measurement(self, timestamp: datetime) -> BatchMeasurement:
        name = fake.random_element(name_pool)
        age = timestamp.year - polar_bear_birth_years[name]
        weight = (100 + (850 - 100) * age / 10 if age < 10 else 850) / 2  # lbs to kg
        life_stage = LifeStage.CUB
        for age_limit, stage in polar_bear_lifestage.items():
            if age_limit <= age:
                life_stage = stage
                break

        return BatchMeasurement(
            name=(name.upper() if fake.boolean(chance_of_getting_true=20) else name),
            age=age,
            weight=weight + fake.random_int(-10, 10),
            daily_steps=fake.random_int(1000, 20000),
            timestamp=timestamp,
            vet_health_check=(
                VetHealthCheck.SICK
                if name == "Peter Panda"  # Peter Panda is always sick
                else fake.random_element(VetHealthCheck)
            ),
            life_stage=life_stage,
        )


if __name__ == "__main__":
    fake.add_provider(MeasurementProvider)
    fake.add_provider(BatchMeasurementProvider)

    N = int(5_000)
    N_batch = int(1000)
    measurements = [fake.measurement() for _ in range(N)]
    with open("data/measurements.csv", "w") as f:
        for t in measurements:
            f.write(
                f"{t.id}|{t.name}|{t.timestamp}|{t.blood_pressure}|{t.heart_rate}|{t.temperature}|{t.blood_glucose}\n"
            )

    timestamps = [datetime(2021, 1, 1) + i * timedelta(days=3) for i in range(N_batch)]
    batch_measurements = [fake.batch_measurement(timestamp) for timestamp in timestamps]
    with open("data/batch_measurements.csv", "w") as f:
        for t in batch_measurements:
            if t.age < 0:
                continue

            f.write(
                f"{t.name}|{t.age}|{t.weight}|{t.daily_steps}|{datetime.strftime(t.timestamp, "%d%m%YT%H:%M:%S")}|{t.vet_health_check.value}|{t.life_stage.value}\n"
            )
