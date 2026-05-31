import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


def _file_response(file_path: Path):
    content_type, _ = mimetypes.guess_type(str(file_path))
    return FileResponse(file_path.open('rb'), content_type=content_type or 'application/octet-stream')


def serve_media(request, path):
    """
    Sirve archivos bajo /media/.
    - Prioridad: MEDIA_ROOT (uploads actuales, p. ej. recipes/details/...)
    - Fallback: carpeta legacy BASE_DIR/recipes/ (imágenes antiguas recipes/foo.png)
    """
    media_path = settings.MEDIA_ROOT / path
    if media_path.is_file():
        return _file_response(media_path)

    if path.startswith('recipes/'):
        relative = path[len('recipes/') :]
        # Solo archivos planos en la raíz legacy (no subcarpetas como details/)
        if relative and '/' not in relative:
            legacy_path = settings.BASE_DIR / 'recipes' / relative
            if legacy_path.is_file():
                return _file_response(legacy_path)

    raise Http404('Media file not found')
