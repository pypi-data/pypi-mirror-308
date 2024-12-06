# TODO check if this is used anywhere? refactor by removing!
from typing import Any

import ray

__all__ = ("new_instance_local_or_remote",)

_actor_class_cache: dict[type, ray.actor.ActorClass] = {}


def new_instance_local_or_remote(
    cls: type,
    args: list[Any] = None,
    kwargs: dict[str, Any] = None,
    remote: bool = False,
) -> Any | ray.actor.ActorHandle:
    """Dynamically create a local instance or a [ray] remote actor based on the given class.

    Args:
        cls ([Type]): The class to instantiate.
        args ([List[Any]], optional): Positional arguments to pass to the class constructor.
        kwargs ([Dict[str, Any]], optional): Keyword arguments to pass to the class constructor.
        remote ([bool], optional): Whether to create a Ray remote actor. Defaults to False.

    Returns:
        [Union[Any, ray.actor.ActorHandle]]: An instance of `cls` or a Ray remote actor handle for `cls`.
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    if remote:
        if cls not in _actor_class_cache:
            _actor_class_cache[cls] = ray.remote(cls)
        ActorClass = _actor_class_cache[cls]
        return ActorClass.remote(*args, **kwargs)
    else:
        return cls(*args, **kwargs)
