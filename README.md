# mkvsubmerge

Split MKV file according to timestamp pairs specified by SRT
subtitle file and then merge into a new video file.

## Requirements

1. Python 3
2. MKVToolNix

## Install

Install latest version:

```bash
 pip install mkvsubmerge
```

For mkvtoolnix installation, see https://mkvtoolnix.download/downloads.html

On macOS you can install mkvtoolnix via brew:

```bash
brew install mkvtoolnix
```

## Upgrade

Upgrade to latest version:

```bash
pip install mkvsubmerge --upgrade
```

## Usage

    usage: mkvsubmerge [-h] [-o OUT] [--srt SRT]
                       [--srt-encoding SRT_ENCODING]
                       [--start-offset START_OFFSET]
                       [--end-offset END_OFFSET]
                       mkv

    positional arguments:
      mkv                   MKV file

    optional arguments:
      -h, --help            show this help message and exit
      -o OUT                output MKV file
      --srt SRT             SRT file
      --srt-encoding SRT_ENCODING
                            SRT file encoding
      --start-offset START_OFFSET
                            offset to apply to every start
                            timestamp
      --end-offset END_OFFSET
                            offset to apply to every end
                            timestamp

## Example

```bash
# Looks for `example_video.srt` under same directory. Will output to `example_video.surbmerge.mkv` under same directory.
mkvsubmerge example_video.mkv

# Will output to `example_video` under same directory.
mkvsubmerge example_video.mkv --srt example_srt.srt

# Will output `output_video.mkv`
mkvsubmerge example_video.mkv --srt example_srt.srt -o output_video.mkv

```

If some sentence appears not complete in the generated video file, chances are that some timestamp falls between two key frames. See https://mkvtoolnix.download/doc/mkvmerge.html#mkvmerge.description for detailed explanation:
> Note that mkvmerge(1) only makes decisions about splitting at key frame positions. This applies to both the start and the end of each range. So even if an end timestamp is between two key frames mkvmerge(1) will continue outputting the frames up to but excluding the following key frame. 

In that case you can extend every timestamp pair by specifying `--start-offset` and `end-offset` to include more key frames.

```bash
# This will extend every timestamp pair by two seconds. Every timestamp will start one second earlier and end one second later.
# No need to worry about overlapping/out-of-bounds timestamps as mkvsubmerge will take care of them.
mkvsubmerge example_video.mkv --start-offset -1000 --end-offset 1000
```

## About

Med0paW

medopaw@gmail.com

https://github.com/medopaw
