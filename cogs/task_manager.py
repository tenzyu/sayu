from datetime import datetime, timezone
from typing import List

from discord import Message, RawReactionActionEvent, TextChannel
from discord.ext.commands import Bot, Cog
from discord.ext.tasks import loop

from const import CHANNEL_ID_TASK_MANAGER

EMOJI_SET_TASK = "\N{PUSHPIN}"
EMOJI_UNSET_TASK = "\N{THUMBS UP SIGN}"


class TaskManager(Cog):
    __slots__ = "bot", "task_manager_channel"

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.task_manager_channel: TextChannel = await self.bot.fetch_channel(CHANNEL_ID_TASK_MANAGER)
        self.task_reminder.start()

    @Cog.listener()
    async def on_raw_reaction_add(self, reaction: RawReactionActionEvent):
        emoji = str(reaction.emoji)
        message: Message = await self.task_manager_channel.fetch_message(reaction.message_id)

        if not (reaction.channel_id == CHANNEL_ID_TASK_MANAGER
                and emoji in [EMOJI_SET_TASK, EMOJI_UNSET_TASK]
                and message.author.id == reaction.user_id):
            return

        if emoji == EMOJI_SET_TASK:
            await self.set_task(message)
        elif emoji == EMOJI_UNSET_TASK:
            await self.unset_task(message)

    @staticmethod
    async def set_task(message: Message) -> None:
        await message.pin(reason="set task")
        await message.reply("タスクを登録したよ！\nタスクが完了したら :thumbsup: を付けよう！")
        await message.clear_reaction(EMOJI_SET_TASK)

    @staticmethod
    async def unset_task(message: Message) -> None:
        await message.unpin(reason="unset task")
        await message.reply(":tada: タスク完了おめでとう！ :tada:")

    @loop(seconds=60)
    async def task_reminder(self) -> None:
        # 11:00 in UTC is 20:00 in JST.
        utc = timezone.utc
        now = datetime.now(utc)
        if now.strftime("%H:%M") != "20:00":
            return

        pinned_tasks: List[Message] = await self.task_manager_channel.pins()
        if len(pinned_tasks) == 0:
            return

        task_author_mentions = set(task.author.mention for task in pinned_tasks)
        task_reminder_message = " ".join(task_author_mentions) + "\n未完了のタスクがあります！\n未完了のタスクはピン留めされています！"
        await self.task_manager_channel.send(task_reminder_message)


def setup(bot: Bot):
    bot.add_cog(TaskManager(bot))
