"""Test cases for Objectapp's comparison"""
from django.test import TestCase

from objectapp.models import Gbobject
from objectapp.comparison import pearson_score
from objectapp.comparison import VectorBuilder
from objectapp.comparison import ClusteredModel


class ComparisonTestCase(TestCase):
    """Test cases for comparison tools"""

    def test_pearson_score(self):
        self.assertEquals(pearson_score([42], [42]), 0.0)
        self.assertEquals(pearson_score([0, 1, 2], [0, 1, 2]), 0.0)
        self.assertEquals(pearson_score([0, 1, 3], [0, 1, 2]),
                          0.051316701949486232)
        self.assertEquals(pearson_score([0, 1, 2], [0, 1, 3]),
                          0.051316701949486232)

    def test_clustered_model(self):
        params = {'title': 'My gbobject 1', 'content': 'My content 1',
                  'tags': 'objectapp, test', 'slug': 'my-gbobject-1'}
        Gbobject.objects.create(**params)
        params = {'title': 'My gbobject 2', 'content': 'My content 2',
                  'tags': 'objectapp, test', 'slug': 'my-gbobject-2'}
        Gbobject.objects.create(**params)
        cm = ClusteredModel(Gbobject.objects.all())
        self.assertEquals(cm.dataset().values(), ['1', '2'])
        cm = ClusteredModel(Gbobject.objects.all(),
                            ['title', 'excerpt', 'content'])
        self.assertEquals(cm.dataset().values(), ['My gbobject 1  My content 1',
                                                  'My gbobject 2  My content 2'])

    def test_vector_builder(self):
        vectors = VectorBuilder(Gbobject.objects.all(),
                                ['title', 'excerpt', 'content'])
        params = {'title': 'My gbobject 1', 'content':
                  'This is my first content',
                  'tags': 'objectapp, test', 'slug': 'my-gbobject-1'}
        Gbobject.objects.create(**params)
        params = {'title': 'My gbobject 2', 'content':
                  'My second gbobject',
                  'tags': 'objectapp, test', 'slug': 'my-gbobject-2'}
        Gbobject.objects.create(**params)
        columns, dataset = vectors()
        self.assertEquals(columns, ['content', 'This', 'my', 'is', '1',
                                    'second', '2', 'first'])
        self.assertEquals(dataset.values(), [[1, 1, 1, 1, 1, 0, 0, 1],
                                             [0, 0, 0, 0, 0, 1, 1, 0]])
