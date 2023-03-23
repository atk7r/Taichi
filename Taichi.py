import argparse
import model.attack
import model.scan
from model import scan


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
    parser.add_argument('-e', '--exp', type=str, metavar="exp_path",
                        help='Please input exp path to scan.')
    return parser.parse_args()


def main():
    args = parse_args()

    rhost = args.rhost
    file = args.file
    outfile = args.outfile
    thread = args.thread
    poc = args.poc
    exp = args.exp

    if rhost:
        if poc:
            scan.scan_one(rhost, poc)
        elif exp:
            model.attack.attack_one(rhost, exp)
        else:
            print("Please input exp or poc to scan.")

    elif file:
        if thread is None:
            if poc:
                scan.scan_all(file, poc, outfile)
            elif exp:
                model.attack.attack_all(file, exp, outfile)
            else:
                print("Please input exp or poc to scan.")

        else:
            if poc:
                scan.scan_all_threads(file, poc, thread_num=thread, outfile=outfile)
            elif exp:
                model.attack.attack_all_threads(file, exp, thread_num=thread, outfile=outfile)
            else:
                print("Please input exp or poc to scan.")
    else:
        print("Please input -h for help.")


if __name__ == "__main__":
    main()
