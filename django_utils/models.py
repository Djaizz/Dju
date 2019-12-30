from abc import \
    ABC, ABCMeta, \
    abstractmethod, \
    abstractclassmethod, abstractstaticmethod, abstractproperty

from django.db.models.base import Model

from django.db.models.fields import \
    AutoField, BigAutoField, SmallAutoField, UUIDField, \
    DateField, DateTimeField

from django.db.models.manager import Manager

from django.contrib.postgres.fields import \
    CICharField, \
    JSONField

from django.core.serializers.json import DjangoJSONEncoder

# from model_utils.models import TimeStampedModel

from uuid import uuid4

from . import MAX_CHAR_FLD_LEN, upper_case


# https://www.postgresql.org/docs/devel/sql-syntax-lexical.html >> Identifiers and Key Words
PGSQL_IDENTIFIER_MAX_LEN = 63


# Field options: https://docs.djangoproject.com/en/dev/ref/models/fields/#common-model-field-options
# - null: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.null
# - blank: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.blank
# - choices: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.choices
#   - Enumeration types: https://docs.djangoproject.com/en/dev/ref/models/fields/#enumeration-types
# - db_column: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.db_column
# - db_index: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.db_index
# - db_tablespace: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.db_tablespace
# - default: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.default
# - editable: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.editable
# - error_messages: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.error_messages
# - help_text: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.help_text
# - primary_key: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.primary_key
# - unique: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.unique
# - unique_for_date: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.unique_for_date
# - unique_for_month: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.unique_for_month
# - unique_for_year: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.unique_for_year
# - verbose_name: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.verbose_name
# - validators: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.validators


# Model attribute interpolation:
# - app_label: e.g., 'App_Label'
# - class: cls.__name__.lower(), e.g., 'modelclass'
# - model_name: cls._meta.model_name.lower(), e.g., 'modelclass'
# - object_name: e.g., 'ModelClass'


class _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC(Model):
    # https://docs.djangoproject.com/en/dev/ref/models/class/#objects
    # https://docs.djangoproject.com/en/dev/ref/models/class/#django.db.models.Model.objects
    objects = Manager()

    # https://docs.djangoproject.com/en/dev/ref/models/options/#model-meta-options
    class Meta:
        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.abstract
        abstract = True

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.app_label
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        # *** so must explicitly set this in non-abstract sub-classes ***
        # app_label = '%(app_label)s'

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.base_manager_name
        base_manager_name = 'objects'

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.db_table
        # https://docs.djangoproject.com/en/dev/ref/models/options/#table-names
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        # *** so must explicitly set this in non-abstract sub-classes ***
        db_table = '"%(app_label)s_%(object_name)s"'   # note: except for Oracle, quotes have no effect

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.db_tablespace
        db_tablespace = None

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.default_manager_name
        default_manager_name = 'objects'

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.default_related_name
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        # *** so must explicitly set this in non-abstract sub-classes ***
        default_related_name = '%(model_name)ss'

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.get_latest_by
        get_latest_by = None

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.managed
        managed = True

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.order_with_respect_to
        order_with_respect_to = None

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.ordering
        ordering = None

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.permissions
        permissions = ()

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.default_permissions
        default_permissions = \
            'add', \
            'change', \
            'delete', \
            'view'

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.proxy
        proxy = False

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.required_db_features
        required_db_features = ()

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.required_db_vendor
        required_db_vendor = 'postgresql'

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.select_on_save
        select_on_save = False

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.indexes
        indexes = ()

        # (MAY BE DEPRECATED)
        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.unique_together
        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.index_together

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.constraints
        constraints = ()

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.verbose_name
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        verbose_name = '%(object_name)s'

        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.verbose_name_plural
        # TODO: *** Django 2 Cannot Interpolate '%(app_label)', etc. ***
        # *** so must explicitly set this in non-abstract sub-classes ***
        verbose_name_plural = '%(object_name)ss'

        # READ-ONLY:
        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.label
        # https://docs.djangoproject.com/en/dev/ref/models/options/#django.db.models.Options.label_lower


class _ModelWithIntPKMixInABC(Model):
    # https://docs.djangoproject.com/en/dev/topics/db/models/#automatic-primary-key-fields
    id = AutoField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.AutoField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=False,
            # error_messages=None,
            help_text='Integer Primary Key',
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Integer Primary Key',
            # validators=()   # must be iterable
        )

    class Meta:
        abstract = True


class _ModelWithBigIntPKMixInABC(Model):
    id = BigAutoField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BigAutoField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=False,
            # error_messages=None,
            help_text='Big Integer Primary Key',
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Big Integer Primary Key',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithSmallIntPKMixInABC(Model):
    id = SmallAutoField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.SmallAutoField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=False,
            # error_messages=None,
            help_text='Small Integer Primary Key',
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Small Integer Primary Key',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithUUIDPKMixInABC(Model):
    uuid = UUIDField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.UUIDField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=uuid4,
            editable=False,
            # error_messages=None,
            help_text='UUID Primary Key',
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='UUID Primary Key',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithCreatedAndUpdatedMixInABC(Model):
    created = \
        DateTimeField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField
            null=False,
            blank=True,   # auto_now_add=True -> blank=True
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            # default=None,   # auto_now_add, auto_now and default are mutually exclusive
            editable=False,   # auto_now_add=True -> editable=False
            error_messages=None,
            help_text='Created at',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Created at',
            # validators=(),

            auto_now_add=True,
            auto_now=False)

    updated = \
        DateTimeField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField
            null=False,
            blank=True,   # auto_now=True -> blank=True
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            # default=None,   # auto_now_add, auto_now and default are mutually exclusive
            editable=False,   # auto_now=True -> editable=False
            error_messages=None,
            help_text='Last Updated at',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Last Updated at',
            # validators=(),

            auto_now_add=False,
            auto_now=True)

    class Meta:
        abstract = True


class _ModelWithNullableDateMixInABC(Model):
    date = \
        DateField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages=None,
            help_text='Date',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Date',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta:
        abstract = True


class _ModelWithNonNullableDateMixInABC(Model):
    date = \
        DateField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages=None,
            help_text='Date',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Date',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta:
        abstract = True


class _ModelWithAutoCompleteSearchFieldsMixInABC:
    @staticmethod
    @abstractmethod
    def search_fields():
        return NotImplementedError

    @classmethod
    def autocomplete_search_fields(cls):
        return ['{}__icontains'.format(search_field)
                for search_field in cls.search_fields()]


class _ModelWithPostgreSQLCICharPKAndJSONValueMixInABC(_ModelWithAutoCompleteSearchFieldsMixInABC, Model):
    key = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages=None,
            help_text='KEY',
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='KEY',
            # validators=(),
            
            max_length=MAX_CHAR_FLD_LEN)

    value = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages=None,
            help_text='Value (JSON)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Value',
            # validators=(),
            
            encoder=DjangoJSONEncoder
                # https://docs.djangoproject.com/en/dev/topics/serialization/#django.core.serializers.json.DjangoJSONEncoder
        )

    class Meta:
        abstract = True

        ordering = 'key',

    @staticmethod
    def search_fields():
        return 'key', \
               'value'

    def __str__(self):
        cls = type(self)

        return '{}.{} {} = {}'.format(
                cls.__module__,
                cls.__qualname__,
                self.key,
                self.value)

    def save(self, *args, **kwargs):
        self.key = upper_case(self.key)
        assert self.key

        super().save(*args, **kwargs)


class _EnvVarABC(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithPostgreSQLCICharPKAndJSONValueMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithPostgreSQLCICharPKAndJSONValueMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        abstract = True

        default_related_name = 'env_vars'
        
        verbose_name = 'Environment Variable'
        verbose_name_plural = 'Environment Variables'
