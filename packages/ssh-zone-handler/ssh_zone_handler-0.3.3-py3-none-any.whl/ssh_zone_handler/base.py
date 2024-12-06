"""Base classes"""

import logging
from collections.abc import KeysView, Sequence
from subprocess import CalledProcessError, CompletedProcess, run
from typing import Final, Iterator, Optional

from .types import ZoneHandlerConf


class InvokeError(Exception):
    """Used to propagate an error to the top level wrapper method"""


class SshZoneHandler:
    """Parse shared config, define constants, etc"""

    def __init__(self, config: ZoneHandlerConf):
        self.config: ZoneHandlerConf = config
        self.log_user: Final[str] = config.system.log_access_user
        self.server: Final[str] = config.system.server_type
        self.service_user: Final[str] = config.system.server_user
        service_unit: Final[str] = config.system.systemd_unit

        self.journal_cmd: Final[tuple[str, str, str, str]] = (
            "/usr/bin/journalctl",
            f"--unit={service_unit}",
            "--since=-5days",
            "--utc",
        )


class SshZoneSudoers(SshZoneHandler):
    """Common class to pre-generate needed sudoers rules"""

    def __log_rules(self) -> list[str]:
        users: KeysView[str] = self.config.zones.keys()
        command: str = " ".join(self.journal_cmd)
        rules: list[str] = []

        user: str
        for user in users:
            rule = f"{user}\tALL=({self.log_user}) NOPASSWD: {command}"
            rules.append(rule)

        return rules

    def _server_command_rules(self) -> list[str]:
        raise NotImplementedError("Gets defined in each daemon specific subclass")

    def generate(self) -> None:
        """Outputs all the needed sudoers rules."""

        all_rules: list[str] = []
        all_rules += self.__log_rules()
        all_rules += self._server_command_rules()

        rule: str
        for rule in all_rules:
            print(rule)


class SshZoneCommand(SshZoneHandler):
    """Command class to runs the actual commands"""

    def __init__(self, config: ZoneHandlerConf):
        super().__init__(config)

        self.sudo_prefix: Final[tuple[str, str]] = (
            "/usr/bin/sudo",
            f"--user={self.service_user}",
        )

    def __zone_list(self, username: str) -> Sequence[str]:
        user_zones: Sequence[str] = ()

        try:
            user_zones = tuple(self.config.zones[username])
        except KeyError:
            pass

        return user_zones

    @staticmethod
    def __parse(
        ssh_command: str, user_zones: Sequence[str]
    ) -> tuple[Optional[str], list[str]]:
        args: list[str] = ssh_command.split()
        command: Optional[str] = None
        zones: list[str] = []

        if args[0] in ["help", "list", "dump", "logs", "retransfer", "status"]:
            command = args[0]
        args.pop(0)

        for arg in args:
            if arg in user_zones:
                zones.append(arg)

        return command, zones

    @staticmethod
    def _runner(command: Sequence[str], failure: str) -> CompletedProcess[str]:
        try:
            result = run(command, capture_output=True, check=True, text=True)
        except (FileNotFoundError, CalledProcessError) as err:
            logging.debug("%s: %s", type(err).__name__, str(err))
            if isinstance(err, CalledProcessError):
                logging.debug(err.stderr)
            raise InvokeError(failure) from err

        return result

    @staticmethod
    def __usage() -> None:
        print("usage: command [ZONE]")
        print()
        print("help\t\t\tDisplay this help message")
        print("list\t\t\tList available zones")
        print("dump ZONE\t\tOutput full content of ZONE")
        print("logs ZONE1 [ZONE2]\tOutput the last five days' log entries for ZONE(s)")
        print("retransfer ZONE\t\tTrigger a full (AXFR) retransfer of ZONE")
        print("status ZONE\t\tShow ZONE status")

    @staticmethod
    def _filter_logs(log_lines: list[str], zones: list[str]) -> Iterator[str]:
        raise NotImplementedError("Gets defined in each daemon specific subclass")

    def __logs(self, zones: list[str]) -> None:
        zones_str = ", ".join(zones)
        failure = f"Failed to output log lines for the following zone(s): {zones_str}"
        command = ("/usr/bin/sudo", f"--user={self.log_user}") + self.journal_cmd

        logging.info("Outputting logs for the following zone(s): %s", zones_str)

        result: CompletedProcess[str] = self._runner(command, failure)
        log_lines: list[str] = result.stdout.split("\n")

        line: str
        for line in self._filter_logs(log_lines, zones):
            print(line)

    def _dump(self, zone: str) -> None:
        raise NotImplementedError("Gets defined in each daemon specific subclass")

    def _retransfer(self, zone: str) -> None:
        raise NotImplementedError("Gets defined in each daemon specific subclass")

    def _status(self, zone: str) -> None:
        raise NotImplementedError("Gets defined in each daemon specific subclass")

    def invoke(self, ssh_command: str, username: str) -> None:
        """
        Pick what, if any, command to invoke.

        :param ssh_command: The full SSH_ORIGINAL_COMMAND
        :param username: Current user, executing the program
        """

        user_zones: Sequence[str] = self.__zone_list(username)

        if not user_zones:
            raise InvokeError(f'No zones configured for user "{username}"')

        command: Optional[str]
        zones: list[str]
        command, zones = self.__parse(ssh_command, user_zones)

        if not command:
            raise InvokeError('Invalid command, try "help"')

        if command == "help":
            self.__usage()
        elif command == "list":
            uzn: str
            for uzn in user_zones:
                print(uzn)
        elif not zones:
            raise InvokeError("No valid zone provided")
        elif command == "dump":
            self._dump(zones[0])
        elif command == "logs":
            self.__logs(zones)
        elif command == "retransfer":
            self._retransfer(zones[0])
        elif command == "status":
            self._status(zones[0])
