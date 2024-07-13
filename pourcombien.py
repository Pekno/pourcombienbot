import discord
import os
from discord import ui, app_commands
from datetime import datetime
import uuid

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True

class Defi:
    all_messages = []
    f_value = 0
    t_value = 0
    max_value = 0
    done = False
    id = uuid.uuid4()

    def __init__(self, f, t, origin_message):
        self.f = f
        self.t = t
        self.origin_message = origin_message

    async def clear(self):
        print(f"ID _{self.id}_ CLEARING at {datetime.now()}")
        for mess in self.all_messages:
            if mess is not None:
                await mess.delete()

    async def timeout(self):
        if self.done != True:
            print(f"ID _{self.id}_ has TIMEOUT at {datetime.now()}")
            self.done = True
            embed = self.origin_message.embeds[0]
            embed.description += f"\n## **{self.t.mention} n'a pas répondu, le défi a donc expiré** ❌"
            embed.title = embed.title.replace("🔓", "🔒")
            embed.color = discord.Colour.red()
            await self.origin_message.edit(embed=embed)
            await self.clear()


class client(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'{self.user.name} a démarré avec succès.')
        
class pourcombien_modal(ui.Modal, title = ""):
    def __init__(self, member: str):
        super().__init__()
        self._selected_member = member
        self.title = f"Alors, {self._selected_member.display_name} pour combien ?"

        self.answer = ui.TextInput(label = "Défi", style = discord.TextStyle.short, custom_id="defi",  required = True)
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = f"🔓 {self.title}",
            description = f"## {self.answer.label} : _{self.answer}_",
            timestamp = datetime.now(),
            color = discord.Colour.blue()
        )
        embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar)
        await interaction.response.send_message(embed = embed)
        defi = Defi(interaction.user, self._selected_member, await interaction.original_response())
        print(f"ID _{defi.id}_ was CREATED at {datetime.now()}")

        view = accept_buttons(defi)
        accept_message = await defi.origin_message.reply(
            f"{self._selected_member.mention}, vous avez été défié par {interaction.user.mention} avec le défi suivant : **{self.answer}**.\n Vous avez 10 minutes pour répondre",
            view = view
        )
        view.message = accept_message
        defi.all_messages.append(
            accept_message
        )

class accept_buttons(discord.ui.View):
    def __init__(self, defi: Defi):
        super().__init__(timeout = 600)
        self.defi = defi
        self.add_buttons()

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message is not None:
            await self.message.edit(content="Le défi a expiré", view=self)
            await self.message.delete()
            self.defi.all_messages.remove(self.message)
            await self.defi.timeout()

    def add_buttons(self):
        b1 = discord.ui.Button(label = "Accepter", style = discord.ButtonStyle.green)
        async def accept(interaction: discord.Interaction):
            if self.defi.t == interaction.user:
                print(f"ID _{self.defi.id}_ was ACCEPTED at {datetime.now()}")
                await interaction.response.send_modal(maximum_modal(self.defi, interaction.message)) 
            else:
                await interaction.response.send_message(f"🖕 **Tu n'es pas celui défié** 🖕", ephemeral=True, delete_after=5)
        b1.callback = accept
        self.add_item(b1)

        b2 = discord.ui.Button(label = "Refuser", style = discord.ButtonStyle.red)
        async def refuse(interaction: discord.Interaction):
            if self.defi.t == interaction.user:
                print(f"ID _{self.defi.id}_ was REFUSED at {datetime.now()}")
                self.defi.all_messages.remove(interaction.message)
                await interaction.message.delete()
                self.defi.all_messages.remove(interaction.message)

                embed = self.defi.origin_message.embeds[0]
                embed.description += f"\n a été **REFUSÉ**"
                embed.title = embed.title.replace("🔓", "🔒")
                self.defi.done = True
                await self.defi.origin_message.edit(embed=embed)
            else:
                await interaction.response.send_message(f"🖕 **Tu n'es pas celui défié** 🖕", ephemeral=True, delete_after=5)
        b2.callback = refuse
        self.add_item(b2)

class maximum_modal(ui.Modal, title = ""):
    def __init__(self, defi: Defi, parent):
        super().__init__()
        self.defi = defi
        self.title = f"Alors, {self.defi.t.display_name} pour combien ?"
        self.parent = parent

        self.answer = ui.TextInput(label = "Maximum", style = discord.TextStyle.short, custom_id="valeur",  required = True)
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            val = int(self.answer.value)
            if val <= 1:
                print(f"ID _{self.defi.id}_ [WARNING] {val} was submitted by user {self.defi.f.display_name} at {datetime.now()}")
                raise Exception(f"La valeur est en dessous de 1, faute de jeu !")
        except ValueError:
            print(f"ID _{self.defi.id}_ [WARNING] {self.answer.value} was submitted by user {self.defi.f.display_name} at {datetime.now()}")
            raise Exception(f"Ce n'est pas une valuer numérique, faute de jeu !")
        
        print(f"ID _{self.defi.id}_ was assigned maximum value of {val} at {datetime.now()}")
        await self.parent.delete()
        self.defi.all_messages.remove(self.parent)
        self.defi.max_value = val
        embed = self.defi.origin_message.embeds[0]
        embed.description += f"\n a été **ACCEPTÉ** pour **{val}**"
        if val == 2:
            embed.description += f" 🚨"
        await self.defi.origin_message.edit(embed=embed)
        self.defi.all_messages.append(
            await interaction.response.send_message(f"Tu as accepté le pour combiens, bonne chance ! 🤞", ephemeral=True, delete_after=0.1)
        )
        view = guess_buttons(self.defi)
        guess_message = await self.defi.origin_message.reply(
            f"{self.defi.t.mention}, a été accepté sur une base de {val}. **{self.defi.f.mention} & {self.defi.t.mention} tenez-vous pret !** 🤼\nVous avez 10 minutes pour répondre",
            view = view
        )
        view.message = guess_message
        self.defi.all_messages.append(
            guess_message
        )

class guess_buttons(discord.ui.View):
    def __init__(self, defi: Defi):
        super().__init__(timeout = 600)
        self.defi = defi
        self.add_buttons()

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message is not None:
            await self.message.edit(content="Le défi a expiré", view=self)
            await self.message.delete()
            self.defi.all_messages.remove(self.message)
            await self.defi.timeout()

    def add_buttons(self):
        b1 = discord.ui.Button(label = self.defi.f.display_name, style = discord.ButtonStyle.blurple)
        async def f(interaction: discord.Interaction):
            if self.defi.f == interaction.user:
                print(f"ID _{self.defi.id}_ was cliked by user {self.defi.f.display_name} at {datetime.now()}")
                await interaction.response.send_modal(guess_modal(self.defi, b1, interaction.message, self)) 
            else:
                await interaction.response.send_message(f"🖕 **Tu n'est pas celui défié** 🖕", ephemeral=True, delete_after=5)
        b1.callback = f
        self.add_item(b1)

        b2 = discord.ui.Button(label = self.defi.t.display_name, style = discord.ButtonStyle.blurple)
        async def t(interaction: discord.Interaction):
            if self.defi.t == interaction.user:
                print(f"ID _{self.defi.id}_ was cliked by user {self.defi.t.display_name} at {datetime.now()}")
                await interaction.response.send_modal(guess_modal(self.defi, b2, interaction.message, self)) 
            else:
                await interaction.response.send_message(f"🖕 **Tu n'est pas celui défié** 🖕", ephemeral=True, delete_after=5)
        b2.callback = t
        self.add_item(b2)

class guess_modal(ui.Modal, title = ""):
    def __init__(self, defi: Defi, b: discord.ui.Button, message, view: ui.View):
        super().__init__()
        self.defi = defi
        self.title = f"Pour {self.defi.max_value}, Attention ! 1, 2, 3, ..."

        self.b = b
        self.message = message
        self.view = view

        self.answer = ui.TextInput(label = f"Devine (1-{self.defi.max_value})", style = discord.TextStyle.short, custom_id="valeur",  required = True)
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            val = int(self.answer.value)
            if val > self.defi.max_value:
                print(f"ID _{self.defi.id}_ [WARNING] {val} was submitted by user {self.defi.f.display_name} at {datetime.now()}")
                raise Exception(f"La valeur est au dessus de la valeur maximum, faute de jeu !")
            elif val < 1:
                print(f"ID _{self.defi.id}_ [WARNING] {val} was submitted by user {self.defi.f.display_name} at {datetime.now()}")
                raise Exception(f"La valeur est en dessous de 1, faute de jeu !")
        except ValueError:
            print(f"ID _{self.defi.id}_ [WARNING] {self.answer.value} was submitted by user {self.defi.f.display_name} at {datetime.now()}")
            raise Exception(f"Ce n'est pas une valuer numérique, faute de jeu !")

        self.b.disabled = True
        await self.message.edit(view=self.view)
        other = None

        if self.defi.f == interaction.user:
            self.defi.f_value = val
            other = self.defi.t
            print(f"ID _{self.defi.id}_ was filled with {self.defi.f_value} by user {self.defi.f.display_name} at {datetime.now()}")
        else:
            self.defi.t_value = val
            other = self.defi.f
            print(f"ID _{self.defi.id}_ was filled with {self.defi.t_value} by user {self.defi.t.display_name} at {datetime.now()}")

        self.defi.all_messages.append(
            await interaction.response.send_message(f"Houla, j'aurais pas mis ca ! 😬", ephemeral=True, delete_after=0.1)
        )

        if self.defi.f_value != 0 and self.defi.t_value != 0 and self.defi.done == False:
            self.defi.done = True
            embed = self.defi.origin_message.embeds[0]
            embed.description += f"\n|| {self.defi.f.mention} a choisi **{self.defi.f_value}** ||"
            embed.description += f"\n|| {self.defi.t.mention} a choisi **{self.defi.t_value}** ||"

            if self.defi.f_value == self.defi.t_value:
                embed.description += f"\n## **{self.defi.t.mention} doit donc REALISER le défi** ✔️"
                embed.color = discord.Colour.green()
            else:
                if self.defi.max_value == 2:
                    embed.description += f"\n## **{self.defi.f.mention} doit donc REALISER le défi** ✔️"
                    embed.color = discord.Colour.green()
                else:
                    embed.description += f"\n## **{self.defi.t.mention} est DISPENSÉ du défi** ❌"
                    embed.color = discord.Colour.red()
            embed.title = embed.title.replace("🔓", "🔒")

            button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Click Me!")

            await self.defi.origin_message.edit(embed=embed, components=[button])
            await self.defi.clear()
            print(f"ID _{self.defi.id}_ has ENDED at {datetime.now()}")
        else:
            self.defi.all_messages.append(
                await self.defi.origin_message.reply(
                    f"Vite {other.mention}!!**{interaction.user.mention}, a choisi un chiffre !** "
                )
            )

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(name = 'pourcombien', description='Un petit pour combiens ?')
@app_commands.describe(member="Qui souhaite-tu defier ?")
@app_commands.rename(member='cible')
async def modal(interaction: discord.Interaction, member: discord.Member):
    if member == interaction.user:
        await interaction.response.send_message(f"Impossible de se défier soi-même", ephemeral=True)
    else:
        await interaction.response.send_modal(pourcombien_modal(member))
try:
    aclient.run(
        os.getenv("DISCORD_TOKEN")
    )
except Exception:
    print(f"Can't find Discord Bot Token")