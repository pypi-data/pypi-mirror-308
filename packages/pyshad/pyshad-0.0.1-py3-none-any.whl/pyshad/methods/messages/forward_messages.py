from typing import Union


class ForwardMessages:
    async def forward_messages(
            self,
            from_object_guid: str,
            to_object_guid: str,
            message_ids: Union[str, int, list],
    ):
        if not isinstance(message_ids, list):
            message_ids = [str(message_ids)]

        return await self.builder('forwardMessages',
                                  input={
                                      'from_object_guid': from_object_guid,
                                      'to_object_guid': to_object_guid,
                                      'message_ids': message_ids,
                                  })