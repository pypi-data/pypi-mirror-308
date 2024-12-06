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
  parser.add_argument('--secret', type=str, **env('SECRET'), help='Authorization secret')

  parser.add_argument('--tfs-host', type=str, **env('TFS_HOST', default='http://localhost'))
  parser.add_argument('--tfs-port', type=int, **env('TFS_PORT', default=8501))
  parser.add_argument('--tfs-endpoint', type=str, **env('TFS_ENDPOINT', default='/v1/models/baseline:predict'))
  parser.add_argument('--batch-size', type=int, default=8)


  parser.add_argument('--host', type=str, default='0.0.0.0')
  parser.add_argument('-p', '--port', type=int, default=8000)

  args = parser.parse_args()

  from kv import KV
  from pipeteer import Backend
  import uvicorn
  from moveread.pipelines.ocr import ocr_predict, OcrContext

  blobs = KV.of(args.blobs, bytes)

  backend = Backend.sql(sql_url=args.db, url=args.url, secret=args.secret)
  ctx = OcrContext(
    backend, blobs=blobs, default_endpoint=args.tfs_endpoint,
    tfs_host=args.tfs_host, tfs_port=args.tfs_port, batch_size=args.batch_size
  )

  backend.mount(ocr_predict, ctx)

  procs = [
    ocr_predict.run(ctx),
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
    '--db', 'sqlite+aiosqlite:///docker/data/ocr.db',
    '--blobs', 'file://docker/data/blobs',
    '--url', 'http://localhost:8002',
    '-p', '8002',
    '--secret', 'secret',
  ])
  main()