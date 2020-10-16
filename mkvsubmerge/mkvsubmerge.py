#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# The MIT License (MIT)
# 
# Copyright (c) 2020 Med0paW
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# add correct version number here
__version__ = "0.0.4"

PROGRAMNAME = "mkvsubmerge"
VERSION = __version__
COPYRIGHT = "(C) 2020 Med0paW"

import logging
import argparse
import pysrt
from pysrt.srttime import SubRipTime
from pymkv import MKVFile
from os import path


def to_timestamp(self):
    return str(self).replace(',', '.')


def main():
    logger = logging.getLogger(__name__)

    SubRipTime.to_timestamp = to_timestamp

    parser = argparse.ArgumentParser(prog='mkvsubmerge', description='Split MKV file according to timestamp pairs '
                                                                     'specified by SRT subtitle file and then merge '
                                                                     'into a new video file.')
    parser.add_argument('mkv', help='MKV file')
    parser.add_argument('-o', dest='out', help='output MKV file')
    parser.add_argument('--srt', help='SRT file')
    parser.add_argument('--srt-encoding', help='SRT file encoding')
    parser.add_argument('--start-offset', type=int, default=0, help='offset to apply to every start timestamp')
    parser.add_argument('--end-offset', type=int, default=0, help='offset to apply to every end timestamp')

    args = parser.parse_args()

    mkv_path = args.mkv
    output_path = args.out or '{}.submerge.mkv'.format(path.splitext(mkv_path)[0])
    srt_path = args.srt or '{}.srt'.format(path.splitext(mkv_path)[0])
    srt_encoding = args.srt_encoding
    start_offset = args.start_offset
    end_offset = args.end_offset

    # Ensure both files exist
    if not path.exists(mkv_path):
        logger.error('{} does not exist.'.format(mkv_path))
        exit(1)
    if not path.exists(srt_path):
        logger.error('{} does not exist.'.format(srt_path))
        exit(1)

    # Read srt file
    subs = pysrt.open(srt_path, encoding=srt_encoding)
    subs.clean_indexes()  # Sort first to ensure order

    # Form timestamps
    timestamps = []  # In even number
    for sub_item in subs:
        # Address the key frame problem by introducing offset parameter.
        # See https://mkvtoolnix.download/doc/mkvmerge.html#mkvmerge.description
        start_timestamp = (sub_item.start + start_offset).to_timestamp()
        end_timestamp = (sub_item.end + end_offset).to_timestamp()
        if len(timestamps) == 0:
            timestamps.append(start_timestamp)
            # timestamps.append(0)
            timestamps.append(end_timestamp)
        else:
            last_timestamp = timestamps[-1]
            if end_timestamp > last_timestamp:  # Otherwise the clip is contained by the previous one
                if start_timestamp > last_timestamp:  # Notice that it should be > instead of >=
                    timestamps.append(start_timestamp)
                    timestamps.append(end_timestamp)
                else:  # Replace last timestamp with `end_timestamp`
                    timestamps[-1] = end_timestamp

    logger.info('{} timestamp pair(s) in total.'.format(len(timestamps) / 2))

    # Generate new files
    mkv = MKVFile(mkv_path)
    mkv.split_timestamp_parts([timestamps])
    mkv.mux(output_path)


if __name__ == "__main__":
    main()
