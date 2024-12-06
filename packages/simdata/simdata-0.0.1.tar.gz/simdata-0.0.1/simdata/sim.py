from typing import Any, Optional, Literal
Int = int
Float = float

from pydantic import BaseModel, ConfigDict
from numpy.random import normal as r_normal
from random import choices as r_choices

class simd_func (BaseModel):
    def simulate(self):
        raise NotImplementedError()
    
class simd (BaseModel):
    model_config = ConfigDict(extra="allow")

    def __init__(self, **data):
        super().__init__(**data)
        simd_funcs = {f.__name__:f for f in simd_func.__subclasses__()}
        for field, value in self.__pydantic_extra__.items():
            if isinstance(value, dict) and "func" in value:
                func_type = value["func"]
                func_class = simd_funcs.get(func_type)
                if func_class: 
                    setattr(self, field, func_class(**value))

    def simulate(self):
        return { 
            field: getattr(self, field).simulate()
            for field in sorted(self.model_fields_set)
        }

class float (simd_func):
    func:Literal["float"]="float"
    mean:Float
    std:Float
    min:Float
    max:Float
    precision:Optional[Int]=3

    def simulate(self):
        value = r_normal(self.mean, self.std)
        while value < self.min or value > self.max:
            value = r_normal(self.mean, self.std)
        return round(value, self.precision)
    
class int (float):
    func:Literal['int']="int"

    def simulate(self):
        return Int(super().simulate())
    
class choice (simd_func):
    func:Literal["choice"]="choice"
    choices:list[Any]
    weights:list[Int|Float]
    n:Optional[Int]=1

    def simulate(self):
        choice = r_choices(self.choices, weights=self.weights, k=self.n)
        if self.n == 1: return choice[0]
        return choice

class literal (simd_func):
    func:Literal["literal"]="literal"
    value:Any

    def simulate(self):
        return self.value