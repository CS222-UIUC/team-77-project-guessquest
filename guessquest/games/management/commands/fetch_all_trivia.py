# myapp/management/commands/fetch_all_trivia.py
import time, requests
from django.core.management.base import BaseCommand
from ...models import TriviaQuestion 

API_URL   = "https://opentdb.com/api.php"
TOTAL     = 4516
BATCH_SIZE= 50

class Command(BaseCommand):
    help = "Fetch all trivia questions in 50‑question batches"

    def handle(self, *args, **opts):
        no_new_rounds = 0
        while TriviaQuestion.objects.count() < TOTAL and no_new_rounds < 5:
            resp = requests.get(API_URL, params={
                "amount": BATCH_SIZE,
                "type":   "multiple",
                "encode": "base64"   # avoid HTML entities
            })
            data = resp.json().get("results", [])
            new = 0

            for item in data:
                # decode base64 fields
                import base64
                def d(s): return base64.b64decode(s).decode()
                qtxt = d(item["question"])
                if not TriviaQuestion.objects.filter(question_text=qtxt).exists():
                    TriviaQuestion.objects.create(
                        question_text               = qtxt,
                        correct_answer     = d(item["correct_answer"]),
                        incorrect_answers  = [d(x) for x in item["incorrect_answers"]],
                    )
                    new += 1

            total = TriviaQuestion.objects.count()
            self.stdout.write(f"+{new} → {total}/{TOTAL}")
            no_new_rounds = no_new_rounds + 1 if new == 0 else 0
            time.sleep(1)

        self.stdout.write(
            self.style.SUCCESS("Done!") 
            if total >= TOTAL else 
            self.style.WARNING(f"Stopped at {total}/{TOTAL}")
        )