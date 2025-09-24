from typing import List, Dict
import pandas as pd
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

class PartsStore:
    def __init__(self, path: Path = DATA_DIR / "parts.csv"):
        self.df = pd.read_csv(path)

    def search(self, platform: str | None = None, limit: int = 20) -> List[Dict]:
        df = self.df
        if platform:
            df = df[df["platform"].str.upper()==platform.upper()]
        return df.head(limit).to_dict(orient="records")

class PolicyStore:
    def __init__(self, path: Path = DATA_DIR / "policies.json"):
        self.rules = json.loads(Path(path).read_text())

    def check(self, platform: str) -> Dict:
        default = self.rules.get("default", {})
        return self.rules.get(platform, default)