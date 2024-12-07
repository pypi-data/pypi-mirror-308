import grpc
import rich_click as click

from datetime import timedelta
from typing import List, Tuple, Union

from armonik.client.sessions import ArmoniKSessions
from armonik.common import SessionStatus, Session, TaskOptions

from armonik_cli.console import console
from armonik_cli.errors import error_handler
from armonik_cli.commands.common import (
    endpoint_option,
    output_option,
    debug_option,
    KeyValuePairParam,
    TimeDeltaParam,
)


SESSION_TABLE_COLS = [("ID", "SessionId"), ("Status", "Status"), ("CreatedAt", "CreatedAt")]
session_argument = click.argument("session-id", required=True, type=str, metavar="SESSION_ID")


@click.group(name="sessions")
def sessions() -> None:
    """Manage cluster sessions."""
    pass


@sessions.command()
@endpoint_option
@output_option
@debug_option
@error_handler
def list(endpoint: str, output: str, debug: bool) -> None:
    """List the sessions of an ArmoniK cluster."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        total, sessions = sessions_client.list_sessions()

    if total > 0:
        sessions = [_clean_up_status(s) for s in sessions]
        console.formatted_print(sessions, format=output, table_cols=SESSION_TABLE_COLS)

    console.print(f"\n{total} sessions found.")


@sessions.command()
@endpoint_option
@output_option
@debug_option
@session_argument
@error_handler
def get(endpoint: str, output: str, session_id: str, debug: bool) -> None:
    """Get details of a given session."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session = sessions_client.get_session(session_id=session_id)
        session = _clean_up_status(session)
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


@sessions.command()
@endpoint_option
@click.option(
    "--max-retries",
    type=int,
    required=True,
    help="Maximum default number of execution attempts for session tasks.",
    metavar="NUM_RETRIES",
)
@click.option(
    "--max-duration",
    type=TimeDeltaParam(),
    required=True,
    help="Maximum default task execution time (format HH:MM:SS.MS).",
    metavar="DURATION",
)
@click.option(
    "--priority", type=int, required=True, help="Default task priority.", metavar="PRIORITY"
)
@click.option(
    "--partition",
    type=str,
    multiple=True,
    help="Partition to add to the session.",
    metavar="PARTITION",
)
@click.option(
    "--default-partition",
    type=str,
    default="default",
    show_default=True,
    help="Default partition.",
    metavar="PARTITION",
)
@click.option(
    "--application-name", type=str, required=False, help="Default application name.", metavar="NAME"
)
@click.option(
    "--application-version",
    type=str,
    required=False,
    help="Default application version.",
    metavar="VERSION",
)
@click.option(
    "--application-namespace",
    type=str,
    required=False,
    help="Default application namespace.",
    metavar="NAMESPACE",
)
@click.option(
    "--application-service",
    type=str,
    required=False,
    help="Default application service.",
    metavar="SERVICE",
)
@click.option(
    "--engine-type", type=str, required=False, help="Default engine type.", metavar="ENGINE_TYPE"
)
@click.option(
    "--option",
    type=KeyValuePairParam(),
    required=False,
    multiple=True,
    help="Additional default options.",
    metavar="KEY=VALUE",
)
@output_option
@debug_option
@error_handler
def create(
    endpoint: str,
    max_retries: int,
    max_duration: timedelta,
    priority: int,
    partition: Union[List[str], None],
    default_partition: str,
    application_name: Union[str, None],
    application_version: Union[str, None],
    application_namespace: Union[str, None],
    application_service: Union[str, None],
    engine_type: Union[str, None],
    option: Union[List[Tuple[str, str]], None],
    output: str,
    debug: bool,
) -> None:
    """Create a new session."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session_id = sessions_client.create_session(
            default_task_options=TaskOptions(
                max_duration=max_duration,
                priority=priority,
                max_retries=max_retries,
                partition_id=default_partition,
                application_name=application_name,
                application_version=application_version,
                application_namespace=application_namespace,
                application_service=application_service,
                engine_type=engine_type,
                options={k: v for k, v in option} if option else None,
            ),
            partition_ids=partition if partition else [default_partition],
        )
        session = sessions_client.get_session(session_id=session_id)
        session = _clean_up_status(session)
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


@sessions.command()
@endpoint_option
@click.confirmation_option("--confirm", prompt="Are you sure you want to cancel this session?")
@output_option
@debug_option
@session_argument
@error_handler
def cancel(endpoint: str, output: str, session_id: str, debug: bool) -> None:
    """Cancel a session."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session = sessions_client.cancel_session(session_id=session_id)
        session = _clean_up_status(session)
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


@sessions.command()
@endpoint_option
@output_option
@debug_option
@session_argument
@error_handler
def pause(endpoint: str, output: str, session_id: str, debug: bool) -> None:
    """Pause a session."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session = sessions_client.pause_session(session_id=session_id)
        session = _clean_up_status(session)
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


@sessions.command()
@endpoint_option
@output_option
@debug_option
@session_argument
@error_handler
def resume(endpoint: str, output: str, session_id: str, debug: bool) -> None:
    """Resume a session."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session = sessions_client.resume_session(session_id=session_id)
        session = _clean_up_status(session)
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


@sessions.command()
@endpoint_option
@click.confirmation_option("--confirm", prompt="Are you sure you want to close this session?")
@output_option
@debug_option
@session_argument
@error_handler
def close(endpoint: str, output: str, session_id: str, debug: bool) -> None:
    """Close a session."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session = sessions_client.close_session(session_id=session_id)
        session = _clean_up_status(session)
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


@sessions.command()
@endpoint_option
@click.confirmation_option("--confirm", prompt="Are you sure you want to purge this session?")
@output_option
@debug_option
@session_argument
@error_handler
def purge(endpoint: str, output: str, session_id: str, debug: bool) -> None:
    """Purge a session."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session = sessions_client.purge_session(session_id=session_id)
        session = _clean_up_status(session)
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


@sessions.command()
@endpoint_option
@click.confirmation_option("--confirm", prompt="Are you sure you want to delete this session?")
@output_option
@debug_option
@session_argument
@error_handler
def delete(endpoint: str, output: str, session_id: str, debug: bool) -> None:
    """Delete a session and associated data from the cluster."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session = sessions_client.delete_session(session_id=session_id)
        session = _clean_up_status(session)
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


@sessions.command()
@endpoint_option
@session_argument
@click.option(
    "--clients-only",
    is_flag=True,
    default=False,
    help="Prevent only clients from submitting new tasks in the session.",
)
@click.option(
    "--workers-only",
    is_flag=True,
    default=False,
    help="Prevent only workers from submitting new tasks in the session.",
)
@output_option
@debug_option
@error_handler
def stop_submission(
    endpoint: str, session_id: str, clients_only: bool, workers_only: bool, output: str, debug: bool
) -> None:
    """Stop clients and/or workers from submitting new tasks in a session."""
    with grpc.insecure_channel(endpoint) as channel:
        sessions_client = ArmoniKSessions(channel)
        session = sessions_client.stop_submission_session(
            session_id=session_id, client=clients_only, worker=workers_only
        )
        console.formatted_print(session, format=output, table_cols=SESSION_TABLE_COLS)


def _clean_up_status(session: Session) -> Session:
    session.status = SessionStatus.name_from_value(session.status).split("_")[-1].capitalize()
    return session
