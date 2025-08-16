import discord
from discord.ext import commands
import asyncio
import tkinter as tk
from tkinter import messagebox

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Variables globales pour Tkinter
user_id_to_delete = None
channel_id_to_use = None
token_value = None

async def delete_messages_from_user(channel: discord.TextChannel, user_id: int):
    deleted_count = 0
    try:
        async for msg in channel.history(limit=None):
            if msg.author.id == user_id:
                try:
                    await msg.delete()
                    deleted_count += 1
                    print(f"[{deleted_count}] Message supprimé")
                    await asyncio.sleep(1)  # anti rate-limit
                except discord.errors.HTTPException as e:
                    if e.status == 429:  # rate limit
                        print("⚠️ Rate limit atteint. Pause 5 sec...")
                        await asyncio.sleep(5)
    except Exception as e:
        print(f"[Erreur] {channel.name} : {e}")
    print(f"✅ Terminé. {deleted_count} messages supprimés.")

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    channel = bot.get_channel(channel_id_to_use)
    if channel:
        await delete_messages_from_user(channel, user_id_to_delete)
    else:
        print("❌ Salon introuvable")
    await bot.close()

# ----------- Tkinter Panel ------------
def start_bot():
    global user_id_to_delete, channel_id_to_use, token_value
    try:
        user_id_to_delete = int(entry_user.get())
        channel_id_to_use = int(entry_channel.get())
        token_value = entry_token.get()
        root.destroy()
        bot.run(token_value)
    except Exception as e:
        messagebox.showerror("Erreur", f"Entrée invalide : {e}")

root = tk.Tk()
root.title("Cleaner de messages Discord")

tk.Label(root, text="Token du bot :").pack()
entry_token = tk.Entry(root, width=50, show="*")
entry_token.pack()

tk.Label(root, text="ID du salon (channel ID) :").pack()
entry_channel = tk.Entry(root, width=30)
entry_channel.pack()

tk.Label(root, text="ID de l'utilisateur :").pack()
entry_user = tk.Entry(root, width=30)
entry_user.pack()

tk.Button(root, text="Lancer la suppression", command=start_bot).pack(pady=10)

root.mainloop()
