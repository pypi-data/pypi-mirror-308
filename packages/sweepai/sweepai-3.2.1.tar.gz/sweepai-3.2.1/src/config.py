import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=bool(os.environ.get("ENVIRONMENT")), verbose=True)

ENV: Literal["dev", "prod"] = os.environ.get("ENV", "prod")  # type: ignore
DEV: bool = ENV.lower() == "dev"
