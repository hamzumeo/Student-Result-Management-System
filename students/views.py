from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from .models import Student, Result
from .forms import StudentForm, ResultForm

# Home
def home(request):
    return render(request, 'students/home.html')

# STUDENTS
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_add.html', {'form': form})

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')
    return render(request, 'students/student_add.html', {'form': form, 'edit': True})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')

# RESULTS
def result_list(request):
    students_totals = Student.objects.all().annotate(
        total_marks=Coalesce(Sum('results__marks', output_field=FloatField()), 0.0)
    )

    results_summary = []
    for s in students_totals:
        total = s.total_marks
        subject_count = s.results.count()
        percentage = (total / (subject_count * 100) * 100) if subject_count > 0 else 0

        if subject_count == 0:
            grade = 'N/A'
            status = 'fail'
        else:
            if percentage >= 80:
                grade = 'A'
            elif percentage >= 65:
                grade = 'B'
            elif percentage >= 50:
                grade = 'C'
            else:
                grade = 'Fail'
            status = 'pass' if percentage >= 50 else 'fail'

        results_summary.append({
            'student': s,
            'total': int(total),
            'percentage': round(percentage, 2),
            'grade': grade,
            'status': status,
            'subjects': s.results.all()
        })

    return render(request, 'students/result_list.html', {'results_summary': results_summary})

def add_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result added successfully!')
            return redirect('result_list')
    else:
        form = ResultForm()
    return render(request, 'students/result_add.html', {'form': form})

def edit_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    form = ResultForm(request.POST or None, instance=result)
    if form.is_valid():
        form.save()
        messages.success(request, 'Result updated successfully!')
        return redirect('result_list')
    return render(request, 'students/result_edit.html', {'form': form})

def delete_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    result.delete()
    messages.success(request, 'Result deleted successfully!')
    return redirect('result_list')
