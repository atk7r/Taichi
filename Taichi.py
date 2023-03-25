import argparse
import configuration.config
import model.scan
from model.load_all import load_all_files
import model.load_all


def parse_args():
    parser = argparse.ArgumentParser(description="Taichi by atk7r")
    parser.add_argument('-rh', '--rhost', type=str, metavar="remote_host",
                        help='Please input host to scan.')
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), metavar="file_path",
                        help='Please input file path to scan.')
    parser.add_argument('-o', '--outfile', metavar="outfile_path",
                        help="Please input path for output file.")
    parser.add_argument('-t', '--thread', type=int, metavar="thread_num",
                        help='Please input thread number.')
    parser.add_argument('-p', '--poc', type=str, metavar="poc_path",
                        help='Please input poc path to scan.')
    parser.add_argument('-a', '--all', type=str, metavar="all poc or exp",
                        help='Please input poc path to scan.')

    return parser.parse_args()


def main():
    args = parse_args()

    rhost = args.rhost
    file = args.file
    outfile = args.outfile
    thread = args.thread
    poc = args.poc
    all = args.all

    if rhost:
        if all:
            for i in load_all_files(all):
                model.scan.scan_one(rhost, poc=i)
        else:
            if all is None:
                model.scan.scan_one(rhost, poc)
            else:
                print("Please input poc to scan.")

    elif file:
        if thread is None:
            if all:
                for i in load_all_files(all):
                    model.scan.scan_all(file, poc=i, outfile=outfile)
            else:
                if all is None:
                    model.scan.scan_all(file, poc, outfile=outfile)
                else:
                    print("Please input poc path to scan.")

        else:
            if all:
                for i in load_all_files(all):
                    model.scan.scan_all_threads(file, poc=i, thread_num=thread, outfile=outfile)
            else:
                if all is None:
                    model.scan.scan_all_threads(file, poc, thread_num=thread, outfile=outfile)
                else:
                    print("Please input poc to scan.")
    else:
        print("Please input -h for help.")


if __name__ == "__main__":
    main()
