from pathlib import Path
from app.config.settings import settings


class FileStorage:
    def save(self, image_data, path_segments: list[str]) -> str:
        path = settings.IMAGES_DIR.joinpath(*path_segments)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            f.write(image_data)
        return str(path)