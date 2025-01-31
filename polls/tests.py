from django.test import TestCase

import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
            Tests the 'was_published_recently' method with a future publication date.

            This test ensures that the 'was_published_recently' method of the Question model
            correctly identifies that a Question instance with a publication date in the
            future does not fall into the category of recently published.

            Parameters
            ----------
            self : TestCase instance
                Represents the instance of the test case running the method.

            Raises
            ------
            AssertionError
                If the 'was_published_recently' method incorrectly returns True for a
                Question pub_date set in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        Tests if the `was_published_recently` method correctly identifies an old question.

        This test checks that a question with a `publication_date` older than one day
        plus one second is identified as not recently published.

        Arguments:
            self: The instance of the test case.

        Raises:
            AssertionError: If the result of `was_published_recently` for a question
            older than one day and one second does not return `False`.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(publication_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        Tests the `was_published_recently` method of a Question object to ensure it
        correctly identifies if the question was published recently. A recent question
        is defined as one with a publication date within the last day.

        Parameters
        ----------
        self : TestCase
            Instance of the test case containing necessary test setup and context.

        Raises
        ------
        AssertionError
            If the test conditions do not pass as expected.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(publication_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Creates a question with a given text and publication date offset.

    This function is used to create a question object with the specified
    text and a publication date offset relative to the current date.

    Args:
        question_text (str): The text of the question to be created.
        days (int): The offset in days applied to the current date
            to determine the publication date. Positive values indicate
            future dates, while negative values indicate past dates.

    Returns:
        Question: The created Question object with specified text and
        publication date.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, publication_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        This method tests the behavior or functionality of a system when there are no
        questions present. It ensures the system handles the absence of questions
        gracefully and accordingly.

        Args:
            self: Represents the instance of the class to which this method belongs.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Check if a question is from the past by comparing the date property.

        This method performs a comparison of the date attribute of the question object
        with the current date to determine if the question was posed in the past. It uses
        the 'question.date' property to perform the evaluation.

        Args:
            self (TestCase): Represents the test case class instance.

        Returns:
            None
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )


    def test_future_question(self):
        """
        Tests the creation and validation of a future question to ensure it behaves as
        expected within the system. This test method helps in verifying that questions
        with a future publication date are handled properly.

        Args:
            self (TestCase): The instance of the test case that holds the test context
            and methods.

        Returns:
            None
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_future_question_and_past_question(self):
        """
        Tests whether Question objects with pub_date in the past or future behave
        as expected when the `was_published_recently` method is invoked. This
        method determines if a question was published within the last day.

        The function ensures correct behavior of the method when:
        - The question's publication date is in the future (should return False).
        - The question's publication date is in the past within the last day
          (should return True).
        - The question's publication date is in the past beyond the last day
          (should return False).

        Parameters
        ----------
        self : TestCase
            The test case instance to execute the test.

        Raises
        ------
        AssertionError
            If any of the assertions verifying the expected outcomes of the
            `was_published_recently` method fails.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

class QuestionDetailVewTest(TestCase):
    def test_future_question(self):
        """
        Test if a question with a future publication date is not publicly displayed.

        This test ensures that a question with a publication date in the future is
        not visible when querying for published questions.

        Parameters
        ----------
        self : TestCase
            Instance of the test case invoking this method.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Tests functionality for handling past questions.

        This method is responsible for verifying the behavior of the system
        when interacting with past questions, ensuring expected results and
        adherence to business logic.

        Raises:
            AssertionError: If test conditions fail.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)