from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"


class DirConfig:
    root_dir = PROJECT_ROOT
    src_dir = SRC_DIR
    data_dir = DATA_DIR


class GeoConfig:
    root = DATA_DIR / "geo"
    encrypted_database_fp = root / "db.gz"
    decompressed_data_fp = root / "decompressed.bin"
    decompressed_json_fp = root / "decompressed.json"


class NAICS2022Config:
    edition = "2022"
    root = DATA_DIR / "naics/2022"
    encrypted_database_fp = root / "database.bin"
    search_data_fp = root / "database.json"


class Config:
    dir = DirConfig
    geo = GeoConfig
    encryption_key = PROJECT_ROOT / "key.key"
