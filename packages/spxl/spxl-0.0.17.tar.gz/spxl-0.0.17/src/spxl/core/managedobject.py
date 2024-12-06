#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
from uuid import UUID, uuid4
from .baseclass import BaseClass
from .weakedreference import WeakedReference


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = "ManagedObject")


#--------------------------------------------------------------------------------
# 관리된 오브젝트.
#--------------------------------------------------------------------------------
class ManagedObject(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__identifier: str


	#--------------------------------------------------------------------------------
	# 인스턴스 고유 식별자.
	#--------------------------------------------------------------------------------
	@property
	def Identifier(self) -> str:
		return self.__identifier


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, *arguments, **keywordArguments):
		try:
			base = super()
			base.__init__()

			unique: UUID = uuid4()
			# self.__identifier = str(unique) # 550e8400-e29b-41d4-a716-446655440000
			self.__identifier = str(unique.hex) # 550e8400e29b41d4a716446655440000
			self.OnCreate(*arguments, **keywordArguments)
		except Exception as exception:
			raise


	#--------------------------------------------------------------------------------
	# 파괴됨.
	#--------------------------------------------------------------------------------
	def __del__(self) -> None:
		try:
			self.OnDestroy()

			# base = super()
			# base.__del__()
		except Exception as exception:
			raise


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def OnCreate(self, *arguments, **keywordArguments) -> None:
		return


	#--------------------------------------------------------------------------------
	# 파괴됨.
	#--------------------------------------------------------------------------------
	def OnDestroy(self) -> None:
		return
	

	#--------------------------------------------------------------------------------
	# 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Instantiate(referenceType: Type[T], *arguments, **keywordArguments) -> WeakedReference[T]:
		obj: T = referenceType(*arguments, **keywordArguments)
		ManagedObjectCollection.Register(obj.Identifier, obj)
		weakedReference: WeakedReference[T] = ManagedObjectCollection.FindWeakedReference(referenceType, obj.Identifier)
		return weakedReference


	#--------------------------------------------------------------------------------
	# 검색.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Find(identifier: str) -> ManagedObject:
		obj: ManagedObject = ManagedObjectCollection.Find(identifier)
		return obj
	
	#--------------------------------------------------------------------------------
	# 검색.
	#--------------------------------------------------------------------------------
	@staticmethod
	def FindObject(identifier: str) -> WeakedReference[ManagedObject]:
		weakedReference: WeakedReference[ManagedObject] = ManagedObject.FindObjectOfType(ManagedObject, identifier)
		return weakedReference
	

	#--------------------------------------------------------------------------------
	# 검색.
	#--------------------------------------------------------------------------------
	@staticmethod
	def FindObjectOfType(referenceType: Type[T], identifier: str) -> WeakedReference[T]:
		weakedReference: WeakedReference[T] = ManagedObjectCollection.FindWeakedReference(referenceType, identifier)
		return weakedReference
	

	#--------------------------------------------------------------------------------
	# 파괴.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Destroy(obj: ManagedObject) -> None:
		ManagedObjectCollection.Unregister(obj)


#--------------------------------------------------------------------------------
# 매니지드 오브젝트 컬렉션. (내부 관리용)
#--------------------------------------------------------------------------------
class ManagedObjectCollection(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Objects: dict[str, ManagedObject] = dict()


	#--------------------------------------------------------------------------------
	# 갯수 프로퍼티.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Count() -> int:
		return len(ManagedObjectCollection.Objects)


	#--------------------------------------------------------------------------------
	# 전체 제거.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Cleanup() -> bool:
		if not ManagedObjectCollection.Objects:
			return False		
		ManagedObjectCollection.Objects.clear()
		return True	
	

	#--------------------------------------------------------------------------------
	# 추가.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Register(obj: ManagedObject) -> bool:
		if not obj:
			return False		
		if obj.Identifier in ManagedObjectCollection.Objects:
			return False
		ManagedObjectCollection.Objects[obj.Identifier] = obj
		return True	


	#--------------------------------------------------------------------------------
	# 제거.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Unregister(identifier: str) -> bool:
		if identifier not in ManagedObjectCollection.Objects:
			return False		
		del ManagedObjectCollection.Objects[identifier]
		return True


	#--------------------------------------------------------------------------------
	# 포함 여부.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Contains(identifier: str) -> bool:
		if identifier not in ManagedObjectCollection.Objects:
			return False
		return True
	

	#--------------------------------------------------------------------------------
	# 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Find(identifier: str) -> ManagedObject:
		if identifier not in ManagedObjectCollection.Objects:
			return None
		obj: ManagedObject = ManagedObjectCollection.Objects[identifier]
		return obj


	#--------------------------------------------------------------------------------
	# 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def FindWeakedReference(referenceType: Type[T], identifier: str) -> Optional[WeakedReference[T]]:
		obj: ManagedObject = ManagedObjectCollection.Find(identifier)
		if not obj:
			return None
		if not isinstance(obj, referenceType):
			return None		
		weakedReference: WeakedReference[T] = WeakedReference[T](obj)
		return weakedReference