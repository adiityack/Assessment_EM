

# import json
# from collections import Counter
# import language_tool_python
# import os

# class MCQValidator:
#     def __init__(self, mcq_list):
#         self.mcq_list = mcq_list
#         self.grammar_checker = language_tool_python.LanguageTool('en-US')
    
#     def check_duplicate_options(self, options):
#         return [item for item, count in Counter(options.values()).items() if count > 1]
    
#     def check_answer_mismatch(self, options, answer):
#         return answer not in options
    
#     def check_text_issues(self, text):
#         matches = self.grammar_checker.check(text)
#         return [{
#             "error": text[match.offset:match.offset + match.errorLength],
#             "message": match.message,
#             "suggestions": match.replacements
#         } for match in matches]
    
#     def validate_and_update(self):
#         # Track duplicate questions
#         question_texts = [q["question"].strip().lower() for q in self.mcq_list]
#         duplicate_questions = [item for item, count in Counter(question_texts).items() if count > 1]
        
#         for q in self.mcq_list:
#             # Initialize error tracking structure
#             q["validation"] = {
#                 "status": "Passed",
#                 "errors": [],
#                 "suggestions": {}
#             }
            
#             # Check for duplicate question
#             if q["question"].strip().lower() in duplicate_questions:
#                 q["validation"]["status"] = "Failed"
#                 q["validation"]["errors"].append("Duplicate question detected")
#                 q["validation"]["suggestions"]["question"] = ["This question and type of this questions already exits so make new question on class 9th law of motion"]
            
#             # Check for duplicate options
#             dup_options = self.check_duplicate_options(q["options"])
#             if dup_options:
#                 q["validation"]["status"] = "Failed"
#                 q["validation"]["errors"].append(f"Duplicate options: {', '.join(dup_options)}")
#                 q["validation"]["suggestions"]["options"] = ["Make each option distinct"]
            
#             # Check answer exists in options
#             if self.check_answer_mismatch(q["options"], q["answer"]):
#                 q["validation"]["status"] = "Failed"
#                 q["validation"]["errors"].append(f"Answer key '{q['answer']}' not in options")
#                 q["validation"]["suggestions"]["answer"] = ["Add matching option or correct answer key"]
            
#             # Check question text
#             question_issues = self.check_text_issues(q["question"])
#             if question_issues:
#                 q["validation"]["status"] = "Failed"
#                 q["validation"]["errors"].append("Question text issues")
#                 q["validation"]["suggestions"]["question_text"] = question_issues
            
#             # Check options text
#             option_issues = {}
#             for opt_key, opt_text in q["options"].items():
#                 issues = self.check_text_issues(opt_text)
#                 if issues:
#                     option_issues[opt_key] = issues
            
#             if option_issues:
#                 q["validation"]["status"] = "Failed"
#                 q["validation"]["errors"].append("Option text issues")
#                 q["validation"]["suggestions"]["option_text"] = option_issues
            
#             # Clean empty suggestion fields
#             if not q["validation"]["suggestions"]:
#                 q["validation"]["suggestions"] = "No suggestions"
#             else:
#                 # Format suggestions more cleanly
#                 formatted_suggestions = {}
#                 for key, value in q["validation"]["suggestions"].items():
#                     if isinstance(value, list):
#                         formatted_suggestions[key] = "\n".join([str(v) for v in value])
#                     else:
#                         formatted_suggestions[key] = value
#                 q["validation"]["suggestions"] = formatted_suggestions

# def main():
#     # Load questions
#     with open("questions.json", "r") as f:
#         mcqs = json.load(f)
    
#     # Process questions
#     validator = MCQValidator(mcqs)
#     validator.validate_and_update()
    
#     # Save back to original file
#     with open("questions.json", "w") as f:
#         json.dump(mcqs, f, indent=2)
    
#     # Generate report
#     passed = sum(1 for q in mcqs if q["validation"]["status"] == "Passed")
#     print(f"\nValidation Complete: {passed}/{len(mcqs)} passed")
#     print("Updated questions.json with detailed error information and suggestions")

# if __name__ == "__main__":
#     main()



import json
from collections import Counter
import language_tool_python
import os

class MCQValidator:
    def __init__(self, mcq_list):
        self.mcq_list = mcq_list
        self.grammar_checker = language_tool_python.LanguageTool('en-US')
    
    def check_duplicate_options(self, options):
        return [item for item, count in Counter(options.values()).items() if count > 1]
    
    def check_answer_mismatch(self, options, answer):
        return answer not in options
    
    def check_text_issues(self, text):
        matches = self.grammar_checker.check(text)
        return [{
            "error": text[match.offset:match.offset + match.errorLength],
            "message": match.message,
            "suggestions": match.replacements
        } for match in matches]
    
    def validate_and_update(self):
        # Track duplicate questions
        question_texts = [q["question"].strip().lower() for q in self.mcq_list]
        duplicate_questions = [item for item, count in Counter(question_texts).items() if count > 1]
        
        for q in self.mcq_list:
            # Initialize error tracking structure
            q["validation"] = {
                "status": "Passed",
                "errors": [],
                "suggestions": {}
            }
            
            # Check for duplicate question
            if q["question"].strip().lower() in duplicate_questions:
                q["validation"]["status"] = "Failed"
                q["validation"]["errors"].append("Duplicate question detected")
                q["validation"]["suggestions"]["question"] = ["This question and type of this questions already exists so make a new question on class 9th law of motion"]
            
            # Check for duplicate options
            dup_options = self.check_duplicate_options(q["options"])
            if dup_options:
                q["validation"]["status"] = "Failed"
                q["validation"]["errors"].append(f"Duplicate options: {', '.join(dup_options)}")
                q["validation"]["suggestions"]["options"] = ["Make each option distinct"]
            
            # Check answer exists in options
            if self.check_answer_mismatch(q["options"], q["answer"]):
                q["validation"]["status"] = "Failed"
                q["validation"]["errors"].append(f"Answer key '{q['answer']}' not in options")
                q["validation"]["suggestions"]["answer"] = ["Add matching option or correct answer key"]
            
            # Check question text
            question_issues = self.check_text_issues(q["question"])
            if question_issues:
                q["validation"]["status"] = "Failed"
                q["validation"]["errors"].append("Question text issues")
                q["validation"]["suggestions"]["question_text"] = question_issues
            
            # Check options text
            option_issues = {}
            for opt_key, opt_text in q["options"].items():
                issues = self.check_text_issues(opt_text)
                if issues:
                    option_issues[opt_key] = issues
            
            if option_issues:
                q["validation"]["status"] = "Failed"
                q["validation"]["errors"].append("Option text issues")
                q["validation"]["suggestions"]["option_text"] = option_issues
            
            # Clean empty suggestion fields
            if not q["validation"]["suggestions"]:
                q["validation"]["suggestions"] = "No suggestions"
            else:
                # Format suggestions more cleanly
                formatted_suggestions = {}
                for key, value in q["validation"]["suggestions"].items():
                    if isinstance(value, list):
                        formatted_suggestions[key] = "\n".join([str(v) for v in value])
                    else:
                        formatted_suggestions[key] = value
                q["validation"]["suggestions"] = formatted_suggestions

def main():
    # Correct the file path for questions.json
    QUESTION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'questions.json'))
    
    # Load questions
    if not os.path.exists(QUESTION_FILE_PATH):
        print(f"Error: {QUESTION_FILE_PATH} not found.")
        return

    with open(QUESTION_FILE_PATH, "r") as f:
        mcqs = json.load(f)
    
    # Process questions
    validator = MCQValidator(mcqs)
    validator.validate_and_update()
    
    # Save back to the correct file
    with open(QUESTION_FILE_PATH, "w") as f:
        json.dump(mcqs, f, indent=2)
    
    # Generate report
    passed = sum(1 for q in mcqs if q["validation"]["status"] == "Passed")
    print(f"\nValidation Complete: {passed}/{len(mcqs)} passed")
    print("Updated questions.json with detailed error information and suggestions")

if __name__ == "__main__":
    main()
