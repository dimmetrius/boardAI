from boarddocs import BoardDocsReader
import json

# ----------------------------------------------
print("initializing reader")
site = "ca/redwood"
committeeID = "A4EP6J588C05"
reader = BoardDocsReader(site, committeeID)
# ----------------------------------------------
print("receiving board meetings list")
meetings = reader.get_meeting_list()
meetings_ids = list(
    filter(lambda id: id != None, map(lambda m: m["meetingID"], meetings))
)
# ----------------------------------------------
print("receiving board meetings texts")
llama_docs = reader.load_data(meetings_ids)
for doc in llama_docs:
    with open("./docs/" + doc.doc_id + ".json", "w") as f:
        json.dump(doc.to_json(), f)
