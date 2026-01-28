import argparse

parser = argparse.ArgumentParser(
    prog='healthcheck',
    description='Check if the provided addresses return an HTTP 200 status code.'
)

parser.add_argument('-u', '--urls', nargs='+', help="URL's.", type=str)
parser.add_argument('-l', '--logprefix', help='Log file prefix.', type=str, default='mirror')
parser.add_argument('-v', '--verbose', help='Verbose mode.', action='store_true')
parser.add_argument('-s', '--sendmail', help='Send email if an error occurs.', action='store_true')

args = parser.parse_args()