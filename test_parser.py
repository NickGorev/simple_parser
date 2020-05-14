# -*- coding: utf-8 -*-
import pytest
import my_parser


def test_correct_parseLine():
    p = my_parser.Parser()
    with open('correct_tests.txt') as ftests,\
        open('correct_answers.txt') as fanswers:
        test_line = ftests.readline()
        answer_line = fanswers.readline().strip()
        assert p.parseLine(test_line) == answer_line

def test_incorrect_parseLine():
    p = my_parser.Parser()
    with open('incorrect_tests.txt') as ftests,\
        open('incorrect_answers.txt') as fanswers:
        test_line = ftests.readline()
        answer_line = fanswers.readline().strip()
        with pytest.raises(my_parser.ParserError)  as excinfo:
            p.parseLine(test_line)
        assert str(excinfo.value) == answer_line