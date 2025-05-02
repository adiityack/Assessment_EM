
# import json
# from collections import Counter
# import language_tool_python

# class MCQValidator:
#     def __init__(self, mcq_list):
#         self.mcq_list = mcq_list
#         self.grammar_checker = language_tool_python.LanguageTool('en-US')

#     def check_duplicate_options(self, options):
#         duplicates = [item for item, count in Counter(options.values()).items() if count > 1]
#         return duplicates

#     def check_answer_mismatch(self, options, answer):
#         return answer not in options

#     def check_grammar(self, text):
#         matches = self.grammar_checker.check(text)
#         issues = []
#         for match in matches:
#             issues.append({
#                 "message": match.message,
#                 "suggestions": match.replacements,
#                 "offset": match.offset,
#                 "length": match.errorLength,
#                 "context": text[match.offset:match.offset + match.errorLength]
#             })
#         return issues

#     def validate(self):
#         results = []
#         for idx, q in enumerate(self.mcq_list, start=1):
#             entry_result = {
#                 "question_number": idx,
#                 "question": q.get("question", ""),
#                 "issues": []
#             }

#             # 1. Duplicate Options
#             duplicates = self.check_duplicate_options(q["options"])
#             if duplicates:
#                 entry_result["issues"].append({
#                     "type": "Duplicate Options",
#                     "details": f"Duplicate options found: {duplicates}"
#                 })

#             # 2. Answer Mismatch
#             if self.check_answer_mismatch(q["options"], q["answer"]):
#                 entry_result["issues"].append({
#                     "type": "Answer Mismatch",
#                     "details": f"Answer '{q['answer']}' not in options"
#                 })

#             # 3. Grammar Check
#             grammar_issues = self.check_grammar(q["question"])
#             if grammar_issues:
#                 entry_result["issues"].append({
#                     "type": "Grammar Issue",
#                     "details": grammar_issues
#                 })

#             if entry_result["issues"]:
#                 results.append(entry_result)
#         return results

# if __name__ == "__main__":
#     with open("questions.json", "r") as f:
#         mcqs = json.load(f)

#     validator = MCQValidator(mcqs)
#     errors = validator.validate()

#     if errors:
#         print("Detected Issues:\n")
#         for item in errors:
#             print(f"Question {item['question_number']}: {item['question']}")
#             for issue in item["issues"]:
#                 print(f"  - [{issue['type']}] {issue['details']}")
#             print()
#     else:
#         print("All questions passed validation!")


# import json
# from collections import Counter
# import language_tool_python

# class MCQValidator:
#     def __init__(self, mcq_list):
#         self.mcq_list = mcq_list
#         self.grammar_checker = language_tool_python.LanguageTool('en-US')
    
#     def check_duplicate_options(self, options):
#         return [item for item, count in Counter(options.values()).items() if count > 1]
    
#     def check_answer_mismatch(self, options, answer):
#         return answer not in options
    
#     def check_grammar_and_spelling(self, text):
#         matches = self.grammar_checker.check(text)
#         return [{
#             "message": match.message,
#             "suggestions": match.replacements,
#             "context": text[match.offset:match.offset + match.errorLength]
#         } for match in matches]
    
#     def check_duplicate_questions(self):
#         question_texts = [q["question"].strip().lower() for q in self.mcq_list]
#         return [item for item, count in Counter(question_texts).items() if count > 1]
    
#     def validate_and_update(self):
#         duplicate_questions = self.check_duplicate_questions()
#         failed_count = 0
        
#         for q in self.mcq_list:
#             issues = []
            
#             # Check for duplicate question
#             if q["question"].strip().lower() in duplicate_questions:
#                 issues.append("Duplicate question detected")
            
#             # Check for duplicate options
#             dup_options = self.check_duplicate_options(q["options"])
#             if dup_options:
#                 issues.append(f"Duplicate options: {', '.join(dup_options)}")
            
#             # Check answer exists in options
#             if self.check_answer_mismatch(q["options"], q["answer"]):
#                 issues.append(f"Answer '{q['answer']}' not in options")
            
#             # Check question grammar/spelling
#             if self.check_grammar_and_spelling(q["question"]):
#                 issues.append("Question has grammar/spelling issues")
            
#             # Check options grammar/spelling
#             for opt_text in q["options"].values():
#                 if self.check_grammar_and_spelling(opt_text):
#                     issues.append("Options have grammar/spelling issues")
#                     break
            
#             # Update error detection status
#             q["error_detection"] = "Failed" if issues else "Passed"
#             if issues:
#                 failed_count += 1
        
#         return failed_count

# def main():
#     # Load questions from existing file
#     with open("questions.json", "r") as f:
#         mcqs = json.load(f)
    
#     # Validate and update questions
#     validator = MCQValidator(mcqs)
#     failed_count = validator.validate_and_update()
    
#     # Save updated questions back to the same file
#     with open("questions.json", "w") as f:
#         json.dump(mcqs, f, indent=2)
    
#     # Print summary
#     print("\nMCQ Validation Complete")
#     print(f"Total Questions: {len(mcqs)}")
#     print(f"Passed: {len(mcqs) - failed_count}")
#     print(f"Failed: {failed_count}")
#     print("\nUpdated questions with error detection status have been saved back to questions.json")

# if __name__ == "__main__":
#     main()



import json
from collections import Counter
import language_tool_python

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
                q["validation"]["suggestions"]["question"] = ["This question and type of this questions already exits so make new question on class 9th law of motion"]
            
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
    # Load questions
    with open("questions.json", "r") as f:
        mcqs = json.load(f)
    
    # Process questions
    validator = MCQValidator(mcqs)
    validator.validate_and_update()
    
    # Save back to original file
    with open("questions.json", "w") as f:
        json.dump(mcqs, f, indent=2)
    
    # Generate report
    passed = sum(1 for q in mcqs if q["validation"]["status"] == "Passed")
    print(f"\nValidation Complete: {passed}/{len(mcqs)} passed")
    print("Updated questions.json with detailed error information and suggestions")

if __name__ == "__main__":
    main()