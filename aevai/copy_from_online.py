"""Copy workspaces' datasets (settings + records, no responses) from the online Argilla to the local one.

Env: ONLINE_API_KEY, LOCAL_API_KEY; optional ONLINE_URL, LOCAL_URL, WORKSPACE (default interns).
Datasets that already exist locally are skipped (delete them in the UI to re-copy).
"""
import os
import tempfile

import argilla as rg

online = rg.Argilla(api_url=os.environ.get("ONLINE_URL", "https://labels.aevai-health.com"), api_key=os.environ["ONLINE_API_KEY"])
local = rg.Argilla(api_url=os.environ.get("LOCAL_URL", "http://127.0.0.1:6900"), api_key=os.environ["LOCAL_API_KEY"])
WS = os.environ.get("WORKSPACE", "interns")

ws = local.workspaces(WS) or rg.Workspace(name=WS, client=local).create()
for d in online.workspaces(WS).datasets:
    src = online.datasets(d.name, workspace=WS)  # the workspace listing doesn't load settings
    if local.datasets(src.name, workspace=ws):
        print(f"skip {src.name}: already exists locally")
        continue
    # shortcut: responses aren't copied (they belong to online user ids); add them if you need annotated data locally
    path = os.path.join(tempfile.mkdtemp(), "settings.json")
    src.settings.to_json(path)
    settings = rg.Settings.from_json(path)
    dst = rg.Dataset(name=src.name, workspace=ws, settings=settings, client=local).create()
    recs = [rg.Record(id=r.id, fields=dict(r.fields), metadata=dict(r.metadata)) for r in src.records]
    dst.records.log(recs)
    print(f"copied {src.name}: {len(recs)} records")
