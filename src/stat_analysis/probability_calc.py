"""
probability_calc.py

This module provides a probability expressions parser and evaluator.

----------------------------------------------------

----------------------------------------------------
                 Summary Statistics
----------------------------------------------------

Uncertainty is all around us. Probability is the study of randomness.

Probability theory is based on three main concepts:

    - **Experiment**: Any procedure that can be replicated an infinite number of times
      and for which a defined set of possible outcomes is available (sample space).
      If the sample space contains only one possible outcome, the experiment is deterministic.

        - *Trials*: Multiple repetitions of the same experiment.

    - **Event**: A set of outcomes from an experiment, with probability P(E).

    - **Probability**: A number between 0 and 1 that measures the degree of uncertainty
      associated with the realization of an event.

        - *Certain event*: P(E) = 1
        - *Impossible event*: P(E) = 0
"""

import string
#from dataclasses import dataclass
from pathlib import Path
from typing import Union, Any

__all__ = []
__version__ = "1.0.0"
__author__ = "github: pedro-franesqui"


_T_UNKNOWN = "UNKNOWN"
_T_INT = "INT"
_T_FLOAT = "FLOAT"
_T_PLUS = "PLUS"
_T_MINUS = "MINUS"
_T_MUL = "MUL"
_T_DIV = "DIV"
_T_RPAR = "RPAR"
_T_LPAR = "LPAR"
_T_EQUALS = "EQUALS"
_T_POW = "POW"
_T_COND = "COND"
_T_PROB = "PROB"
_T_EVENT = "EVENT"
_T_UNION = "UNION"
_T_INTER = "INTER"
_T_COMP = "COMP"

class Error:
    def __init__(self, err_name: str, details: str) -> None:
        self.err_name = err_name
        self.details = details

    def to_string(self) -> str:
        return f"{self.err_name}: {self.details}"

class IllegalCharError(Error):
    def __init__(self, details: str) -> None:
        super().__init__("IllegalCharError", details)

class Token:
    def __init__(self, token_type: str, value: Union[int, float]=None) -> None:
        self.token_type = token_type
        self.value = value

    def __repr__(self) -> str:
        return f"{self.token_type}:{self.value}" if self.value else f"{self.token_type}"

class ProbabilityParser:
    def __init__(self, src: Union[str, Path], from_file: bool = False) -> None:
        self.current_char = None
        self.pos = -1
        self.src = src
        self.expr: str = ""
        self.from_file = from_file

    def expr_eval(self):
        self.expr = self.__read_file()
        self.__advance()
        print(self.__tokenize())

    def __read_file(self) -> str:
        if self.from_file:
            file_path: Path = Path(self.src)
            if not file_path.exists():
                raise FileNotFoundError(f"File '{file_path}' not found.")
            return file_path.read_text(encoding="utf-8")
        else:
            return self.src

    def __tokenize(self) -> tuple[list[Any], IllegalCharError] | tuple[list[Token], None]:
        tokens: list[Token] = []
        while self.current_char is not None:
            match self.current_char:
                case "\t" | " ":
                    self.__advance()
                case '+':
                    tokens.append(Token(_T_PLUS))
                    self.__advance()
                case '-':
                    tokens.append(Token(_T_MINUS))
                    self.__advance()
                case '*':
                    tokens.append(Token(_T_MUL))
                    self.__advance()
                case '/':
                    tokens.append(Token(_T_DIV))
                    self.__advance()
                case '(':
                    tokens.append(Token(_T_LPAR))
                    self.__advance()
                case ')':
                    tokens.append(Token(_T_RPAR))
                    self.__advance()
                case '=':
                    tokens.append(Token(_T_EQUALS))
                    self.__advance()
                case '^':
                    tokens.append(Token(_T_POW))
                    self.__advance()
                case '|':
                    tokens.append(Token(_T_COND))
                    self.__advance()
                case 'P' | 'p':
                    tokens.append(Token(_T_PROB))
                    self.__advance()
                case 'U' | 'u' | '∪':
                    tokens.append(Token(_T_UNION))
                    self.__advance()
                case '∩' | 'n':
                    tokens.append(Token(_T_INTER))
                    self.__advance()
                case '¬' | '~' | '!':
                    tokens.append(Token(_T_COMP))
                    self.__advance()
                case _ :
                    if self.current_char in string.ascii_letters:
                        tokens.append(self.__make_event_identifier())
                    elif self.current_char in string.digits:
                        tokens.append(self.__make_number())
                    else:
                        char = self.current_char
                        self.__advance()
                        return [], IllegalCharError("'" + char + "'")

        return tokens, None

    def __advance(self):
        self.pos += 1
        self.current_char = self.expr[self.pos] if self.pos < len(self.expr) else None

    def __make_event_identifier(self) -> Token:
        id_str = ""
        pos_start = self.pos

        while self.current_char is not None and self.current_char in string.ascii_letters + string.digits + '_':
            id_str += self.current_char
            self.__advance()

        return Token(_T_EVENT, id_str)

    def __make_number(self) -> Token:
        num_str = ""
        dot_count = 0

        while self.current_char is not None and self.current_char in string.digits + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.__advance()

        if dot_count == 0:
            return Token(_T_INT, int(num_str))
        else:
            return Token(_T_FLOAT, float(num_str))