from django.template.response import TemplateResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_object_or_404,
                              redirect)

from reviews.models import Review
from users.models import UserProfile
from cr_admin.forms import QuotaForm
from cr_admin.models import AdminQuota
from cr_admin.decorators import (middcourses_admin_required,
                                 middcourses_moderator_required)

@login_required
@middcourses_moderator_required
def index(request):
    return TemplateResponse(request, 'cr_admin/index.html')

@login_required
@middcourses_admin_required
def quota(request):
    users_quota_count = UserProfile.objects.values('total_reviews') \
        .order_by().annotate(Count('total_reviews'))

    admin_quota = AdminQuota.objects.all().first()

    quota_form = QuotaForm()

    return TemplateResponse(request, 'cr_admin/quota.html', {'quota_data': users_quota_count,
                                                             'quota_form': quota_form,
                                                             'current_admin_quota': admin_quota})

@login_required
@middcourses_moderator_required
def flags(request):
    flagged_reviews = Review.objects.filter(flagged=True, flagged_mod=None)
    return TemplateResponse(request, 'cr_admin/flags.html', {'reviews': flagged_reviews})

@login_required
@middcourses_admin_required
def flags_moderated(request):
    flagged_reviews = Review.objects.all().exclude(flagged_mod=None)
    return TemplateResponse(request, 'cr_admin/flags_moderated.html', {'reviews': flagged_reviews})

@login_required
@middcourses_moderator_required
def flagged_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'GET':
        return TemplateResponse(request, 'cr_admin/flagged_review.html', {'review': review})
    elif request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'Unflag':
            review.flagged = False
            review.save()
            return redirect('admin_flags')
        elif action == 'Remove':
            review.flagged_mod = request.user
            review.save()
            return redirect('admin_flags')
    return TemplateResponse(request, 'cr_admin/flagged_review.html', {'review': review})
