from django.contrib.staticfiles.storage import CachedFilesMixin
from pipeline.storage import PipelineMixin, NonPackagingMixin
from storages.backends.s3boto import S3BotoStorage


class S3PipelineStorage(PipelineMixin, CachedFilesMixin, S3BotoStorage):
    pass

class NonPackagingS3PipelineStorage(NonPackagingMixin, S3PipelineStorage):
    pass
