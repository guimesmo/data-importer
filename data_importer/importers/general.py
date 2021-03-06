# -*- coding: utf-8 -*-
from data_importer.readers.xls_reader import XLSReader
from data_importer.readers.xlsx_reader import XLSXReader
from data_importer.readers.csv_reader import CSVReader
from data_importer.core.exceptions import UnsuportedFile
from .base import BaseImporter


class DefaultImporter(BaseImporter):
    """
    An implementation of BaseImporter that sets the right reader
    by file extension.
    Probably the best choice for almost all implementation cases
    """
    def set_reader(self):
        reader = self.get_reader_class()
        self._reader = reader(self)

    def get_reader_class(self):
        """
        Gets the right file reader class by source file extension
        """
        readers = {
            'xls': XLSReader,
            'xlsx': XLSXReader,
            'csv': CSVReader,
            }
        source_file_extension = self.get_source_file_extension()

        # No reader for invalid extensions
        if source_file_extension not in readers.keys():
            raise UnsuportedFile("Unsuported File")

        return readers[source_file_extension]

    def get_source_file_extension(self):
        """
        Gets the source file extension. Used to choose the right reader
        """
        if isinstance(self.source, str):
            filename = self.source
        else:
            try:
                filename = self.source.file.name  # DataImporter.FileHistory instances
            except AttributeError:
                filename = self.source.name  # Default Python opened file
        ext = filename.split('.')[-1]
        return ext.lower()
