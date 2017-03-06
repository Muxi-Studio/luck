import base64
import asyncio
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

def create_app():
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    # ====== app set ======
    setup(app, EncryptedCookieStorage(secret_key)) # for csrf? o(*￣▽￣*)ゞ
    # =====================

    # ====== url map ======
    # =====================

    # ====== sub app ======
    from api import api
    app.add_subapp('/api/', api)
    # =====================
    return app

app = create_app()
loop = asyncio.get_event_loop()
