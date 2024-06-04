from dataclasses import dataclass


@dataclass
class UserStats:
    user_id: int
    max_streak: int
    streak: int
    cookies: int
    career: str
    total_shifts: int
    job: str


@dataclass
class MemberStats:
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
    msg_rank: int
    msg_total_members: int
    voice_rank: int
    voice_total_members: int


@dataclass
class MemberActivity:
    days: int
    user_id: int
    guild_id: int
    msg_count: int
    voice_min: int
    msg_rank: int
    voice_rank: int
    current_voice_minutes: int


@dataclass
class GuildActivity:
    days: int
    messages: dict[str, int]
    total_messages: int
    total_voice_minutes: int
    top_channel: int
    top_channel_messages: int
    most_active_user_day: int | None
    most_active_user_hour: int | None