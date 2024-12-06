import uuid

import pytest
from django.db.models import Q, RestrictedError

from translate.core.settings import BASE_DIR
from translate.service.utils.file_utils import read_json_files, read_po_files


@pytest.fixture
def readiness_provider(provider_to_fixture):
    """Readiness provider fixture."""
    from translate.service.tests.providers import ReadinessCheckProvider

    provider_to_fixture.add_provider(ReadinessCheckProvider)

    yield provider_to_fixture


@pytest.fixture(scope="session")
@pytest.mark.xdist_group(name="group_db")
def language_factory():
    """Language factory fixture."""
    from translate.service.tests.factories import LanguageFactory

    obj = LanguageFactory.create()

    yield obj

    obj.delete()


@pytest.fixture(
    params=[
        "general_accept",
        "1another_one",
        "$my_translation",
        "my msgid " "%$#$@@#534",
    ],
)
@pytest.mark.xdist_group(name="group_db")
def translation_key_factory(request, worker_id):
    """``TranslationKey`` factory fixture."""
    from translate.service.models import TranslationKey as Tk
    from translate.service.tests.factories import TranslationKeyFactory

    obj = TranslationKeyFactory.create(
        snake_name=f"{request.param}_{worker_id}",
        category=Tk.Category.SERVICE,
    )

    yield obj

    obj.delete()


@pytest.fixture(
    params=[
        {
            "keys": [
                {
                    "key": "$my_context_key",
                    "usage_context": "$my_translation context",
                },
                {
                    "key": "and_1another_one",
                    "usage_context": "1another_one context",
                },
            ]
        },
    ],
)
def translation_key_with_context_factory(request):
    """``TranslationKey`` that have usage context inserted factory fixture."""
    from translate.service.models import TranslationKey as Tk
    from translate.service.tests.factories import TranslationKeyFactory

    tks = [
        TranslationKeyFactory.create(
            snake_name=f"{tk.get('key')}_{uuid.uuid4().hex}",
            category=Tk.Category.SERVICE,
            usage_context=tk.get("usage_context"),
        )
        for tk in request.param.get("keys")
    ]

    yield tks

    for tk in tks:
        tk.delete()


@pytest.fixture(
    params=[
        "snake_name_one",
        "snake_name_two2",
        "snake_name_%$#@%^&@",
    ],
)
def translation_key_mimo_factory(request):
    """``TranslationKey`` with mimo snake_names factory fixture."""
    from translate.service.models import TranslationKey as Tk
    from translate.service.tests.factories import TranslationKeyFactory

    tk = TranslationKeyFactory.create(
        snake_name=f"{request.param}_{uuid.uuid4().hex}",
        category=Tk.Category.SERVICE,
    )

    yield tk
    tk.delete()


@pytest.fixture
@pytest.mark.xdist_group(name="group_db")
def translation_factory(language_factory, translation_key_factory):
    """Translation factory fixture."""
    from translate.service.tests.factories import TranslationFactory

    obj = TranslationFactory.create(language=language_factory, key=translation_key_factory)

    yield obj, language_factory, translation_key_factory

    obj.delete()


@pytest.fixture
@pytest.mark.xdist_group(name="group_db")
def translation_mimo_factory(language_factory, translation_key_mimo_factory):
    """Translation factory fixture."""
    from translate.service.tests.factories import TranslationFactory

    obj = TranslationFactory.create(language=language_factory, key=translation_key_mimo_factory)

    yield obj, language_factory, translation_key_mimo_factory
    obj.delete()


@pytest.fixture
def translation_provider(provider_to_fixture):
    """Translation provider fixture."""
    from translate.service.tests.providers import TranslationProvider

    provider_to_fixture.add_provider(TranslationProvider)

    yield provider_to_fixture


@pytest.fixture
def language_provider(provider_to_fixture):
    """Language provider fixture."""
    from translate.service.tests.providers import LanguageProvider

    provider_to_fixture.add_provider(LanguageProvider)

    yield provider_to_fixture


@pytest.fixture
def translation_key_provider(provider_to_fixture):
    """Translation key provider."""
    from translate.service.tests.providers import TranslationKeyProvider

    provider_to_fixture.add_provider(TranslationKeyProvider)

    yield provider_to_fixture


@pytest.fixture
def user_account(worker_id):
    """Use a different account in each xdist worker"""
    return f"account_{worker_id}"


@pytest.fixture
def import_german_translations_fixture():
    """Inserts data into test database before running tests. Needed for ``client`` tests."""
    from django.core.management import call_command

    from translate.service.models import Language, Translation, TranslationKey

    translations_used = [*read_po_files("german_fixtures")]

    used_json_translations = read_json_files("german_fixtures", "snake_translations")
    json_translations_snake_names = used_json_translations.get("de").get("translation_center_marketing")
    for key in json_translations_snake_names.keys():
        translations_used.append(json_translations_snake_names[key]["translations"])

    call_command("import_translations", translations_dir="translate/service/tests/fixtures/german_fixtures")
    yield

    Translation.objects.filter(
        translation__in=translations_used,
        language__lang_info="de",
    ).delete()
    TranslationKey.objects.filter(
        Q(snake_name__in=json_translations_snake_names.keys()) | Q(id_name__in=translations_used)
    ).delete()
    Language.objects.filter(lang_info="de").delete()


@pytest.fixture
def import_french_translations_fixture():
    """Inserts data into test database before running tests. Needed for ``client`` tests."""
    from django.core.management import call_command

    from translate.service.models import Language, Translation, TranslationKey

    Translation.objects.all().delete()
    TranslationKey.objects.all().delete()
    Language.objects.all().delete()

    call_command("import_translations", translations_dir="translate/service/tests/fixtures/french_fixtures")
    yield

    Translation.objects.all().delete()
    TranslationKey.objects.all().delete()
    Language.objects.all().delete()


@pytest.fixture
def request_serializer_fixture(make_request):
    from translate.service.serializers import TranslationRequestSerializer

    lang = {"language": "de"}
    arguments = {
        "views": ["translation_center_frontend", "translations_center_placeholders"],
        "page": 1,
        "page_size": 5,
    }
    data = dict(lang, **arguments)
    yield TranslationRequestSerializer(data=data)


@pytest.fixture
def export_csv_fixture(import_german_translations_fixture):
    """Yields path of generated CSV file"""
    import os
    from pathlib import Path

    from django.core.management import call_command

    language_code = "de"
    file_name = f"translations_{language_code}.csv"

    call_command("export_csv", language_code)
    file_path = Path(file_name)

    yield file_path

    os.remove(file_name)


@pytest.fixture()
def melon_languages_factory():
    """``Language`` factory fixture. Creates languages used in melon project and returns them as a list."""
    from translate.service.models import Language

    objs = []
    lang_list = ["en", "de", "fr"]
    for lang_code in lang_list:
        lang, _ = Language.objects.get_or_create(lang_info=lang_code)
        objs.append(lang)

    yield objs

    for obj in objs:
        try:
            obj.delete()
        except RestrictedError:
            continue


@pytest.fixture
def bulk_import_translations_from_csv_fixture(melon_languages_factory):
    """Yields path of generated CSV file"""
    from django.core.management import call_command

    file_name = f"{BASE_DIR}/translate/service/tests/fixtures/bulk_import_translations_from_csv_test_fixture.csv"
    call_command("bulk_import_translations_from_csv", file_name)
    yield
