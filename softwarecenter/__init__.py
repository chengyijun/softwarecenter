from pathlib import Path

from django.conf import settings

uploads_dir = Path(settings.UPLOADS_ROOT)
if not uploads_dir.exists():
    uploads_dir.mkdir(mode=777)
    print("uploads文件夹被创建")
