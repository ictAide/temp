from django.core.management.base import BaseCommand
from django_seed import Seed
from app_stucourse.models import Student, Course, Enrollment
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Seed database with test data"

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # Add students
        seeder.add_entity(Student, 15, {
            'name': lambda x: seeder.faker.name(),
            'email': lambda x: seeder.faker.email(),
        })

        # Add courses
        seeder.add_entity(Course, 5, {
            'title': lambda x: seeder.faker.unique.word().capitalize(),
        })

        inserted_pks = seeder.execute()

        # Add enrollments
        students = Student.objects.all()
        courses = Course.objects.all()

        for _ in range(30):  # Create 30 random enrollments
            Enrollment.objects.create(
                student=random.choice(students),
                course=random.choice(courses),
                date_enrolled=datetime.now() - timedelta(days=random.randint(1, 365))
            )

        self.stdout.write("Database successfully seeded!")
