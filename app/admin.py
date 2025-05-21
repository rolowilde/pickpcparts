from django.contrib import admin

from .models import *

models = [Manufacturer, Socket, Processor, ProcessorCooler, GraphicsCard, CaseFormFactor, Case, CaseFan, Motherboard,
          Memory, StorageFormFactor, StorageInterface, Storage, PowerSupply, Build, MemoryType]

for model in models:
    admin.site.register(model)
