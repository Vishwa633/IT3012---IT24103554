class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def tell_fact(self, fact_string: str) -> None:
        self.facts.add(fact_string)

    def tell_rule(self, premise_list: list[str], conclusion_string: str) -> None:
        self.rules.append((premise_list, conclusion_string))

    def clear_facts(self) -> None:
        self.facts.clear()            