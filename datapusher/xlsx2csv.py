import csv
import tempfile
import openpyxl
import ckanserviceprovider.util as util


def convert(file, logger):
    outfile = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    try:
        file.seek(0)
        wb = openpyxl.load_workbook(file)
        sheet = wb.active
        with open(outfile.name, "w", newline="") as f:
            writer = csv.writer(f)
            for row in sheet.rows:
                writer.writerow([cell.value for cell in row])

    except IOError or csv.Error as e:
        logger.exception(e)
        raise util.JobError("An {} exception occurred : ".format(e), str(type(e)) , "with text \n", str(e))

    outfile.seek(0)
    return outfile
