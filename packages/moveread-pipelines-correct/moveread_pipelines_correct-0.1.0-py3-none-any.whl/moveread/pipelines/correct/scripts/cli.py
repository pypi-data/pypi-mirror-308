import os
from argparse import ArgumentParser

def env(variable: str, *, default = None, required: bool = True) -> dict:
  if (value := os.getenv(variable, default)) is not None:
    return dict(default=value)
  return dict(required=required)

def main():
  parser = ArgumentParser()
  parser.add_argument('--db', type=str, **env('DB_URL'), help='DB connection string')
  parser.add_argument('--cache', type=str, **env('CACHE_URL'), help='Cache connection string')
  parser.add_argument('--blobs', type=str, **env('BLOBS_URL'), help='Blobs KV connection string')
  parser.add_argument('--url', type=str, **env('SELF_URL'), help='Self URL')
  parser.add_argument('--secret', type=str, **env('SECRET'), help='Authorization secret')

  parser.add_argument('--host', type=str, default='0.0.0.0')
  parser.add_argument('-p', '--port', type=int, default=8000)

  args = parser.parse_args()

  import uvicorn
  from fastapi import Request, Response
  from fastapi.middleware.cors import CORSMiddleware
  from kv import KV, LocatableKV, ServerKV
  from pipeteer import Backend
  from moveread.pipelines.correct import Context, correct, Annotations

  cache = KV.of(args.cache, Annotations)
  blobs = KV.of(args.blobs, bytes)
  if not isinstance(blobs, LocatableKV):
    blobs = blobs.served(args.url.rstrip('/') + '/blobs', secret=args.secret)

  backend = Backend.sql(sql_url=args.db, url=args.url, secret=args.secret)
  ctx = Context(backend, cache=cache, blobs=blobs)

  backend.mount(correct, ctx)

  api = correct.run(ctx)
  @api.middleware('http')
  async def check_token(req: Request, call_next):
    if (
      req.headers.get('Authorization') == f'Bearer {args.secret}'
      or req.url.path.startswith('/blobs/')
      or req.url.path.startswith('/api/preds/')
    ):
      return await call_next(req)
    else:
      return Response(status_code=401, content='Unauthorized')
    
  backend.app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
  backend.app.mount('/blobs', ServerKV(blobs, type=bytes, secret=args.secret))
  backend.app.mount('/api', api)

  uvicorn.run(backend.app, host=args.host, port=args.port)


if __name__ == '__main__':
  import sys
  os.chdir('/home/m4rs/mr-github/rnd/pipelines-v2')
  sys.argv.extend([
    '--db', 'sqlite+aiosqlite:///docker/data/correct.db',
    '--blobs', 'file://docker/data/blobs',
    '--url', 'http://localhost:8003',
    '-p', '8003',
    '--secret', 'secret',
  ])
  main()