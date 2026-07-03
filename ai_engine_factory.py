from sqlalchemy.orm import Session

from app.engines.ai.rule_based_ai_engine import RuleBasedAIEngine


def get_ai_engine(db: Session | None = None):
    return RuleBasedAIEngine(db=db)
