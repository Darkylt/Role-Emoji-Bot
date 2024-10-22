import typing

import bot_utils as utils
import config_reader as config
import hikari
import lightbulb

plugin = lightbulb.Plugin("auto_role", "Assign an emoji to a user based on a role")


async def get_emoji_by_role_id(role_ids: list[int]) -> str:
    roles_dict = config.Roles.roles_lookup

    # Iterate over the role IDs and return the first matching emoji
    for role_id in role_ids:
        emoji = roles_dict.get(str(role_id))
        if emoji:
            return emoji

    # Return None or a default value if no matching emoji is found
    return None


async def get_new_nickname(emoji: str, username: str) -> str | bool:
    # Check if the username already starts with the specified emoji
    if username.startswith(emoji):
        return False

    # Check if the username starts with an emoji
    # We can consider the first character as an emoji for this check
    first_char = username[0]

    # If the first character is not the specified emoji, check if it's an emoji from the roles_dict
    if first_char in config.Roles.roles_lookup.values():
        # Replace the existing emoji with the new one
        return (
            emoji + username[1:]
        )  # Concatenate the new emoji with the rest of the username
    else:
        # If it's a different emoji, prepend the new emoji
        return emoji + username


@plugin.listener(hikari.events.MemberUpdateEvent)
async def on_member_update(event: hikari.MemberUpdateEvent):
    all_roles = event.member.role_ids

    emoji = await get_emoji_by_role_id(all_roles)

    # Do nothing if no matching role is found
    if emoji is None:
        return

    username = event.member.username
    if username is None:
        username = event.member.global_name

    new_username = await get_new_nickname(emoji, username)
    await event.member.edit(nickname=new_username)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove(plugin)
