from PySide6.QtCore import QTranslator, QLibraryInfo, QLocale
from PySide6.QtWidgets import QApplication
import settings


__qt_translator = None
__qt_base_translator = None
__app_translator = None


def set_language(language):
    global __qt_translator, __qt_base_translator, __app_translator

    app = QApplication.instance()

    settings.update({
        "language": language
    })

    locale = QLocale(language)
    translations_dir = QLibraryInfo.path(QLibraryInfo.TranslationsPath)

    if __qt_translator is not None:
        app.removeTranslator(__qt_translator)
    __qt_translator = QTranslator()
    if __qt_translator.load(locale, "qt", "_", translations_dir):
        app.installTranslator(__qt_translator)
    else:
        __qt_translator = None

    if __qt_base_translator is not None:
        app.removeTranslator(__qt_base_translator)
    __qt_base_translator = QTranslator()
    if __qt_base_translator.load(locale, "qtbase", "_", translations_dir):
        app.installTranslator(__qt_base_translator)
    else:
        __qt_base_translator = None

    if __app_translator is not None:
        app.removeTranslator(__app_translator)
    __app_translator = QTranslator()
    if __app_translator.load(locale, "app", "_", ":/i18n"):
        app.installTranslator(__app_translator)
    else:
        __app_translator = None
