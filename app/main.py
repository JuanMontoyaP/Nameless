"""
Nameless app
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import users
from .routers import items


app = FastAPI()

app.add_middleware(
    CORSMiddleware
)

app.include_router(users.router)
app.include_router(items.router)
