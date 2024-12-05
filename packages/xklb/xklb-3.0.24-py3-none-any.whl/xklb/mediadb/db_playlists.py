import os, sqlite3

from xklb.utils import consts, date_utils, db_utils, iterables, objects
from xklb.utils.log_utils import log

"""
playlists table
    profile = Type of extractor -- consts.DBType
    extractor_key = Name of the Extractor -- "Local", "Imgur", "YouTube"
    extractor_playlist_id = ID that the extractor uses to refer to playlists (yt-dlp playlist_id)

media table
    extractor_id = ID that the Extractor uses to refer to media
    playlists_id = Foreign key to playlists table
"""


def consolidate(args, v: dict) -> dict:
    upload_time = date_utils.tube_date(v)

    cv = {}
    cv["profile"] = iterables.safe_unpack(getattr(args, "profile", None), v.pop("profile", None))
    cv["time_uploaded"] = upload_time
    cv["time_modified"] = consts.now()
    cv["time_deleted"] = 0

    cv["extractor_config"] = {
        **(v.pop("extractor_config", None) or {}),
        **(getattr(args, "extractor_config", None) or {}),
    }

    cv["extractor_key"] = iterables.safe_unpack(
        v.pop("ie_key", None),
        v.pop("extractor_key", None),
        v.pop("extractor", None),
    )
    cv["extractor_playlist_id"] = iterables.safe_unpack(v.pop("playlist_id", None), v.pop("id", None))
    cv["title"] = iterables.safe_unpack(v.get("playlist_title"), v.pop("title", None))

    cv["uploader"] = iterables.safe_unpack(
        v.pop("playlist_uploader_id", None),
        v.pop("playlist_uploader", None),
        v.pop("playlist_channel_id", None),
        v.pop("playlist_channel", None),
        v.pop("channel_id", None),
        v.pop("uploader_url", None),
        v.pop("channel_url", None),
        v.pop("uploader", None),
        v.pop("channel", None),
        v.pop("uploader_id", None),
    )

    v = {
        k: v
        for k, v in v.items()
        if not (k.startswith("_") or k in consts.MEDIA_KNOWN_KEYS + consts.PLAYLIST_KNOWN_KEYS or v is None)
    }
    if v != {}:
        log.info("Extra playlists data %s", v)
        # breakpoint()

    return objects.dict_filter_bool(cv) or {}


def get_id(args, playlist_path) -> int:
    return args.db.pop("select id from playlists where path=?", [str(playlist_path)])


def _add(args, entry):
    playlists_id = get_id(args, entry["path"])
    if playlists_id:
        entry["id"] = playlists_id
        args.db["playlists"].upsert(entry, pk="id", alter=True)
    else:
        entry["time_created"] = consts.APPLICATION_START
        entry["hours_update_delay"] = 70  # about three days
        args.db["playlists"].insert(entry, pk="id", alter=True)
        playlists_id = get_id(args, entry["path"])
    return playlists_id


def exists(args, playlist_path) -> bool:
    try:
        known = args.db.pop("select 1 from playlists where path=?", [str(playlist_path)])
    except sqlite3.OperationalError as e:
        log.debug(e)
        return False
    if known is None:
        return False
    return True


def get_parentpath_playlists_id(args, playlist_path) -> int | None:
    try:
        known = args.db.pop(
            "select id from playlists where ? like path || '%' and path != ?",
            [str(playlist_path), str(playlist_path)],
        )
    except sqlite3.OperationalError as e:
        log.debug(e)
        return None
    return known


def delete_subpath_playlists(args, playlist_path) -> int | None:
    try:
        with args.db.conn:
            args.db.conn.execute(
                """
                DELETE from playlists
                WHERE COALESCE(time_deleted, 0)=0
                    AND path LIKE ?
                    AND path != ?
                """,
                [str(playlist_path) + os.sep + "%", str(playlist_path)],
            )
    except sqlite3.OperationalError:
        pass


def add(args, playlist_path: str, info: dict, check_subpath=False, extractor_key=None) -> int:
    playlist_path = playlist_path.strip()
    if check_subpath:
        parentpath_playlist_id = get_parentpath_playlists_id(args, playlist_path)
        if parentpath_playlist_id:
            return parentpath_playlist_id
        else:
            delete_subpath_playlists(args, playlist_path)

    pl = consolidate(args, objects.dumbcopy(info))
    playlist = {**pl, "path": playlist_path}
    if extractor_key:
        playlist["extractor_key"] = extractor_key
    return _add(args, objects.dict_filter_bool(playlist) or {})


def media_exists(args, playlist_path, path) -> bool:
    m_columns = db_utils.columns(args, "media")
    try:
        known = args.db.execute(
            f"select 1 from media where playlists_id in (select id from playlists where path = ?) and (path=? or {'webpath' if 'webpath' in m_columns else 'path'}=?)",
            [str(playlist_path), str(path), str(path)],
        ).fetchone()
    except sqlite3.OperationalError as e:
        log.debug(e)
        return False
    if known is None:
        return False
    return True


def decrease_update_delay(args, playlist_path: str) -> None:
    if "playlists" not in args.db.table_names():
        return

    try:
        with args.db.conn:
            args.db.conn.execute(
                """
                UPDATE playlists
                SET time_modified = cast(STRFTIME('%s', 'now') as int)
                , hours_update_delay = CASE
                    WHEN 0.3 * hours_update_delay <= 1 THEN 1
                    WHEN 0.3 * hours_update_delay >= 8760 THEN 8760
                    ELSE cast(0.3 * hours_update_delay as int)
                END
                WHERE hours_update_delay IS NOT NULL
                    AND path = ?
                """,
                [playlist_path],
            )
    except sqlite3.OperationalError as e:
        try:
            with args.db.conn:
                args.db.conn.execute("ALTER TABLE playlists ADD COLUMN hours_update_delay INTEGER DEFAULT 70")
        except Exception:
            raise e


def increase_update_delay(args, playlist_path: str) -> None:
    if "playlists" not in args.db.table_names():
        return

    try:
        with args.db.conn:
            args.db.conn.execute(
                """
                UPDATE playlists
                SET time_modified = cast(STRFTIME('%s', 'now') as int)
                ,   hours_update_delay = CASE
                    WHEN 2 * hours_update_delay <= 1 THEN 1
                    WHEN 2 * hours_update_delay >= 8760 THEN 8760
                    ELSE 2 * hours_update_delay
                END
                WHERE hours_update_delay IS NOT NULL
                    AND path = ?
                """,
                [playlist_path],
            )
    except sqlite3.OperationalError as e:
        try:
            with args.db.conn:
                args.db.conn.execute("ALTER TABLE playlists ADD COLUMN hours_update_delay INTEGER DEFAULT 70")
        except Exception:
            raise e


def get_all(args, cols="path, extractor_config", sql_filters=None, order_by="random()") -> list[dict]:
    pl_columns = db_utils.columns(args, "playlists")
    if sql_filters is None:
        sql_filters = []
    if "time_deleted" in pl_columns:
        sql_filters.append("AND COALESCE(time_deleted,0) = 0")
    if "hours_update_delay" in pl_columns and not getattr(args, "force", False):
        sql_filters.append("AND (cast(STRFTIME('%s', 'now') as int) - time_modified) >= (hours_update_delay * 60 * 60)")

    try:
        known_playlists = list(
            args.db.query(f"select {cols} from playlists where 1=1 {' '.join(sql_filters)} order by {order_by}"),
        )
    except TypeError:
        known_playlists = []
    return known_playlists


def log_problem(args, playlist_path) -> None:
    if exists(args, playlist_path):
        log.warning("Start of known playlist reached %s", playlist_path)
    else:
        log.warning("Could not add playlist %s", playlist_path)


def save_undownloadable(args, playlist_path) -> None:
    entry = {"path": playlist_path, "extractor_config": args.extractor_config}
    _add(args, objects.dict_filter_bool(entry) or {})
