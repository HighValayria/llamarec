"""STEP 2/3 实现：随机候选采样。

当前 MVP 的 N 任务负候选只表示“不是本样本真实 next item 的候选 item”。
不要在这里按用户正反馈序列过滤，也不要把负候选解释成“不喜欢的电影”。
"""

from collections.abc import Iterable
from random import Random


def build_negative_pool(
    all_movie_ids: Iterable[str],
    target_movie_id: str,
    extra_excluded_movie_ids: Iterable[str] | None = None,
) -> list[str]:
    """返回某个 N 样本可用的随机负候选池。"""

    # N 的负候选只排除当前 ground truth；不按用户偏好过滤。
    excluded = {str(target_movie_id)}
    if extra_excluded_movie_ids is not None:
        excluded.update(str(movie_id) for movie_id in extra_excluded_movie_ids)

    return sorted(
        str(movie_id)
        for movie_id in set(all_movie_ids)
        if str(movie_id) not in excluded
    )


def sample_random_negatives(pool: Iterable[str], n: int, rng: Random) -> list[str]:
    """从候选池中无放回采样，随机性完全由外部传入的 rng 控制。"""

    pool_list = list(pool)
    if len(pool_list) < n:
        raise ValueError(f"负候选池大小不足: need={n}, available={len(pool_list)}")
    return rng.sample(pool_list, n)


def sample_random_negatives_from_all_movies(
    all_movie_ids: list[str],
    target_movie_id: str,
    n: int,
    rng: Random,
    extra_excluded_movie_ids: Iterable[str] | None = None,
) -> list[str]:
    """从全电影列表中高效采样负候选。

    语义等同于先构造 ``all_movies_minus_current_ground_truth_item`` 再采样，
    但不会在 32M 的每个样本上重复复制完整电影池。
    """

    excluded = {str(target_movie_id)}
    if extra_excluded_movie_ids is not None:
        excluded.update(str(movie_id) for movie_id in extra_excluded_movie_ids)

    # all_movie_ids 来自 movie metadata 的唯一 movie_id 列表；这里不为每个样本重建 set。
    available = len(all_movie_ids) - len(excluded)
    if available < n:
        raise ValueError(f"负候选池大小不足: need={n}, available={available}")

    negatives = []
    seen = set()
    while len(negatives) < n:
        movie_id = str(rng.choice(all_movie_ids))
        if movie_id in excluded or movie_id in seen:
            continue
        negatives.append(movie_id)
        seen.add(movie_id)
    return negatives
