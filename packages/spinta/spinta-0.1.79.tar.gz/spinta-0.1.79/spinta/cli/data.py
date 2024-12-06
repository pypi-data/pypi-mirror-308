import asyncio
import itertools
import json
from typing import Optional

from typer import Context as TyperContext
from typer import Option

from spinta import commands
from spinta.backends.helpers import validate_and_return_transaction
from spinta.cli.helpers.auth import require_auth
from spinta.cli.helpers.store import prepare_manifest
from spinta.cli.helpers.data import process_stream
from spinta.commands.write import write


def import_(
    ctx: TyperContext,
    source: str,
    auth: Optional[str] = Option(None, '-a', '--auth', help=(
        "Authorize as a client"
    )),
    limit: Optional[int] = Option(None, help=(
        "Limit number of rows read from source."
    )),
):
    """Import data from a file"""
    context = ctx.obj
    store = prepare_manifest(context)
    manifest = store.manifest
    root = commands.get_namespace(context, manifest, '')

    with context:
        require_auth(context, auth)
        context.attach('transaction', validate_and_return_transaction, context, manifest.backend, write=True)
        with open(source) as f:
            stream = (json.loads(line.strip()) for line in f)
            stream = itertools.islice(stream, limit) if limit else stream
            stream = write(context, root, stream, changed=True)
            coro = process_stream(source, stream)
            asyncio.get_event_loop().run_until_complete(coro)
