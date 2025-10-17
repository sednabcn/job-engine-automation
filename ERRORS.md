Run mypy src/ --ignore-missing-imports
  mypy src/ --ignore-missing-imports
  shell: /usr/bin/bash -e {0}
  env:
    pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
pyproject.toml: [mypy]: python_version: Python 3.8 is not supported (must be 3.9 or higher)
src/utils/validators.py: note: In member "validate_file_extension" of class "FileValidator":
src/utils/validators.py:135:34: error: Incompatible types in assignment
(expression has type "set[str]", variable has type "Optional[list[str]]") 
[assignment]
                allowed_extensions = FileValidator._SUPPORTED_EXTENSIONS
                                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/utils/validators.py:137:34: error: Incompatible types in assignment
(expression has type "set[str]", variable has type "Optional[list[str]]") 
[assignment]
                allowed_extensions = {ext.lower() for ext in allowed_exten...
                                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~...
src/utils/validators.py:139:12: error: Unsupported right operand type for in
("Optional[list[str]]")  [operator]
            if extension not in allowed_extensions:
               ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/utils/validators.py:142:39: error: Argument 1 to "join" of "str" has
incompatible type "Optional[list[str]]"; expected "Iterable[str]"  [arg-type]
                    f"Allowed: {', '.join(allowed_extensions)}"
                                          ^~~~~~~~~~~~~~~~~~
src/utils/validators.py: note: In member "validate_years_experience" of class "SkillValidator":
src/utils/validators.py:236:40: error: Argument 2 to "validate_type" of
"Validator" has incompatible type "tuple[type[int], type[float]]"; expected
"type"  [arg-type]
            Validator.validate_type(years, (int, float), "Years of experie...
                                           ^~~~~~~~~~~~
src/utils/validators.py: note: In member "validate_skill_score" of class "SkillValidator":
src/utils/validators.py:250:40: error: Argument 2 to "validate_type" of
"Validator" has incompatible type "tuple[type[int], type[float]]"; expected
"type"  [arg-type]
            Validator.validate_type(score, (int, float), "Skill score")
                                           ^~~~~~~~~~~~
src/utils/validators.py: note: In member "validate_learning_item" of class "LearningPlanValidator":
src/utils/validators.py:459:58: error: Argument 2 to "validate_type" of
"Validator" has incompatible type "tuple[type[int], type[float]]"; expected
"type"  [arg-type]
    ...Validator.validate_type(item["estimated_hours"], (int, float), "Estima...
                                                        ^~~~~~~~~~~~
src/utils/helpers.py: note: In function "extract_keywords":
src/utils/helpers.py:162:5: error: Need type annotation for "word_freq" (hint:
"word_freq: dict[<type>, <type>] = ...")  [var-annotated]
        word_freq = {}
        ^~~~~~~~~
src/utils/helpers.py: note: In function "retry_on_error":
src/utils/helpers.py:1393:13: error: Exception must be derived from
BaseException  [misc]
                raise last_exception
                ^~~~~~~~~~~~~~~~~~~~
src/utils/helpers.py: note: In function "memoize":
src/utils/helpers.py:1437:9: error: Need type annotation for "cache" (hint:
"cache: dict[<type>, <type>] = ...")  [var-annotated]
            cache = {}
            ^~~~~
src/utils/helpers.py:1461:9: error:
"_Wrapped[[VarArg(Any), KwArg(Any)], Any, [VarArg(Any), KwArg(Any)], Any]" has
no attribute "cache_clear"  [attr-defined]
            wrapper.cache_clear = lambda: (cache.clear(), cache_order.clea...
            ^~~~~~~~~~~~~~~~~~~
src/utils/helpers.py:1461:40: error: "clear" of "MutableMapping" does not
return a value (it only ever returns None)  [func-returns-value]
            wrapper.cache_clear = lambda: (cache.clear(), cache_order.clea...
                                           ^~~~~~~~~~~~~
src/utils/helpers.py:1461:55: error: "clear" of "MutableSequence" does not
return a value (it only ever returns None)  [func-returns-value]
    ...    wrapper.cache_clear = lambda: (cache.clear(), cache_order.clear())
                                                         ^~~~~~~~~~~~~~~~~~~
src/utils/helpers.py:1462:9: error:
"_Wrapped[[VarArg(Any), KwArg(Any)], Any, [VarArg(Any), KwArg(Any)], Any]" has
no attribute "cache_info"  [attr-defined]
            wrapper.cache_info = lambda: {"size": len(cache), "max_size": ...
            ^~~~~~~~~~~~~~~~~~
src/utils/formatters.py: note: In member "format_skill_summary" of class "SkillFormatter":
src/utils/formatters.py:190:9: error: Need type annotation for "by_level"
(hint: "by_level: dict[<type>, <type>] = ...")  [var-annotated]
            by_level = {}
            ^~~~~~~~
src/utils/formatters.py: note: In member "format_learning_plan" of class "LearningPlanFormatter":
src/utils/formatters.py:339:23: error: Need type annotation for "by_priority" 
[var-annotated]
            by_priority = {"high": [], "medium": [], "low": []}
                          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/utils/data_loader.py: note: In member "load" of class "MasterSkillsetLoader":
src/utils/data_loader.py:127:9: error: Returning Any from function declared to
return "dict[str, Any]"  [no-any-return]
            return self.load_json(
            ^
src/utils/data_loader.py: note: In member "get_skill" of class "MasterSkillsetLoader":
src/utils/data_loader.py:149:9: error: Returning Any from function declared to
return "Optional[dict[str, Any]]"  [no-any-return]
            return skillset["skills"].get(skill_name)
            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/utils/data_loader.py: note: In member "load" of class "JobAnalysisLoader":
src/utils/data_loader.py:159:9: error: Returning Any from function declared to
return "list[dict[str, Any]]"  [no-any-return]
            return self.load_json(self.FILENAME, default=[])
            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/utils/data_loader.py: note: In member "load" of class "LearningProgressLoader":
src/utils/data_loader.py:194:9: error: Returning Any from function declared to
return "dict[str, Any]"  [no-any-return]
            return self.load_json(
            ^
src/utils/data_loader.py: note: In member "load" of class "SprintHistoryLoader":
src/utils/data_loader.py:227:9: error: Returning Any from function declared to
return "list[dict[str, Any]]"  [no-any-return]
            return self.load_json(self.FILENAME, default=[])
            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/utils/data_loader.py: note: In member "load" of class "WorkflowStateLoader":
src/utils/data_loader.py:268:9: error: Returning Any from function declared to
return "dict[str, Any]"  [no-any-return]
            return self.load_json(
            ^
src/utils/data_loader.py: note: In member "load" of class "SkillTestsLoader":
src/utils/data_loader.py:311:9: error: Returning Any from function declared to
return "dict[str, Any]"  [no-any-return]
            return self.load_json(self.FILENAME, default={"tests": [], "re...
            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~...
src/python_advanced_job_engine.py: note: In member "check_quality_gates" of class "AdvancedJobEngine":
src/python_advanced_job_engine.py:661:34: error: Value of type "object" is not
indexable  [index]
                score_met = score >= requirements["score"]
                                     ^~~~~~~~~~~~~~~~~~~~~
src/python_advanced_job_engine.py:662:40: error: Value of type "object" is not
indexable  [index]
                projects_met = projects >= requirements["projects"]
                                           ^~~~~~~~~~~~~~~~~~~~~~~~
src/python_advanced_job_engine.py:665:16: error: Unsupported right operand type
for in ("object")  [operator]
                if "brand" in requirements:
                   ^~~~~~~~~~~~~~~~~~~~~~~
src/python_advanced_job_engine.py:667:18: error: Unsupported right operand type
for in ("object")  [operator]
                elif "tests_passed" in requirements:
                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/python_advanced_job_engine.py:668:25: error: Value of type "object" is not
indexable  [index]
                    level = requirements["tests_passed"]  # FIX: Define le...
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/python_advanced_job_engine.py: note: In member "_get_resources" of class "AdvancedJobEngine":
src/python_advanced_job_engine.py:1680:9: error: Returning Any from function
declared to return "dict[str, list[str]]"  [no-any-return]
            return self.LEARNING_RESOURCES.get(skill_lower, self.LEARNING_...
            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~...
src/python_advanced_job_engine.py: note: In function "main":
src/python_advanced_job_engine.py:2251:22: error: Incompatible types in
assignment (expression has type "str", variable has type "dict[Any, Any]") 
[assignment]
                result = engine.export_all(analysis["job_id"])
                         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/python_advanced_job_engine.py:2293:26: error: Incompatible types in
assignment (expression has type "str", variable has type "dict[Any, Any]") 
[assignment]
                    result = engine.export_all(analysis["job_id"])
                             ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/python_advanced_job_engine.py:2305:18: error: Incompatible types in
assignment (expression has type "str", variable has type "dict[Any, Any]") 
[assignment]
            result = engine.export_all(analysis["job_id"])
                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/python_advanced_job_engine.py:2306:22: error: Unsupported operand types for
+ ("str" and "dict[Any, Any]")  [operator]
            print("\n" + result)
                         ^~~~~~
src/utils/file_readers.py: note: In member "read_file" of class "FileReader":
src/utils/file_readers.py:23:5: error: Missing return statement  [return]
        def read_file(file_path: str) -> str:
        ^
src/utils/file_readers.py: note: In member "read" of class "TXTReader":
src/utils/file_readers.py:202:5: error: Missing return statement  [return]
        def read(file_path: str, encoding: str = "utf-8") -> str:
        ^
Found 35 errors in 6 files (checked 28 source files)