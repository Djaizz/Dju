from django.db import migrations

from django.contrib.postgres.operations import \
        CreateExtension, \
        BtreeGinExtension, BtreeGistExtension, \
        CITextExtension, \
        CryptoExtension, \
        HStoreExtension, \
        TrigramExtension, \
        UnaccentExtension


class Migration(migrations.Migration):
    initial = True

    dependencies = ()

    operations = \
        BtreeGinExtension(), BtreeGistExtension(), \
        CITextExtension(), \
        CryptoExtension(), \
        HStoreExtension(), \
        TrigramExtension(), \
        UnaccentExtension()
