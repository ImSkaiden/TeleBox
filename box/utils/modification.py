from pyrogram import utils
from box.utils.all import *

def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"

utils.get_peer_type = get_peer_type_new

import pyrogram
from pyrogram import __version__, __license__
from pyrogram import enums
from pyrogram import utils
from pyrogram.errors import (
    SessionPasswordNeeded,
    BadRequest
)
from pyrogram.types import User, TermsOfService
from pyrogram.utils import ainput
from pyrogram.methods import Methods
import logging
log = logging.getLogger(__name__)

class newClient(Methods):
    async def authorize(self) -> User:
            if self.bot_token:
                return await self.sign_in_bot(self.bot_token)

            while True:
                try:
                    if not self.phone_number:
                        while True:
                            value = await ainput("Введите номер телефона или токен бота: ")

                            if not value:
                                continue

                            confirm = (await ainput(f'Phone number "{value}" valid? (y/N): ')).lower()

                            if confirm == "y":
                                break

                        if ":" in value:
                            self.bot_token = value
                            return await self.sign_in_bot(value)
                        else:
                            self.phone_number = value

                    sent_code = await self.send_code(self.phone_number)
                except BadRequest as e:
                    print(e.MESSAGE)
                    self.phone_number = None
                    self.bot_token = None
                else:
                    break

            sent_code_descriptions = {
                enums.SentCodeType.APP: "Telegram app",
                enums.SentCodeType.SMS: "SMS",
                enums.SentCodeType.CALL: "Call",
                enums.SentCodeType.FLASH_CALL: "Flash call",
                enums.SentCodeType.FRAGMENT_SMS: "Fragment SMS",
                enums.SentCodeType.EMAIL_CODE: "Email"
            }

            print(f"Code sent via {sent_code_descriptions[sent_code.type]}")

            while True:
                if not self.phone_code:
                    self.phone_code = await ainput("Verification code: ")

                try:
                    signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
                except BadRequest as e:
                    print(e.MESSAGE)
                    self.phone_code = None
                except SessionPasswordNeeded as e:
                    print(e.MESSAGE)

                    while True:
                        print("Hint: {}".format(await self.get_password_hint()))

                        if not self.password:
                            self.password = await ainput("Enter password (empty to reset): ", hide=self.hide_password)

                        try:
                            if not self.password:
                                confirm = await ainput("Reset password? (y/n): ")

                                if confirm == "y":
                                    email_pattern = await self.send_recovery_code()
                                    print(f"Recovery code sent to email: {email_pattern}")

                                    while True:
                                        recovery_code = await ainput("Recovery code: ")

                                        try:
                                            return await self.recover_password(recovery_code)
                                        except BadRequest as e:
                                            print(e.MESSAGE)
                                        except Exception as e:
                                            log.exception(e)
                                            raise
                                else:
                                    self.password = None
                            else:
                                return await self.check_password(self.password)
                        except BadRequest as e:
                            print(e.MESSAGE)
                            self.password = None
                else:
                    break

            if isinstance(signed_in, User):
                return signed_in

            while True:
                first_name = await ainput("First name: ")
                last_name = await ainput("Second name (empty to skip): ")

                try:
                    signed_up = await self.sign_up(
                        self.phone_number,
                        sent_code.phone_code_hash,
                        first_name,
                        last_name
                    )
                except BadRequest as e:
                    print(e.MESSAGE)
                else:
                    break

            if isinstance(signed_in, TermsOfService):
                print("\n" + signed_in.text + "\n")
                await self.accept_terms_of_service(signed_in.id)

            return signed_up
    
pyrogram.Client.authorize = newClient.authorize