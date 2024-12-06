#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import BaseClass


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
BASE: str = "base"


#--------------------------------------------------------------------------------
# 기본 클래스.
#--------------------------------------------------------------------------------
class BaseAgent(Object):
	def OnCreate(self) -> None:
		pass
	def OnDestroy(self) -> None:
		pass