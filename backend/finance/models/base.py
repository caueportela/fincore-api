from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """Permite fazer soft delete e restore em massa via QuerySet."""
    
    def delete(self):
        return super().update(deleted_at=timezone.now(), updated_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return super().update(deleted_at=None, updated_at=timezone.now())


class SoftDeleteManager(models.Manager):
    """Manager que oculta registros excluídos por padrão."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=False)


class BaseModel(models.Model):
    """Modelo abstrato base com auditoria e soft delete."""

    created_at = models.DateTimeField(
        "Data de criação",
        auto_now_add=True,
        help_text="Data e hora de criação do registro",
    )
    updated_at = models.DateTimeField(
        "Data de atualização",
        auto_now=True,
        help_text="Data e hora da última atualização",
    )
    deleted_at = models.DateTimeField(
        "Data de exclusão",
        null=True,
        blank=True,
        help_text="Data em que o registro foi excluído (soft delete)",
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        """Marca a instância individual como excluída."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def restore(self):
        """Restaura a instância individual."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])

    @property
    def is_deleted(self):
        return self.deleted_at is not None