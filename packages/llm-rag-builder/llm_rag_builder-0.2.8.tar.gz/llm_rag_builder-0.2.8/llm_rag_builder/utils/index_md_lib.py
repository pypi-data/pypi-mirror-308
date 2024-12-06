import glob
import os
import re
from uuid import uuid4


def index_md_lib(path):
    """
    Index the markdown files in the library.

    ! THIS IS A BULLSHIT VERSION, ITS SYNC AND SLOW !

    Returns:
        dict: A dictionary of the markdown files in the library.
    """
    # Get the markdown files in the library
    md_files = glob.glob(path + "/**/*.md", recursive=True)

    # Index the markdown files
    md_index = []
    for md_file in md_files:
        # Get the relative path of the markdown file
        md_file_rel = os.path.relpath(md_file, path)

        # Get the title of the markdown file
        with open(md_file, "r") as f:
            text = f.read()
            chunks = re.split(r"(?<=\n)(#{1,6} .+?)(?=\n)", text)

            for chunk in chunks:
                md_index.append({
                    "meta": {"path": md_file_rel},
                    "uuid": str(uuid4()),
                    "text": chunk
                })

    print(md_index)
    return md_index


def index_to_db(path, db):
    data = index_md_lib(path)
    db.bulk_insert(data)
