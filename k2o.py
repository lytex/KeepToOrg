import datetime
import json
import sys
from glob import glob

# Example json structure
{
    "color": "DEFAULT",
    "isTrashed": False,
    "isPinned": False,
    "isArchived": False,
    "textContent": "Note content",
    "title": "Note title, empty if dictated from Android Auto",
    "userEditedTimestampUsec": 1673456350742000,
    "createdTimestampUsec": 1673456350742000,
    "labels": [{"name": "tag2"}, {"name": "tag1"}],  # This can be empty if there is no tag
}


def main(keep_dir, org_file):
    notes = []
    for file in glob(keep_dir + "/*/*.json"):
        with open(file) as f:
            contents = json.load(f)
            notes.append(contents)
    # Sort by edition time asc
    notes = sorted(notes, key=lambda x: x["userEditedTimestampUsec"])
    org_contents = "\n".join(map(generate_headline, notes))
    with open(org_file, "w") as f:
        f.write(org_contents)


def generate_headline(note):
    tags = ["ARCHIVE"] * note["isArchived"]
    created = datetime.datetime.fromtimestamp(note["userEditedTimestampUsec"] / 1e6).strftime("[%Y-%m-%d %a %H:%M]")
    properties = f":PROPERTIES:\n:CREATED: {created}\n:END:"

    if note.get("labels"):
        tags += [x["name"] for x in note["labels"]]
    if tags != []:
        tags = " :" + ":".join(tags) + ":"
    else:
        tags = ""

    if not note["isTrashed"]:
        if note["title"] == "":
            return f"* {note['textContent']}{tags}\n{properties}"
        else:
            return f"* {note['title']}{tags}\n{properties}\n{note['textContent']}"
    else:
        return ""


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong number of arguments!\nUsage:\n\tpython k2o.py /path/to/google/Keep/folder /path/to/org/file.org")
    else:
        keep_dir = sys.argv[1]
        org_file = sys.argv[2]
        main(keep_dir, org_file)
