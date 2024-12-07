import winzy
import os
import sys


def create_parser(subparser):
    parser = subparser.add_parser("notify", description="Notify in mac and windows")
    parser.add_argument("msg", type=str, nargs="*", help="The message to show.")
    parser.add_argument("-t", "--title", type=str, help="Title to use.", default="Notify")
    
    return parser


class HelloWorld:
    """ Notify in mac and windows """
    __name__ = "notify"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.notify)

    def notify(self, args):
        if args.msg:
            msg = " ".join(args.msg)
        else:
            msg = sys.stdin.read()

        title = args.title.strip()

        rest_command = f"""'display notification "{msg}" with title "{title}" sound name "Submarine"'"""
        os.system("osascript -e " + rest_command)
    
    def hello(self, args):
        # this routine will be called when "winzy notify is called."
        print("Hello! This is an example ``winzy`` plugin.")

notify_plugin = HelloWorld()
