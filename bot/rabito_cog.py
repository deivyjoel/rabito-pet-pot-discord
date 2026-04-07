from discord.ext import commands
import discord
from discord import app_commands


class RabitoCog(commands.Cog):
    def __init__(self, bot, api):
        self.bot = bot
        self.api = api

    # /crear_rabito
    @app_commands.command(
        name="crear_rabito",
        description="Crea un nuevo rabito"
    )
    async def crear_rabito(
        self,
        interaction: discord.Interaction,
        nombre: str
    ):
        try:
            result = self.api.create_rabito(
                interaction.user.id,
                nombre
            )
            await interaction.response.send_message(
                f"Rabito creado: {result}"
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Error: {e}"
            )

    # /listar_rabitos
    @app_commands.command(
        name="listar_rabitos",
        description="Lista tus rabitos"
    )
    async def listar_rabitos(
        self,
        interaction: discord.Interaction
    ):
        try:
            rabitos = self.api.list_rabitos(interaction.user.id)

            if not rabitos:
                msg = "No tienes rabitos."
            else:
                msg = f"Rabitos: {', '.join(rabitos)}"

            await interaction.response.send_message(msg)

        except Exception as e:
            await interaction.response.send_message(
                f"Error: {e}"
            )

    # /alimentar_rabito
    @app_commands.command(
        name="alimentar_rabito",
        description="Alimenta un rabito"
    )
    async def alimentar_rabito(
        self,
        interaction: discord.Interaction,
        rabito_id: int,
        comida_id: int
    ):
        try:
            result = self.api.feed_rabito(
                rabito_id,
                comida_id,
                interaction.user.id
            )

            await interaction.response.send_message(
                f"Rabito alimentado: {result}"
            )

        except Exception as e:
            await interaction.response.send_message(
                f"Error: {e}"
            )
