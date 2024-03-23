import discord
from discord import app_commands, Interaction
from discord.app_commands import AppCommandError
from discord.ext import commands

class OwnerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id != self.bot.owner_id

    async def cog_app_command_error(self, interaction: Interaction, error: AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            embed = discord.Embed(
                title = "Permission denied",
                description = "Hey! This is an owner-only command.",
                color = discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        else:
            print(error)

    @app_commands.command(
        name = "sendmsg",
        description = "Send a DM to a user of choice."
    )
    async def send_private_message(
        self,
        interaction: Interaction,
        user: discord.User,
        message: str
    ):
        embed = discord.Embed(
            title = f"Message sent to {user.name}!",
            description = f"*{message}*",
            color = discord.Color.green()
        )
        await user.send(message)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name = "sendsurvey",
        description = "Send a DM survey to a user of choice."
    )
    async def send_survey(self, interaction: Interaction, user: discord.User):
        embed = discord.Embed(
            title = f"Survey was sent to {user.name}!",
            description = "Waiting on their response...",
            color = discord.Color.dark_gray()
        )
        view_var = DMSurveyView(interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        view_var.message = await user.send(embed=view_var.receiver_embed, view=view_var)

class DMSurveyView(discord.ui.View):
    def __init__(self, orig_interaction: Interaction, fields: dict = None, **kwargs):
        super().__init__(**kwargs)
        # Should be assigned with return value of abc.Messagable.send()
        self.message: discord.Message = None
        # Allows survey sender to receive modal responses on submission
        self.orig_interaction = orig_interaction
        self.fields = fields
        self.receiver_embed = discord.Embed(
            title = f"{orig_interaction.user.name} sent you an in-app survey!",
            description = "Click the button below to open it.",
            color = discord.Color.green()
        )

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        self.receiver_embed.set_footer(text="This survey can no longer be taken.")
        await self.message.edit(embed=self.receiver_embed, view=self)

    @discord.ui.button(label="Take the survey", style=discord.ButtonStyle.blurple)
    async def send_modal(self, interaction: Interaction, button: discord.ui.Button):
        # Opens the modal on the receiver's end
        await interaction.response.send_modal(
            DMSurveyModal(parent_view=self)
        )

class DMSurveyModal(discord.ui.Modal):
    def __init__(self, parent_view: DMSurveyView, **kwargs):
        super().__init__(
            title = f"{parent_view.orig_interaction.user.name}'s Survey",
            **kwargs
        )
        self.parent_view = parent_view
        if self.parent_view.fields is None:
            self.fields = {
                "Name": discord.TextStyle.short,
                "Age": discord.TextStyle.short,
                "Bio": discord.TextStyle.long,
                "Social Security Number": discord.TextStyle.short
            }
        for field in self.fields:
            self.add_item(
                discord.ui.TextInput(
                    label = field,
                    style = self.fields[field]
                )
            )

    async def on_submit(self, interaction: Interaction):
        # This embed containing modal responses is sent to the survey
        # sender where the command was originally called.
        surveyor_embed = discord.Embed(
            title = f"{interaction.user} submitted a response!",
            color = discord.Color.green()
        )
        for input in self.children:
            surveyor_embed.add_field(
                name = input.label,
                value = input.value,
                inline = False
            )
        # Edits the view's embed in response to modal submission
        self.parent_view.receiver_embed.title = \
            "Thank you for taking " \
            + f"{self.parent_view.orig_interaction.user.name}'s survey!"
        self.parent_view.receiver_embed.description = \
            "Responses were sent to the survey sender."
        # Adds a footer to the view's embed and disables the survey button
        await self.parent_view.on_timeout()
        await self.parent_view.message.edit(view=self.parent_view)
        # Sends the response embed to the survey sender
        await self.parent_view.orig_interaction.followup.send(
            embed = surveyor_embed,
            ephemeral = True
        )
        # The interaction needs to be responded to somehow
        await interaction.response.defer()

async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerCommands(bot))