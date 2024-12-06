"""事件处理器模块"""

import logging
from typing import Any, Optional, Union, Dict
from vxsched.event import VXEvent, VXTrigger
from vxsched import vxsched, VXScheduler


class VXSubscriber:
    """订阅器"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __call__(self) -> VXEvent:
        raise NotImplementedError


class VXPublisher:
    """发布器"""

    def __init__(self, *, target_scheduler: Optional[VXScheduler] = None) -> None:
        self._sched = target_scheduler or vxsched

    def __call__(
        self,
        event: Union[str, VXEvent],
        *,
        trigger: Optional[VXTrigger] = None,
        data: Optional[Dict[str, Any]] = None,
        channel: str = "default",
        priority: int = 10,
        reply_to: str = "",
    ) -> None:
        if isinstance(event, str):
            event = VXEvent(
                type=event,
                data=data or {},
                priority=priority,
                channel=channel,
                reply_to=reply_to,
            )
        # self._queue.put(event, trigger=trigger)
        self._sched.publish(event, trigger=trigger)
        logging.debug(f"Put event: {event} with trigger: {trigger} into queue.")


if __name__ == "__main__":
    pass
