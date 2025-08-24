import json
import os


class FileStorageMixin:
    def save_json(self, filepath: str, data: dict) -> str:
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

            return "Stored successfully"

        except Exception as e:
            return f"Error storing data: {e}"

    def load_json(self, filepath: str) -> dict:
        if not os.path.exists(filepath):
            return {}

        try:
            with open(filepath, "r") as f:
                content = f.read().strip()
                return json.loads(content) if content else {}

        except Exception as e:
            return {}
