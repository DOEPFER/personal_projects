import argparse

parser = argparse.ArgumentParser(
    prog='mirror',
    description='Creates an exact copy of the directory specified in (source) to the directory specified in (mirror).',
    epilog='''
        Warning: The file synchronization flow is (source) -> (mirror).
        Any content (files and folders) in the (mirror) directory that is not present in the (source)
        will be deleted to maintain an exact copy of the (source) directory.
        Swapping the directories in the --source and --mirror arguments may result in file loss.
    '''
)

parser.add_argument('-s', '--source', help='Source directory.', type=str)
parser.add_argument('-m', '--mirror', help='Mirror directory.', type=str)
parser.add_argument('-i', '--ignore', nargs='*', help='Directories to ignore. Search scope: recursive.', type=str)
parser.add_argument('-l', '--logprefix', help='Log file prefix.', type=str, default='mirror')
parser.add_argument('-v', '--verbose', help='Verbose mode.', action='store_true')

args = parser.parse_args()