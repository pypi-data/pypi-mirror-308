import os
from argparse import ArgumentParser

def env(variable: str, *, default = None, required: bool = True) -> dict:
  if (value := os.getenv(variable, default)) is not None:
    return dict(default=value)
  return dict(required=required)

def main():
  parser = ArgumentParser()
  parser.add_argument('--db', type=str, **env('DB_URL'), help='DB connection string')
  parser.add_argument('--blobs', type=str, **env('BLOBS_URL'), help='Blobs KV connection string')
  parser.add_argument('--url', type=str, **env('SELF_URL'), help='Self URL')
  parser.add_argument('--extract', type=str, **env('EXTRACT_URL'), help='Extract pipeline URL')
  parser.add_argument('--secret', type=str, **env('SECRET'), help='Authorization secret')

  parser.add_argument('--host', type=str, default='0.0.0.0')
  parser.add_argument('-p', '--port', type=int, default=8000)

  args = parser.parse_args()

  from multiprocessing import Process
  import uvicorn
  from fastapi import Request, Response
  from fastapi.middleware.cors import CORSMiddleware
  from kv import KV, LocatableKV, ServerKV
  from pipeteer import Backend
  from moveread.pipelines.tatr import extract
  from moveread.pipelines.preprocess import preprocess, descale, preoutput, api, PreprocessContext

  blobs = KV.of(args.blobs, type=bytes)
  if not isinstance(blobs, LocatableKV):
    blobs = blobs.served(args.url.rstrip('/') + '/blobs', secret=args.secret)

  backend = Backend.sql(sql_url=args.db, url=args.url, secret=args.secret)
  ctx = PreprocessContext(backend, blobs)

  extract.as_client(args.extract)

  backend.mount(preprocess, ctx)
  backend.mount(descale, ctx)
  backend.mount(preoutput, ctx)
  backend.mount(api, ctx)

  app = api.run(ctx)
  @app.middleware('http')
  async def check_token(req: Request, call_next):
    if req.headers.get('Authorization') == f'Bearer {args.secret}' or req.url.path.startswith('/blobs/'):
      return await call_next(req)
    else:
      return Response(status_code=401, content='Unauthorized')

  backend.app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
  backend.app.mount('/api', api.run(ctx))
  backend.app.mount('/blobs', ServerKV(blobs, secret=args.secret, type=bytes))

  procs = [
    preprocess.run(ctx),
    descale.run(ctx),
    preoutput.run(ctx),
    backend.run()
  ]
  
  for proc in procs:
    proc.start()

  uvicorn.run(backend.app, host=args.host, port=args.port)

  for proc in procs:
    proc.join()


if __name__ == '__main__':
  import sys
  os.chdir('/home/m4rs/mr-github/rnd/pipelines-v2')
  sys.argv.extend([
    '--db', 'sqlite+aiosqlite:///docker/data/preprocess.db',
    '--blobs', 'file://docker/data/blobs',
    '--url', 'http://localhost:8000',
    '-p', '8000',
    '--extract', 'http://localhost:8001/pipelines/extract/input',
    '--secret', 'secret',
  ])
  main()