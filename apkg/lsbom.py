import argparse
import logging
from .bom import BillOfMaterials

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='test lsbom implementation')
    parser.add_argument('bom', help='Path to BOMStore')

    args = parser.parse_args()

    with open(args.bom, 'rb') as fd:
        print('isbom')
        print(BillOfMaterials.is_bom(fd))
        b = BillOfMaterials(fileobj=fd)
        b.parse()
