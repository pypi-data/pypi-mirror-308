import argparse, difflib, os, re, shlex, tempfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path

from xklb import usage
from xklb.files import sample_compare, sample_hash
from xklb.mediadb import db_media
from xklb.playback import media_printer
from xklb.utils import (
    arggroups,
    argparse_utils,
    consts,
    db_utils,
    devices,
    file_utils,
    path_utils,
    processes,
    sql_utils,
    strings,
)
from xklb.utils.consts import DBType
from xklb.utils.log_utils import log


def parse_args() -> argparse.Namespace:
    parser = argparse_utils.ArgumentParser(usage=usage.dedupe_media)
    arggroups.sql_fs(parser)

    profile = parser.add_mutually_exclusive_group()
    profile.add_argument(
        "--audio",
        action="store_const",
        dest="profile",
        const=DBType.audio,
        help="Dedupe database by artist + album + title",
    )
    profile.add_argument(
        "--extractor-id",
        "--id",
        action="store_const",
        dest="profile",
        const="extractor_id",
        help="Dedupe database by extractor_id",
    )
    profile.add_argument(
        "--title",
        action="store_const",
        dest="profile",
        const="title",
        help="Dedupe database by title",
    )
    profile.add_argument(
        "--same-duration",
        action="store_const",
        dest="profile",
        const="duration",
        help="Dedupe database by duration (caution obviously)",
    )
    profile.add_argument(
        "--filesystem",
        "--fs",
        "--hash",
        action="store_const",
        dest="profile",
        const=DBType.filesystem,
        help="Dedupe filesystem database",
    )
    profile.add_argument(
        "--text",
        action="store_const",
        dest="profile",
        const=DBType.text,
        help=argparse.SUPPRESS,
        #  "Dedupe text database",
    )
    profile.add_argument(
        "--image",
        action="store_const",
        dest="profile",
        const=DBType.image,
        help=argparse.SUPPRESS,
        # "Dedupe image database",
    )

    parser.set_defaults(limit="100")

    parser.add_argument("--dedupe-cmd", help=argparse.SUPPRESS)
    parser.add_argument("--force", "-f", action="store_true")

    parser.add_argument("--compare-dirs", action="store_true")
    parser.add_argument("--basename", action="store_true")
    parser.add_argument("--dirname", action="store_true")
    parser.add_argument(
        "--min-similarity-ratio",
        type=float,
        default=consts.DEFAULT_DIFFLIB_RATIO,
        help="Filter out matches with less than this ratio. A sane value is in the range of 0.7~0.9",
    )

    arggroups.debug(parser)

    arggroups.database(parser)
    parser.add_argument("search", nargs="*")
    parser.set_defaults(fts=False)
    args = parser.parse_intermixed_args()
    arggroups.args_post(args, parser)

    arggroups.sql_fs_post(args, table_prefix="m1.")

    m_columns = db_utils.columns(args, "media")
    if args.compare_dirs:
        args.table2 = "media"
        search_sql, search_bindings = sql_utils.construct_search_bindings(
            include=[args.include.pop()],
            exclude=args.exclude,
            columns=[f"m2.{k}" for k in m_columns if k in db_utils.config["media"]["search_columns"] if k in m_columns],
            exact=args.exact,
            flexible_search=args.flexible_search,
        )
        args.filter_sql.extend(search_sql)
        args.filter_bindings = {**args.filter_bindings, **search_bindings}
    else:
        args.table2, _ = sql_utils.search_filter(args, m_columns, table_prefix="m2.")
    args.table, _ = sql_utils.search_filter(args, m_columns, table_prefix="m1.")

    return args


def get_music_duplicates(args) -> list[dict]:
    m_columns = db_utils.columns(args, "media")

    query = f"""
    SELECT
        m1.path keep_path
        -- , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) num_slash
        -- , length(m1.path)-length(REPLACE(m1.path, '.', '')) num_dot
        -- , length(m1.path) len_p
        , m2.path duplicate_path
        , m2.size duplicate_size
    FROM
        {args.table} m1
    JOIN {args.table2} m2 on 1=1
        and m2.path != m1.path
        and ABS(m1.duration - m2.duration) <= 8
        and m1.title = m2.title
        {"and m1.artist = m2.artist" if 'artist' in m_columns else ''}
        {"and m1.album = m2.album" if 'album' in m_columns else ''}
    WHERE 1=1
        and coalesce(m1.time_deleted,0) = 0 and coalesce(m2.time_deleted,0) = 0
        and m1.title != ''
        {"and m1.artist != ''" if 'artist' in m_columns else ''}
        {"and m1.album != ''" if 'album' in m_columns else ''}
        {" ".join(args.filter_sql)}
    ORDER BY 1=1
        {', m1.audio_count > 0 DESC' if 'audio_count' in m_columns else ''}
        {', ' + args.sort.replace('m.', 'm1.') if args.sort else ''}
        {', m1.video_count > 0 DESC' if 'video_count' in m_columns else ''}
        {', m1.subtitle_count > 0 DESC' if 'subtitle_count' in m_columns else ''}
        {', m1.uploader IS NOT NULL DESC' if 'uploader' in m_columns else ''}
        , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) DESC
        , length(m1.path)-length(REPLACE(m1.path, '.', ''))
        , length(m1.path)
        , m1.size DESC
        , m1.time_modified DESC
        , m1.time_created DESC
        , m1.duration DESC
        , m1.path DESC
    """

    media = list(args.db.query(query, args.filter_bindings))

    return media


def get_id_duplicates(args) -> list[dict]:
    m_columns = db_utils.columns(args, "media")

    query = f"""
    SELECT
        m1.path keep_path
        -- , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) num_slash
        -- , length(m1.path)-length(REPLACE(m1.path, '.', '')) num_dot
        -- , length(m1.path) len_p
        , m2.path duplicate_path
        , m2.size duplicate_size
    FROM
        {args.table} m1
    JOIN {args.table2} m2 on 1=1
        and m1.extractor_id = m2.extractor_id
        and ABS(m1.duration - m2.duration) <= 8
        and m2.path != m1.path
    WHERE 1=1
        and coalesce(m1.time_deleted,0) = 0 and coalesce(m2.time_deleted,0) = 0
        and m1.extractor_id != ''
        {" ".join(args.filter_sql)}
    ORDER BY 1=1
        {', m1.video_count > 0 DESC' if 'video_count' in m_columns else ''}
        {', m1.audio_count > 0 DESC' if 'audio_count' in m_columns else ''}
        {', ' + args.sort.replace('m.', 'm1.') if args.sort else ''}
        {', m1.subtitle_count > 0 DESC' if 'subtitle_count' in m_columns else ''}
        {', m1.audio_count DESC' if 'audio_count' in m_columns else ''}
        , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) DESC
        , length(m1.path)-length(REPLACE(m1.path, '.', ''))
        , length(m1.path)
        , m1.size DESC
        , m1.time_modified DESC
        , m1.time_created DESC
        , m1.duration DESC
        , m1.path DESC
    """

    media = list(args.db.query(query, args.filter_bindings))

    return media


def get_title_duplicates(args) -> list[dict]:
    m_columns = db_utils.columns(args, "media")

    query = f"""
    SELECT
        m1.path keep_path
        -- , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) num_slash
        -- , length(m1.path)-length(REPLACE(m1.path, '.', '')) num_dot
        -- , length(m1.path) len_p
        , m2.path duplicate_path
        , m2.size duplicate_size
    FROM
        {args.table} m1
    JOIN {args.table2} m2 on 1=1
        and m2.path != m1.path
        and ABS(m1.duration - m2.duration) <= 8
    WHERE 1=1
        and coalesce(m1.time_deleted,0) = 0 and coalesce(m2.time_deleted,0) = 0
        and m1.title != '' and m1.title = m2.title
        {" ".join(args.filter_sql)}
    ORDER BY 1=1
        {', m1.video_count > 0 DESC' if 'video_count' in m_columns else ''}
        {', m1.audio_count > 0 DESC' if 'audio_count' in m_columns else ''}
        {', ' + args.sort.replace('m.', 'm1.') if args.sort else ''}
        {', m1.subtitle_count > 0 DESC' if 'subtitle_count' in m_columns else ''}
        {', m1.audio_count DESC' if 'audio_count' in m_columns else ''}
        {', m1.uploader IS NOT NULL DESC' if 'uploader' in m_columns else ''}
        , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) DESC
        , length(m1.path)-length(REPLACE(m1.path, '.', ''))
        , length(m1.path)
        , m1.size DESC
        , m1.time_modified DESC
        , m1.time_created DESC
        , m1.duration DESC
        , m1.path DESC
    """

    media = list(args.db.query(query, args.filter_bindings))

    return media


def get_duration_duplicates(args) -> list[dict]:
    m_columns = db_utils.columns(args, "media")

    query = f"""
    SELECT
        m1.path keep_path
        -- , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) num_slash
        -- , length(m1.path)-length(REPLACE(m1.path, '.', '')) num_dot
        -- , length(m1.path) len_p
        , m2.path duplicate_path
        , m2.size duplicate_size
    FROM
        {args.table} m1
    JOIN {args.table2} m2 on 1=1
        and m2.path != m1.path
        and ABS(m1.duration - m2.duration) <= 8
    WHERE 1=1
        and coalesce(m1.time_deleted,0) = 0 and coalesce(m2.time_deleted,0) = 0
        and m1.duration = m2.duration
        {" ".join(args.filter_sql)}
    ORDER BY 1=1
        {', m1.video_count > 0 DESC' if 'video_count' in m_columns else ''}
        {', m1.audio_count > 0 DESC' if 'audio_count' in m_columns else ''}
        {', ' + args.sort.replace('m.', 'm1.') if args.sort else ''}
        {', m1.subtitle_count > 0 DESC' if 'subtitle_count' in m_columns else ''}
        {', m1.audio_count DESC' if 'audio_count' in m_columns else ''}
        {', m1.uploader IS NOT NULL DESC' if 'uploader' in m_columns else ''}
        , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) DESC
        , length(m1.path)-length(REPLACE(m1.path, '.', ''))
        , length(m1.path)
        , m1.size DESC
        , m1.time_modified DESC
        , m1.time_created DESC
        , m1.duration DESC
        , m1.path DESC
    """

    media = list(args.db.query(query, args.filter_bindings))

    return media


def get_fs_duplicates(args) -> list[dict]:
    m_columns = db_utils.columns(args, "media")

    query = f"""
    SELECT
        path
        , size
        {', hash' if 'hash' in m_columns else ''}
    FROM
        {args.table} m1
    WHERE 1=1
        and coalesce(m1.time_deleted,0) = 0
        and m1.size > 0
        {"and type != 'directory'" if 'type' in m_columns else ''}
        {" ".join(args.filter_sql)}
    ORDER BY 1=1
        , length(m1.path)-length(REPLACE(m1.path, '{os.sep}', '')) DESC
        , length(m1.path)-length(REPLACE(m1.path, '.', ''))
        , length(m1.path)
        , m1.size DESC
        , m1.time_modified DESC
        , m1.time_created DESC
        , m1.path DESC
    """
    media = list(args.db.query(query, args.filter_bindings))

    size_groups = defaultdict(list)
    for m in media:
        size_groups[m["size"]].append(m)
    size_groups = [l for l in size_groups.values() if len(l) > 1]

    size_paths = {d["path"] for g in size_groups for d in g}
    media = [d for d in media if d["path"] in size_paths]
    log.info(
        "Got %s size duplicates (%s groups). Doing sample-hash comparison...",
        len(size_paths),
        len(size_groups),
    )

    path_media_map = {d["path"]: d for d in media}

    need_sample_hash_paths = [d["path"] for d in media if not d.get("hash") and d["path"] is not None]
    if need_sample_hash_paths:
        with ThreadPoolExecutor(max_workers=20) as pool:
            hash_results = list(pool.map(sample_hash.sample_hash_file, need_sample_hash_paths))

        for path, file_hash in zip(need_sample_hash_paths, hash_results, strict=True):
            if file_hash is None:
                del path_media_map[path]
            else:
                path_media_map[path]["hash"] = file_hash
                args.db["media"].upsert(path_media_map[path], pk=["path"], alter=True)  # save sample-hash back to db
        media = [
            path_media_map[d["path"]] for d in media if d["path"] in path_media_map
        ]  # replace media with path_media_map in original order (args.sort)

    sample_hash_groups = defaultdict(set)
    for m in media:
        sample_hash_groups[m["hash"]].add(m["path"])
    sample_hash_groups = [l for l in sample_hash_groups.values() if len(l) > 1]

    sample_hash_paths = set().union(*sample_hash_groups)
    log.info(
        "Got %s sample-hash duplicates (%s groups). Doing full hash comparison...",
        len(sample_hash_paths),
        len(sample_hash_groups),
    )

    with ThreadPoolExecutor(max_workers=20) as pool:
        path_hash_map = dict(
            zip(sample_hash_paths, pool.map(sample_compare.full_hash_file, sample_hash_paths), strict=True)
        )

    full_hash_groups = defaultdict(list)
    for path, file_hash in path_hash_map.items():
        if file_hash is not None:
            full_hash_groups[file_hash].append(path)
    full_hash_groups = [l for l in full_hash_groups.values() if len(l) > 1]

    dup_media = []
    for hash_group_paths in full_hash_groups:
        paths = [d["path"] for d in media if d["path"] in hash_group_paths]  # get the correct order from media
        keep_path = paths[0]
        dup_media.extend(
            {"keep_path": keep_path, "duplicate_path": p, "duplicate_size": path_media_map[keep_path]["size"]}
            for p in paths[1:]
        )

    # TODO: update false-positive sample-hash matches? probably no because then future sample-hash duplicates won't match

    return dup_media


def filter_split_files(paths):
    pattern = r"\.\d{3,5}\."
    return filter(lambda x: not re.search(pattern, x), paths)


def dedupe_media() -> None:
    args = parse_args()

    if args.profile == DBType.audio:
        duplicates = get_music_duplicates(args)
    elif args.profile == "extractor_id":
        duplicates = get_id_duplicates(args)
    elif args.profile == "title":
        duplicates = get_title_duplicates(args)
    elif args.profile == "duration":
        duplicates = get_duration_duplicates(args)
    elif args.profile == DBType.filesystem:
        duplicates = get_fs_duplicates(args)
    elif args.profile == DBType.image:
        print(
            """
        You should use `czkawka` or `cbird` instead:

            $ czkawka image -d (pwd) > dupes.txt
            $ wget https://raw.githubusercontent.com/chapmanjacobd/computer/main/bin/czkawka_output_dupdelete.py
            $ python czkawka_output_dupdelete.py dupes.txt

            $ cbird -i.algos 1 -update
            $ cbird -dups -select-result -sort-rev resolution -chop -nuke  # exact duplicates
            $ cbird -p.dht 1 -similar -select-result -sort-rev resolution -chop -nuke  # similar photos
        """,
        )
        return
    else:
        raise argparse.ArgumentError(args.profile, "Profile not set. Use --audio OR --id OR --title OR --filesystem")

    deletion_candidates = []
    deletion_paths = []
    for d in duplicates:
        if args.dirname and (
            difflib.SequenceMatcher(
                None,
                path_utils.parent(d["keep_path"]),
                path_utils.parent(d["duplicate_path"]),
            ).ratio()
            < args.min_similarity_ratio
        ):
            continue

        if args.basename and (
            difflib.SequenceMatcher(
                None,
                path_utils.basename(d["keep_path"]),
                path_utils.basename(d["duplicate_path"]),
            ).ratio()
            < args.min_similarity_ratio
        ):
            continue

        if any(
            [
                d["keep_path"] in deletion_paths or d["duplicate_path"] in deletion_paths,
                d["keep_path"] == d["duplicate_path"],
            ],
        ):
            continue

        if not consts.PYTEST_RUNNING and not Path(d["keep_path"]).resolve().exists():
            continue

        deletion_paths.append(d["duplicate_path"])
        deletion_candidates.append(d)
    duplicates = deletion_candidates

    if not duplicates:
        log.error("No duplicates found")
        raise SystemExit(1)
    if consts.PYTEST_RUNNING:
        for d in duplicates:
            db_media.mark_media_deleted(args, d["duplicate_path"])
        return

    tbl = deepcopy(duplicates)
    tbl = tbl[: int(args.limit)]
    media_printer.media_printer(args, tbl, units="duplicates", media_len=len(duplicates))

    try:
        import pandas as pd

        csv_path = tempfile.mktemp(".csv")
        pd.DataFrame(duplicates).to_csv(csv_path, index=False)
        print("Full list saved to:", csv_path)
    except ModuleNotFoundError:
        log.info("Skipping CSV export because pandas is not installed")

    duplicates_size = sum(filter(None, [d["duplicate_size"] for d in duplicates]))
    print(f"Approx. space savings: {strings.file_size(duplicates_size // 2)}")

    if duplicates and (args.force or devices.confirm("Delete duplicates?")):  # type: ignore
        log.info("Deleting...")
        for d in duplicates:
            path = d["duplicate_path"]
            if path.startswith("http"):
                pass
            elif args.dedupe_cmd:
                processes.cmd(
                    *shlex.split(args.dedupe_cmd), d["duplicate_path"], d["keep_path"]
                )  # follows rmlint interface
            else:
                file_utils.trash(args, path, detach=False)
            db_media.mark_media_deleted(args, path)


if __name__ == "__main__":
    dedupe_media()
