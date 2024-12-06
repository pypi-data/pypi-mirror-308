"""
Handle downloading datasets from our content URL
"""

import os
import zipfile

from urllib.request import urlopen

from .signature import sha256sum
from .path import get_data_home, cleanup_dataset

from construe.exceptions import DatasetsError


# Downlod chunk size
CHUNK = 524288


def download_data(url, signature, data_home=None, replace=False, extract=True):
    """
    Downloads the zipped data set specified at the given URL, saving it to
    the data directory specified by ``get_data_home``. This function verifies
    the download with the given signature and extracts the archive.
    """
    data_home = get_data_home(data_home)

    # Get the name of the file from the URL
    basename = os.path.basename(url)
    name, _ = os.path.splitext(basename)

    # Get the archive and data directory paths
    archive = os.path.join(data_home, basename)
    datadir = os.path.join(data_home, name)

    # If the archive exists cleanup or raise override exception
    if os.path.exists(archive):
        if not replace:
            raise DatasetsError(
                ("dataset already exists at {}, set replace=False to overwrite").format(
                    archive
                )
            )

        cleanup_dataset(name, data_home=data_home)

    # Create the output directory if it does not exist
    if not os.path.exists(datadir):
        os.mkdir(datadir)

    # Fetch the response in a streaming fashion and write it to disk.
    response = urlopen(url)

    with open(archive, "wb") as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)

    # Compare the signature of the archive to the expected one
    if sha256sum(archive) != signature:
        raise ValueError("Download signature does not match hardcoded signature!")

    # If extract, extract the zipfile.
    if extract:
        zf = zipfile.ZipFile(archive)
        zf.extractall(path=data_home)
