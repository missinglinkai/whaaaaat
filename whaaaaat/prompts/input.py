# -*- coding: utf-8 -*-
"""
`input` type question
"""
from __future__ import print_function, unicode_literals
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.shortcuts import create_prompt_application
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.layout.lexers import SimpleLexer

# use std prompt-toolkit control


def question(message, **kwargs):
    default = kwargs.pop('default', '')
    validate_prompt = kwargs.pop('validate', None)
    if validate_prompt:
        if issubclass(validate_prompt, Validator):
            kwargs['validator'] = validate_prompt()
        elif callable(validate_prompt):
            class _InputValidator(Validator):
                def validate(self, document):
                    verdict = validate_prompt(document.text)
                    if not verdict == True:
                        if verdict == False:
                            verdict = 'invalid input'
                        raise ValidationError(
                            message=verdict,
                            cursor_position=len(document.text))
            kwargs['validator'] = _InputValidator()

    # TODO style defaults on detail level
    if not 'style' in kwargs:
        kwargs['style'] = style_from_dict({
            Token.QuestionMark: '#5F819D',
            #Token.Selected: '#FF9D00',  # AWS orange
            Token.Instruction: '',  # default
            Token.Answer: '#FF9D00 bold',  # AWS orange
            Token.Question: 'bold',
        })

    def _get_prompt_tokens(cli):
        return [
            (Token.QuestionMark, '?'),
            (Token.Question, ' %s ' % message)
        ]

    return create_prompt_application(
        get_prompt_tokens=_get_prompt_tokens,
        lexer=SimpleLexer(Token.Answer),
        default=default,
        **kwargs
    )