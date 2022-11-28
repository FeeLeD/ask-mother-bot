from typing import List
from messages import ChatMessage, answers, QUESTIONS


class Response:
    def __init__(self,
                 answer: ChatMessage = None,
                 questions: List[ChatMessage] = [],
                 current_question: ChatMessage = None,
                 is_bad_input: bool = False):
        self.answer = answer
        self.questions = questions
        self.current_question = current_question
        self.is_bad_input = is_bad_input


def get_questions(*keys: int):
    found_questions: List[ChatMessage] = []
    for key in keys:
        found_questions += [q for q in QUESTIONS if q.key == key]

    return found_questions


def get_answer(key: int):
    return [a for a in answers if a.key == key]


def get_response_from(message):
    current_question = next((q for q in QUESTIONS if q.text == message.text), None)

    if current_question is None:
        return Response(is_bad_input=True)

    if not hasattr(current_question, 'next_messages') or len(current_question.next_messages) == 0:
        return None

    answer_key = current_question.next_messages[0]
    found_answers = get_answer(answer_key)

    if not hasattr(found_answers[0], 'next_messages') or len(found_answers[0].next_messages) == 0:
        return Response(answer=found_answers[0], current_question=current_question)

    found_questions = get_questions(*found_answers[0].next_messages)
    if len(found_questions) > 0:
        return Response(answer=found_answers[0], questions=found_questions,
                        current_question=current_question)


# def get_response_from(message):
#     current_question = next((q for q in questions if q.text == message.text), None)
#
#     if current_question is None:
#         return 'Пожалуйста, выберите вопрос из предложенных вариантов 👀'
#
#     if not hasattr(current_question, 'next_messages') or len(current_question.next_messages) == 0:
#         return None
#
#     answer_key = current_question.next_messages[0]
#     found_answers = get_answer(answer_key)
#
#     if not hasattr(found_answers[0], 'next_messages') or len(found_answers[0].next_messages) == 0:
#         return found_answers[0].text
#
#     found_questions = get_questions(*found_answers[0].next_messages)
#     if len(found_questions) > 0:
#         return found_answers[0].text, found_questions[0].text, found_questions[1].text


def is_good_question(message):
    current_question = next((q for q in QUESTIONS if q.text == message.text), None)

    if current_question is None:
        return False

    return current_question.is_good_question
