import time
from pathlib import Path
from typing import List, Dict
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils.encoding import escape_uri_path
from django.views import View


class IndexView(View):
    def get(self, request: WSGIRequest):
        return render(request, "index.html")


class HistoryView(View):
    def get(self, request: WSGIRequest):
        file_infos = get_files()

        return render(request, "history.html", {"file_infos": file_infos})


class UploadView(View):
    def get(self, request: WSGIRequest):
        file_infos = get_files()
        return render(request, "upload.html", {"file_infos": file_infos})

    def post(self, request: WSGIRequest):
        files = request.FILES

        file: InMemoryUploadedFile = files.get("file")
        file_path = Path(settings.UPLOADS_ROOT).joinpath(file.name)
        with open(str(file_path), 'wb') as f:
            for chuck in file.chunks():
                f.write(chuck)
        return JsonResponse({"status": True})


def get_files() -> List[Dict[str, str]]:
    """
    获取文件信息
    :return:
    """
    uploads_dir = Path(settings.UPLOADS_ROOT)
    files = uploads_dir.glob("*.*")

    files_sorted = sorted(files, key=lambda x: x.stat().st_ctime, reverse=True)
    file_infos = [
        {"filename": f.name,
         "filectime": time.strftime("%Y-%m-%d", time.localtime(f.stat().st_ctime))}
        for f in
        files_sorted]
    return file_infos


class DownloadFileView(View):
    def get(self, request: WSGIRequest, target: str):
        # try:
        #     response = FileResponse(open(f"uploads/{target}", 'rb'))
        #     response['content_type'] = "application/octet-stream"
        #     response['Content-Disposition'] = 'attachment; filename=' + escape_uri_path(target)
        #     return response
        # except Exception:
        #     raise Http404

        # chunk_size = 8192
        # file_path = f"uploads/{target}"
        # response = StreamingHttpResponse(
        #     FileWrapper(open(file_path, 'rb'), chunk_size),
        #     content_type="application/octet-stream"
        # )
        # # 高速浏览器 文件的的大小 这很重要
        # response['Content-Length'] = os.path.getsize(file_path)
        # response['Content-Disposition'] = 'attachment; filename=' + escape_uri_path(target)
        # return response

        chunk_size = 8192
        file_path = Path(settings.UPLOADS_ROOT).joinpath(target)
        response = FileResponse(
            FileWrapper(open(str(file_path), 'rb'), chunk_size),
            content_type="application/octet-stream"
        )

        # 高速浏览器 文件的的大小 这很重要
        response['Content-Length'] = file_path.stat().st_size
        response['Content-Disposition'] = 'attachment; filename=' + escape_uri_path(target)
        return response


class DeleteFileView(View):
    def get(self, request: WSGIRequest, target: str):
        # os.remove(f"uploads/{target}")
        file_path = Path(settings.UPLOADS_ROOT).joinpath(target)
        if file_path.exists():
            file_path.unlink()
        return redirect(reverse("app:upload"))
