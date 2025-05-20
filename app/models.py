from django.contrib.auth.models import User
from django.db import models


class Component(models.Model):
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Socket(models.Model):
    name = models.CharField(max_length=255)


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


class GraphicsCard(Component):
    memory = models.PositiveIntegerField()
    core_clock = models.PositiveIntegerField()
    boost_clock = models.PositiveIntegerField()
    length = models.PositiveIntegerField()


class CaseFormFactor(models.Model):
    name = models.CharField(max_length=255)


class Case(Component):
    formfactor = models.ForeignKey(CaseFormFactor, on_delete=models.CASCADE)
    external_volume = models.PositiveIntegerField()


class CaseFan(Component):
    size = models.PositiveIntegerField()
    rpm = models.PositiveIntegerField()
    noise_level = models.PositiveIntegerField()
    pwm = models.BooleanField(default=False)


class Motherboard(Component):
    max_memory = models.PositiveIntegerField()
    memory_slots = models.PositiveIntegerField()
    formfactor = models.ForeignKey(CaseFormFactor, on_delete=models.CASCADE)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)


class Memory(Component):
    speed = models.PositiveIntegerField()
    modules = models.PositiveIntegerField()
    first_word_latency = models.PositiveIntegerField()
    cas_latency = models.PositiveIntegerField()


class StorageFormFactor(models.Model):
    name = models.CharField(max_length=255)


class StorageInterface(models.Model):
    name = models.CharField(max_length=255)


class Storage(Component):
    capacity = models.PositiveIntegerField()
    cache = models.PositiveIntegerField()
    form_factor = models.ForeignKey(StorageFormFactor, on_delete=models.CASCADE)
    interface = models.ForeignKey(StorageInterface, on_delete=models.CASCADE)


class PowerSupply(Component):
    MODULARITY = [
        (0, "None"),
        (1, "Semi"),
        (2, "Full"),
    ]

    EFFICIENCY = [
        (0, "None"),
        (1, "Plus"),
        (2, "Bronze"),
        (3, "Silver"),
        (4, "Gold"),
        (5, "Platinum"),
        (6, "Titanium"),
    ]

    formfactor = models.ForeignKey(StorageFormFactor, on_delete=models.CASCADE)
    wattage = models.PositiveIntegerField()
    efficiency = models.CharField(max_length=1, choices=EFFICIENCY)
    modularity = models.CharField(max_length=1, choices=MODULARITY)


class Build(models.Model):
    name = models.TextField()
    notes = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
