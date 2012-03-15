# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


# This project incorporates work covered by the following copyright and permission notice:  

#    Copyright (c) 2009, Julien Fache
#    All rights reserved.

#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions
#    are met:

#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#    * Neither the name of the author nor the names of other
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.

#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#    OF THE POSSIBILITY OF SUCH DAMAGE.
"""Search module with complex query parsing for Objectapp"""
from pyparsing import Word
from pyparsing import alphas
from pyparsing import WordEnd
from pyparsing import Combine
from pyparsing import opAssoc
from pyparsing import Optional
from pyparsing import OneOrMore
from pyparsing import StringEnd
from pyparsing import printables
from pyparsing import quotedString
from pyparsing import removeQuotes
from pyparsing import ParseResults
from pyparsing import CaselessLiteral
from pyparsing import operatorPrecedence

from django.db.models import Q

from objectapp.models import Gbobject
from objectapp.settings import STOP_WORDS


def createQ(token):
    """Creates the Q() object"""
    meta = getattr(token, 'meta', None)
    query = getattr(token, 'query', '')
    wildcards = None

    if isinstance(query, basestring):  # Unicode -> Quoted string
        search = query
    else:  # List -> No quoted string (possible wildcards)
        if len(query) == 1:
            search = query[0]
        elif len(query) == 3:
            wildcards = 'BOTH'
            search = query[1]
        elif len(query) == 2:
            if query[0] == '*':
                wildcards = 'START'
                search = query[1]
            else:
                wildcards = 'END'
                search = query[0]

    # Ignore connective words (of, a, an...) and STOP_WORDS
    if (len(search) < 3 and not search.isdigit()) or \
           search in STOP_WORDS:
        return Q()

    if not meta:
        return Q(content__icontains=search) | \
               Q(excerpt__icontains=search) | \
               Q(title__icontains=search)

    if meta == 'Objecttype':
        if wildcards == 'BOTH':
            return Q(objecttypes__title__icontains=search) | \
                    Q(objecttypes__slug__icontains=search)
        elif wildcards == 'START':
            return Q(objecttypes__title__iendswith=search) | \
                    Q(objecttypes__slug__iendswith=search)
        elif wildcards == 'END':
            return Q(objecttypes__title__istartswith=search) | \
                    Q(objecttypes__slug__istartswith=search)
        else:
            return Q(objecttypes__title__iexact=search) | \
                    Q(objecttypes__slug__iexact=search)
    elif meta == 'author':
        if wildcards == 'BOTH':
            return Q(authors__username__icontains=search)
        elif wildcards == 'START':
            return Q(authors__username__iendswith=search)
        elif wildcards == 'END':
            return Q(authors__username__istartswith=search)
        else:
            return Q(authors__username__iexact=search)
    elif meta == 'tag':  # TODO: tags ignore wildcards
        return Q(tags__icontains=search)


def unionQ(token):
    """Appends all the Q() objects"""
    query = Q()
    operation = 'and'
    negation = False

    for t in token:
        if type(t) is ParseResults:  # See tokens recursively
            query &= unionQ(t)
        else:
            if t in ('or', 'and'):  # Set the new op and go to next token
                operation = t
            elif t == '-':  # Next tokens needs to be negated
                negation = True
            else:  # Append to query the token
                if negation:
                    t = ~t
                if operation == 'or':
                    query |= t
                else:
                    query &= t
    return query


NO_BRTS = printables.replace('(', '').replace(')', '')
SINGLE = Word(NO_BRTS.replace('*', ''))
WILDCARDS = Optional('*') + SINGLE + Optional('*') + WordEnd(wordChars=NO_BRTS)
QUOTED = quotedString.setParseAction(removeQuotes)

OPER_AND = CaselessLiteral('and')
OPER_OR = CaselessLiteral('or')
OPER_NOT = '-'

TERM = Combine(Optional(Word(alphas).setResultsName('meta') + ':') +
               (QUOTED.setResultsName('query') |
                WILDCARDS.setResultsName('query')))
TERM.setParseAction(createQ)

EXPRESSION = operatorPrecedence(TERM, [
    (OPER_NOT, 1, opAssoc.RIGHT),
    (OPER_OR, 2, opAssoc.LEFT),
    (Optional(OPER_AND, default='and'), 2, opAssoc.LEFT)])
EXPRESSION.setParseAction(unionQ)

QUERY = OneOrMore(EXPRESSION) + StringEnd()
QUERY.setParseAction(unionQ)


def advanced_search(pattern):
    """Parse the grammar of a pattern
    and build a queryset with it"""
    query_parsed = QUERY.parseString(pattern)
    return Gbobject.published.filter(query_parsed[0]).distinct()
