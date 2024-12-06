"""
Manifest handlers for downloading and checking signatures
"""

import os
import json
import glob

from urllib.parse import urljoin

from .signature import sha256sum
from ..version import get_version
from .path import FIXTURES, MANIFEST


BASE_URL = "https://storage.googleapis.com/"


def load_manifest(path=MANIFEST):
    with open(MANIFEST, "r") as f:
        return json.load(f)


def generate_manifest(fixtures=FIXTURES, out=MANIFEST):
    out = out or MANIFEST

    manifest = {}
    version = get_version(short=True)

    for path in glob.glob(os.path.join(fixtures, "*.zip")):
        fname = os.path.basename(path)
        name, _ = os.path.splitext(fname)

        manifest[name] = {
            "url": urljoin(BASE_URL, f"construe/v{version}/{fname}"),
            "signature": sha256sum(path),
        }

    with open(out, "w") as o:
        json.dump(manifest, o, indent=2)
