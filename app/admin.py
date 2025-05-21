from django.contrib import admin

from .models import *

models = [Socket, Processor, ProcessorCooler, GraphicsCard, CaseFormFactor, Case, CaseFan, Motherboard, Memory,
          StorageFormFactor, StorageInterface, Storage, PowerSupply, Build]

for model in models:
    admin.site.register(model)
