import typing

from django.contrib.auth.models import User
from django.db import models


class Lookup(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Manufacturer(Lookup):
    pass


class Component(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.manufacturer} {self.model}"


class Socket(Lookup):
    pass


class Processor(Component):
    core_count = models.PositiveIntegerField()
    core_clock = models.PositiveIntegerField()
    boost_clock = models.PositiveIntegerField()
    tdp = models.PositiveIntegerField()
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)


class ProcessorCooler(Component):
    rpm = models.PositiveIntegerField()
    noise_level = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    socket = models.ManyToManyField(Socket)


class GraphicsCard(Component):
    memory = models.PositiveIntegerField()
    core_clock = models.PositiveIntegerField()
    boost_clock = models.PositiveIntegerField()
    length = models.PositiveIntegerField()


class CaseFormFactor(Lookup):
    pass


class Case(Component):
    formfactor = models.ForeignKey(CaseFormFactor, on_delete=models.CASCADE)
    external_volume = models.PositiveIntegerField()


class CaseFan(Component):
    size = models.PositiveIntegerField()
    rpm = models.PositiveIntegerField()
    noise_level = models.PositiveIntegerField()
    pwm = models.BooleanField(default=False)


class MemoryType(Lookup):
    pass


class Memory(Component):
    capacity_per_module = models.PositiveIntegerField()
    modules = models.PositiveIntegerField()
    speed = models.PositiveIntegerField()
    first_word_latency = models.PositiveIntegerField()
    cas_latency = models.PositiveIntegerField()
    type = models.ForeignKey(MemoryType, on_delete=models.CASCADE)

    @property
    def capacity(self):
        return self.modules * self.capacity_per_module

    def __str__(self):
        return f"{super().__str__()} {self.capacity}GB {self.type}-{self.speed} CL{self.cas_latency}"


class Motherboard(Component):
    max_memory = models.PositiveIntegerField()
    memory_slots = models.PositiveIntegerField()
    supported_memory = models.ManyToManyField(MemoryType)
    formfactor = models.ForeignKey(CaseFormFactor, on_delete=models.CASCADE)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)


class StorageFormFactor(Lookup):
    pass


class StorageInterface(Lookup):
    pass


class Storage(Component):
    capacity = models.PositiveIntegerField()
    cache = models.PositiveIntegerField()
    form_factor = models.ForeignKey(StorageFormFactor, on_delete=models.CASCADE)
    interface = models.ForeignKey(StorageInterface, on_delete=models.CASCADE)

    @property
    def capacity_with_unit(self):
        return f"{int(self.capacity / 1000)}TB" if self.capacity % 1000 == 0 else f"{self.capacity}GB"

    def __str__(self):
        return f"{super().__str__()} {self.capacity_with_unit}"


# noinspection PyTypeChecker
class PowerSupply(Component):
    class Modularity(models.IntegerChoices):
        NONE = 0
        SEMI = 1
        FULL = 2

    class Efficiency(models.IntegerChoices):
        NONE = 0
        PLUS = 1
        BRONZE = 2
        SILVER = 3
        GOLD = 4
        PLATINUM = 5
        TITANIUM = 6

    formfactor = models.ForeignKey(CaseFormFactor, on_delete=models.CASCADE)
    wattage = models.PositiveIntegerField()
    efficiency = models.IntegerField(choices=Efficiency)
    modularity = models.IntegerField(choices=Modularity)


class Build(models.Model):
    name = models.TextField()
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    processor_cooler = models.ForeignKey(ProcessorCooler, on_delete=models.CASCADE)
    graphics_card = models.ForeignKey(GraphicsCard, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    case_fans = models.ManyToManyField(CaseFan, blank=True)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE)
    memory = models.ManyToManyField(Memory)
    storage = models.ManyToManyField(Storage)
    power_supply = models.ForeignKey(PowerSupply, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def total_memory(self):
        memory = 0
        for m in self.memory.all():
            memory += m.capacity
        return memory


# noinspection PyTypeChecker
COMPONENTS: typing.List[Component] = \
    [Processor, ProcessorCooler, GraphicsCard, Case, CaseFan, Motherboard, Memory, Storage, PowerSupply]
# noinspection PyTypeChecker
LOOKUPS: typing.List[Lookup] = [Manufacturer, Socket, CaseFormFactor, StorageFormFactor, StorageInterface, MemoryType]
MODELS: typing.List[models.Model] = COMPONENTS + LOOKUPS
