from writer.abstract import register_abstract_template
from writer.ss_types import AbstractTemplate
from writer.workflows_blocks.blocks import WorkflowBlock


class WriterAddChatMessage(WorkflowBlock):

    @classmethod
    def register(cls, type: str):
        super(WriterAddChatMessage, cls).register(type)
        register_abstract_template(type, AbstractTemplate(
            baseType="workflows_node",
            writer={
                "name": "Add chat message",
                "description": "Add a message to a conversation.",
                "category": "Writer",
                "fields": {
                    "conversationStateElement": {
                        "name": "Conversation state element",
                        "desc": "Where the conversation is stored",
                        "type": "Text",
                    },
                    "message": {
                        "name": "Message",
                        "type": "Object",
                        "init": '{ "role": "assistant", "content": "Hello" }'
                    }
                },
                "outs": {
                    "success": {
                        "name": "Success",
                        "description": "If the function doesn't raise an Exception.",
                        "style": "success",
                    },
                    "error": {
                        "name": "Error",
                        "description": "If the function raises an Exception.",
                        "style": "error",
                    },
                },
            }
        ))

    def run(self):
        try:
            import writer.ai

            conversation_state_element = self._get_field("conversationStateElement")
            message = self._get_field("message", as_json=True)
            conversation = self.evaluator.evaluate_expression(conversation_state_element, self.instance_path, self.execution_env)

            if conversation is None or not isinstance(conversation, writer.ai.Conversation):
                self.result = "The state element specified doesn't contain a conversation. Initialize one using the block 'Initialize chat'."
                self.outcome = "error"
                return

            if message is None:
                self.result = "No message has been specified."
                self.outcome = "error"
                return
            
            try:
                writer.ai.Conversation.validate_message(message)
            except ValueError:
                self.result = "Invalid message."
                self.outcome = "error"
            finally:
                if self.outcome:
                    return            

            conversation += message

            self.evaluator.set_state(conversation_state_element, self.instance_path, conversation, base_context=self.execution_env)            
            self.result = "Success"
            self.outcome = "success"
        except BaseException as e:
            self.outcome = "error"
            raise e

    