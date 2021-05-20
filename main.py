import csv
import logging

from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import NotMasterError


client = MongoClient()
db = client.my_db
zno = db.zno_collection

zno2019='OpenDataZNO2019/Odata2019FileUTF.csv'
zno2020='OpenDataZNO2020/Odata2020FileUTF.csv'

LOG = logging.getLogger(__name__)
logging.basicConfig(
    filename="database_logs.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s::%(funcName)s: %(message)s"
)

def do_the_lab():
    create_inserted()

    start_time = datetime.now()
    LOG.info(f"Start time {start_time}")

    inserted_2019 = db.inserted.find_one({"year": 2019})["inserted"]
    inserted_2020 = db.inserted.find_one({"year": 2020})["inserted"]

    if not inserted_2019:
        populate_collection(zno2019, 2019)
    if not inserted_2020:
        populate_collection(zno2020, 2020)

    end_time = datetime.now()
    LOG.info(f"End time {end_time}")
    LOG.info(f"Inserting executing time {end_time - start_time}")

    get_result_csv()

def create_inserted():
    db_collections = db.list_collection_names()

    if "inserted" not in db_collections:
        bp = db.inserted

        length_2019 = get_csv_length(zno2019)
        length_2020 = get_csv_length(zno2020)

        bp.insert_many([
            {"year": 2019, "inserted": False, "length": length_2019},
            {"year": 2020, "inserted": False, "length": length_2020}
        ])

def get_csv_length(zno_file):
    with open(zno_file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        count = 0

        for line in csv_reader:
            count += 1

    return count

def populate_collection(zno_file, year):
    with open(zno_file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")

        i = 1

        bp = get_breakpoint()

        for line in csv_reader:
            if i <= bp:
                i += 1  
                continue

            try:
                insert_dict(line, year)
            except Exception as err:
                LOG.info(f"Whoopsies, looks like the database is down (◕︵◕)")
                raise err

        db.inserted.update_one({"year": year}, {"$set": {"inserted": True}})

def get_breakpoint():
    length = db.inserted.find_one({"year": 2019})["length"]
    bp = zno.count({})

    if bp < length:
        return bp

    return bp - length 


def insert_dict(line, year):
    line["year"] = year

    clean_line(line)

    zno.insert_one(line)

def clean_line(line):
    make_floats(line)
    make_ints(line)

def make_floats(row):
    subjects = [
        "UkrBall100",
        "histBall100",
        "mathBall100",
        "physBall100",
        "chemBall100",
        "bioBall100",
        "geoBall100",
        "engBall100",
        "fraBall100",
        "deuBall100",
        "spaBall100",
    ]

    for subject in subjects:
        if row[subject] != "null":
            row[subject] = float(row[subject].replace(",", "."))
        else:
            row[subject] = None

def make_ints(row):
    subjects = [
        "UkrBall12",
        "UkrBall",
        "histBall12",
        "histBall",
        "mathBall12",
        "mathBall",
        "physBall12",
        "physBall",
        "chemBall12",
        "chemBall",
        "bioBall12",
        "bioBall",
        "geoBall12",
        "geoBall",
        "engBall12",
        "fraBall12",
        "deuBall12",
        "spaBall12",
        "engBall",
        "fraBall",
        "deuBall",
        "spaBall"
    ]

    for subject in subjects:
        if row[subject] == "null":
            row[subject] = None
        else:
            row[subject] = int(row[subject])

def get_result_csv():
    query = zno.aggregate(
        [
            {"$match": {"UkrTestStatus": "Зараховано"}},
            {"$group": {"_id": {"year": "$year",
                                "region": "$REGNAME"},
                        "ukrMin": {"$min": "$UkrBall100"}}},
        ]
    )

    with open("result.csv", "w") as csvfile:
        csq_writer = csv.DictWriter(csvfile, fieldnames=["year", "region", "ukrMin"])
        csq_writer.writeheader()
        for row in query:
            row["year"] = row["_id"]["year"]
            row["region"] = row["_id"]["region"]
            del row["_id"]
            csq_writer.writerow(row)


if __name__ == "__main__":
    do_the_lab()