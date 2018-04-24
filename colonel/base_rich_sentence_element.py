# Copyright 2018 The NLP Odyssey Authors.
# Copyright 2018 Marco Nicola <marconicola@disroot.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module providing the :class:`.BaseSentenceElement` class."""

from typing import Optional, Any
from colonel.base_sentence_element import BaseSentenceElement
from colonel.upostag import UposTag

__all__ = ['BaseRichSentenceElement']


class BaseRichSentenceElement(BaseSentenceElement):
    """Abstract class containing basic information in common with some specific
    elements being part of a sentence.

    It is compliant with the *CoNLL-U* format, so that it provides a common
    foundation for elements of type *word* and *empty nodes*, which can be
    made up of a richer set of fields in comparison to other more minimal
    elements, such as the *(multiword) tokens*.
    """

    __slots__ = ('lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps')

    def __init__(
            self,
            lemma: Optional[str] = None,
            upos: Optional[UposTag] = None,
            xpos: Optional[str] = None,
            feats: Optional[Any] = None,
            deps: Optional[Any] = None,
            **kwargs
    ) -> None:
        super(BaseRichSentenceElement, self).__init__(**kwargs)

        #: Lemma of the element.
        #:
        #: It is compatible with *CoNLL-U* ``LEMMA`` field.
        self.lemma: Optional[str] = lemma

        #: Universal part-of-speech tag.
        #:
        #: It is compatible with *CoNLL-U* ``UPOS`` field.
        self.upos: Optional[UposTag] = upos

        #: Language-specific part-of-speech tag.
        #:
        #: It is compatible with *CoNLL-U* ``XPOS`` field.
        self.xpos: Optional[str] = xpos

        #: List of morphological features from the universal feature inventory
        #: or from a defined language-specific extension.
        #:
        #: It is compatible with *CoNLL-U* ``FEATS`` field.
        #:
        #: You are free to use any kind of value suitable for your project.
        self.feats: Optional[Any] = feats

        #: Enhanced dependency graph, usually in the form of a list of
        #: head-deprel pairs.
        #:
        #: It is compatible with *CoNLL-U* ``DEPS`` field.
        #:
        #: You are free to use any kind of value suitable for your project.
        self.deps: Optional[Any] = deps

    def is_valid(self):
        """Returns whether or not the object can be considered valid,
        without considering the context of the sentence in which the word
        itself is possibly inserted.

        An instance of type :class:`.BaseRichSentenceElement` is **always**
        considered valid, independently from any of its attributes' value.
        """
        super(BaseRichSentenceElement, self).is_valid()
