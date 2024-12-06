#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import Object
from .target import Target


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
LINEFEED: str = "\n"
READTEXT: str = "rt"
READBINARY: str = "rb"
WRITETEXT: str = "wt"
WRITEBINARY: str = "wb"
UTF8: str = "utf-8"
DATAJSONFILENAME: str = "data.json"
JNKFILEEXTENSION: str = ".jnk"
TAB: str = "\t"


#------------------------------------------------------------------------
# 작업 공정.
#------------------------------------------------------------------------
class Task(Object):
	#------------------------------------------------------------------------
	# 멤버 변수 목록.
	#------------------------------------------------------------------------


	#------------------------------------------------------------------------
	# 생성됨.
	#------------------------------------------------------------------------
	def __init__(self) -> None:
		base = super()
		base.__init__()

		self.OnCreate()


	#------------------------------------------------------------------------
	# 파괴됨.
	#------------------------------------------------------------------------
	def __del__(self) -> None:
		try:
			self.OnDestroy()
		except Exception as exception:
			raise


	#------------------------------------------------------------------------
	# 생성됨.
	#------------------------------------------------------------------------
	def OnCreate(self) -> None:
		return
		

	#------------------------------------------------------------------------
	# 파괴됨.
	#------------------------------------------------------------------------
	def OnDestroy(self) -> None:
		return


	#------------------------------------------------------------------------
	# 시작됨.
	#------------------------------------------------------------------------
	def OnStart(self, target: Target) -> None:
		return


	#------------------------------------------------------------------------
	# 종료됨.
	#------------------------------------------------------------------------
	def OnComplete(self, target: Target, resultCode: int) -> None:
		return


	#------------------------------------------------------------------------
	# 실행됨.
	#------------------------------------------------------------------------
	def OnExecute(self, target: Target, *arguments, **keywordArguments) -> int:
		return 0
	

	#------------------------------------------------------------------------
	# 실행.
	#------------------------------------------------------------------------
	def Execute(self, target: Target, *arguments, **keywordArguments) -> int:
		try:
			self.OnStart(target)
			resultCode = self.OnExecute(target, *arguments, **keywordArguments)
			self.OnComplete(target, resultCode)
			return resultCode
		except Exception as exception:
			raise
