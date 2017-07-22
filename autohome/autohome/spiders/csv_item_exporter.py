from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter

class MyCsvItemExporter(CsvItemExporter):
	def __init__(self, *args, **kwargs):
		kwargs['delimiter'] = settings.get('CSV_DELIMITER', ',')
		fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
		if fields_to_export:
			kwargs['fields_to_export'] = fields_to_export
		super(MyCsvItemExporter, self).__init__(*args, **kwargs)