#!/usr/bin/env python

import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(description = "Scan devices on LAN")
parser.add_argument("network",dest)