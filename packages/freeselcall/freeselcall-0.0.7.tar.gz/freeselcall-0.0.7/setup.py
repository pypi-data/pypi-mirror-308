# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freeselcall']

package_data = \
{'': ['*'],
 'freeselcall': ['static/*',
                 'static/bootstrap-5.3.3-dist/*',
                 'static/bootstrap-5.3.3-dist/css/*',
                 'static/bootstrap-5.3.3-dist/js/*']}

install_requires = \
['cffi>=1.16.0,<2.0.0',
 'configargparse>=1.7,<2.0',
 'flask-socketio>=5.3.6,<6.0.0',
 'flask>=3.0.2,<4.0.0',
 'prompt-toolkit>=3.0.43,<4.0.0',
 'pyaudio>=0.2.11,<0.3.0',
 'pydub>=0.25.1,<0.26.0',
 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['freeselcall = freeselcall:__main__.main']}

setup_kwargs = {
    'name': 'freeselcall',
    'version': '0.0.7',
    'description': '',
    'long_description': "Freeselcall\n==\n[![scratchanitch.dev badge](https://img.shields.io/badge/scratchanitch-dev-FFC4B5)](https://scratchanitch.dev)\n\nCodan 4 digit Selcall encoder and decoder\n\n> [!IMPORTANT]  \n> This project is to scratch an itch. It works on a very limited set of Codan HF Selcall. It likely won't work with other vendors or even other types of Codan Selcall. If you want to have support for these, you'll have to work it out - though I will accept well crafted pull requests.\n> \n> Code in this repo is hacky and barely functional. There are likely performance issues and many edge cases. Feel free to log issues for these, however I won't be able to address all of them. Nor will I be timely.\n>\n> I made this because I couldn't find anything else that did this. I did not want to make this.\n> \n> This is not a place of honor\n\n## Features\n - Codan HF Selcall (4 digits)\n - Codan Page calls - sending and receiving - with magic bytes\n - Basic web interface\n - CLI interface\n - Websockets for application integration\n\n![Screenshot of the CLI for freeselcall](./docs/cli.png)\n\n## Unsupported\n - Windows\n\n## Requirements\n - hamlib\n - portaudio / pyaudio\n - c build tools / cmake\n\n## Running with Docker\n\nExample:\n```\ndocker run -p 5001:5001 --name freeselcall --rm --device /dev/snd -it ghcr.io/xssfox/freeselcall:latest --help\n```\n\n## Install with pip\n```\n# install required system packages\nsudo apt-get update\nsudo apt install git build-essential cmake portaudio19-dev python3 python3-dev libhamlib-utils\n\nsudo apt install pipx\npipx ensurepath\n\n# make sure the PATH is set correctly\nsource ~/.profile\n\npipx install freeselcall\n\nfreeselcall --help\n```\n\n\n## Install from source\n\nInstructions for a raspberrypi. Requires bookworm or python 3.11 to be installed. UNTESTED\n\n```sh\n# install required system packages\nsudo apt-get update\nsudo apt install git build-essential cmake portaudio19-dev python3 python3-dev libhamlib-utils\n\nsudo apt install pipx\npipx ensurepath\n\n# make sure the PATH is set correctly\nsource ~/.profile\n\npipx install poetry\n\n\n# install freeselcall\ngit clone --recurse-submodules https://github.com/xssfox/freeselcall.git\ncd freeselcall\n\n# the headers installed by libcodec2 make install don't include kiss_fftr.h required by the modem\npoetry install\npoetry shell\npython3 -m freeselcall\n```\n\n\n## Running\n```\n# Run rigctld in background. See rigctld --help on how to configure your rig\nrigctld -m 1 -r /dev/null &\n\n# Test to make sure rigctl works\nrigctl -m 2 T 1 # enable PTT\nrigctl -m 2 T 0 # disable PTT\n\n# Get argument help\nfreeselcall --help\n\n#list audio devices\nfreeselcall --list-audio-devices\n\nfreeselcall --output-device 0 --input-device 0 --log-level DEBUG # it's useful to have debug turned on when first testing\n```\n\n## Testing\n\nThe CLI has a handy `test_ptt` to make test that PTT and sound output is working.\n\n## Web\nBy default the web interface runs on port 5002. It can be accessed at http://localhost:5002/\n\n![Freeselcall web interface](./docs/web.png)\n\nSocket.io is used to. Subscribe to:\n - selcall\n - preamble\n - info\n\nEmit:\n - info\n - selcall, id\n\n## Command line arguments\n```\nfreeselcall --help\n\\usage: freeselcall [-h] [-c C] [--no-cli] [--list-audio-devices] [--log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}] [--input-device INPUT_DEVICE] [--output-device OUTPUT_DEVICE]\n                   [--output-volume OUTPUT_VOLUME] [--rigctld-port RIGCTLD_PORT] [--rigctld-selcall-commands RIGCTLD_SELCALL_COMMANDS] [--rigctld-pretx RIGCTLD_PRETX] [--rigctld-posttx RIGCTLD_POSTTX]\n                   [--rigctld-host RIGCTLD_HOST] [--ptt-on-delay-ms PTT_ON_DELAY_MS] [--ptt-off-delay-ms PTT_OFF_DELAY_MS] [--id ID] [--no-web] [--web-host WEB_HOST] [--web-port WEB_PORT]\n\noptions:\n  -h, --help            show this help message and exit\n  -c C, -config C       config file path\n  --no-cli              [env var: FREESELCALL_NO_CLI]\n  --list-audio-devices\n  --log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}\n                        [env var: FREESELCALL_LOG_LEVEL]\n  --input-device INPUT_DEVICE\n                        [env var: FREESELCALL_INPUT_DEVICE]\n  --output-device OUTPUT_DEVICE\n                        [env var: FREESELCALL_OUTPUT_DEVICE]\n  --output-volume OUTPUT_VOLUME\n                        in db. postive = louder, negative = quiter [env var: FREESELCALL_OUTPUT_DB]\n  --rigctld-port RIGCTLD_PORT\n                        TCP port for rigctld - set to 0 to disable rigctld support [env var: FREESELCALL_RIGTCTLD_PORT]\n  --rigctld-selcall-commands RIGCTLD_SELCALL_COMMANDS\n                        Commands to send the rigctl server - for example 'L SQL 0' on ICOM will disable squelch when selcall is received [env var: FREESELCALL_RIGTCTLD_COMMAND]\n  --rigctld-pretx RIGCTLD_PRETX\n                        Commands to send the rigctl server before TXing (PTT already included) [env var: FREESELCALL_RIGTCTLD_PRETX_COMMAND]\n  --rigctld-posttx RIGCTLD_POSTTX\n                        Commands to send the rigctl server after TXing [env var: FREESELCALL_RIGTCTLD_POSTTX_COMMAND]\n  --rigctld-host RIGCTLD_HOST\n                        Host for rigctld [env var: FREESELCALL_RIGTCTLD_HOST]\n  --ptt-on-delay-ms PTT_ON_DELAY_MS\n                        Delay after triggering PTT before sending data [env var: FREESELCALL_PTT_ON_DELAY_MS]\n  --ptt-off-delay-ms PTT_OFF_DELAY_MS\n                        Delay after sending data before releasing PTT [env var: FREESELCALL_PTT_OFF_DELAY_MS]\n  --id ID               ID to notify of selcall and used to send selcall [env var: FREESELCALL_ID]\n  --no-web              [env var: FREESELCALL_NO_WEB]\n  --web-host WEB_HOST   [env var: FREESELCALL_WEB_HOST]\n  --web-port WEB_PORT   [env var: FREESELCALL_WEB_PORT]\n\nArgs that start with '--' can also be set in a config file (~/.freeselcall.conf or specified via -c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). In\ngeneral, command-line values override environment variables which override config file values which override defaults.\n```\n\n## CLI commands\n```\nFreeselcall Help \n--------------- \nclear \n   Clears TX queues \ndebug \n   Open the debug shell \nexception \n   Raises and exemption to test the shell \nexit \n   Exits freeselcall \nhelp \n   This help \nid \n   Sets ID - example: callsign N0CALL \nlist_audio_devices \n   Lists audio device parameters \nlog_level \n   Set the log level \nsave_config \n   Save a config file to ~/.freeselcall.conf. Warning this will override your current config \nselcall \n   Performs a selcall - example: selcall 1234 \ntest_ptt \n   Turns on PTT for 2 seconds \nvolume \n   Set the volume gain in db for output level - you probably want to use soundcard configuration or radio configuration rather than this.\n```\n\nCredits\n--\nDavid Rowe and the FreeDV team for developing the modem and libraries ",
    'author': 'xssfox',
    'author_email': 'xss@sprocketfox.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}
from build_lib import *
build(setup_kwargs)

setup(**setup_kwargs)
