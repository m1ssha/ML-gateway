import re
from dataclasses import dataclass

@dataclass
class ResponseAnalysis:
    is_safe: bool
    reasons: list[str]

class ResponseAnalyzer:
    def __init__(self):
        # Сигнатуры для поиска системных инструкций и подозрительных паттернов
        self.patterns = [
            (re.compile(r"you are (a|an|the) assistant", re.I), "System prompt leak (role declaration)"),
            (re.compile(r"ignore (all )?previous instructions", re.I), "Prompt injection pattern"),
            (re.compile(r"eval\(|exec\(|subprocess\.|os\.system", re.I), "Code execution attempt"),
            (re.compile(r"bash|sh\s+-c|curl\s+http", re.I), "Shell command pattern"),
            (re.compile(r"BEGIN\s+SYSTEM\s+PROMPT", re.I), "System prompt markers")
        ]

    def analyze(self, llm_response: str) -> ResponseAnalysis:
        reasons = []
        for pattern, reason in self.patterns:
            if pattern.search(llm_response):
                reasons.append(reason)
        
        return ResponseAnalysis(
            is_safe=len(reasons) == 0,
            reasons=reasons
        )

response_analyzer = ResponseAnalyzer()
