import hashlib
import importlib
import logging
import os
from io import BytesIO

from django.core.handlers.wsgi import WSGIRequest
from django.utils.http import parse_header_parameters

logger = logging.getLogger(__name__)


def alter_old_distutils_request(request: WSGIRequest):
    """Alter the request body for compatibility with older distutils clients

    Due to a bug in the Python distutils library, the request post is sent
    using \n as a separator instead of the \r\n that the HTTP spec demands.
    This breaks the Django form parser and therefore we have to write a
    custom parser.

    This bug was fixed in the Python 2.7.4 and 3.4:

    http://bugs.python.org/issue10510
    """
    # We first need to retrieve the body before accessing POST or FILES since
    # it can only be read once.
    body = request.body
    if request.POST or request.FILES:
        return

    new_body = BytesIO()

    # Split the response in the various parts based on the boundary string
    content_type, opts = parse_header_parameters(request.META['CONTENT_TYPE'])
    if "xml" in content_type:
        return
    parts = body.split(b'\n--' + (opts.get('boundary', "")).encode("utf8") + b'\n')
    for part in parts:
        if b'\n\n' not in part:
            continue

        headers, content = part.split(b'\n\n', 1)
        if not headers:
            continue

        new_body.write(b'--' + opts['boundary'].encode("utf8") + b'\r\n')
        new_body.write(headers.replace(b'\n', b'\r\n'))
        new_body.write(b'\r\n\r\n')
        new_body.write(content)
        new_body.write(b'\r\n')
    new_body.write(b'--' + (opts.get('boundary', "")).encode("utf8") + b'--\r\n')

    request._body = new_body.getvalue()
    request.META['CONTENT_LENGTH'] = len(request._body)

    # Clear out _files and _post so that the request object re-parses the body
    if hasattr(request, '_files'):
        delattr(request, '_files')
    if hasattr(request, '_post'):
        delattr(request, '_post')


def delete_files(sender, **kwargs):
    """Signal callback for deleting old files when database item is deleted"""
    instance = kwargs['instance']

    try:
        if not hasattr(instance.distribution, 'path'):
            return
    except ValueError:
        return

    if not os.path.exists(instance.distribution.path):
        return

    # Check if there are other instances which reference this fle
    is_referenced = (
        instance.__class__.objects
        .filter(distribution=instance.distribution)
        .exclude(pk=instance._get_pk_val())
        .exists())
    if is_referenced:
        return

    try:
        instance.distribution.storage.delete(instance.distribution.path)
    except Exception:
        logger.exception(
            'Error when trying to delete file %s of package %s:' % (
                instance.pk, instance.distribution.path))


def md5_hash_file(fh):
    """Return the md5 hash of the given file-object"""
    md5 = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


def get_versio_versioning_scheme(full_class_path):
    """Return a class based on it's full path"""
    module_path = '.'.join(full_class_path.split('.')[0:-1])
    class_name = full_class_path.split('.')[-1]
    try:
        module = importlib.import_module(module_path)
    except ImportError:
        raise RuntimeError('Invalid specified Versio schema {}'.format(full_class_path))

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise RuntimeError(
            'Could not find Versio schema class {!r} inside {!r} module.'.format(
                class_name, module_path))
