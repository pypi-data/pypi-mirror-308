from __future__ import annotations

import json
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from memento import crud, models

if TYPE_CHECKING:
    from redis import Redis
    from redis.asyncio import Redis as AsyncRedis
    from valkey import Valkey
    from valkey.asyncio import Valkey as AsyncValkey


class BaseRecorder:
    def __init__(self, conversation: models.Conversation) -> None:
        self.conversation = conversation

    def add_message(
        self,
        role: str,
        content: str | None = None,
        tools: dict | None = None,
        uuid: UUID | None = None,
    ) -> None:
        message = models.Message(
            self.conversation.id,
            role=role,
            content=content,
            tools=json.dumps(tools) if tools else None,
            feedback=None,
            uuid=uuid,
        )
        self.conversation.messages.append(message)

    def to_openai_format(self) -> list[dict]:
        return [message.to_openai_format() for message in self.conversation.messages]

    def add_openai_response(self, response) -> None:
        message = response.choices[0].message

        self.add_message(
            role=message.role,
            content=message.content,
            tools=tools if (tools := message.tools) else None,
        )


class Recoder(BaseRecorder):
    def __init__(self, conversation: models.Conversation) -> None:
        super().__init__(conversation)

    @classmethod
    def from_conversation(
        cls, session: Session, id: int | UUID, *, cache: Redis | Valkey | None = None
    ) -> "Recoder":
        if cache:
            uuid = None

            if isinstance(id, UUID):
                uuid = id
                cached_id = cache.get(str(uuid)).decode("utf-8")  # type: ignore
            else:
                cached_id = str(id)

            if cache_result := cache.get(cached_id):
                cached_messages = json.loads(cache_result.decode("utf-8"))  # type: ignore

                conversation = models.Conversation("cache")
                conversation.id = int(cached_id)
                conversation.messages = [models.Message(**m) for m in cached_messages]

                if uuid is not None:
                    conversation.uuid = uuid

            else:
                conversation = crud.get_conversation(session, id)

                value = json.dumps(conversation._messages_to_cache_format())

                cache.setex(str(conversation.uuid), 300, str(conversation.id))
                cache.setex(str(conversation.id), 300, value)

        else:
            conversation = crud.get_conversation(session, id)

        return cls(conversation)

    def commit_messages(
        self, session: Session, *, cache: Redis | Valkey | None = None
    ) -> None:
        if (conversation := self.conversation) not in session:
            session.add_all(conversation.messages)
            session.expunge(conversation)

        if cache:
            value = json.dumps(conversation._messages_to_cache_format())

            cache.setex(str(conversation.uuid), 300, str(conversation.id))
            cache.setex(str(conversation.id), 300, value)

        session.commit()


class AsyncRecoder(BaseRecorder):
    def __init__(self, conversation: models.Conversation) -> None:
        self.conversation = conversation

    @classmethod
    async def from_conversation(
        cls,
        session: AsyncSession,
        id: int | UUID,
        *,
        cache: AsyncRedis | AsyncValkey | None = None,
    ) -> "AsyncRecoder":
        if cache:
            uuid = None

            if isinstance(id, UUID):
                uuid = id
                cached_id = (await cache.get(str(uuid))).decode("utf-8")  # type: ignore
            else:
                cached_id = str(id)

            if cache_result := await cache.get(cached_id):
                cached_messages = json.loads(cache_result.decode("utf-8"))  # type: ignore

                conversation = models.Conversation("cache")
                conversation.id = int(cached_id)
                conversation.messages = [models.Message(**m) for m in cached_messages]

                if uuid is not None:
                    conversation.uuid = uuid

            else:
                conversation = await crud.get_conversation_async(session, id)

                value = json.dumps(conversation._messages_to_cache_format())

                await cache.setex(str(conversation.uuid), 300, str(conversation.id))
                await cache.setex(str(conversation.id), 300, value)
        else:
            conversation = await crud.get_conversation_async(session, id)

        return cls(conversation)

    async def commit_messages(
        self, session: AsyncSession, *, cache: AsyncRedis | AsyncValkey | None = None
    ) -> None:
        if (conversation := self.conversation) not in session:
            session.add_all(conversation.messages)
            session.expunge(conversation)

        if cache:
            value = json.dumps(conversation._messages_to_cache_format())

            await cache.setex(str(conversation.uuid), 300, str(conversation.id))
            await cache.setex(str(conversation.id), 300, value)

        await session.commit()
