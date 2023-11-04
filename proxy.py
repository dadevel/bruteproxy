from pathlib import Path
import logging
import warnings

from mitmproxy import http
from mitmproxy.script import concurrent
from mitmproxy.net.http import http1

MAGIC_PASSWORD = b'FUZZPASS'
DUMP_DIR = Path('./logins')
DUMP_DIR.mkdir(exist_ok=True)
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')


async def request(flow: http.HTTPFlow) -> None:
    if flow.is_replay == 'request':
        return

    if flow.request.method != 'POST' or not flow.request.content or MAGIC_PASSWORD not in flow.request.content:
        return

    filepath = DUMP_DIR/f'{pathfilter(flow.request.scheme)}-{pathfilter(flow.request.host)}-{flow.request.port}.req.txt'
    with open(filepath, 'wb') as file:
        file.write(http1.assemble_request(flow.request))
    logger.info(f'detected magic password in request to {flow.request.url} and dumped request to {filepath}')

    # TODO: start brute forcing in background thread
    #flow = flow.copy()
    #if 'view' in ctx.master.addons:
    #    ctx.master.commands.call('view.flows.duplicate', [flow])
    #ctx.master.commands.call('replay.client', [flow])


def pathfilter(data: str) -> str:
    return data.replace('/', '').replace('..', '')


async def response(flow: http.HTTPFlow) -> None:
    # TODO: create custom wordlists based on website content
    pass
