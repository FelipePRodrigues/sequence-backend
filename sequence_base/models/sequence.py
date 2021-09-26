from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _


class Sequence(models.Model):
    letters = ArrayField(models.CharField(
        max_length=255), verbose_name='Letters', default=[])
    letters_hash = models.CharField(
        verbose_name='Letters Hash', max_length=255)
    is_valid = models.BooleanField(verbose_name='Is Valid', default=False)
    creation_date = models.DateTimeField(
        verbose_name='Creation Date', auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['letters_hash'])]
        ordering = ['-id']
        verbose_name = _('Sequence')
        verbose_name_plural = _(u'Sequences')
