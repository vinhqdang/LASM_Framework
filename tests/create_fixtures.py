import json
import os

def create_fixtures():
    os.makedirs("tests/fixtures", exist_ok=True)
    with open("tests/fixtures/sample_systems.json", "w") as f:
        json.dump({"name": "TestSys", "scope": "S1"}, f)

if __name__ == "__main__":
    create_fixtures()
