from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)
        selected_choices = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice = Choice.objects.get(pk=value)
                selected_choices.append(choice)
        submission.choices.set(selected_choices)
        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()
    
    total_score = 0
    earned_score = 0
    
    for question in course.question_set.all():
        total_score += question.grade
        selected_ids = selected_choices.filter(question=question).values_list('id', flat=True)
        if question.is_get_score(selected_ids):
            earned_score += question.grade

    context = {
        'course': course,
        'selected_choices': selected_choices,
        'grade': earned_score,
        'total_score': total_score
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
