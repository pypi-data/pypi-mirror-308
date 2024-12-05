# DFRobotUPS.__main__



import argparse
import functools
import logging
import logging.handlers
import os
import sys
from time import sleep

from . import (__version__, DFRobotUPS, DEFAULT_ADDR, DEFAULT_BUS, PID,
               DETECT_OK, DETECT_NOSMBUS, DETECT_NODEVICE, DETECT_INVALIDPID)



# --- constants ---



# default and ranges of values for command line parameters

DEFAULT_PERCENT = 7
DEFAULT_INTERVAL = 60
DEFAULT_RETRY = 10
DEFAULT_CMD = "/sbin/halt"

MIN_PERCENT = 5
MAX_PERCENT = 95

MIN_INTERVAL = 1
MAX_INTERVAL = 600



# --- parse arguments ---



# factory function for range-checked integer as type of ArgumentParser
# arguments

def int_range(min=0, max=100):
    def int_range_check(s):
        v = int(s)
        if min <= v <= max:
            return v
        else:
            raise argparse.ArgumentTypeError(f"value not in range {min}-{max}")

    return int_range_check


parser = argparse.ArgumentParser(
    # override the program name as running this as a __main__ inside a
    # module # directory will use '__main__' by default - this name
    # isn't necessarily correct, but it looks better than that
    prog="DFRobotUPS",

    # text to display after the command line arguments help
    epilog="By default, the current charge status and battery voltage"
           " will be displayed and the program will terminate.  Using"
           " the -s option will cause the program to poll the charge"
           " level and run a shutdown command, when it drops below a"
           " specified level."
    )

parser.add_argument(
    "-s", "--shutdown",
    action="store_true",
    help="poll the battery SoC and initiate system shutdown when level"
         " drops below the defined level")

parser.add_argument(
    "-p", "--percent",
    type=int_range(MIN_PERCENT, MAX_PERCENT),
    default=DEFAULT_PERCENT,
    help="State of Charge (SoC) percentage at which to trigger shutdown"
         f" shutdown (min: {MIN_PERCENT}, max: {MAX_PERCENT}, default: "
         f" {DEFAULT_PERCENT})")

parser.add_argument(
    "-i", "--interval",
    type=int_range(MIN_INTERVAL, MAX_INTERVAL),
    default=DEFAULT_INTERVAL,
    help="number of seconds between polls of the battery SoC (min:"
         f" {MIN_INTERVAL}, max: {MAX_INTERVAL}, default:"
         f" {DEFAULT_INTERVAL})")

parser.add_argument(
    "-c", "--cmd",
    nargs="+",
    default=(DEFAULT_CMD, ),
    metavar=("CMD", "ARG"),
    help=f"command to run to trigger shutdown (default: {DEFAULT_CMD})")

parser.add_argument(
    "-a", "--addr",
    type=functools.partial(int, base=0),
    default=DEFAULT_ADDR,
    help="I2C address for UPS HAT; can be specified in hex as 0xNN"
         f" (default: 0x{DEFAULT_ADDR:02x})")

parser.add_argument(
    "-b", "--bus",
    type=int,
    default=DEFAULT_BUS,
    help=f"I2C SMBus number for UPS HAT (default: {DEFAULT_BUS})")

parser.add_argument(
    "-r", "--retry",
    type=int,
    default=DEFAULT_RETRY,
    help="number of times to try connecting to the UPS HAT (default:"
         f" {DEFAULT_RETRY})")

parser.add_argument(
    "-d", "--debug",
    action="count",
    default=0,
    help="increase debugging level (max: 2, default: 0)")

parser.add_argument(
    "-v", "--version",
    action="version",
    version=__version__)

args = parser.parse_args()



# --- create logger ---



# create logger object and set the overall debugging level (we'll
# override this in each handler, below, but this level stops anything
# being logged that is less severe, in any handler)

logger = logging.getLogger("DFRobotUPS")
logger.setLevel(logging.DEBUG)


# create logging handler with formatter for stderr - the level here
# depends on the command line options specified

stderr_loghandler = logging.StreamHandler(stream=sys.stderr)
stderr_logformatter = logging.Formatter("%(levelname)s: %(message)s")
stderr_loghandler.setFormatter(stderr_logformatter)
stderr_loghandler.setLevel(logging.DEBUG if args.debug >= 2
                               else logging.INFO if args.debug >= 1
                               else logging.WARNING)


# add the stderr handler as a logger destination

logger.addHandler(stderr_loghandler)


# create a syslog handler, if we're running in shutdown mode

if args.shutdown:
    # create logging handler with formatter for syslog - we always log
    # at INFO level here
    syslog_loghandler = logging.handlers.SysLogHandler(address="/dev/log")
    syslog_logformatter = logging.Formatter(
                              "%(name)s[%(process)d]: %(message)s")
    syslog_loghandler.setFormatter(syslog_logformatter)
    syslog_loghandler.setLevel(logging.INFO)

    # add the syslog handler as a logger destination
    logger.addHandler(syslog_loghandler)



# --- main ---



logger.info("startup: DFRobotUPS v{__version__}")


# try to detect the UPS

logger.info(f"searching for UPS HAT on bus {args.bus} at I2C address"
            f" 0x{args.addr:02x}")

tries = 0
while True:
    tries += 1
    ups = DFRobotUPS(addr=args.addr, bus=args.bus)

    if ups.detect == DETECT_OK:
        break

    logger.warning(
        f"connection failed error code {ups.detect}"
        f" ({ups.detectstr()}), try {tries} of {args.retry}")

    # if we've run out of tries, stop
    if tries == args.retry:
        break

    sleep(1)

if ups.detect != DETECT_OK:
    if ups.detect == DETECT_NODEVICE:
        logger.error("no device found at I2C address")

    elif ups.detect == DETECT_INVALIDPID:
        logger.error("device PID invalid for UPS HAT")

    else:
        logger.error(f"detection failed - unknown reason: {ups.detect}")

    sys.exit(1)


# log some information about the UPS and, if we're debugging print it
# there too

logger.info(f"UPS HAT found with product ID 0x{ups.pid:02x}, firmware"
            + (" version %d.%d" % ups.fwver))


# if we're in shutdown polling mode, do that

if args.shutdown:
    logger.info(
        f"initial SoC {ups.soc:.2f}%, polling for shutdown at"
        f" {args.percent}% every {args.interval}s, shutdown command:"
        f" { ' '.join(args.cmd) }")

    while True:
        soc = ups.soc

        if soc <= args.percent:
            break

        logger.debug(f"current SoC {soc:.2f}% above shutdown threshold at"
                     f" {args.percent}% - sleeping for {args.interval}s")

        sleep(args.interval)

    logger.info(
        f"shutdown: current SoC {soc:.2f}% has reached trigger at"
        f" {args.percent}% - executing:" f" { ' '.join(args.cmd) }")

    # execute the shutdown command, which will replace this process
    os.execv(args.cmd[0], args.cmd)

    # we'll never get here


# we're in information mode, so just print that

print(f"State of Charge (SoC) {ups.soc:.2f}%, battery voltage {ups.vcell}mV")
