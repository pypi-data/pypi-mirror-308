#!/usr/bin/env -S rye run python

import os

from lastmile import Lastmile

client = Lastmile(
    # This is the default and can be omitted
    bearer_token=os.environ.get("LASTMILE_API_TOKEN"),
)

print(client.evaluation.list_metrics())
