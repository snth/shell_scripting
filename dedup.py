import click
from pathlib import Path

@click.group(chain=True)
def cli():
    pass

@cli.command()
@click.option('--hash-type', '-h', type=click.Choice(['md5', 'sha1']),
              default='md5')
@click.option('-p', '--path', type=click.Path(exists=True, file_okay=False),
              default='.')
@click.pass_context
def digests(ctx, hash_type, path):
    """Generate the digests for all files in a path"""
    from hashlib import md5, sha1
    hashfunc = locals()[hash_type]
    hashobj = hashfunc()
    p = Path(path)  # FIXME
    d = {}
    for q in p.iterdir():
        if q.is_file():
            with q.open('rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hashobj.update(chunk)
            # click.echo("{} {}".format(hashobj.hexdigest(), q))
            d[hashobj.hexdigest()] = q
    ctx.obj['digests'] = d

@cli.command()
@click.pass_context
def print(ctx):
    if 'digests' in ctx.obj:
        for digest, path in ctx.obj['digests'].items():
            click.echo("{} {}".format(digest, path))

if __name__=='__main__':
    cli(obj={})
