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
"""Comparison tools for Gstudio
Based on clustered_models app"""
from math import sqrt

from gstudio.settings import F_MIN
from gstudio.settings import F_MAX


def pearson_score(list1, list2):
    """Compute the pearson score between 2 lists of vectors"""
    sum1 = sum(list1)
    sum2 = sum(list2)
    sum_sq1 = sum([pow(l, 2) for l in list1])
    sum_sq2 = sum([pow(l, 2) for l in list2])

    prod_sum = sum([list1[i] * list2[i] for i in range(len(list1))])

    num = prod_sum - (sum1 * sum2 / len(list1))
    den = sqrt((sum_sq1 - pow(sum1, 2) / len(list1)) *
               (sum_sq2 - pow(sum2, 2) / len(list2)))
    if den == 0:
        return 0.0
    return 1.0 - num / den


class ClusteredModel(object):
    """Wrapper around Model class
    building a dataset of instances"""

    def __init__(self, queryset, fields=['id']):
        self.fields = fields
        self.queryset = queryset

    def dataset(self):
        """Generate a dataset with the queryset
        and specified fields"""
        dataset = {}
        for item in self.queryset.filter():
            dataset[item] = ' '.join([unicode(item.__dict__[field])
                                      for field in self.fields])
        return dataset


class VectorBuilder(object):
    """Build a list of vectors based on datasets"""

    def __init__(self, queryset, fields):
        self.key = ''
        self.columns = []
        self.dataset = {}
        self.clustered_model = ClusteredModel(queryset, fields)
        self.build_dataset()

    def build_dataset(self):
        """Generate whole dataset"""
        data = {}
        words_total = {}

        model_data = self.clustered_model.dataset()
        for instance, words in model_data.items():
            words_item_total = {}
            for word in words.split():
                words_total.setdefault(word, 0)
                words_item_total.setdefault(word, 0)
                words_total[word] += 1
                words_item_total[word] += 1
            data[instance] = words_item_total

        top_words = []
        for word, count in words_total.items():
            frequency = float(count) / len(data)
            if frequency > F_MIN and frequency < F_MAX:
                top_words.append(word)

        self.dataset = {}
        self.columns = top_words
        for instance in data.keys():
            self.dataset[instance] = [data[instance].get(word, 0)
                                      for word in top_words]
        self.key = self.generate_key()

    def generate_key(self):
        """Generate key for this list of vectors"""
        return self.clustered_model.queryset.count()

    def flush(self):
        """Flush the dataset"""
        if self.key != self.generate_key():
            self.build_dataset()

    def __call__(self):
        self.flush()
        return self.columns, self.dataset
