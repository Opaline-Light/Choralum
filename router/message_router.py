import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
from voices import aegis
from voices import gaia
from voices import lucent
from voices import wonder
from voices import fable

BASE_PATH = Path(__file__).resolve().parent.parent
MEMORY_PATH = BASE_PATH / "memory"
LOG_PATH = BASE_PATH / "logs"
CONFIG_PATH = BASE_PATH / "choralum.json"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def route_message(message_path):
    with open(message_path) as f:
        message = json.load(f)

    voice_id = message["to"]
    content = message["content"]
    context = message.get("context", "")

    
    if voice_id == "lucent":
        response = lucent.generate_response(content, context)
    elif voice_id == "wonder":
        response = wonder.generate_response(content, context)
    elif voice_id == "gaia":
        response = gaia.generate_response(content, context)
    elif voice_id == "aegis":
        response = aegis.generate_response(content, context)
    elif voice_id == "fable":
        response = fable.generate_response(content, context)
    else:
        response = f"[{voice_id}] is not yet implemented."


    log_entry = {
        "from": message["from"],
        "to": voice_id,
        "context": context,
        "input": content,
        "response": response
    }

    # Append log
    log_file = LOG_PATH / "scroll_of_continuity.log"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"Message processed. Response: {response}")

if __name__ == "__main__":
    for msg_file in MEMORY_PATH.glob("*.json"):
        route_message(msg_file)
