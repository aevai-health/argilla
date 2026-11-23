"""Local only (needs this fork's frontend): move project3's "### Case N – Answer X" heading into the field titles.

Field titles become "Case {case_no}" / "Alva’s progression advice – Answer {answer_letter}", filled per record from metadata (see RecordFields.vue).
Run after copy_from_online.py. Env: LOCAL_API_KEY, optional LOCAL_URL.
"""
import os
import re

import argilla as rg

c = rg.Argilla(api_url=os.environ.get("LOCAL_URL", "http://127.0.0.1:6900"), api_key=os.environ["LOCAL_API_KEY"])
ds = c.datasets("project3", workspace="interns")

s = ds.settings
for name in ("case_no", "answer_letter"):  # must differ from field names
    if name not in [m.name for m in s.metadata]:
        s.metadata.add(rg.TermsMetadataProperty(name=name, visible_for_annotators=True))  # annotators' UI only gets visible metadata
s.fields["case"].title = "Case {case_no}"
s.fields["answer"].title = "Alva’s progression advice – Answer {answer_letter}"
ds.update()

recs = []
for r in ds.records:
    m = re.match(r"### Case (\d+) – Answer ([AB])\n\n", r.fields["case"])
    if m:
        recs.append(rg.Record(id=r.id, fields={"case": r.fields["case"][m.end():], "answer": r.fields["answer"]},
                              metadata={"case_no": m[1], "answer_letter": m[2]}))
if recs:  # already moved on a re-run
    ds.records.log(recs)
print(f"updated {len(recs)} records")
