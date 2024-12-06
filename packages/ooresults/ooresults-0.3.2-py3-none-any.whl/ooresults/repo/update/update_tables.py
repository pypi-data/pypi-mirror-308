# Copyright (C) 2022 Rainer Garus
#
# This file is part of the ooresults Python package, a software to
# compute results of orienteering events.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging

from ooresults.repo.update import update_008
from ooresults.repo.update import update_009
from ooresults.repo.update import update_010
from ooresults.repo.update import update_011
from ooresults.repo.update import update_012
from ooresults.repo.update import update_013


VERSION = 13


def update_tables(db, path: str = "ooresults.sqlite") -> None:
    t = db.transaction()
    db.ctx.db.execute("BEGIN EXCLUSIVE TRANSACTION;")

    values = list(db.query("SELECT value FROM version"))
    if not values:
        raise RuntimeError("DB error - table version is empty")

    else:
        version = values[0].value
        logging.info(f"DB version is {version}")

        if version > VERSION:
            raise RuntimeError(
                f"DB version to high - version = {version}, but must be at most {VERSION}"
            )

        elif version < VERSION:
            t.rollback()

            if version <= 6:
                raise RuntimeError(
                    f"DB version to low - version = {version}, but must be at least 7"
                )
            if version <= 7:
                logging.info("Update DB to version 8 ...")
                update_008.update(path=path)
            if version <= 8:
                logging.info("Update DB to version 9 ...")
                update_009.update(path=path)
            if version <= 9:
                logging.info("Update DB to version 10 ...")
                update_010.update(path=path)
            if version <= 10:
                logging.info("Update DB to version 11 ...")
                update_011.update(path=path)
            if version <= 11:
                logging.info("Update DB to version 12 ...")
                update_012.update(path=path)
            if version <= 12:
                logging.info("Update DB to version 13 ...")
                update_013.update(path=path)

            logging.info(f"DB updated to version {VERSION}")
        else:
            t.rollback()
