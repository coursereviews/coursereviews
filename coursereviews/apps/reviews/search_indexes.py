import datetime
from haystack import indexes
from reviews.models import Course, Professor

class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    code = indexes.CharField(model_attr="code")
    title = indexes.CharField(model_attr="title")
    description = indexes.CharField(model_attr="description")
    department = indexes.CharField(model_attr="dept")

    def get_model(self):
        return Course

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ProfessorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    first_name = indexes.CharField(model_attr="first")
    last_name = indexes.CharField(model_attr="last")
    email = indexes.CharField(model_attr="email")
    department = indexes.CharField(model_attr="dept")

    def get_model(self):
        return Professor

    def index_queryset(self, using=None):
        return self.get_model().objects.all()