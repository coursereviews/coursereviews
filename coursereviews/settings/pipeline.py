PIPELINE = {
    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
    'CSSMIN_BINARY': 'cssmin',
    'JS_COMPRESSOR': 'pipeline.compressors.slimit.SlimItCompressor',
    'COMPILERS': (
        'pipeline.compilers.less.LessCompiler',
    ),
    'STYLESHEETS': {
        'local_bs': {
            'source_filenames': (
                'coursereviews/vendorcss/bootstrap-glyphicons.css',
                'coursereviews/vendorcss/bootstrap.min.css',
            ),
            'output_filename': 'css/bootstrap.css',
            'variant': 'datauri',
        },
        'base': {
            'source_filenames': (
                'coursereviews/less/base.less',
            ),
            'output_filename': 'css/base.css',
            'variant': 'datauri',
        },
        'reviews': {
            'source_filenames': (
                'coursereviews/vendorcss/select2.css',
                'coursereviews/vendorcss/slider.css',
                'reviews/less/reviews.less',
            ),
            'output_filename': 'css/reviews.css',
            'variant': 'datauri',
        },
        'static_pages': {
            'source_filenames': (
                'static_pages/less/static_pages.less',
            ),
            'output_filename': 'css/static_pages_base.css',
            'variant': 'datauri',
        },
        'splash': {
            'source_filenames': (
                'static_pages/less/splash.less',
            ),
            'output_filename': 'css/splash.css',
            'variant': 'datauri',
        },
        'users': {
            'source_filenames': (
                'users/less/users.less',
            ),
            'output_filename': 'css/user.css',
            'variant': 'datauri',
        },
        'cr_admin': {
            'source_filenames': (
                'cr_admin/less/cr_admin.less',
            ),
            'output_filename': 'css/cr_admin.css'
        },
        'stats': {
            'source_filenames': (
                'stats/less/stats.less',
            ),
            'output_filename': 'css/stats.css'
        }
    },
    'JAVASCRIPT': {
        'local_libs_development': {
            'source_filenames': (
                'coursereviews/js/jquery-1.9.0.js',
                'coursereviews/js/bootstrap/bootstrap.min.js',
                'coursereviews/js/global.js',
            ),
            'output_filename': 'js/libs.js'
        },
        'local_libs_production': {
            'source_filenames': (
                'coursereviews/js/global.js',
            ),
            'output_filename': 'js/libs.js'
        },
        'new_review': {
            'source_filenames': (
                'reviews/js/reviews.js',
            ),
            'output_filename': 'js/new_review.js'
        },
        'review_detail': {
            'source_filenames': (
                'reviews/js/detail.js',
            ),
            'output_filename': 'js/detail.js'
        },
        'cr_admin': {
            'source_filenames': (
                'cr_admin/js/cr_admin.js',
            ),
            'output_filename': 'js/cr_admin.js'
        },
        'stats': {
            'source_filenames': (
                'stats/js/stats.js',
            ),
            'output_filename': 'js/stats.js'
        },
        'catalog': {
            'source_filenames': (
                'vendor/js/underscore.js',
                'vendor/js/backbone.js',
                'reviews/js/routers/catalog-router.js',
                'reviews/js/models/department.js',
                'reviews/js/models/professor.js',
                'reviews/js/models/course.js',
                'reviews/js/collections/departments.js',
                'reviews/js/collections/courses.js',
                'reviews/js/collections/professors.js',
                'reviews/js/views/catalog-view.js',
                'reviews/js/views/catalog-item-view.js',
                'reviews/js/catalog.js'
            ),
            'output_filename': 'js/catalog.js'
        },
    }
}
