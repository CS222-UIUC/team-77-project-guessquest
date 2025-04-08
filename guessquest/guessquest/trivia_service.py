import requests

class TriviaService:
    BASE_URL = "https://opentdb.com/api.php"
    
    @staticmethod
    def get_questions(amount=10, category=None, difficulty=None, question_type=None):
        """
        Fetch trivia questions from Open Trivia Database
        
        Parameters:
        - amount: Number of questions (1-50)
        - category: Category ID (optional)
        - difficulty: easy, medium or hard (optional)
        - question_type: multiple or boolean (optional)
        """
        params = {'amount': amount}
        
        if category:
            params['category'] = category
        if difficulty:
            params['difficulty'] = difficulty
        if question_type:
            params['type'] = question_type
            
        response = requests.get(TriviaService.BASE_URL, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed with status code {response.status_code}"}