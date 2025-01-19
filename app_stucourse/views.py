from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Enrollment, Student, Course
from .forms import EnrollmentForm

from django.contrib import messages  # To display alerts
from datetime import datetime # To date related operations

def enrollment_view(request):
    if request.method == "POST":

        # Check if we are editing an existing enrollment or adding a new one
        enrollment_id = request.POST.get('enrollment_id')  # Get enrollment_id from hidden input
        student_id = request.POST.get('student')  # Get student ID from the form
        course_id = request.POST.get('course')  # Get course ID from the form
        enrollment_date = request.POST.get('enrollment_date')  # Get date from the form

        # Check if enrollment_date is missing
        if not enrollment_date:
            messages.warning(request, "Enrollment date is required.")
            return redirect('enrollment')  # Redirect to stop further execution

        # Convert enrollment_date to datetime object to compare
        enrollment_date = datetime.strptime(enrollment_date, '%Y-%m-%d')

        if enrollment_id:
            # Editing existing record
            enrollment = get_object_or_404(Enrollment, id=enrollment_id)
            form = EnrollmentForm(request.POST, instance=enrollment)
            if form.is_valid():
                form.save()  # Save the updated record
                messages.success(request, "Enrollment updated successfully!")
                return redirect('enrollment')
        else:
            # Adding new record
            # Check if the combination (student, course, enrollment_date) already exists in the database
            if Enrollment.objects.filter(enrollment_date=enrollment_date, course_id=course_id, student_id=student_id ).exists():
                messages.warning(request, "This enrollment record already exists for the selected date!")
            # Check if any of the fields are empty
            if not student_id:
                messages.warning(request, "Student is required.")
            elif not course_id:
                messages.warning(request, "Course is required.")
            elif not enrollment_date:
                messages.warning(request, "Enrollment date is required.")
            else:
                form = EnrollmentForm(request.POST)
                if form.is_valid():
                    form.save()  # Save the new record
                    messages.success(request, "Enrollment added successfully!")
                    return redirect('enrollment')  # Redirect to clear form on submission
    else:
        form = EnrollmentForm()

   # Populate dropdowns
    students = Student.objects.all()
    courses = Course.objects.all()

    # Get all Enrollment records
    enrollments = Enrollment.objects.all().order_by('-id')  # Order by most recently added first
    
   # Set up pagination with 5 records per page
    paginator = Paginator(enrollments, 5)  
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object

    # Pass the page object to the template
    return render(request, 'enrollment.html', { 'students': students,  # Pass student objects for the dropdown
                                                'courses': courses,  # Pass course objects for the dropdown
                                                'enrollments': enrollments,  # Pass enrollment objects for the table
                                                'page_obj': page_obj})
