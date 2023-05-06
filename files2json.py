"""
convert flat txt file with full names to
 - json file with dirs and files
 - csv with dirs, csv  with files with id's
 """

from json import dump
from pathlib import Path
from dataclasses import dataclass, astuple, fields
import csv

FULL_NAMES_LIST_TXT = "data/full_names.txt"
DIRS_AND_FILES_JSON = "data/dirs_and_files.json"
DIRS_CSV = "data/dirs.csv"
FILES_CSV = "data/files.csv"

@dataclass
class Directory:
    id: int
    name: str


@dataclass
class File:
    id: int
    id_dir: int
    name: str


def get_full_json(file_name):
    json_data = {}
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            path_file = Path(line)
            dir_name = path_file.parts[-2]
            if dir_name not in json_data:
                json_data[dir_name] = []
            json_data[dir_name].append(path_file.stem)
    return json_data


def dataclass2csv(filename: str, rows: list, header: bool = True):
    # from dataclasses import astuple, fields
    # rows is list of dataclass
    with open(filename, 'w', encoding='utf-8', newline='') as csv_file:
        # dialect='unix' for quoting all fields
        csv_writer = csv.writer(csv_file, dialect='unix')
        if header:
            csv_writer.writerow(field.name for field in fields(rows[0]))
        csv_writer.writerows([astuple(row) for row in rows])


full_json = get_full_json(FULL_NAMES_LIST_TXT)
with open(DIRS_AND_FILES_JSON, "w", encoding="utf-8") as file:
    dump(full_json, file, indent=4, ensure_ascii=False)

dirs = []
for id, dir_name in enumerate(full_json):
    dirs.append(Directory(id + 1, dir_name))

files = []
for directory in dirs:
    for file in full_json[directory.name]:
        files.append(File(id=int(file[:3]), id_dir=directory.id, name=file))

assert len(files) == len(set(f.id for f in files))

dataclass2csv(DIRS_CSV, dirs, header=True)
dataclass2csv(FILES_CSV, files, header=True)

print("Done.")
