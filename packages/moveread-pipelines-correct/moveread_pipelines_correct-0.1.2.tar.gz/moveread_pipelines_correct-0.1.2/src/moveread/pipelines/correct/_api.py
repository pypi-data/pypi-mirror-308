import asyncio
from pydantic import BaseModel
from kv import LocatableKV
from fastapi import FastAPI, Response
from sse_starlette import EventSourceResponse
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
from moveread.pipelines.correct import SDK, Message, Meta, Item, Annotations, Done, Preds
from moveread.pipelines.correct.util import Streams

def api(
  sdk: SDK, images: LocatableKV[bytes], *,
  logger = Logger.click().prefix('[GAME CORRECTION]')
):

  streams = Streams[Message]()
  reqIds: dict[str, str] = {}

  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER),
    )
  )
  
  @app.get('/items', response_model_exclude_none=True)
  async def get_items() -> list[Meta]:
    return [x async for x in sdk.items()]
  
  @app.get('/item', response_model_exclude_none=True)
  async def get_item(id: str, resp: Response) -> Item | None:
    if (item := (await sdk.item(id))):
      item.boxes = [images.url(box) for box in item.boxes]
      return item
    else:
      resp.status_code = 404

  class ConfirmParams(BaseModel):
    pgn: list[str]
    early: bool
    
  @app.post('/confirm')
  async def confirm(id: str, params: ConfirmParams, resp: Response) -> bool:
    ok = await sdk.confirm(id, pgn=params.pgn, early=params.early)
    if not ok:
      resp.status_code = 404
    return ok
  
  @app.post('/repreprocess')
  async def repreprocess(id: str, resp: Response) -> bool:
    ok = await sdk.repreprocess(id)
    if not ok:
      resp.status_code = 404
    return ok
  
  @app.post('/annotate')
  async def annotate(id: str, anns: Annotations, resp: Response) -> bool:
    await sdk.annotate(id, anns)
    return True

  @app.post('/predict')
  async def predict(id: str, userId: str, reqId: str, fen: str) -> list[Preds|Done]:
    reqIds[userId] = reqId
    preds = []

    for ps in await sdk.predict(id, fen=fen):
      if reqIds.get(userId) != reqId:
        logger(f'UserID: {userId}, ReqId: {reqId} got canceled.', level='DEBUG')
        return preds
      msg = Preds(reqId=reqId, preds=ps) # type: ignore
      streams.push(userId, msg)
      await asyncio.sleep(0) # yield control to the event loop, to force result streaming
      preds.append(msg)
    
    streams.push(userId, Done(reqId=reqId))
    return preds

  @app.get('/preds/{userId}')
  def preds(userId: str):
    return EventSourceResponse(streams.listen(userId).map(lambda m: m.model_dump_json()))
  
  return app


# def clientgen():
#   from argparse import ArgumentParser

#   parser = ArgumentParser()
#   parser.add_argument('-o', '--output', required=True)

#   args = parser.parse_args()

#   from openapi_ts import generate_client

#   schema = fastapi({}, {}).openapi() # type: ignore
#   generate_client(schema, args.output)