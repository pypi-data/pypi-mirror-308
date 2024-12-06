#!/usr/bin/env python3
import argparse
import asyncio
import os
import sys
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .models import get_model, get_supported_providers
from .utils import (
    get_current_head,
    get_git_diff,
    git_pull,
    parse_commit_range,
    stream_response,
    verify_commit_exists,
    verify_git_repo,
)


async def summarize_async(from_commit: str, to_commit: str, provider_name: str, model_name: str):
    """Summarize changes between commits."""
    try:
        # Get the diff
        diff = get_git_diff(from_commit, to_commit)
        if diff is None:
            print(
                f"Error: Could not generate diff between '{from_commit}' and '{to_commit}'")
            sys.exit(1)

        if not diff.strip():
            print(f"No changes found between {from_commit} and {to_commit}")
            return

        # Initialize chain
        model = get_model(provider_name, model_name)
        system_prompt = (
            "You are a helpful AI that summarizes git diffs. Provide a clear, concise "
            "summary of important changes and their impact. Unimportant changes do not "
            "need to be mentioned. If the diff is empty, say so."
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Summarize this git diff:\n\n{diff}")
        ])
        chain = prompt | model | StrOutputParser()

        # Stream the summary
        stream = chain.astream({"diff": diff})
        await stream_response(stream)

    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for git-summarize command."""
    try:
        default_provider = os.getenv('GIT_SUMMARIZE_PROVIDER') or 'anthropic'
        default_model = os.getenv(
            'GIT_SUMMARIZE_MODEL') or 'claude-3-5-sonnet-latest'

        parser = argparse.ArgumentParser(
            description='Summarize git changes between commits',
        )
        parser.add_argument(
            '--provider',
            default=default_provider,
            help=f'Provider name (default: {default_provider})',
        )
        parser.add_argument(
            '--model',
            default=default_model,
            help=f'Model name (default: {default_model})',
        )
        parser.add_argument(
            '--pull',
            action='store_true',
            help='Pull and summarize changes',
        )
        parser.add_argument(
            'commit_range',
            nargs='?',
            help='Commit range (e.g. commit1..commit2) or single commit',
        )
        parser.add_argument(
            '--list-providers',
            action='store_true',
            help='List supported providers',
        )

        args = parser.parse_args()

        if args.list_providers:
            providers = get_supported_providers()
            for provider in providers:
                print(f"- {provider}")
            sys.exit(0)

        verify_git_repo()

        if args.provider != default_provider and args.model == default_model:
            args.model = None

        if args.pull:
            # Pull and summarize changes between old HEAD and new HEAD
            from_commit = get_current_head()
            if not from_commit:
                print("Error: Could not get current HEAD")
                sys.exit(1)

            success, output = git_pull()
            print(output.strip())

            if not success:
                sys.exit(1)
            if "Already up to date." in output:
                sys.exit(0)

            to_commit = get_current_head()
            if not to_commit:
                print("Error: Could not get new HEAD")
                sys.exit(1)
        else:
            if not args.commit_range:
                parser.print_help()
                sys.exit(1)

            # Summarize changes between commits (or commit and HEAD)
            from_commit, to_commit = parse_commit_range(args.commit_range)

            if not verify_commit_exists(from_commit):
                print(f"Error: Commit '{from_commit}' not found")
                sys.exit(1)
            if not verify_commit_exists(to_commit):
                print(f"Error: Commit '{to_commit}' not found")
                sys.exit(1)

        asyncio.run(
            summarize_async(
                from_commit,
                to_commit,
                args.provider,
                args.model,
            )
        )

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
