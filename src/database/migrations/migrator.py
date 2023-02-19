from __future__ import annotations

import datetime
import os
import uuid

for file in os.listdir():
    if file.endswith(".sql"):
        if file.count(".") == 1:
            new_uuid = uuid.uuid4()
            os.rename(file, f"{datetime.datetime.now().timestamp()}-{new_uuid}.sql")
