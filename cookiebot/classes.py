from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    max_streak: int
    streak: int
    cookies: int
    career: str
    total_shifts: int
    job: str


@dataclass
class UserGuild:
    user_id: int
    guild_id: int
    level: int
    xp: int
    msg_count: int
    voice_min: int
    voice_xp: int
    voice_level: int
    current_level_progress: int
    current_level_end: int
    rank: int
    rank_total: int
    voice_rank: int
    voice_rank_total: int


@dataclass
class UserStat:
    user_id: int
    guild_id: int
    messages: int
    voice_minutes: int
    message_rank: int
    voice_rank: int
    current_voice_minutes: int


@dataclass
class Guild:
    messages: dict[str, int]
    total_messages: int
    total_voice_minutes: int
    top_channel: int
    top_channel_messages: int
    most_active_user_day: int | None
    most_active_user_hour: int | None


class UserNotFound(Exception):
    pass


class GuildNotFound(Exception):
    pass
