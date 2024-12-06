"""
Command-line interface for PromptStudio SDK
"""

import click
import asyncio
import json
import os
from typing import Optional
from .prompt import PromptManager
from .prompt.types import MessageType, Memory, MessageContent, RequestPayload
from .utils import setup_logging, load_environment_variables

logger = setup_logging()


@click.group()
@click.version_option()
def cli():
    """PromptStudio CLI - Interact with PromptStudio from the command line"""
    pass


@cli.command()
@click.option(
    "--api-key", envvar="PROMPTSTUDIO_API_KEY", help="Your PromptStudio API key"
)
@click.option(
    "--env",
    type=click.Choice(["test", "prod"]),
    default="test",
    help="Environment to use",
)
@click.option("--bypass/--no-bypass", default=False, help="Enable/disable bypass mode")
@click.option("--prompt-id", required=True, help="Prompt ID to use")
@click.option("--message", required=True, help="Message to send")
@click.option(
    "--memory-type",
    type=click.Choice(["fullMemory", "windowMemory", "summarizedMemory"]),
    default="summarizedMemory",
    help="Type of memory to use",
)
@click.option("--window-size", type=int, default=10, help="Window size for memory")
@click.option("--session-id", help="Session ID for conversation")
@click.option("--version", type=float, help="Prompt version")
@click.option("--image-url", help="URL of image to analyze")
def chat(
    api_key: str,
    env: str,
    bypass: bool,
    prompt_id: str,
    message: str,
    memory_type: str,
    window_size: int,
    session_id: Optional[str],
    version: Optional[float],
    image_url: Optional[str],
):
    """Chat with a prompt"""

    async def run_chat():
        try:
            prompt_manager = PromptManager(api_key=api_key, env=env, bypass=bypass)

            # Prepare user message
            user_message = [MessageContent(type=MessageType.TEXT, text=message)]

            # Add image if provided
            if image_url:
                user_message.append(
                    MessageContent(type=MessageType.FILE, file_url={"url": image_url})
                )

            # Create request payload
            request = RequestPayload(
                user_message=user_message,
                memory_type=memory_type,
                window_size=window_size,
                session_id=session_id or "",
                variables={},
                version=version,
            )

            # Make the request
            response = await prompt_manager.chat_with_prompt(prompt_id, request)

            # Pretty print the response
            click.echo(json.dumps(response, indent=2))

        except Exception as e:
            click.echo(f"Error: {str(e)}", err=True)
            raise click.Abort()

    asyncio.run(run_chat())


@cli.command()
@click.option("--session-id", required=True, help="Session ID to clear")
def clear_session(session_id: str):
    """Clear a specific conversation session"""

    async def run_clear():
        try:
            prompt_manager = PromptManager(
                api_key=os.getenv("PROMPTSTUDIO_API_KEY", ""),
                env=os.getenv("PROMPTSTUDIO_ENV", "test"),
            )
            await prompt_manager.cache.remove_session(session_id)
            click.echo(f"Session {session_id} cleared successfully")
        except Exception as e:
            click.echo(f"Error clearing session: {str(e)}", err=True)
            raise click.Abort()

    asyncio.run(run_clear())


@cli.command()
def clear_cache():
    """Clear all cached conversations"""

    async def run_clear_cache():
        try:
            prompt_manager = PromptManager(
                api_key=os.getenv("PROMPTSTUDIO_API_KEY", ""),
                env=os.getenv("PROMPTSTUDIO_ENV", "test"),
            )
            await prompt_manager.cache.clear_cache()
            click.echo("Cache cleared successfully")
        except Exception as e:
            click.echo(f"Error clearing cache: {str(e)}", err=True)
            raise click.Abort()

    asyncio.run(run_clear_cache())


@cli.command()
def init():
    """Initialize PromptStudio configuration"""
    api_key = click.prompt("Enter your PromptStudio API key", type=str)
    env = click.prompt(
        "Choose environment", type=click.Choice(["test", "prod"]), default="test"
    )

    config = {"api_key": api_key, "env": env}

    config_dir = click.get_app_dir("promptstudio")
    os.makedirs(config_dir, exist_ok=True)

    config_path = os.path.join(config_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    click.echo(f"Configuration saved to {config_path}")


def main():
    """Main entry point for the CLI"""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)


if __name__ == "__main__":
    main()
