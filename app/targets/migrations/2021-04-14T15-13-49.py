from piccolo.apps.migrations.auto import MigrationManager
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import BigInt
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Real
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class Target(Table, tablename="target"):
    pass


ID = "2021-04-14T15:13:49"
VERSION = "0.17.5"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="targets")

    manager.add_table("Detection", tablename="detection")

    manager.add_table("Target", tablename="target")

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="target",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Target,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="candid",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": 0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": True,
            "index": True,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="filter",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="magpsf",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="sigmapsf",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="diffmaglim",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="isdiffpos",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 1,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="jd",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="utc",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Detection",
        tablename="detection",
        column_name="created",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": True,
            "index": True,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="classification",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "requird": False,
            "length": 255,
            "default": "",
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="ra",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="dec",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="utc",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="latest_r_mag",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="latest_g_mag",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="max_r_mag",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="max_g_mag",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": None,
            "null": True,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    manager.add_column(
        table_class_name="Target",
        tablename="target",
        column_name="created",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": False,
            "primary": False,
            "key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
        },
    )

    return manager
