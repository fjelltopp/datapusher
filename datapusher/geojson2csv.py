import ijson
import json
import csv
import os
import tempfile
import codecs
import ckanserviceprovider.util as util


def floaten(event):
    """
    If the ijson event is numeric, ensure that it is a Float and not Decimal.
    """
    if event[1] == 'number':
        return (event[0], event[1], float(event[2]))
    else:
        return event


def convert(file, logger):

    file.seek(0)
    outfile = tempfile.TemporaryFile()
    wrapper_file = codecs.getwriter('utf-8')(outfile)
    events = map(floaten, ijson.parse(file))
    features = ijson.common.items(events, 'features.item')
    writer = False

    for feature in features:
        try:
            if not writer:
                fieldnames = list(feature['properties'].keys())
                fieldnames = fieldnames + ['geometry']  # Ensure geometry is last
                writer = csv.DictWriter(
                    wrapper_file,
                    fieldnames=fieldnames,
                    lineterminator=os.linesep
                )
                writer.writeheader()
            row = feature['properties']
            row['geometry'] = json.dumps(feature['geometry'])
            writer.writerow(row)

        except KeyError as e:
            logger.exception(e)
            raise util.JobError("GeoJSON feature must have 'properties' and 'geometry' fields.")
        except ValueError as e:
            logger.exception(e)
            raise util.JobError("Each GeoJSON feature must have the same properties in order to convert to table. ")

    if not outfile.tell():
        raise util.JobError("No valid features found in the GeoJSON")

    outfile.seek(0)
    return outfile
