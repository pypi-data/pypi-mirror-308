import os
from argparse import ArgumentParser

def env(variable: str, *, default = None, required: bool = True) -> dict:
  if (value := os.getenv(variable, default)) is not None:
    return dict(default=value)
  return dict(required=required)

def main():
  parser = ArgumentParser()
  parser.add_argument('-w', '--weights', type=str, **env('WEIGHTS_PATH', default='/tatr.pth'), help='Path to the weights file')
  parser.add_argument('--db', type=str, **env('DB_URL'), help='DB connection string')
  parser.add_argument('--blobs', type=str, **env('BLOBS_URL'), help='Blobs KV connection string')
  parser.add_argument('--url', type=str, **env('SELF_URL'), help='Self URL')
  parser.add_argument('--secret', type=str, **env('SECRET'), help='Authorization secret')

  parser.add_argument('--host', type=str, default='0.0.0.0')
  parser.add_argument('-p', '--port', type=int, default=8000)

  args = parser.parse_args()

  from kv import KV
  from dslog import Logger

  log = Logger.click().limit('INFO')
  log('Loading imports...')

  from pipeteer import Backend
  import uvicorn
  from moveread.tatr import TableDetector
  from moveread.pipelines.tatr import extract, TatrContext

  import torch
  torch.set_num_threads(1)

  blobs = KV.of(args.blobs, bytes)

  log('Loading model...')
  model = TableDetector()
  model.load(args.weights)
  log('Model loaded')

  backend = Backend.sql(sql_url=args.db, url=args.url, secret=args.secret)
  ctx = TatrContext(backend, model=model, blobs=blobs)

  backend.mount(extract, ctx)

  procs = [
    extract.run(ctx),
    backend.run(),
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
    '--db', 'sqlite+aiosqlite:///docker/data/tatr.db',
    '--blobs', 'file://docker/data/blobs',
    '--url', 'http://localhost:8001',
    '-p', '8001',
    '--weights', 'tatr/tatr.pth',
    '--secret', 'secret',
  ])
  main()