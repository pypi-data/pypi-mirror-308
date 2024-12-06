import winzy
import sys
import os

BASEURL = " 'https://wttr.in/{city}{cmdlist}'"

def get_initial_command():
    return "powershell -c Invoke-RestMethod" if sys.platform.startswith("win") else "curl"


def create_parser(subparser):
    parser = subparser.add_parser("weather", description="Weather using the excellent wttr.in")
    # Add subprser arguments here.
    parser.add_argument("-c", "--city", type=str, default=None, help="Name of the city")
    parser.add_argument("-w", "--wide", action="store_true", help="Print in wide format")
    parser.add_argument("-nf", "--no-forecast", action="store_true", help="Show current weather. No forecast")
    parser.add_argument("-t", "--today", action="store_true", help="Show Today's forecast")
    parser.add_argument("-f", "--full", action="store_true", help="Show Full 3 day's forecast")


    return parser


class HelloWorld:
    """ Weather using the excellent wttr.in """
    __name__ = "weather"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.main)

    def build_cmd(self, args):
        prog_cmd = get_initial_command()

        city = args.city if args.city else ""
        
        cmdlist = ["?qF"]
        if not args.wide:
           cmdlist.append("n")

        if args.no_forecast:
            cmdlist.append("0")

        if args.today:
            cmdlist.append("1")
        
        if args.full:
            cmdlist.append("2")

        cmd = prog_cmd+ BASEURL.format(city=city, cmdlist="".join(cmdlist))

        return cmd
    

    def main(self, args):
        cmd = self.build_cmd(args)
        _=os.system(cmd)    
        
    
    def hello(self, args):
        # this routine will be called when "winzy weather is called."
        print("Hello! This is an example ``winzy`` plugin.")

weather_plugin = HelloWorld()
