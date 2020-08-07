import ijson
import csv
import os
import tempfile
import codecs


def convert(file, logger):
    file.seek(0)
    outfile = tempfile.TemporaryFile()
    wrapper_file = codecs.getwriter('utf-8')(outfile)
    features = ijson.items(file, 'features.item')
    writer = False
    for feature in features:
        row = feature['properties']
        row['geometry'] = feature['geometry']
        if not writer:
            writer = csv.DictWriter(
                wrapper_file,
                fieldnames=row.keys(),
                lineterminator=os.linesep
            )
            writer.writeheader()
        writer.writerow(row)
    outfile.seek(0)
    return outfile
