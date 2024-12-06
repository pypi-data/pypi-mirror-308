#!/usr/bin/env python3
import asyncio
from argparse import ArgumentParser
from json import dumps
from sys import stdout

from yatc import TermColor
from . import okta_client


parser = ArgumentParser(description="Get Okta user by email or ID")
parser.add_argument("user", help="Email or ID of the user. Can also be a comma-separated list of emails or IDs")
parser.add_argument("--groups", "-g", action="store_true", help="Include user groups")
parser.add_argument("--no-color", action="store_true", help="Disable color output")
args = parser.parse_args()

no_color = (args.no_color or (not stdout.isatty()))

async def main():
    try:
        if "@" not in args.user:
            username = f"{args.user}@hingehealth.com".lower()
        else:
            username = args.user.lower()

        user = (await okta_client.get_user(username))[0]

        if not user:
            raise IndexError

    except IndexError:
        print(f"User {args.user} not found")
        exit(1)

    res = user.as_dict()

    if args.groups:
        groups = (await okta_client.list_user_groups(user.id))[0]

        groups = [
            {
                "id": x.id,
                "name": x.profile.name,
                "description": x.profile.description,
                "phiaccess": getattr(x.profile, "phiaccess", False),
            }
            for x in groups
            if x.type.value == "OKTA_GROUP"
        ]
    
        res["groups"] = groups

    del res["_links"]
    del res["credentials"]
    del res["type"]

    # res = dumps(res, indent=2, default=lambda x: str(x))
    if not no_color:

        if getattr(user.profile, "phiaccess", False):
            res["profile"]["phiaccess"] = TermColor.decorate(str(res["profile"]["phiaccess"]), ["GREEN"])
            res["profile"]["email"] = TermColor.decorate(res["profile"]["email"], ["GREEN"])
        else:
            res["profile"]["phiaccess"] = TermColor.decorate(str(res["profile"]["phiaccess"]), ["RED"])
            res["profile"]["email"] = TermColor.decorate(res["profile"]["email"], ["RED"])

        if res.get("groups"):
            for i, group in enumerate(res["groups"]):
                if group["phiaccess"]:
                    res["groups"][i]["name"] = TermColor.decorate(group["name"], ["RED"])
                else:
                    res["groups"][i]["name"] = TermColor.decorate(group["name"], ["GREEN"])

        res = dumps(res, indent=2, default=lambda x: str(x))
        res = res.encode("utf-8").decode("unicode_escape")

    else:
        res = dumps(res, indent=2, default=lambda x: str(x))

    print(res)


def cli():
    asyncio.run(main())