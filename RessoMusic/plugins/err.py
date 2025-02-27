from pyrogram impot ChatMemberStatus
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges


async def banall_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /banall command - demote admin or ban user."""
    if update.effective_chat.type == Chat.PRIVATE:
        await update.message.reply_text("This command can only be used in groups.")
        return

    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)

    if is_admin(chat_member) and chat_member.status != ChatMemberStatus.OWNER:
        await context.bot.promote_chat_member(update.effective_chat.id, update.effective_user.id, can_manage_chat=False,
                                              can_delete_messages=False, can_invite_users=False, can_restrict_members=False,
                                              can_pin_messages=False, can_manage_video_chats=False, can_change_info=False,
                                              can_promote_members=False)
        db.remove_admin(update.effective_user.id, update.effective_chat.id)
        db.log_mod_action(context.bot.id, update.effective_chat.id, "banall_admin_demotion", update.effective_user.id,
                          "Admin demoted for attempting to use /banall command")
        await update.message.reply_html(f"⚠️ Admin {mention_html(update.effective_user.id, update.effective_user.first_name)} "
                                        "has been demoted for using /banall.")
    elif not is_admin(chat_member):
        await context.bot.ban_chat_member(update.effective_chat.id, update.effective_user.id)
        db.log_mod_action(context.bot.id, update.effective_chat.id, "banall_attempt_ban", update.effective_user.id,
                          "User banned for attempting to use /banall command")
    else:
        await update.message.reply_text("⚠️ Warning: The /banall command is dangerous and could harm your group.")
