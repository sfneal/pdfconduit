import json
import os


def main():
    from argparse import ArgumentParser

    # Declare argparse argument descriptions
    usage = "View test timings"
    description = "View test timings saved to json."

    # construct the argument parse and parse the arguments
    ap = ArgumentParser(usage=usage, description=description)
    ap.add_argument(
        "--times", action="store_true", help="Sort test results by execution time"
    )
    ap.add_argument(
        "--ascending", action="store_true", help="Order test results in ascending order"
    )
    args = ap.parse_args()

    json_path = os.path.join(os.path.dirname(__file__), "data", "timings.json")

    with open(json_path, "r") as json_file:
        data = json.load(json_file)

    if args.times:
        data = dict(
            sorted(
                data.items(),
                key=lambda item: item[1],
                reverse=args.ascending if args.ascending else False,
            )
        )

    for test_name, time in data.items():
        first = "{0:85}".format(test_name)
        print("{0:86} {1:7} msecs".format(first, time))


if __name__ == "__main__":
    main()
