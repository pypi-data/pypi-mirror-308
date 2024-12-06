# managers/polymorphic.py
try:
    from polymorphic.managers import PolymorphicManager
    from .polymorphic_querysets import APolymorphicQuerySet


    class APolymorphicManager(PolymorphicManager.from_queryset(APolymorphicQuerySet)):
        pass
except ImportError:
    pass
