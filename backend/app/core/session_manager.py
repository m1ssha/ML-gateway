import uuid
from typing import Any
from app.storage.database import AsyncSessionLocal
from app.storage.repositories.session_repository import SessionRepository
from app.storage.repositories.message_repository import MessageRepository
from app.core.context_builder import context_builder
from app.services.ml_client import ml_client
from app.core.decision_engine import decision_engine
from app.services.llm_provider import llm_provider
from app.core.response_analyzer import response_analyzer
from app.core.event_logger import event_logger
from app.config import settings

class SessionManager:
    async def create_session(self, user_id: uuid.UUID | None = None) -> uuid.UUID:
        async with AsyncSessionLocal() as db:
            repo = SessionRepository(db)
            session = await repo.create(user_id)
            await event_logger.log(session.id, "session_created", {"user_id": str(user_id) if user_id else None})
            return session.id

    async def process_chat_message(self, session_id: uuid.UUID, user_message: str) -> dict[str, Any]:
        async with AsyncSessionLocal() as db:
            session_repo = SessionRepository(db)
            message_repo = MessageRepository(db)
            
            # 1. Получаем сессию и проверяем блокировку
            session = await session_repo.get_by_id(session_id)
            if not session:
                raise ValueError("Session not found")
            if session.is_blocked:
                return self._blocked_response(session_id, 0, "Session is already blocked")

            # Логируем входящий запрос
            await event_logger.log(session_id, "request", {"message": user_message})

            # 2. Определяем текущий шаг (на основе количества сообщений)
            history = await message_repo.get_session_history(session_id, limit=50)
            current_step = (history[0].step + 1) if history else 1

            # 3. Формируем контекст
            context = await context_builder.build_context(session_id)

            # 4. ML-инференс
            ml_result = await ml_client.predict(session_id, context)
            await event_logger.log(session_id, "ml_inference", ml_result)

            risk_score = ml_result["risk_score"]
            is_attack = ml_result["is_attack"]

            # 5. Обновляем накопительный риск (экспоненциальное сглаживание)
            # new = 0.7 * old + 0.3 * current
            new_cumulative_risk = 0.7 * session.cumulative_risk + 0.3 * risk_score
            await session_repo.update_cumulative_risk(session_id, new_cumulative_risk)

            # 6. Принимаем решение
            decision = decision_engine.decide(risk_score, is_attack, new_cumulative_risk)
            await event_logger.log(session_id, "decision", {
                "status": decision.status, 
                "cumulative_risk": new_cumulative_risk,
                "risk_score": risk_score
            })

            if decision.status == "blocked":
                # При превышении критического порога блокируем сессию навсегда
                if new_cumulative_risk >= settings.CUMULATIVE_SESSIONS_BLOCK_THRESHOLD:
                    await session_repo.block_session(session_id)
                    await event_logger.log(session_id, "block", {"reason": "cumulative_risk_threshold_exceeded"})
                
                await message_repo.add_message(
                    session_id, current_step, "user", user_message, 
                    risk_score, is_attack, decision.status
                )
                return self._blocked_response(session_id, current_step, "Request blocked by safety policy", risk_score, is_attack, new_cumulative_risk)

            # 7. Вызов LLM
            # Формируем историю для адаптера (OpenAI формат)
            llm_history = [{"role": m.role, "content": m.content} for m in reversed(history[:4])]
            
            llm_adapter = llm_provider.get_adapter()
            llm_reply = await llm_adapter.generate(
                user_message, 
                llm_history, 
                system_prompt=decision.llm_system_prompt_override
            )
            await event_logger.log(session_id, "llm_call", {"reply_length": len(llm_reply)})

            # 8. Пост-анализ ответа LLM
            analysis = response_analyzer.analyze(llm_reply)
            await event_logger.log(session_id, "response_analysis", {
                "is_safe": analysis.is_safe, 
                "reasons": analysis.reasons
            })

            if not analysis.is_safe:
                llm_reply = settings.SAFE_NOTIFICATION
                await event_logger.log(session_id, "block", {"reason": "unsafe_llm_response", "details": analysis.reasons})

            # 9. Сохраняем сообщения
            await message_repo.add_message(
                session_id, current_step, "user", user_message, 
                risk_score, is_attack, decision.status
            )
            await message_repo.add_message(
                session_id, current_step + 1, "assistant", llm_reply
            )

            return {
                "session_id": str(session_id),
                "step": current_step + 1,
                "status": decision.status,
                "reply": llm_reply,
                "risk_score": risk_score,
                "cumulative_risk": new_cumulative_risk,
                "is_attack": is_attack
            }

    def _blocked_response(self, session_id, step, reason, risk_score=1.0, is_attack=True, cumulative_risk=0.0):
        return {
            "session_id": str(session_id),
            "step": step,
            "status": "blocked",
            "reply": settings.SAFE_NOTIFICATION,
            "risk_score": risk_score,
            "cumulative_risk": cumulative_risk,
            "is_attack": is_attack,
            "reason": reason
        }

session_manager = SessionManager()
