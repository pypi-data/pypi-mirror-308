from pydantic import BaseModel, ConfigDict

from .sim import simd_func

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
