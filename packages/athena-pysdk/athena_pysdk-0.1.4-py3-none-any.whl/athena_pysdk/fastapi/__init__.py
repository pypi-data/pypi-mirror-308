from starlette_context.middleware import ContextMiddleware
from fastapi.middleware import Middleware
from pinpointPy.Fastapi import PinPointMiddleWare
from .middleware.pinpoint import pinpoint_init
from fastapi.middleware.cors import CORSMiddleware

pinpoint_init()

AthenaMiddleware = [
    Middleware(ContextMiddleware),
    Middleware(PinPointMiddleWare),
    Middleware(CORSMiddleware,
               allow_origins=["*"],
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"],
               )
]

__all__ = ['AthenaMiddleware']
