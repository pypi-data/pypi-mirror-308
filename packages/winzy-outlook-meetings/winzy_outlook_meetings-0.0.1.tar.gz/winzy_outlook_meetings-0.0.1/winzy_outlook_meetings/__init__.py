import winzy
from winzy_outlook_meetings.app import get_outlook_schedule
from datetime import datetime


def create_parser(subparser):
    parser = subparser.add_parser(
        "outcal", description="Get outlook calendar entries in commandline "
    )
    parser.add_argument(
        "-s",
        "--start",
        help="Start date (YYYY-MM-DD)",
        default=datetime.today(),
        type=str,
    )
    parser.add_argument("-d", "--days", type=int, default=1)
    return parser


class HelloWorld:
    """ Get outlook calendar entries in commandline  """

    __name__ = "outcal"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.run)

    def run(self, args):
        output = get_outlook_schedule(begin=args.start, days=args.days)
        with open(output, "r") as fin:
            for line in fin:
                print(line.strip())

    def hello(self, args):
        # this routine will be called when "winzy outcal is called."
        print("Hello! This is an example ``winzy`` plugin.")


outcal_plugin = HelloWorld()
