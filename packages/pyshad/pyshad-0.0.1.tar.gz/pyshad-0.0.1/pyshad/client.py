from .sessions import SQLiteSession, StringSession
from .parser import Markdown
from .methods import Methods
from typing import Optional, Union


class Client(Methods):
    DEFAULT_PLATFORM = {"app_name": "Main", "app_version": "4.4.17", "platform": "Web", "package": "web.shad.ir",
                        "lang_code": "fa"}

    USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/102.0.0.0 Safari/537.36')

    API_VERSION = '6'

    def __init__(self,
                 name: str,
                 auth: Optional[str] = None,
                 private_key: Optional[Union[str, bytes]] = None,
                 bot_token: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 user_agent: Optional[str] = None or USER_AGENT,
                 timeout: Optional[Union[str, int]] = 20,
                 lang_code: Optional[str] = 'fa',
                 parse_mode: Optional[str] = 'All',
                 ) -> None:
        super().__init__()
        if auth and not isinstance(auth, str):
            raise ValueError('`auth` is `string` arg.')

        if private_key:
            if not type(private_key) in (str, bytes):
                raise ValueError('`private_key` is `string` or `bytes` arg.')

        if bot_token and not isinstance(bot_token, str):
            raise ValueError('`bot_token` is `string` arg.')

        if phone_number and not isinstance(phone_number, str):
            raise ValueError('`phone_number` is `string` arg.')

        if user_agent and not isinstance(user_agent, str):
            raise ValueError('`user_agent` is `string` arg.')

        if not isinstance(timeout, int):
            timeout = int(timeout)

        if isinstance(name, str):
            session = SQLiteSession(name)

        elif not isinstance(name, StringSession):
            raise TypeError('The given session must be a '
                            'str or [rubpy.sessions.StringSession]')

        if parse_mode not in ('All', 'html', 'markdown', 'mk'):
            raise ValueError('The `parse_mode` argument can only be in `("All", "html", "markdown", "mk")`.')

        self.DEFAULT_PLATFORM['lang_code'] = lang_code
        self.name = name
        self.auth = auth
        self.private_key = private_key
        self.bot_token = bot_token
        self.phone_number = phone_number
        self.user_agent = user_agent
        self.lang_code = lang_code
        self.timeout = timeout
        self.session = session
        self.parse_mode = parse_mode
        self.markdown = Markdown()
        self.database = None
        self.decode_auth = None
        self.import_key = None
        self.guid = None
        self.key = None
        self.handlers = {}

    def __enter__(self):
        return self.start()

    def __exit__(self, *args, **kwargs):
        try:
            return self.disconnect()
        except Exception as exc:
            print(exc.__name__, exc)

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args, **kwargs):
        try:
            return await self.disconnect()
        except Exception as exc:
            print(exc.__name__, exc)
