import click
from pathlib import Path
from collections import defaultdict, Counter

@click.group(chain=True, context_settings=dict(obj={}))
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
    p = Path(path)
    digests = []
    for q in p.iterdir():
        if q.is_file():
            hashobj = hashfunc()
            with q.open('rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hashobj.update(chunk)
            digests.append( (hashobj.hexdigest(), q) )
    ctx.obj['digests'] = digests

@cli.command()
@click.pass_context
def show(ctx):
    if 'digests' in ctx.obj:
        for digest, path in ctx.obj['digests']:
            click.echo("{} {}".format(digest, path))

@cli.command()
@click.pass_context
def duplicates(ctx):
    if 'digests' in ctx.obj:
        coll = defaultdict(set)
        for digest, path in ctx.obj['digests']:
            coll[digest].add(path)
        duplicates = []
        for digest, paths in coll.items():
            if len(paths)>1:
                for path in paths:
                    duplicates.append( (digest, path) )
        ctx.obj['digests'] = duplicates

if __name__=='__main__':
    cli()
