#!/usr/bin/env python3
import asyncio
from argparse import ArgumentParser, SUPPRESS
from json import dumps
from re import compile as re_compile, IGNORECASE
from yatc import TermColor
from . import okta_client


parser = ArgumentParser(description="Get Okta user by email or ID")
parser.add_argument("--case-sensitive", "-c", action="store_true", help="Case sensitive search")

sub_parsers = parser.add_subparsers(help="Sub-command help", dest="command")

search_cmd = sub_parsers.add_parser("search", help="List all groups")
search_cmd.add_argument("query", help="Query string to use. Supports regex", nargs="*", default=SUPPRESS)
search_cmd.add_argument("--type", "-t", type=str, help="Filter by group type", choices=["OKTA_GROUP", "APP_GROUP"], default="OKTA_GROUP")
search_cmd.add_argument("--verbose", action="store_true", help="Return full group object")


get_cmd = sub_parsers.add_parser("get", help="Get group by name or ID")
get_cmd.add_argument("group", help="Name or ID of the group")
get_cmd.add_argument("--users", "-u", action="store_true", help="Include group users")
get_cmd.add_argument("--id", "-i", action="store_true", help="Use group ID instead of name")
get_cmd.add_argument("--no-color", action="store_true", help="Disable color output")
get_cmd.add_argument("--add-user", "-a", type=str, help="Add user to the group")
get_cmd.add_argument("--remove-user", "-r", type=str, help="Remove user from the group")
args = parser.parse_args()


async def search(args):
    query = " ".join(args.query)
    re_flags = 0 if args.case_sensitive else IGNORECASE

    regex = re_compile(args.query[0], flags=re_flags)

    res = []

    opts = {
        "search": f"type eq \"{args.type}\""
    }

    while True:
        groups, resp, error = await okta_client.list_groups(query_params=opts)
        res += groups
        if not resp.has_next():
            break
        if error:
            print(f"Error: {error}")
            exit(1)

    if args.verbose:
        res = [
            x.as_dict() for x in res if regex.match(x.profile.name)
        ]
    else:
        res = [
            x.profile.name for x in res if regex.match(x.profile.name)
        ]

    print(dumps(res, indent=2, default=lambda x: str(x)))


async def get_group(args):
    if args.add_user and args.remove_user:
        print("Cannot add and remove user at the same time")
        exit(1)

    username = args.add_user or args.remove_user
    try:
        if args.id:
            group = (await okta_client.get_group(args.group))[0][0]
        else:
            opts = {
                "search": f"type eq \"OKTA_GROUP\" and profile.name eq \"{args.group}\""
            }
            group = (await okta_client.list_groups(query_params=opts))[0][0]
        if not group:
            raise IndexError
    except IndexError:
        print(f"Group {args.group} not found")
        exit(1)

    
    
    res = group.as_dict()

    if args.users:
        users = (await okta_client.list_group_users(group.id))[0]
        users = [x for x in users if x.status.value == "ACTIVE"]

        if not args.no_color:
            for i, user in enumerate(users):
                if getattr(user.profile, "phiaccess", False):
                    users[i] = TermColor.decorate(user.profile.login, ["GREEN"])
                else:
                    users[i] = TermColor.decorate(user.profile.login, ["RED"])
 
        else:
            users = [x.profile.login for x in users]

        res["users"] = users

    del res["_links"]
    del res["type"]

    if not args.no_color:
        res = dumps(res, indent=2, default=lambda x: str(x)).encode("utf-8").decode("unicode_escape")
    else:
        res = dumps(res, indent=2, default=lambda x: str(x))
    print(res)

    if username:
        if "@" not in username:
            username = f"{username}@hingehealth.com".lower()
        else:
            username = username.lower()

        try:
            res = await okta_client.get_user(username)

            if res[1].get_status() not in  (200, 204):
                raise Exception(res[1].get_body())

            user = res[0]
        except Exception as e:
            print(f"Error getting user: {e}")
            exit(1)

    if args.add_user:
        try:
            res = await okta_client.add_user_to_group(group.id, user.id)

            if res[0].get_status() not in (204, 200):
                raise Exception(res[1].get_body())

            print(f"User {username} added to group {args.group}")
        except Exception as e:
            print(f"Error adding user to group: {e}")

    if args.remove_user:
        try:
            res = await okta_client.remove_user_from_group(group.id, user.id)

            if res[0].get_status() not in (204, 200):
                raise Exception(res[1].get_body())

            print(f"User {username} removed from group {args.group}")
        except Exception as e:
            print(f"Error adding user to group: {e}")
    

async def main():
    if args.command == "search":
        await search(args)
        exit(0)

    if args.command == "get":
        await get_group(args)
        exit(0)


def cli():
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())