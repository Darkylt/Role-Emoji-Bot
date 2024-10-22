import typing

import bot_utils as utils
import config_reader as config
import hikari
import lightbulb

plugin = lightbulb.Plugin("assign_role", "Assign an emoji role to a user")


def emojis_only() -> typing.List[str]:
    roles_dict: dict = config.Roles.roles_lookup

    return list(roles_dict.values())


async def get_role_id_by_emoji(emoji: str) -> int | None:
    roles_dict = config.Roles.roles_lookup

    # Find the role ID by matching the emoji with the dictionary values
    for role_id, role_emoji in roles_dict.items():
        if role_emoji == emoji:
            return int(role_id)

    # Return None or raise an exception if the emoji is not found
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


@plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.app_command_permissions(
    hikari.Permissions.ADMINISTRATOR, dm_enabled=False  # Admin perms needed
)
@lightbulb.option(
    "emoji",
    "Choose which emoji you want to assign",
    str,
    choices=emojis_only(),
    required=True,
)
@lightbulb.option(
    "user",
    "Which user do you want to add a role to?",
    type=hikari.Member,
    required=True,
)
@lightbulb.command(
    "assign_role",
    "Assign an emoji role to a user",
    pass_options=True,
    auto_defer=True,
    ephemeral=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def assign_role_command(
    ctx: lightbulb.SlashContext, emoji: str, user: hikari.Member
):
    if not await utils.validate_command(ctx):
        return

    role = await get_role_id_by_emoji(emoji)

    if role is None:
        await ctx.respond("The specified emoji wasn't found.")
        return

    await user.add_role(role, reason=f"Assigned {emoji} to the user.")

    username = user.username
    if username is None:
        username = user.global_name

    new_username = await get_new_nickname(emoji, username)

    await user.edit(nickname=new_username)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove(plugin)
