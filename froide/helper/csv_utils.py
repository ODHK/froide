from django.utils import six
from django.http import StreamingHttpResponse


def export_csv_response(generator, name='export.csv'):
    response = StreamingHttpResponse(generator, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % name
    return response


class FakeFile(object):
    # unicodecsv doesn't return values
    # so temp store them in here
    def write(self, string):
        self._last_string = string
        if six.PY3:
            self._last_string = self._last_string.encode('utf-8')


def export_csv(queryset, fields):
    if six.PY3:
        import csv
    else:
        import unicodecsv as csv

    f = FakeFile()
    writer = csv.DictWriter(f, fields)
    writer.writeheader()
    yield f._last_string
    for obj in queryset:
        if hasattr(obj, 'get_dict'):
            d = obj.get_dict(fields)
        else:
            d = {}
            for field in fields:
                value = getattr(obj, field, '')
                if value is None:
                    d[field] = ""
                else:
                    d[field] = six.text_type(value)
        writer.writerow(d)
        yield f._last_string


def export_csv_bytes(generator):
    return six.binary_type().join(generator)
