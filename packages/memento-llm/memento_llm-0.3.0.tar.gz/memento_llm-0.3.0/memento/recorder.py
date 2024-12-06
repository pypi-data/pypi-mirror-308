from __future__ import annotations

import json
from datetime import timedelta
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
        if cache is not None:
            cached_conversation = cache.get(str(id))
            if cached_conversation is not None:
                cache_dict = json.loads(cached_conversation.decode("utf-8"))  # type: ignore

                conversation = models.Conversation(cache_dict["agent"])
                conversation.id = cache_dict["id"]
                conversation.uuid = UUID(cache_dict["uuid"])
            else:
                conversation = crud.get_conversation(session, id)

                cached_conversation = {
                    "id": conversation.id,
                    "uuid": str(conversation.uuid),
                    "agent": conversation.agent,
                }

                expiration = 300
                value = json.dumps(cached_conversation)

                cache.setex(str(conversation.id), expiration, value)
                cache.setex(str(conversation.uuid), expiration, value)
        else:
            conversation = crud.get_conversation(session, id)
        return cls(conversation)

    def commit_messages(self, session: Session) -> None:
        if self.conversation not in session:
            session.add_all(self.conversation.messages)
            session.expunge(self.conversation)

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
        if cache is not None:
            cached_conversation = await cache.get(str(id))
            if cached_conversation is not None:
                cache_dict = json.loads(cached_conversation.decode("utf-8"))  # type: ignore

                conversation = models.Conversation(cache_dict["agent"])
                conversation.id = cache_dict["id"]
                conversation.uuid = UUID(cache_dict["uuid"])

            else:
                conversation = await crud.get_conversation_async(session, id)

                cached_conversation = {
                    "id": conversation.id,
                    "uuid": str(conversation.uuid),
                    "agent": conversation.agent,
                }

                expiration = 300
                value = json.dumps(cached_conversation)

                await cache.setex(str(conversation.id), expiration, value)
                await cache.setex(str(conversation.uuid), expiration, value)
        else:
            conversation = await crud.get_conversation_async(session, id)

        return cls(conversation)

    async def commit_messages(self, session: AsyncSession) -> None:
        if self.conversation not in session:
            session.add_all(self.conversation.messages)
            session.expunge(self.conversation)

        await session.commit()
