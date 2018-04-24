
"""Module providing the :class:`.BaseSentenceElement` class."""

from typing import Optional

__all__ = ['BaseSentenceElement']


class BaseSentenceElement:
    """Abstract class containing the minimum information in common with
    all more specific elements being part of a sentence.

    In the context of this library, it is expected that each item of a sentence
    is an instance of a :class:`.BaseSentenceElement` subclass (or, in rare
    cases, at least an instance of :class:`.BaseSentenceElement` itself).

    The generic term *element* is used in order to prevent confusion, while
    each specialized element (i.e. a subclass of :class:`.BaseSentenceElement`)
    will adopt a more appropriate nomenclature, so that, for example, a
    sentence will be formed by *words*, a *tokens* or *nodes*.
    """

    __slots__ = ('form', 'misc')

    def __init__(
            self,
            form: Optional[str] = None,
            misc: Optional[str] = None
    ) -> None:
        #: Word form or punctuation symbol.
        #:
        #: It is compatible with *CoNLL-U* ``FORM`` field.
        self.form: Optional[str] = form

        #: Any other annotation.
        #:
        #: It is compatible with *CoNLL-U* ``MISC`` field.
        self.misc: Optional[str] = misc

    @staticmethod
    def is_valid() -> bool:
        """Returns whether or not the object can be considered valid,
        without considering the context of the sentence in which the word
        itself is possibly inserted.

        An instance of type :class:`.BaseWord` is **always** considered valid,
        independently from the value of :attr:`.form` and :attr:`.misc`.
        """
        return True
